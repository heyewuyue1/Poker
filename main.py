from fastapi import FastAPI
import uvicorn
from enum import IntEnum, Enum
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import time
import random
from pydantic import BaseModel
from collections import Counter
from itertools import combinations
import sys

# TODO
# 超时q
# 完善结算，显示牌型
# xxx to call
SEAT_NUM = 10
pot = 0
last_bet = 0
last_result = {}
last_winners = []
showdown_info = ''

trans = ["","","2","3","4","5","6","7","8","9","T","J","Q","K","A"]

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

def translate(card):
    return card[0] + trans[card[1]]

class Point(IntEnum):
    Ace = 14
    Two = 2
    Three = 3
    Four = 4
    Five = 5
    Six = 6
    Seven = 7
    Eight = 8
    Nine = 9
    Ten = 10
    Jack = 11
    Queen = 12
    King = 13

class TableStat(IntEnum):
    END = 0
    PRE = 1
    FLOP = 2
    TURN = 3
    RIVER = 4

class PlayerStat(Enum):
    WAITING = 0
    MOVED = 1
    FOLDED = 2

class Dealer:
    def __init__(self) -> None:
        self.deck = list((x, y) for x in colors for y in points)
        r.shuffle(self.deck)
        self.btn = 0
    def deal(self):
        return self.deck.pop(0)
    
    def shuffle(self):
        print('shuffling...')
        self.deck = list((x, y) for x in colors for y in points)
        r.shuffle(self.deck)

    def flop(self):
        public.append(self.deal())
        public.append(self.deal())
        public.append(self.deal())
        print('flop: ' + self.public)

    def turn(self):
        public.append(self.deal())
        print('turn: ' + self.public)

    def river(self):
        public.append(self.deal())
        print('river: ' + self.public)

class Player:
    def __init__(self, name, seat):
        self.name = name
        self.hand = []
        self.stack = 2000
        self.status = PlayerStat.FOLDED
        self.bet_street = 0
        self.seat = seat
        self.bet_hand = 0
    #现为输入添加
    def bet(self, chips):
        global pot, last_bet
        if self.stack <= chips:
            pot += self.stack
            self.bet_street += self.stack
            self.bet_hand += self.stack
            last_bet = self.bet_street
            self.stack = 0
            action.append(f'{self.name}[{self.seat}] bet all in ({self.bet_street}).')
            print(f'{self.name}[{self.seat}] bet all in ({self.bet_street}).')
            self.status = PlayerStat.MOVED
        else:
            self.stack -= chips
            pot += chips
            self.bet_street += chips
            self.bet_hand += chips
            last_bet = self.bet_street
            action.append(f'{self.name}[{self.seat}] bet {self.bet_street}.')
            print(f'{self.name}[{self.seat}] bet {self.bet_street}.')
            self.status = PlayerStat.MOVED

    def call(self, chips):
        global pot, last_bet
        if self.stack <= chips:
            pot += self.stack
            self.bet_street += self.stack
            self.bet_hand += self.stack
            self.stack = 0
            action.append(f'{self.name}[{self.seat}] call all in ({self.bet_street}).')
            print(f'{self.name}[{self.seat}] call all in ({self.bet_street}).')
            self.status = PlayerStat.MOVED

        else:
            self.stack -= chips
            pot += chips
            self.bet_street += chips
            self.bet_hand += chips
            action.append(f'{self.name}[{self.seat}] call {self.bet_street}.')
            print(f'{self.name}[{self.seat}] call {self.bet_street}.')
            self.status = PlayerStat.MOVED


    def fold(self):
        self.status = PlayerStat.FOLDED
        action.append(f'{self.name}[{self.seat}] fold.')
        print(f'{self.name}[{self.seat}] fold.')
    
    def check(self):
        self.status = PlayerStat.MOVED
        action.append(f'{self.name}[{self.seat}] check.')
        print(f'{self.name}[{self.seat}] check.')

    def win(self, chips):
        self.stack += chips

class User(BaseModel):
    name: str
    chips: int

class Move(BaseModel):
    seat: int
    move: str

def is_straight(cards):
    values = sorted([int(card[1]) for card in cards], reverse=True)
    return all(values[i] - 1 == values[i + 1] for i in range(len(values) - 1)) or values == [14, 5, 4, 3, 2]

def is_flush(cards):
    suits = set(card[0] for card in cards)
    return len(suits) == 1

def is_straight_flush(cards):
    return is_flush(cards) and is_straight(cards)

