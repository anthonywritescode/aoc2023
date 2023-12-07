from __future__ import annotations

import argparse
import collections
import enum
import os.path
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

W = enum.IntEnum('W', 'FIVE FOUR FULL THREE TWO ONE HIGH')
ORDER = 'AKQT98765432J'


class Hand(NamedTuple):
    w: W
    order: tuple[int, ...]
    bid: int
    s: str

    @classmethod
    def parse(cls, s: str) -> Hand:
        hand, n_s = s.split()
        counts = collections.Counter(hand)

        order = tuple(ORDER.index(c) for c in hand)

        if hand != 'JJJJJ':
            js = counts.pop('J', 0)
            (c, _), = counts.most_common(1)
            counts[c] += js

        common = counts.most_common(2)
        if len(common) == 1:
            tp = W.FIVE
        elif common[0][1] == 4:
            tp = W.FOUR
        elif common[0][1] == 3 and common[1][1] == 2:
            tp = W.FULL
        elif common[0][1] == 3:
            tp = W.THREE
        elif common[0][1] == 2 and common[1][1] == 2:
            tp = W.TWO
        elif common[0][1] == 2:
            tp = W.ONE
        else:
            tp = W.HIGH

        return cls(tp, order, int(n_s), hand)


def compute(s: str) -> int:
    hands = [Hand.parse(line) for line in s.splitlines()]
    hands.sort(reverse=True)
    return sum(i * hand.bid for i, hand in enumerate(hands, 1))


INPUT_S = '''\
32T3K 765
T55J5 684
KK677 28
KTJJT 220
QQQJA 483
'''
EXPECTED = 5905


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
