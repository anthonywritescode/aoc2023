from __future__ import annotations

import argparse
import collections
import os.path
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

ORDER = 'J23456789TQKA'


class Hand(NamedTuple):
    w: tuple[int, ...]
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

        w = tuple(n for _, n in counts.most_common(2))
        order = tuple(ORDER.index(c) for c in hand)

        return cls(w, order, int(n_s), hand)


def compute(s: str) -> int:
    hands = [Hand.parse(line) for line in s.splitlines()]
    hands.sort()
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
