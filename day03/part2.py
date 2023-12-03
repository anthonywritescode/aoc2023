from __future__ import annotations

import argparse
import os.path
import re
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

NUM = re.compile(r'\d+')


class Num(NamedTuple):
    n: int
    y: int
    x: tuple[int, int]

    def adjacent(self, x: int, y: int) -> bool:
        return (
            self.x[0] - 1 <= x < self.x[1] + 1 and
            self.y - 1 <= y <= self.y + 1
        )


def compute(s: str) -> int:
    lines = s.splitlines()

    stars = []

    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '*':
                stars.append((x, y))

    nums = []
    total = 0
    for y, line in enumerate(lines):
        for match in NUM.finditer(line):
            nums.append(Num(int(match[0]), y, match.span()))

    total = 0
    for x, y in stars:
        adj = [
            num
            for num in nums
            if num.adjacent(x, y)
        ]
        if len(adj) == 2:
            total += adj[0].n * adj[1].n

    return total


INPUT_S = '''\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
'''
EXPECTED = 467835


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