def hand_rank(cards):
    value_count = Counter([int(card[1]) for card in cards])
    sorted_values = sorted(value_count.keys(), reverse=True)  # Sort values in descending order
    
    max_count = max(value_count.values())
    
    if max_count == 4:
        return 7, [max(value_count, key=value_count.get)], sorted_values  # Four of a Kind
    elif max_count == 3 and len(value_count) == 2:
        return 6, [max(value_count, key=value_count.get), min(value_count, key=value_count.get)], sorted_values  # Full House
    elif is_flush(cards):
        if is_straight(cards):
            return 8, [max(int(card[1]) for card in cards)], sorted_values  # Straight Flush
        else:
            return 5, [max(int(card[1]) for card in cards)], sorted_values  # Flush
    elif is_straight(cards):
        return 4, [max(int(card[1]) for card in cards)], sorted_values  # Straight
    elif max_count == 3:
        return 3, [max(value_count, key=value_count.get)], sorted_values  # Three of a Kind
    elif max_count == 2 and len(value_count) == 3:
        pairs = [key for key, value in value_count.items() if value == 2]
        return 2, sorted(pairs, reverse=True), sorted_values  # Two Pair
    elif max_count == 2:
        return 1, [max(value_count, key=value_count.get)], sorted_values  # One Pair
    else:
        return 0, sorted_values[:5], sorted_values  # High Card

def compare_hands(hand1, hand2):
    rank1, *args1 = hand_rank(hand1)
    rank2, *args2 = hand_rank(hand2)

    if rank1 > rank2:
        return 1
    elif rank1 < rank2:
        return -1
    else:
        for a1, a2 in zip(args1, args2):
            if a1 > a2:
                return 1
            elif a1 < a2:
                return -1
        return 0

def find_best_hand(player_hand, public_cards):
    all_cards = player_hand + public_cards
    best_hand = None
    
    for combo in combinations(all_cards, 5):
        if best_hand == None:
            best_hand = combo
        else:
            if compare_hands(combo, best_hand) == 1:
                best_hand = combo
    return best_hand

def compare_hands_for_players(hands):
    global players, last_winners
    winner = []
    for k in hands:
        if winner == []:
            winner.append(k)
        else:
            if compare_hands(hands[k], hands[winner[0]]) == 1:
                winner.clear()
                winner.append(k)
            elif compare_hands(hands[k], hands[winner[0]]) == 0:
                winner.append(k)
    return winner

seed = int(time.time())
r = random.Random(seed)
colors = ('♠', '♥', '♦', '♣')
points = (Point.Ace, Point.Two, Point.Three,Point.Four,Point.Five,Point.Six,Point.Seven,Point.Eight,Point.Nine,Point.Ten,Point.Jack,Point.Queen,Point.King)
public = []
players = [None, None, None, None, None, None, None, None, None, None]
action = []
last_street = []
last_public = []
table_stat = TableStat.END
btn = 0
cur_player = 0
seat_loc = [None, None, None, None, None, None]

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许访问的源列表
    allow_credentials=True,  # 允许携带cookie
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头部
)

dealer = Dealer()

