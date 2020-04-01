#!/usr/bin/env python
# -*- coding: utf-8 -*-

# -----------------
# Реализуйте функцию best_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. У каждой карты есть масть(suit) и
# ранг(rank)
# Масти: трефы(clubs, C), пики(spades, S), червы(hearts, H), бубны(diamonds, D)
# Ранги: 2, 3, 4, 5, 6, 7, 8, 9, 10 (ten, T), валет (jack, J), дама (queen, Q), король (king, K), туз (ace, A)
# Например: AS - туз пик (ace of spades), TH - дестяка черв (ten of hearts), 3C - тройка треф (three of clubs)

# Задание со *
# Реализуйте функцию best_wild_hand, которая принимает на вход
# покерную "руку" (hand) из 7ми карт и возвращает лучшую
# (относительно значения, возвращаемого hand_rank)
# "руку" из 5ти карт. Кроме прочего в данном варианте "рука"
# может включать джокера. Джокеры могут заменить карту любой
# масти и ранга того же цвета, в колоде два джокерва.
# Черный джокер '?B' может быть использован в качестве треф
# или пик любого ранга, красный джокер '?R' - в качестве черв и бубен
# любого ранга.

# Одна функция уже реализована, сигнатуры и описания других даны.
# Вам наверняка пригодится itertools.
# Можно свободно определять свои функции и т.п.
# -----------------
import itertools
from typing import Union
from typing import List
from typing import Tuple

RANK: str = "23456789TJQKA"


def hand_rank(hand: List[str]) -> Tuple[int, List[int]]:
    """Возвращает значение определяющее ранг 'руки'"""
    ranks = card_ranks(hand)
    if straight(ranks) and flush(hand):
        return (8, max(ranks))
    elif kind(4, ranks):
        return (7, kind(4, ranks), kind(1, ranks))
    elif kind(3, ranks) and kind(2, ranks):
        return (6, kind(3, ranks), kind(2, ranks))
    elif flush(hand):
        return (5, ranks)
    elif straight(ranks):
        return (4, max(ranks))
    elif kind(3, ranks):
        return (3, kind(3, ranks), ranks)
    elif two_pair(ranks):
        return (2, two_pair(ranks), ranks)
    elif kind(2, ranks):
        return (1, kind(2, ranks), ranks)
    else:
        return (0, ranks)


def card_ranks(hand: List[str]) -> List[int]:
    """Возвращает список рангов (его числовой эквивалент),
    отсортированный от большего к меньшему"""
    ranks = []
    for rank, suit in hand:
        ranks.append(RANK.index(rank))
    return sorted(ranks, reverse=True)


def flush(hand: List[str]) -> bool:
    """Возвращает True, если все карты одной масти"""
    list_suit = []
    for rank, suit in hand:
        list_suit.append(suit)
    return True if len(set(list_suit)) == 1 else False


def straight(ranks: List[int]) -> bool:
    """Возвращает True, если отсортированные ранги формируют последовательность 5ти,
    где у 5ти карт ранги идут по порядку (стрит)"""
    for comb_ranks in itertools.combinations(ranks, 5):
        str_rank = ''.join(str(elem) for elem in comb_ranks)
        if str_rank in ''.join(sorted(RANK, key=lambda x: RANK.index(x), reverse=1)):
            return True
    return False


def kind(n: int, ranks: List[int]) -> Union[int, None]:
    """Возвращает первый ранг, который n раз встречается в данной руке.
    Возвращает None, если ничего не найдено"""
    for rank, group_rank in itertools.groupby(ranks):
        if len(list(group_rank)) == n:
            return rank


def two_pair(ranks: List[int]) -> Union[List[int], None]:
    """Если есть две пары, то возврщает два соответствующих ранга,
    иначе возвращает None"""
    pair_one = kind(2, ranks)
    if pair_one:
        ranks.remove(pair_one)
        ranks.remove(pair_one)
    pair_two = kind(2, ranks)
    return [pair_one, pair_two] if pair_one and pair_two else None


def best_hand(hand: List[str]) -> List[str]:
    """Из "руки" в 7 карт возвращает лучшую "руку" в 5 карт """
    b_h = []
    for comb in itertools.combinations(hand, 5):
        b_h.append(comb)
    return max(b_h, key=hand_rank)


def best_wild_hand(hand: List[str]) -> List[str]:
    """best_hand но с джокерами"""
    if "?B" and "?R" in hand:
        hand.remove("?B")
        hand.remove("?R")
        hand_rem = hand[:]
        hand_b = []
        for rank, suit in itertools.product(RANK, "CS"):
            for rank1, suit1 in itertools.product(RANK, "HD"):
                if rank + suit not in hand_rem and rank1 + suit1 not in hand_rem:
                    hand.append(rank + suit)
                    hand.append(rank1 + suit1)
                hand_b.append(best_hand(hand))
                hand = hand_rem[:]
        return max(hand_b, key=hand_rank)
    elif "?B" in hand:
        hand.remove("?B")
        hand_rem = hand[:]
        hand_b = []
        for rank, suit in itertools.product(RANK, "CS"):
            if rank + suit not in hand_rem:
                hand.append(rank + suit)
            hand_b.append(best_hand(hand))
            hand = hand_rem[:]
        return max(hand_b, key=hand_rank)
    elif "?R" in hand:
        hand.remove("?R")
        hand_rem = hand[:]
        hand_b = []
        for rank, suit in itertools.product(RANK, "HD"):
            if rank + suit not in hand_rem:
                hand.append(rank + suit)
            hand_b.append(best_hand(hand))
            hand = hand_rem[:]
        return max(hand_b, key=hand_rank)
    else:
        return best_hand(hand)


def test_best_hand() -> None:
    print("test_best_hand...")
    assert (sorted(best_hand("6C 7C 8C 9C TC 5C JS".split()))
            == ['6C', '7C', '8C', '9C', 'TC'])
    assert (sorted(best_hand("TD TC TH 7C 7D 8C 8S".split()))
            == ['8C', '8S', 'TC', 'TD', 'TH'])
    assert (sorted(best_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


def test_best_wild_hand() -> None:
    print("test_best_wild_hand...")
    assert (sorted(best_wild_hand("6C 7C 8C 9C TC 5C ?B".split()))
            == ['7C', '8C', '9C', 'JC', 'TC'])
    assert (sorted(best_wild_hand("TD TC 5H 5C 7C ?R ?B".split()))
            == ['7C', 'TC', 'TD', 'TH', 'TS'])
    assert (sorted(best_wild_hand("JD TC TH 7C 7D 7S 7H".split()))
            == ['7C', '7D', '7H', '7S', 'JD'])
    print('OK')


if __name__ == '__main__':
    test_best_hand()
    test_best_wild_hand()
