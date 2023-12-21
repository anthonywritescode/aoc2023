from __future__ import annotations

import argparse
import os.path

import pytest

import support
from support import Direction4

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


REFLECT = {
    (Direction4.RIGHT, '/'): Direction4.UP,
    (Direction4.LEFT, '/'): Direction4.DOWN,
    (Direction4.UP, '/'): Direction4.RIGHT,
    (Direction4.DOWN, '/'): Direction4.LEFT,
    (Direction4.RIGHT, '\\'): Direction4.DOWN,
    (Direction4.LEFT, '\\'): Direction4.UP,
    (Direction4.UP, '\\'): Direction4.LEFT,
    (Direction4.DOWN, '\\'): Direction4.RIGHT,
}


def compute(s: str) -> int:
    coords = {
        (x, y): c
        for y, line in enumerate(s.splitlines())
        for x, c in enumerate(line)
    }

    def _compute(d: Direction4, x: int, y: int) -> int:
        seen: set[tuple[int, int]] = set()
        visited: set[tuple[Direction4, tuple[int, int]]] = set()
        paths = [(d, (x, y))]

        while paths:
            d, (x, y) = paths.pop()

            # have we looped on ourselves?
            if (d, (x, y)) in visited:
                continue
            else:
                visited.add((d, (x, y)))

            x, y = d.apply(x, y)
            c = coords.get((x, y))
            if c is None:  # done: out of bounds!
                continue
            else:
                seen.add((x, y))
                if c == '|' and d in {Direction4.RIGHT, Direction4.LEFT}:
                    paths.append((Direction4.UP, (x, y)))
                    paths.append((Direction4.DOWN, (x, y)))
                elif c == '-' and d in {Direction4.UP, Direction4.DOWN}:
                    paths.append((Direction4.LEFT, (x, y)))
                    paths.append((Direction4.RIGHT, (x, y)))
                elif c in '/\\':
                    paths.append((REFLECT[(d, c)], (x, y)))
                else:
                    paths.append((d, (x, y)))

        return len(seen)

    maximum = 0
    bx, by = support.bounds(coords)
    for x in bx.range:
        maximum = max(maximum, _compute(Direction4.DOWN, x, by.min - 1))
        maximum = max(maximum, _compute(Direction4.UP, x, by.max + 1))
    for y in by.range:
        maximum = max(maximum, _compute(Direction4.RIGHT, bx.min - 1, y))
        maximum = max(maximum, _compute(Direction4.LEFT, bx.max + 1, y))
    return maximum


INPUT_S = r'''
.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
'''.lstrip()
EXPECTED = 51


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
