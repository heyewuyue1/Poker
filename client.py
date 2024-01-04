import pprint
import requests
import time
import os
from pprint import pprint

url = "	http://91a19b1.r12.cpolar.top"
# url = "	http://127.0.0.1"
name = input('>>> ')
print(name)
seat = eval(requests.post(url + '/l', json={"name": name}).text)
print(f'you sit at {seat}')
last_result = {}
last_winners = []

def log_stat(status):
    global last_result
    if status["last_result"] != last_result:
        print('Comparing: ')
        last_result = status["last_result"]
        last_winners = status["last_winners"]
        pprint(last_result)
        print("Winners: ")
        pprint(last_winners)
        time.sleep(10)
    else:
        print(f'Your Hand: {[status["hand"]]}')
        print(f'Current Pot: {status["pot"]}')
        print(f'Public Cards: {status["public"]}')
        print(f'Action Line: {status["actionLine"]}')
        print(f'Your Stack: {status["stack"]}')
        print(f'Your Position: {seat}')
        print(f'Button: {status["btn"]}')
    

while 1:
    for i in range(3):
        try:
            status = eval(requests.get(url + '/s?seat=' + str(seat)).text)
        except:
            pass
    os.system('cls')
    log_stat(status)
    if status['tablestat'] == 0:
        print('game not start')
    else:
        if status['actPlayer'] == seat:
            os.system('cls')
            log_stat(status)
            move = input('>>> ')
            while not move.startswith('c') and not move.startswith('b') and not move.startswith('f'):
                move = input('Wrong Formatt. c for check, b 99 for bet 99, f for fold >>>')
            res = requests.post(url + '/a', json={'seat': seat, 'move': move}).text
    time.sleep(1)
