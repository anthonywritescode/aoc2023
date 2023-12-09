from __future__ import annotations

import argparse
import itertools
import math
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

    def period(current: str) -> int:
        i = 0
        for c in itertools.cycle(dirs):
            i += 1
            if c == 'L':
                current = paths[current][0]
            else:
                current = paths[current][1]
            if current.endswith('Z'):
                return i

        raise NotImplementedError('unreachable')

    ret = 1
    for k in paths:
        if k.endswith('A'):
            ret = math.lcm(ret, period(k))
    return ret


INPUT_S = '''\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
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
