from fastapi import FastAPI
import uvicorn
from enum import IntEnum, Enum
import uvicorn
from fastapi import FastAPI
import time
import random
from pydantic import BaseModel
from collections import Counter
from itertools import combinations

pot = 0

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

class TableStat(Enum):
    END = 0
    PRE = 1
    FLOP = 2
    TURN = 3
    RIVER = 4
    SHOWDOWN = 5

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
    def __init__(self):
        self.hand = []
        self.stack = 2000
        self.status = PlayerStat.FOLDED
    
    def bet(self, chips):
        global pot
        if self.stack < chips:
            raise NoEnoughChipsException(f'bet {chips} but only have {self.stack}')
        else:
            self.stack -= chips
            pot += chips
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
    max_count = max(value_count.values())
    
    if max_count == 4:
        return 7, max(value_count, key=value_count.get)  # Four of a Kind
    elif max_count == 3 and len(value_count) == 2:
        return 6, max(value_count, key=value_count.get), min(value_count, key=value_count.get)  # Full House
    elif is_flush(cards):
        if is_straight(cards):
            return 8, max(int(card[1]) for card in cards)  # Straight Flush
        else:
            return 5, max(int(card[1]) for card in cards)  # Flush
    elif is_straight(cards):
        return 4, max(int(card[1]) for card in cards)  # Straight
    elif max_count == 3:
        return 3, max(value_count, key=value_count.get)  # Three of a Kind
    elif max_count == 2 and len(value_count) == 3:
        return 2, max(value_count, key=value_count.get), min(value_count, key=value_count.get)  # Two Pair
    elif max_count == 2:
        return 1, max(value_count, key=value_count.get)  # One Pair
    else:
        return 0, max(int(card[1]) for card in cards)  # High Card

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
    max_rank = -1
    
    for combo in combinations(all_cards, 5):
        if best_hand == None:
            best_hand = combo
        else:
            if compare_hands(combo, best_hand) == 1:
                best_hand = combo
    return best_hand

def compare_hands_for_players(hands):
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
players = [None, None, None, None, None, None]
action = []
table_stat = TableStat.END
btn = 0
seats = [0, 0, 0, 0, 0, 0]
cur_player = 0
seat_loc = [None, None, None, None, None, None]
last_bet = 0

app = FastAPI()
dealer = Dealer()

def showdown():
    cmp_dict = {}
    for i in range(6):
        if players[i] is not None and players[i].status is PlayerStat.MOVED:
            cmp_dict[i] = find_best_hand(players[i].hand, public)
    winner = compare_hands_for_players(cmp_dict)
    for win in winner:
        players[win].win(pot // len(winner))

def clear():
    global public, pot, action, btn
    public.clear()
    action.clear()
    btn = next_player(btn)
    for player in players:
        if player is not None:
            player.status = PlayerStat.FOLDED
            player.hand.clear()
    pot = 0
    dealer.shuffle()

def step():
    global table_stat, cur_player, action
    sb = next_player(btn)
    bb = next_player(sb)
    if table_stat == TableStat.END:
        table_stat = TableStat.PRE
        for player in players:
            if player is not None:
                player.hand.append(dealer.deal())
                player.hand.append(dealer.deal())
                player.status = PlayerStat.WAITING
        players[sb].bet(10)
        players[sb].status = PlayerStat.MOVED
        action.append(f'{sb} b 10')
        action.append(f'{bb} b 20')
        players[bb].bet(20)
        players[bb].status = PlayerStat.MOVED
        cur_player = next_player(bb)
    elif table_stat == TableStat.PRE:
        action.clear()
        table_stat = TableStat.FLOP
        public.append(dealer.deal())
        public.append(dealer.deal())
        public.append(dealer.deal())
        cur_player = next_mover(sb)
    elif table_stat == TableStat.FLOP:
        action.clear()
        table_stat = TableStat.TURN
        public.append(dealer.deal())
        cur_player = next_mover(sb)
    elif table_stat == TableStat.TURN:
        action.clear()
        table_stat = TableStat.RIVER
        public.append(dealer.deal())
        cur_player = next_mover(sb)
    elif table_stat == TableStat.RIVER:
        action.clear()
        table_stat = TableStat.SHOWDOWN
        cur_player = next_mover(sb)
    elif table_stat == TableStat.SHOWDOWN:
        showdown()
        table_stat = TableStat.END
        clear()
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
        if players[i] is not None and players[i].status is PlayerStat.WAITING:
            return i
        if i == j:
            return i

@app.post('/a')
def reg_act(move: Move):
    global cur_player, action, table_stat
    action.append(f'{seat_loc[move.seat]} ' + move.move)
    if move.move.startswith('b'):
        players[move.seat].bet(eval(move.move.split()[-1]))
        for player in players:
            if player is not None:
                player.status = PlayerStat.WAITING
    elif move.move.startswith('c'):
        if last_bet != 0:
            try:
                players[move.seat].bet(last_bet)
            except:
                players[move.seat].bet(players[move.seat].stack)
    elif move.move.startswith('f'):
        players[move.seat].status = PlayerStat.FOLDED
        cnt = 0
        for player in players:
            if player is not None:
                if player.status is not PlayerStat.FOLDED:
                    cnt += 1
        if cnt == 1:
            players[move.seat].win(pot)
            table_stat = TableStat.END
            clear()
            step()
            return

    players[move.seat].status = PlayerStat.MOVED
    cur_player = next_mover(move.seat)
    if cur_player == move.seat:
        step()

@app.get("/d")
def deal_card():
    return dealer.deal()

@app.get("/s")
def table_info(seat: int):
    return {
        'tablestat': table_stat,
        'public': public,
        'pot': pot,
        'actionLine': action,
        'seats': seats,
        'btn': btn,
        'actPlayer': cur_player,
        'stack': players[seat].stack,
        'hand': players[seat].hand
    }

@app.post('/l')
def login(name: User):
    for i in range(6):
        if seats[i] == 0:
            seats[i] = 1
            players[i] = Player()
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
    uvicorn.run(app, port=10532)