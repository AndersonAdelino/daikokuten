import mysql.connector
from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from datetime import datetime
import time
import re
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore

cred = credentials.Certificate("serviceAccountKey.json")
firebase_admin.initialize_app(cred)
db = firestore.client()

service = Service(ChromeDriverManager().install())
navegador = webdriver.Chrome(service=service)
navegador.maximize_window()
navegador.get('https://blaze.com/pt/games/double')
link = "https://deep-blaze-default-rtdb.firebaseio.com/"

time.sleep(2)

while True:

    conexao = mysql.connector.connect(
        host='localhost',
        user='root',
        password='D1210',
        database='daikokuten'
    )
    cursor = conexao.cursor()

    a = navegador.find_element(By.XPATH, '//*[@id="roulette-recent"]/div/div[1]/div[7]/div/div').get_attribute('class')
    a = re.sub("sm-box ", "", a)
    if a == 'white':
        a = 0
    elif a == 'red':
        a = 1
    else:
        a = 2

    b = navegador.find_element(By.XPATH, '//*[@id="roulette-recent"]/div/div[1]/div[6]/div/div').get_attribute('class')
    b = re.sub("sm-box ", "", b)
    if b == 'white':
        b = 0
    elif b == 'red':
        b = 1
    else:
        b = 2

    c = navegador.find_element(By.XPATH, '//*[@id="roulette-recent"]/div/div[1]/div[5]/div/div').get_attribute('class')
    c = re.sub("sm-box ", "", c)
    if c == 'white':
        c = 0
    elif c == 'red':
        c = 1
    else:
        c = 2

    d = navegador.find_element(By.XPATH, '//*[@id="roulette-recent"]/div/div[1]/div[4]/div/div').get_attribute('class')
    d = re.sub("sm-box ", "", d)
    if d == 'white':
        d = 0
        number_a = '0'
    elif d == 'red':
        d = 1
        number_a = navegador.find_element(By.XPATH, '//*[@id="roulette-recent"]/div/div[1]/div[4]/div/div/div').text
    else:
        d = 2
        number_a = navegador.find_element(By.XPATH, '//*[@id="roulette-recent"]/div/div[1]/div[4]/div/div/div').text

    e = navegador.find_element(By.XPATH, '//*[@id="roulette-recent"]/div/div[1]/div[3]/div/div').get_attribute('class')
    e = re.sub("sm-box ", "", e)
    if e == 'white':
        e = 0
        number_b = '0'
    elif e == 'red':
        e = 1
        number_b = navegador.find_element(By.XPATH, '//*[@id="roulette-recent"]/div/div[1]/div[3]/div/div/div').text
    else:
        e = 2
        number_b = navegador.find_element(By.XPATH, '//*[@id="roulette-recent"]/div/div[1]/div[3]/div/div/div').text

    f = navegador.find_element(By.XPATH, '//*[@id="roulette-recent"]/div/div[1]/div[2]/div/div').get_attribute('class')
    f = re.sub("sm-box ", "", f)
    if f == 'white':
        f = 0
        number_c = '0'
    elif f == 'red':
        f = 1
        number_c = navegador.find_element(By.XPATH, '//*[@id="roulette-recent"]/div/div[1]/div[2]/div/div/div').text
    else:
        f = 2
        number_c = navegador.find_element(By.XPATH, '//*[@id="roulette-recent"]/div/div[1]/div[2]/div/div/div').text

    resultado = navegador.find_element(By.XPATH, '//*[@id="roulette-recent"]/div/div[1]/div[1]/div/div').get_attribute(
        'class')
    resultado = re.sub("sm-box ", "", resultado)
    if resultado == 'white':
        resultado = 0
    elif resultado == 'red':
        resultado = 1
    else:
        resultado = 2

    if resultado == 1:
        reds = 1
        blacks = 0
        whites = 0
        redsp = 1
        blacksp = 0
        whitesp = 0
    elif resultado == 2:
        reds = 0
        blacks = 1
        whites = 0
        redsp = 0
        blacksp = 1
        whitesp = 0
    else:
        reds = 0
        blacks = 0
        whites = 1
        redsp = 0
        blacksp = 0
        whitesp = 1

    if len(number_a) == 1:
        number_a = '0' + str(number_a)

    if len(number_b) == 1:
        number_b = '0' + str(number_b)

    if len(number_c) == 1:
        number_c = '0' + str(number_c)

    now = datetime.now()
    minute = int(now.strftime("%M"))
    hour = now.strftime("%H")

    codMist = str(minute) + str(d) + str(e) + str(f)
    cod4 = str(c) + str(d) + str(e) + str(f)

    # Historic Minutes
    check = f'SELECT * FROM historic'
    cursor.execute(check)
    rows = cursor.fetchall()

    if len(rows) >= 1080:
        cursor.execute('DELETE FROM historic ORDER BY id ASC limit 1')
        for i in range(len(rows) - 1):
            cursor.execute(f'UPDATE historic SET id = {i + 1} WHERE id = {i + 2}')

    check = f'SELECT * FROM historic'
    cursor.execute(check)
    rows = cursor.fetchall()

    add = f'INSERT INTO historic (id, minute, color) VALUES ({len(rows) + 1}, {minute}, {resultado})'
    cursor.execute(add)
    conexao.commit()

    # Repetitions
    cursor.execute('DELETE FROM repetitions')
    check = f'SELECT * FROM historic'
    cursor.execute(check)
    rows = cursor.fetchall()
    conexao.commit()

    for i in range(len(rows)):
        cursor.execute(f'SELECT minute FROM historic WHERE id = {i + 1}')
        min = cursor.fetchall()
        cursor.execute(f'SELECT color FROM historic WHERE id = {i + 1}')
        col = cursor.fetchall()

        newCheck = f'SELECT minute FROM repetitions WHERE EXISTS(SELECT * FROM repetitions WHERE minute={min[0][0]})'
        cursor.execute(newCheck)
        rowsRepetitions = cursor.fetchall()

        if len(rowsRepetitions) == 0:
            if col[0][0] == 0:
                cursor.execute(f'INSERT INTO repetitions (minute, qnt, reds, blacks, whites) '
                               f'VALUES ({min[0][0]}, 1, 0, 0, 1)')
            elif col[0][0] == 1:
                cursor.execute(f'INSERT INTO repetitions (minute, qnt, reds, blacks, whites) '
                               f'VALUES ({min[0][0]}, 1, 1, 0, 0)')
            else:
                cursor.execute(f'INSERT INTO repetitions (minute, qnt, reds, blacks, whites) '
                               f'VALUES ({min[0][0]}, 1, 0, 1, 0)')
        else:
            if col[0][0] == 0:
                cursor.execute(f'UPDATE repetitions SET qnt = qnt + 1, whites = whites + 1 WHERE minute = {min[0][0]}')
            elif col[0][0] == 1:
                cursor.execute(f'UPDATE repetitions SET qnt = qnt + 1, reds = reds + 1 WHERE minute = {min[0][0]}')
            else:
                cursor.execute(f'UPDATE repetitions SET qnt = qnt + 1, blacks = blacks + 1 WHERE minute = {min[0][0]}')
        conexao.commit()

    # Historic Combination
    check = f'SELECT * FROM historic_comb'
    cursor.execute(check)
    rows = cursor.fetchall()

    if len(rows) >= 1440:
        cursor.execute('DELETE FROM historic_comb ORDER BY id ASC limit 1')
        for i in range(len(rows) - 1):
            cursor.execute(f'UPDATE historic_comb SET id = {i + 1} WHERE id = {i + 2}')

    check = f'SELECT * FROM historic_comb'
    cursor.execute(check)
    rows = cursor.fetchall()

    add = f'INSERT INTO historic_comb (id, comb, color) VALUES ({len(rows) + 1}, {cod4}, {resultado})'
    cursor.execute(add)
    conexao.commit()

    # Combinations
    cursor.execute('DELETE FROM combinations')
    check = f'SELECT * FROM historic_comb'
    cursor.execute(check)
    rows = cursor.fetchall()
    conexao.commit()

    for i in range(len(rows)):
        cursor.execute(f'SELECT comb FROM historic_comb WHERE id = {i + 1}')
        cod = cursor.fetchall()
        cursor.execute(f'SELECT color FROM historic_comb WHERE id = {i + 1}')
        col = cursor.fetchall()

        newCheck = f'SELECT comb FROM combinations WHERE EXISTS(SELECT * FROM combinations WHERE comb={cod[0][0]})'
        cursor.execute(newCheck)
        rowsRepetitions = cursor.fetchall()

        if len(rowsRepetitions) == 0:
            if col[0][0] == 0:
                cursor.execute(f'INSERT INTO combinations (comb, qnt, reds, blacks, whites) '
                               f'VALUES ({cod[0][0]}, 1, 0, 0, 1)')
            elif col[0][0] == 1:
                cursor.execute(f'INSERT INTO combinations (comb, qnt, reds, blacks, whites) '
                               f'VALUES ({cod[0][0]}, 1, 1, 0, 0)')
            else:
                cursor.execute(f'INSERT INTO combinations (comb, qnt, reds, blacks, whites) '
                               f'VALUES ({cod[0][0]}, 1, 0, 1, 0)')
        else:
            if col[0][0] == 0:
                cursor.execute(f'UPDATE combinations SET qnt = qnt + 1, whites = whites + 1 WHERE comb = {cod[0][0]}')
            elif col[0][0] == 1:
                cursor.execute(f'UPDATE combinations SET qnt = qnt + 1, reds = reds + 1 WHERE comb = {cod[0][0]}')
            else:
                cursor.execute(f'UPDATE combinations SET qnt = qnt + 1, blacks = blacks + 1 WHERE comb = {cod[0][0]}')
        conexao.commit()

    #Firestore
    if minute == 7:
        check = f'SELECT * FROM repetitions'
        cursor.execute(check)
        rows = cursor.fetchall()
        conexao.commit()
        cont = 0


        for i in range(len(rows)):
            cursor.execute(f'SELECT minute FROM repetitions WHERE minute = {cont}')
            minR = cursor.fetchall()
            cursor.execute(f'SELECT qnt FROM repetitions WHERE minute = {cont}')
            qntR = cursor.fetchall()
            cursor.execute(f'SELECT reds FROM repetitions WHERE minute = {cont}')
            redsR = cursor.fetchall()
            cursor.execute(f'SELECT blacks FROM repetitions WHERE minute = {cont}')
            blacksR = cursor.fetchall()
            cursor.execute(f'SELECT whites FROM repetitions WHERE minute = {cont}')
            whitesR = cursor.fetchall()

            data = {
                'minute': minR[0][0],
                'qnt': qntR[0][0],
                'reds': redsR[0][0],
                'blacks': blacksR[0][0],
                'whites': whitesR[0][0]
            }

            db.collection('List').document(f'{minR[0][0]}').set(data)

            cont += 1

    # Combinations 4
    check = f'SELECT cod FROM combinations_4 WHERE EXISTS(SELECT * FROM combinations_4 WHERE cod={cod4})'
    cursor.execute(check)
    rows = cursor.fetchall()
    if len(rows) == 0:
        comando2 = f'INSERT INTO combinations_4 (cod, qnt, reds, blacks, whites, redsp, blacksp, whitesp) ' \
                   f'VALUES ({cod4},1,{reds},{blacks},{whites},{redsp},{blacksp},{whitesp})'
        cursor.execute(comando2)
        conexao.commit()
    else:
        if resultado == 0:
            checkWhite = f'SELECT whites FROM combinations_4 WHERE cod={cod4}'
            update = f'UPDATE combinations_4 SET whites = whites+1, qnt = qnt+1, redsp = reds/(qnt-whites), ' \
                     f'blacksp = blacks/(qnt-whites), whitesp = whites/qnt WHERE cod = {cod4}'
        elif resultado == 1:
            checkRed = f'SELECT reds FROM combinations_4 WHERE cod={cod4}'
            update = f'UPDATE combinations_4 SET reds = reds+1, qnt = qnt+1, redsp = reds/(qnt-whites), ' \
                     f'blacksp = blacks/(qnt-whites), whitesp = whites/qnt WHERE cod = {cod4}'
        else:
            checkBlack = f'SELECT blacks FROM combinations_4 WHERE cod={cod4}'
            update = f'UPDATE combinations_4 SET blacks = blacks+1, qnt = qnt+1, redsp = reds/(qnt-whites), ' \
                     f'blacksp = blacks/(qnt-whites), whitesp = whites/qnt WHERE cod = {cod4}'

        cursor.execute(update)
        conexao.commit()

    checkMinute1 = f'SELECT minute FROM repetitions_24 WHERE EXISTS(SELECT * FROM repetitions_24 WHERE minute={minute})'
    cursor.execute(checkMinute1)
    rowsMinute1 = cursor.fetchall()
    if len(rowsMinute1) == 0:
        commandMinute1 = f'INSERT INTO repetitions_24 (minute, qnt, reds, blacks, whites, redsp, blacksp, whitesp) ' \
                         f'VALUES ({minute}, 1, {reds},{blacks},{whites},{redsp},{blacksp},{whitesp})'
        cursor.execute(commandMinute1)
        conexao.commit()
    else:
        if resultado == 0:
            checkWhite2 = f'SELECT whites FROM repetitions_24 WHERE minute={minute}'
            update2 = f'UPDATE repetitions_24 SET whites = whites+1, qnt = qnt+1, redsp = reds/(qnt-whites), ' \
                      f'blacksp = blacks/(qnt-whites), whitesp = whites/qnt WHERE minute = {minute}'
        elif resultado == 1:
            checkRed2 = f'SELECT reds FROM repetitions_24 WHERE minute={minute}'
            update2 = f'UPDATE repetitions_24 SET reds = reds+1, qnt = qnt+1, redsp = reds/(qnt-whites), ' \
                      f'blacksp = blacks/(qnt-whites), whitesp = whites/qnt WHERE minute = {minute}'
        else:
            checkBlack2 = f'SELECT blacks FROM repetitions_24 WHERE minute={minute}'
            update2 = f'UPDATE repetitions_24 SET blacks = blacks+1, qnt = qnt+1, redsp = reds/(qnt-whites), ' \
                      f'blacksp = blacks/(qnt-whites), whitesp = whites/qnt WHERE minute = {minute}'

        cursor.execute(update2)
        conexao.commit()

    checkCod = f'SELECT cod_num FROM cod_num WHERE EXISTS(SELECT * FROM cod_num WHERE cod_num={codMist})'
    cursor.execute(checkCod)
    rowsCod = cursor.fetchall()
    if len(rowsCod) == 0:
        commandCod = f'INSERT INTO cod_num (cod_num, qnt, reds, blacks, whites, redsp, blacksp, whitesp) ' \
                     f'VALUES ({codMist}, 1, {reds},{blacks},{whites},{redsp},{blacksp},{whitesp})'
        cursor.execute(commandCod)
        conexao.commit()
    else:
        if resultado == 0:
            checkWhite2 = f'SELECT whites FROM cod_num WHERE cod_num={codMist}'
            update2 = f'UPDATE cod_num SET whites = whites+1, qnt = qnt+1, redsp = reds/(qnt-whites), ' \
                      f'blacksp = blacks/(qnt-whites), whitesp = whites/qnt WHERE cod_num = {codMist}'
        elif resultado == 1:
            checkRed2 = f'SELECT reds FROM cod_num WHERE cod_num={codMist}'
            update2 = f'UPDATE cod_num SET reds = reds+1, qnt = qnt+1, redsp = reds/(qnt-whites), ' \
                      f'blacksp = blacks/(qnt-whites), whitesp = whites/qnt WHERE cod_num = {codMist}'
        else:
            checkBlack2 = f'SELECT blacks FROM cod_num WHERE cod_num={codMist}'
            update2 = f'UPDATE cod_num SET blacks = blacks+1, qnt = qnt+1, redsp = reds/(qnt-whites), ' \
                      f'blacksp = blacks/(qnt-whites), whitesp = whites/qnt WHERE cod_num = {codMist}'

        cursor.execute(update2)
        conexao.commit()

    cursor.close()
    conexao.close()

    time.sleep(30)
