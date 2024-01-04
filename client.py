import pprint
import requests
import time
import os
from pprint import pprint

url = "http://2c7ea9ad.r8.cpolar.top"
# url = "	http://127.0.0.1:10532"
name = input('>>> ')
print(name)
seat = eval(requests.post(url + '/l', json={"name": name}).text)
print(f'you sit at {seat}')
last_result = {}
last_winners = []
last_street = []
last_public = []

def log_stat(status):
    global last_result, last_winners, last_street, last_public
    if status["last_result"] != last_result:
        print('Comparing: ')
        last_result = status["last_result"]
        last_winners = status["last_winners"]
        pprint(last_result)
        print("Winners: ")
        pprint(last_winners)
        time.sleep(10)
    elif status["last_street"] != last_street:
        if status["last_street"] == []:
            print(f'Your Hand: {" ".join(status["hand"])}')
            print(f'Current Pot: {status["pot"]}')
            print(f'Public Cards: {" ".join([str(a) for a in status["public"]])}')
            print(f'Action Line:')
            print('\n'.join(status['actionLine']))
            print(f'Your Stack: {status["stack"]}')
            print(f'Your Position: {seat}')
            print(f'Button: {status["btn"]}')
        # print("pause 3")
        # print("last_street: ", last_street)
        else:
            last_street = status["last_street"]
            # print("last_street: ", last_street)
            last_public = status["last_public"]
            print(f'Your Hand: {" ".join(status["hand"])}')
            print(f'Current Pot: {status["pot"]}')
            print(f'Public Cards: {" ".join([str(a) for a in last_public])}')
            print(f'Action Line:')
            print('\n'.join(last_street))
            print(f'Your Stack: {status["stack"]}')
            print(f'Your Position: {seat}')
            print(f'Button: {status["btn"]}')
            time.sleep(3)
    else:
        # print("last_street: ", last_street)
        # last_street = status["last_street"]
        # print("last_street: ", last_street)
        # last_public = status["last_public"]
        print(f'Your Hand: {" ".join(status["hand"])}')
        print(f'Current Pot: {status["pot"]}')
        print(f'Public Cards: {" ".join([str(a) for a in status["public"]])}')
        print(f'Action Line:')
        print('\n'.join(status['actionLine']))
        print(f'Your Stack: {status["stack"]}')
        print(f'Your Position: {seat}')
        print(f'Button: {status["btn"]}')
    

while 1:
    for i in range(3):
        try:
            status = eval(requests.get(url + '/s?seat=' + str(seat)).text)
        except:
            pass
    os.system('cls' if os.name == 'nt' else 'clear')
    if status['tablestat'] == 0:
        print('game not start')
    else:
        log_stat(status)
        if status['actPlayer'] == seat:
            for i in range(3):
                try:
                    status = eval(requests.get(url + '/s?seat=' + str(seat)).text)
                except:
                    pass
            os.system('cls' if os.name == 'nt' else 'clear')
            log_stat(status)
            move = input('>>> ')
            while not move.startswith('c') and not move.startswith('b') and not move.startswith('f'):
                move = input('Wrong Formatt. c for check, b 99 for bet 99, f for fold >>>')
            while move.startswith('b') and len(move.split()) != 2:
                move = input('Wrong Formatt. c for check, b 99 for bet 99, f for fold >>>')
            res = requests.post(url + '/a', json={'seat': seat, 'move': move}).text
    time.sleep(1)
