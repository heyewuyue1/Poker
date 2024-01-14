from enum import IntEnum

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

def is_straight(cards):
    values = sorted([int(card[1]) for card in cards], reverse=True)
    print(values)
    return all(values[i] - 1 == values[i + 1] for i in range(len(values) - 1)) or values == [14, 5, 4, 3, 2]

print(is_straight([(0, Point.Three), (0, Point.Four), (0, Point.Two), (0, Point.Five), (0, Point.Ace)]))