def showdown():
    global last_result, last_winners, showdown_info
    cmp_dict = {}
    winner = []
    last_result = {}
    for i in range(SEAT_NUM):
        if players[i] is not None and players[i].status is not PlayerStat.FOLDED:
            cmp_dict[i] = find_best_hand(players[i].hand, public)
            last_result[players[i].name] = [translate(card) for card in players[i].hand]
    flag = True
    while cmp_dict != {}:
        winner = compare_hands_for_players(cmp_dict)
        if flag:
            last_winners = [players[k].name for k in winner]
            flag = False
        print(f'winner of this round {winner}')
        min_max_win = sys.maxsize
        mmw_idx = -1
        for win in winner:
            if players[win].bet_hand < min_max_win:
                min_max_win = players[win].bet_hand
                mmw_idx = win
        print(f'shipping chips for {mmw_idx}')
        for player in players:
            if player is not None:
                if player.bet_hand < min_max_win:
                    players[mmw_idx].win(player.bet_hand // len(winner))
                    print(f'player {player.seat} pay player {mmw_idx} {player.bet_hand // len(winner)}')
                    player.bet_hand -= player.bet_hand // len(winner)
                else:
                    players[mmw_idx].win(min_max_win // len(winner))
                    print(f'player {player.seat} pay player {mmw_idx} {min_max_win // len(winner)}')

                    player.bet_hand -= min_max_win // len(winner)
        cmp_dict.pop(mmw_idx)
    showdown_info += 'Comparing:\n'
    for k in last_result:
            showdown_info += f'{k}: {" ".join(last_result[k])}\n'
    showdown_info += "Public Cards: " + " ".join([translate(a) for a in last_public]) + '\n'
    showdown_info += f'Winners: {", ".join([str(a) for a in last_winners])}'
    time.sleep(10)
    showdown_info = ''

def clear():
    global public, pot, action, btn, last_pot
    public = []
    action = []
    last_street.clear()
    btn = next_player(btn)
    for player in players:
        if player is not None:
            player.status = PlayerStat.FOLDED
            player.hand.clear()
            player.bet_hand = 0
            player.bet_street = 0
            if player.stack == 0:
                player.stack = 2000
    pot = 0
    dealer.shuffle()

def step():
    global table_stat, cur_player, action, last_bet, last_street, last_public
    time.sleep(3)
    sb = next_player(btn)
    bb = next_player(sb)
    if table_stat == TableStat.END:
        cnt = 0
        for player in players:
            if player is not None:
                cnt += 1
        if cnt < 2:
            return
        action.append('PRE: ')
        players[sb].bet(10)
        players[bb].bet(20)
        table_stat = TableStat.PRE
        for player in players:
            if player is not None:
                player.hand.append(dealer.deal())
                player.hand.append(dealer.deal())
                player.status = PlayerStat.WAITING
        dealer.deal()
        public.append(dealer.deal())
        public.append(dealer.deal())
        public.append(dealer.deal())
        dealer.deal()
        public.append(dealer.deal())
        dealer.deal()
        public.append(dealer.deal())
        cur_player = next_player(bb)
    elif table_stat == TableStat.PRE:
        last_street = action
        action = []
        table_stat = TableStat.FLOP
        last_public = []
        for player in players:
            if player is not None and player.status == PlayerStat.MOVED:
                player.status = PlayerStat.WAITING
                player.bet_street = 0
        last_bet = 0
        action.append('FLOP: ')
        n_player = next_mover(btn)
        nn_player = next_mover(n_player)
        if n_player == nn_player:
            step()
        else:
            cur_player = n_player
    elif table_stat == TableStat.FLOP:
        last_street = action
        action = []
        table_stat = TableStat.TURN
        last_public = public[:3].copy()
        for player in players:
            if player is not None and player.status == PlayerStat.MOVED:
                player.status = PlayerStat.WAITING                
                player.bet_street = 0
        last_bet = 0
        action.append('TURN: ')
        n_player = next_mover(btn)
        nn_player = next_mover(n_player)
        if n_player == nn_player:
            step()
        else:
            cur_player = n_player
    elif table_stat == TableStat.TURN:
        last_street = action
        action = []
        table_stat = TableStat.RIVER
        last_public = public[:4].copy()
        for player in players:
            if player is not None and player.status == PlayerStat.MOVED:
                player.status = PlayerStat.WAITING
                player.bet_street = 0
        last_bet = 0
        action.append('RIVER: ')
        n_player = next_mover(btn)
        nn_player = next_mover(n_player)
        if n_player == nn_player:
            step()
        else:
            cur_player = n_player
    elif table_stat == TableStat.RIVER:
        last_public = public.copy()
        showdown()
        clear()
        table_stat = TableStat.END
        step()

def next_player(i):
    while 1:
        i = (i + 1) % SEAT_NUM
        if players[i] is not None:
            return i

def next_mover(i):
    j = i
    while 1:
        i = (i + 1) % SEAT_NUM
        if i == j:
            return i
        if players[i] is not None and players[i].status is PlayerStat.WAITING:
            if players[i].stack == 0:
                players[i].check()
            else:
                return i

@app.post('/a')
def reg_act(move: Move):
    global cur_player, action, table_stat, pot
    if move.move.startswith('b'):
        players[move.seat].bet(eval(move.move.split()[-1]) - players[move.seat].bet_street)
        for player in players:
            if player is not None and player.status == PlayerStat.MOVED:
                player.status = PlayerStat.WAITING
        players[move.seat].status = PlayerStat.MOVED
    elif move.move.startswith('c'):
        if last_bet - players[move.seat].bet_street == 0:
            players[move.seat].check()
        else:
            players[move.seat].call(last_bet - players[move.seat].bet_street)
    elif move.move.startswith('f') or move.move.startswith('q'):
        players[move.seat].fold()
        cnt = 0
        j = 0
        for i in range(SEAT_NUM):
            if players[i] is not None and players[i].status is not PlayerStat.FOLDED:
                cnt += 1
                j = i
        if move.move.startswith('q'):
            players[move.seat] = None
        if cnt == 1:
            players[j].win(pot)
            table_stat = TableStat.END
            clear()
            step()
            return

    cur_player = next_mover(move.seat)
    if cur_player == move.seat:
        step()

@app.get("/s")
def table_info(seat: int):
    global table_stat, public, pot, action, last_street, btn, cur_player, players, last_result, last_winners, last_public, showdown_info
    return {
        'tablestat': table_stat,
        'players': [{'name': player.name if player is not None else '', 
                     'left': player.stack if player is not None else '', 
                     'seat': player.seat if player is not None else '', 
                     'status': player.status if player is not None else ''
                     } for player in players],
        'public': [translate(card) for card in public],
        'pot': pot,
        'actionLine': action,
        "last_street": last_street,
        'btn': btn,
        'actPlayer': cur_player,
        'actPlayerName':players[cur_player].name if players[cur_player] is not None else "",
        'stack': players[seat].stack,
        'hand':[translate(card) for card in players[seat].hand],
        "last_result": last_result,
        "last_winners": last_winners,
        "last_public": [translate(card) for card in last_public],
        "showdown_info": showdown_info
    }

@app.post('/l')
def login(name: User):
    for i in range(SEAT_NUM):
        if players[i] == None:
            players[i] = Player(name.name, i)
            players[i].stack = name.chips
            cnt = 0
            for player in players:
                if player is not None:
                    cnt += 1
            if cnt == 2:
                step()
            return i
    return -1

if __name__ == '__main__':
    uvicorn.run("main:app", port=10532, log_level='warning')