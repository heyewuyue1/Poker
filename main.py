from tkinter import N
from turtle import pu
from winsound import PlaySound
from fastapi import FastAPI
from matplotlib.pyplot import plasma
import uvicorn
from enum import IntEnum, Enum
import uvicorn
from fastapi import FastAPI
import time
import random
from pydantic import BaseModel
from collections import Counter
from itertools import combinations

# TODO
# 边池
# gracefully quit，每次开始时判断人数是否够2
# 完善结算，显示牌型
# 显示还有谁在，目前正在等谁
# xxx to call

pot = 0
last_bet = 0
last_result = {}
last_winners = []

trans = ["","","2","3","4","5","6","7","8","9","T","J","Q","K","A"]

def translate(card):
    return "".join([card[0], trans[card[1]]])

class NoEnoughChipsException(Exception):
    def __init__(self, message):
        self.message = message
    
    def __str__(self):
        return f"No Enough Chips: {self.message}"

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
    #现为输入添加
    def bet(self, chips):
        global pot, last_bet
        if self.stack <= chips:
            pot += self.stack
            self.bet_street += self.stack
            last_bet = self.bet_street
            self.stack = 0
            action.append(f'{self.name}[{self.seat}] bet all in ({self.bet_street}). {self.stack} left.')
            print(f'{self.name}[{self.seat}] bet all in ({self.bet_street}). {self.stack} left.')
            self.status = PlayerStat.MOVED
        else:
            self.stack -= chips
            pot += chips
            self.bet_street += chips
            last_bet = self.bet_street
            action.append(f'{self.name}[{self.seat}] bet {self.bet_street}. {self.stack} left.')
            print(f'{self.name}[{self.seat}] bet {self.bet_street}. {self.stack} left.')
            self.status = PlayerStat.MOVED

    def call(self, chips):
        global pot, last_bet
        if self.stack <= chips:
            pot += self.stack
            self.bet_street += self.stack
            self.stack = 0
            action.append(f'{self.name}[{self.seat}] call all in ({self.bet_street}). {self.stack} left.')
            print(f'{self.name}[{self.seat}] call all in ({self.bet_street}). {self.stack} left.')
            self.status = PlayerStat.MOVED

        else:
            self.stack -= chips
            pot += chips
            self.bet_street += chips
            action.append(f'{self.name}[{self.seat}] call {self.bet_street}. {self.stack} left.')
            print(f'{self.name}[{self.seat}] call {self.bet_street}. {self.stack} left.')
            self.status = PlayerStat.MOVED


    def fold(self):
        self.status = PlayerStat.FOLDED
        action.append(f'{self.name}[{self.seat}] fold. {self.stack} left.')
        print(f'{self.name}[{self.seat}] fold. {self.stack} left.')
    
    def check(self):
        self.status = PlayerStat.MOVED
        action.append(f'{self.name}[{self.seat}] check. {self.stack} left.')
        print(f'{self.name}[{self.seat}] check. {self.stack} left.')

    def win(self, chips):
        self.stack += chips

class User(BaseModel):
    name: str

class Move(BaseModel):
    seat: int
    move: str

def is_straight(cards):
    values = sorted([int(card[1]) for card in cards], reverse=True)
    return all(values[i] - 1 == values[i + 1] for i in range(len(values) - 1))

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
        return 2, pairs, sorted_values  # Two Pair
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
    last_winners = [players[k].name for k in winner]
    return winner

seed = int(time.time())
r = random.Random(seed)
colors = ('♠', '♥', '♦', '♣')
points = (Point.Ace, Point.Two, Point.Three,Point.Four,Point.Five,Point.Six,Point.Seven,Point.Eight,Point.Nine,Point.Ten,Point.Jack,Point.Queen,Point.King)
public = []
players = [None, None, None, None, None, None]
action = []
last_street = []
last_public = []
table_stat = TableStat.END
btn = 0
cur_player = 0
seat_loc = [None, None, None, None, None, None]

app = FastAPI()
dealer = Dealer()

def showdown():
    global last_result, last_winners
    cmp_dict = {}
    winner = []
    for i in range(6):
        if players[i] is not None and players[i].status is not PlayerStat.FOLDED:
            cmp_dict[i] = find_best_hand(players[i].hand, public)
            last_result[players[i].name] = [translate(card) for card in players[i].hand]
    winner = compare_hands_for_players(cmp_dict)
    for win in winner:
        players[win].win(pot // len(winner))

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
            player.bet_street = 0
            if player.stack == 0:
                player.stack = 2000
    pot = 0
    dealer.shuffle()

def step():
    global table_stat, cur_player, action, last_bet, last_street, last_public
    sb = next_player(btn)
    bb = next_player(sb)
    if table_stat == TableStat.END:
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
        i = (i + 1) % 6
        if players[i] is not None:
            return i

def next_mover(i):
    j = i
    while 1:
        i = (i + 1) % 6
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
    elif move.move.startswith('f'):
        players[move.seat].fold()
        cnt = 0
        j = 0
        for i in range(6):
            if players[i] is not None and players[i].status is not PlayerStat.FOLDED:
                cnt += 1
                j = i
        if cnt == 1:
            players[j].win(pot)
            table_stat = TableStat.END
            clear()
            step()
            return

    cur_player = next_mover(move.seat)
    if cur_player == move.seat:
        step()

@app.get("/d")
def deal_card():
    return dealer.deal()

@app.get("/s")
def table_info(seat: int):
    global table_stat, public, pot, action, last_street, btn, cur_player, players, last_result, last_winners, last_public
    return {
        'tablestat': table_stat,
        'public': [translate(card) for card in public],
        'pot': pot,
        'actionLine': action,
        "last_street": last_street,
        'btn': btn,
        'actPlayer': cur_player,
        'stack': players[seat].stack,
        'hand':[translate(card) for card in players[seat].hand],
        "last_result": last_result,
        "last_winners": last_winners,
        "last_public": [translate(card) for card in last_public],
    }

@app.post('/l')
def login(name: User):
    for i in range(6):
        if players[i] == None:
            players[i] = Player(name.name, i)
            cnt = 0
            for player in players:
                if player is not None:
                    cnt += 1
            if cnt == 2:
                step()
            return i
    return -1

@app.post('/q')
def quit(name: User):
    players.remove(name.name)

if __name__ == '__main__':
    uvicorn.run("main:app", port=10532, log_level='warning')