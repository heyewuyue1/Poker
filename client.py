import requests
import time
import os

url = "	http://614b13b3.r20.cpolar.top"
# url = "	http://127.0.0.1"
name = input('>>> ')
print(name)
seat = eval(requests.post(url + '/l', json={"name": name}).text)
print(f'you sit at {seat}')

def log_stat(status):
    print(f'Your Hand: {status["hand"]}')
    print(f'Current Pot: {status["pot"]}')
    print(f'Public Cards: {status["public"]}')
    print(f'Action Line: {status["actionLine"]}')
    print(f'Your Stack: {status["stack"]}')
    print(f'Your Position: {seat}')
    print(f'Your Status: {seat}')

while 1:
    status = eval(requests.get(url + '/s?seat=' + str(seat)).text)
    os.system('cls')
    log_stat(status)
    if status['tablestat'] == 0:
        print('game not start')
    else:
        if status['actPlayer'] == seat:
            move = input('>>> ')
            while not move.startswith('c') and not move.startswith('b') and not move.startswith('f'):
                move = input('Wrong Formatt. c for check, b 99 for bet 99, f for fold >>>')
            res = requests.post(url + '/a', json={'seat': seat, 'move': move}).text
    time.sleep(1)
