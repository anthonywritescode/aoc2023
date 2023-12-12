from __future__ import annotations

import argparse
import os.path
import re
from typing import Generator

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def gen(s: str) -> Generator[str, None, None]:
    if not s:
        yield ''
        return
    for rest in gen(s[1:]):
        if s[0] == '?':
            yield '.' + rest
            yield '#' + rest
        else:
            yield s[0] + rest


def counts(s: str) -> list[int]:
    s = re.sub(r'\.+', '.', s.strip('.'))
    return [len(s) for s in s.split('.')]


def compute(s: str) -> int:
    lines = s.splitlines()
    total = 0
    for line in lines:
        pattern, rest = line.split(' ')
        got_counts = support.parse_numbers_comma(rest)
        for cand in gen(pattern):
            if counts(cand) == got_counts:
                total += 1
    return total


INPUT_S = '''\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
'''
EXPECTED = 21


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
