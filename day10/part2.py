from __future__ import annotations

import argparse
import collections
import os.path
from typing import TypeAlias

import pytest

import support
from support import Direction4

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


MOVE = {
    (Direction4.UP, '|'): Direction4.UP,
    (Direction4.UP, '7'): Direction4.LEFT,
    (Direction4.UP, 'F'): Direction4.RIGHT,
    (Direction4.DOWN, '|'): Direction4.DOWN,
    (Direction4.DOWN, 'J'): Direction4.LEFT,
    (Direction4.DOWN, 'L'): Direction4.RIGHT,
    (Direction4.RIGHT, '-'): Direction4.RIGHT,
    (Direction4.RIGHT, 'J'): Direction4.UP,
    (Direction4.RIGHT, '7'): Direction4.DOWN,
    (Direction4.LEFT, '-'): Direction4.LEFT,
    (Direction4.LEFT, 'L'): Direction4.UP,
    (Direction4.LEFT, 'F'): Direction4.DOWN,
}
LR: TypeAlias = dict[tuple[Direction4, str], tuple[Direction4, ...]]
LEFT: LR = {
    (Direction4.UP, '|'): (Direction4.LEFT,),
    (Direction4.UP, '7'): (),
    (Direction4.UP, 'F'): (Direction4.UP, Direction4.LEFT),
    (Direction4.DOWN, '|'): (Direction4.RIGHT,),
    (Direction4.DOWN, 'J'): (Direction4.RIGHT, Direction4.DOWN),
    (Direction4.DOWN, 'L'): (),
    (Direction4.RIGHT, '-'): (Direction4.UP,),
    (Direction4.RIGHT, 'J'): (),
    (Direction4.RIGHT, '7'): (Direction4.UP, Direction4.RIGHT),
    (Direction4.LEFT, '-'): (Direction4.DOWN,),
    (Direction4.LEFT, 'L'): (Direction4.DOWN, Direction4.LEFT),
    (Direction4.LEFT, 'F'): (),
}
RIGHT: LR = {
    (Direction4.UP, '|'): (Direction4.RIGHT,),
    (Direction4.UP, '7'): (Direction4.UP, Direction4.RIGHT),
    (Direction4.UP, 'F'): (),
    (Direction4.DOWN, '|'): (Direction4.LEFT,),
    (Direction4.DOWN, 'J'): (),
    (Direction4.DOWN, 'L'): (Direction4.LEFT, Direction4.DOWN),
    (Direction4.RIGHT, '-'): (Direction4.DOWN,),
    (Direction4.RIGHT, 'J'): (Direction4.DOWN, Direction4.RIGHT),
    (Direction4.RIGHT, '7'): (),
    (Direction4.LEFT, '-'): (Direction4.UP,),
    (Direction4.LEFT, 'L'): (),
    (Direction4.LEFT, 'F'): (Direction4.UP, Direction4.LEFT),
}


def compute(s: str) -> int:
    coords = {}
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            coords[(x, y)] = c
            if c == 'S':
                start = (x, y)

    b_x, b_y = support.bounds(coords)

    seen = {start}

    # seed our beginning!
    for d in Direction4:
        cand = d.apply(*start)
        cand_c = coords.get(cand, '.')
        next_d = MOVE.get((d, cand_c))
        if next_d is not None:
            d, pos = (next_d, cand)
            seen.add(pos)
            break

    orig_d, orig_pos = d, pos

    while True:
        pos = d.apply(*pos)
        if pos in seen:
            break
        else:
            c = coords[pos]
            d = MOVE[(d, c)]
            seen.add(pos)

    coords = {k: v if k in seen else '.' for k, v in coords.items()}
    for y in range(-1, b_y.max + 2):
        for x in range(-1, b_x.max + 2):
            coords.setdefault((x, y), '.')

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
    flood_fill((-1, -1), outside)

    def left_or_right() -> LR:
        d, pos = orig_d, orig_pos
        while True:
            pos = d.apply(*pos)

            c = coords[pos]

            for cand_d in LEFT[(d, c)]:
                if cand_d.apply(*pos) in outside:
                    return RIGHT

            for cand_d in RIGHT[(d, c)]:
                if cand_d.apply(*pos) in outside:
                    return LEFT

            d = MOVE[(d, c)]

    filled: set[tuple[int, int]] = set()
    check = left_or_right()
    d, pos = orig_d, orig_pos
    while True:
        pos = d.apply(*pos)

        if pos == start:
            break

        c = coords[pos]

        for cand_d in check[(d, c)]:
            cand_pos = cand_d.apply(*pos)
            if coords[cand_pos] == '.':
                flood_fill(cand_pos, filled)

        d = MOVE[(d, c)]

    return len(filled)


INPUT_S = '''\
...........
.S-------7.
.|F-----7|.
.||.....||.
.||.....||.
.|L-7.F-J|.
.|..|.|..|.
.L--J.L--J.
...........
'''
EXPECTED = 4
INPUT_S_2 = '''\
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
'''
EXPECTED_2 = 10


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
        (INPUT_S_2, EXPECTED_2),
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
