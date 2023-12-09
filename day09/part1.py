from __future__ import annotations

import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def extrapolate(ns: list[int]) -> int:
    diffs = [ns]
    while not all(n == 0 for n in diffs[-1]):
        diffs.append([b - a for a, b in itertools.pairwise(diffs[-1])])
    diffs[-1].append(0)

    for i in range(len(diffs) - 2, -1, -1):
        diffs[i].append(diffs[i][-1] + diffs[i + 1][-1])

    return diffs[0][-1]


def compute(s: str) -> int:
    lines = s.splitlines()
    return sum(
        extrapolate(support.parse_numbers_split(line))
        for line in lines
    )


INPUT_S = '''\
0 3 6 9 12 15
1 3 6 10 15 21
10 13 16 21 30 45
'''
EXPECTED = 114


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
