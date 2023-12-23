from __future__ import annotations

import argparse
import collections
import os.path

import pytest

import support
from support import Direction4

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

DIRS = {
    'R': Direction4.RIGHT,
    'L': Direction4.LEFT,
    'U': Direction4.UP,
    'D': Direction4.DOWN,
}


def compute(s: str) -> int:
    pos = (0, 0)
    seen = {pos}
    for line in s.splitlines():
        d_s, n_s, _ = line.split()
        d = DIRS[d_s]
        n = int(n_s)
        for _ in range(n):
            pos = d.apply(*pos)
            seen.add(pos)

    bx, by = support.bounds(seen)
    coords = {
        (x, y): '#' if (x, y) in seen else '.'
        for y in range(by.min - 1, by.max + 2)
        for x in range(bx.min - 1, bx.max + 2)
    }

    def flood_fill(pos: tuple[int, int], seen: set[tuple[int, int]]) -> None:
        seen.add(pos)
        todo = collections.deque([pos])
        while todo:
            pos = todo.popleft()
            for d in Direction4:
                cand = d.apply(*pos)
                if coords.get(cand) != '.':
                    continue
                elif cand in seen:
                    continue
                else:
                    seen.add(cand)
                    todo.append(cand)

    outside: set[tuple[int, int]] = set()
    flood_fill((bx.min - 1, by.min - 1), outside)

    inside: set[tuple[int, int]] = set()
    pos = (0, 0)
    for line in s.splitlines():
        d_s, n_s, _ = line.split()
        d = DIRS[d_s]
        n = int(n_s)
        for _ in range(n):
            pos = d.apply(*pos)
            seen.add(pos)

            for cand in (d.cw.apply(*pos), d.ccw.apply(*pos)):
                if cand not in outside and coords.get(cand) == '.':
                    flood_fill(cand, inside)

    return len(inside) + len(seen)


INPUT_S = '''\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
'''
EXPECTED = 62


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
