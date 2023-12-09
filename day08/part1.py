from __future__ import annotations

import argparse
import itertools
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    dirs, rest = s.split('\n\n')
    paths = {}
    for line in rest.splitlines():
        src, rest = line.split(' = ')
        left, right = rest.strip('()').split(', ')
        paths[src] = (left, right)

    i = 0
    current = 'AAA'
    for c in itertools.cycle(dirs):
        i += 1
        if c == 'L':
            current = paths[current][0]
        else:
            current = paths[current][1]
        if current == 'ZZZ':
            break
    return i


INPUT_S = '''\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)
'''
EXPECTED = 6


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
