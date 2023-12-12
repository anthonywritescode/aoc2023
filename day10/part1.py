from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


MOVE = {
    (support.Direction4.UP, '|'): support.Direction4.UP,
    (support.Direction4.UP, '7'): support.Direction4.LEFT,
    (support.Direction4.UP, 'F'): support.Direction4.RIGHT,
    (support.Direction4.DOWN, '|'): support.Direction4.DOWN,
    (support.Direction4.DOWN, 'J'): support.Direction4.LEFT,
    (support.Direction4.DOWN, 'L'): support.Direction4.RIGHT,
    (support.Direction4.RIGHT, '-'): support.Direction4.RIGHT,
    (support.Direction4.RIGHT, 'J'): support.Direction4.UP,
    (support.Direction4.RIGHT, '7'): support.Direction4.DOWN,
    (support.Direction4.LEFT, '-'): support.Direction4.LEFT,
    (support.Direction4.LEFT, 'L'): support.Direction4.UP,
    (support.Direction4.LEFT, 'F'): support.Direction4.DOWN,
}


def compute(s: str) -> int:
    coords = {}
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            coords[(x, y)] = c
            if c == 'S':
                start = (x, y)

    seen = {start}

    paths = []
    # seed our beginning!
    for d in support.Direction4:
        cand = d.apply(*start)
        cand_c = coords.get(cand, '.')
        next_d = MOVE.get((d, cand_c))
        if next_d is not None:
            paths.append((1, next_d, cand))
            seen.add(cand)

    while True:
        new_paths = []
        for n, d, pos in paths:
            cand = d.apply(*pos)
            cand_c = coords.get(cand, '.')
            next_d = MOVE.get((d, cand_c))
            if next_d is not None:
                if cand in seen:
                    return n + 1
                new_paths.append((n + 1, next_d, cand))
                seen.add(cand)
        paths = new_paths

    raise AssertionError('unreachable')


INPUT_S = '''\
.....
.S-7.
.|.|.
.L-J.
.....
'''
EXPECTED = 4


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
