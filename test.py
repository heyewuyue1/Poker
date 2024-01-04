from collections import Counter
from itertools import combinations

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
    global last_result, last_winners, players
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
    last_result = {}
    return winner

res = compare_hands([(0, 12), (1, 12), (3, 10), (3, 10), (2, 4)], [(0, 12), (1, 12), (3, 10), (3, 10), (2, 5)])
print(res)