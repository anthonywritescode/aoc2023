from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _n_diff(left: list[str], right: list[str]) -> int:
    n = 0
    for left_s, right_s in zip(left, right):
        for left_c, right_c in zip(left_s, right_s):
            if left_c != right_c:
                n += 1
                if n > 1:
                    return 2
    return n


def _find_reflection(parts: list[str]) -> int:
    for i in range(1, len(parts)):
        left = parts[:i]
        left.reverse()
        right = parts[i:]
        min_length = min(len(left), len(right))
        if _n_diff(left[:min_length], right[:min_length]) == 1:
            return i
    else:
        return 0


def _columns(s: str) -> list[str]:
    return [''.join(t) for t in zip(*s.splitlines())]


def compute(s: str) -> int:
    total = 0
    for part in s.split('\n\n'):
        total += _find_reflection(_columns(part))
        total += 100 * _find_reflection(part.splitlines())
    return total


INPUT_S = '''\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
'''
EXPECTED = 400


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
