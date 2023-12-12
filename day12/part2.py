from __future__ import annotations

import argparse
import functools
import os.path
import re

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

DOTS = re.compile(r'\.+')


def _can_place(pattern: str, i: int, piece: str) -> bool:
    for pat_c, piece_c in zip(pattern[i:], piece):
        if pat_c == '?':
            continue
        elif pat_c != piece_c:
            return False
    else:
        return True


@functools.lru_cache(maxsize=4096 * 4)
def _compute(pattern: str, pieces: tuple[str, ...]) -> int:
    if not pieces:
        if '#' in pattern:
            return 0
        else:
            return 1

    first = pieces[0]
    rest = tuple(pieces[1:])

    total = 0
    maximum = len(''.join(pieces))
    for i in range(0, len(pattern) - maximum + 1):
        # try and place piece[0] @ i
        if _can_place(pattern, i, first):
            total += 1 * _compute(pattern[i + len(first):], rest)
        if pattern[i] == '#':
            break
    return total


def _simplify(pattern: str) -> str:
    return DOTS.sub('.', pattern.strip('.')) + '.'


def compute(s: str) -> int:
    lines = s.splitlines()

    total = 0
    for line in lines:
        pattern, rest = line.split(' ')
        pattern = '?'.join([pattern] * 5)
        counts = support.parse_numbers_comma(rest) * 5
        pieces = tuple(f'{"#" * count}.' for count in counts)
        pattern = _simplify(pattern)
        total += _compute(pattern, pieces)

    return total


INPUT_S = '''\
???.### 1,1,3
.??..??...?##. 1,1,3
?#?#?#?#?#?#?#? 1,3,1,6
????.#...#... 4,1,1
????.######..#####. 1,6,5
?###???????? 3,2,1
'''
EXPECTED = 525152


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        # ('?#?????##????#??. 1,9', 3),
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
