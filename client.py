import requests
import time
import os

url = "http://2119cbfa.r17.cpolar.top"
buf = input('健康游戏忠告：请先把各种梯子和加速器关了\nPlease input your name and chips(e.g. hjh 2000)\n>>> ')
seat = eval(requests.post(url + '/l', json={"name": buf.split()[0], "chips": eval(buf.split()[1])}).text)
print(f'you sit at {seat}')
last_result = {}
last_winners = []
last_street = []
last_public = []
public = []

# def translate(card):
#     color_pre = ''
#     color_end = ''
#     if card[0] == '♥':
#         color_pre = '\033[31m'
#         color_end = '\33[0m'
#     if card[0] == '♣':
#         color_pre = '\033[32m'
#         color_end = '\33[0m'
#     if card[0] == '♦':
#         color_pre = '\033[34m'
#         color_end = '\33[0m'
#     return color_pre + card[0] + trans[card[1]] + color_end

def log_stat(status):
    global last_result, last_winners, last_street, public, last_public
    show_public = []
    last_public = status["last_public"]
    if status["tablestat"] == 2:
        show_public = public[:3]
    elif status["tablestat"] == 3:
        show_public = public[:4]
    elif status["tablestat"] == 4:
        show_public = public[:5]
    if status["last_result"] != last_result:
        print('Comparing: ')
        last_result = status["last_result"]
        last_winners = status["last_winners"]
        for k in last_result:
            print(f'{k}: {" ".join(last_result[k])}')
        print("Public Cards: " + " ".join([str(a) for a in last_public]))
        print(f'Winners: {", ".join([str(a) for a in last_winners])}')
        time.sleep(10)
    elif status["last_street"] != last_street:
        if status["last_street"] == []:
            for player in status['players']:
                if player['name'] != '':
                    stat = ''
                    if player['status'] == 0:
                        stat = 'WAITING'
                    if player['status'] == 1:
                        stat = 'MOVED'
                    if player['status'] == 2:
                        stat = 'FOLDED'
                    print(f'{player["name"]}[{player["seat"]}] {stat}. {player["left"]} left.')
            print('\n\n')
            print(f'Your Hand: {" ".join(status["hand"])}')
            print(f'Current Pot: {status["pot"]}')
            print(f'Public Cards: {" ".join([str(a) for a in show_public])}')
            print(f'Action Line:')
            print('\n'.join(status['actionLine']))
            print(f'{status["actPlayerName"]}[{status["actPlayer"]}] ...')
            print(f'Your Stack: {status["stack"]}')
            print(f'Your Position: {seat}')
            print(f'Button: {status["btn"]}')
        else:
            last_street = status["last_street"]
            for player in status['players']:
                if player['name'] != '':
                    stat = ''
                    if player['status'] == 0:
                        stat = 'WAITING'
                    if player['status'] == 1:
                        stat = 'MOVED'
                    if player['status'] == 2:
                        stat = 'FOLDED'
                    print(f'{player["name"]}[{player["seat"]}] {stat}. {player["left"]} left.')
            print('\n\n')
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
        for player in status['players']:
                if player['name'] != '':
                    stat = ''
                    if player['status'] == 0:
                        stat = 'WAITING'
                    if player['status'] == 1:
                        stat = 'MOVED'
                    if player['status'] == 2:
                        stat = 'FOLDED'
                    print(f'{player["name"]}[{player["seat"]}] {stat}. {player["left"]} left.')
        print('\n\n')
        print(f'Your Hand: {" ".join(status["hand"])}')
        print(f'Current Pot: {status["pot"]}')
        print(f'Public Cards: {" ".join([str(a) for a in show_public])}')
        print(f'Action Line:')
        print('\n'.join(status['actionLine']))
        print(f'{status["actPlayerName"]}[{status["actPlayer"]}] ...')
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
        public = status["public"]
        log_stat(status)
        if status['actPlayer'] == seat:
            print('\a')
            for i in range(3):
                try:
                    status = eval(requests.get(url + '/s?seat=' + str(seat)).text)
                except:
                    pass
            os.system('cls' if os.name == 'nt' else 'clear')
            public = status["public"]
            log_stat(status)
            move = input('>>> ')
            while not move.startswith('c') and not move.startswith('b') and not move.startswith('f') and not move.startswith('q'):
                move = input('Wrong Formatt. c for check, b 99 for bet 99, f for fold >>>')
            while move.startswith('b') and len(move.split()) != 2:
                move = input('Wrong Formatt. c for check, b 99 for bet 99, f for fold >>>')
            res = requests.post(url + '/a', json={'seat': seat, 'move': move}).text
            if move.startswith('q'):
                exit()
    time.sleep(1)
