from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

NUM = re.compile(r'\d+')


def compute(s: str) -> int:
    coords = {}
    lines = s.splitlines()
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c != '.' and not c.isdigit():
                coords[(x, y)] = c

    # def symbol_in_

    total = 0
    for y, line in enumerate(lines):
        for match in NUM.finditer(line):
            matched = False
            for i in range(*match.span()):
                for cand_x, cand_y in support.adjacent_8(i, y):
                    if (cand_x, cand_y) in coords:
                        break
                else:
                    continue
                matched = True

            if matched:
                total += int(match[0])

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
EXPECTED = 4361


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
