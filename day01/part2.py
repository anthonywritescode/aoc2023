from __future__ import annotations

import argparse
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

DIGIT = {
    'one': '1',
    'two': '2',
    'three': '3',
    'four': '4',
    'five': '5',
    'six': '6',
    'seven': '7',
    'eight': '8',
    'nine': '9',
    'zero': '0',
}
PAT = re.compile(fr'(\d|{"|".join(DIGIT)})')
PAT_REV = re.compile(fr'(\d|{"|".join(s[::-1] for s in DIGIT)})')


def _must_search(p: re.Pattern[str], s: str) -> str:
    match = p.search(s)
    assert match is not None
    return match[0]


def compute(s: str) -> int:
    total = 0
    lines = s.splitlines()
    for line in lines:
        first = _must_search(PAT, line)
        last = _must_search(PAT_REV, line[::-1])[::-1]
        digits = [DIGIT.get(first, first), DIGIT.get(last, last)]
        total += int(digits[0]) * 10 + int(digits[-1])
    return total


INPUT_S = '''\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
1twone
'''
EXPECTED = 292


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
