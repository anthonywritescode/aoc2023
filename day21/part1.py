from __future__ import annotations

import argparse
import operator
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str, *, steps: int = 64) -> int:
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c == 'S':
                start = (x, y)

    width = len(s.splitlines()[0])
    height = len(s.splitlines())

    seen = {start}
    coords = support.parse_coords_hash(s)
    paths = [start]
    for _ in range(steps):
        new_paths = []
        for path in paths:
            for cand in support.adjacent_4(*path):
                if (
                        (cand[0] % width, cand[1] % height) not in coords and
                        cand not in seen
                ):
                    new_paths.append(cand)
                    seen.add(cand)
        paths = new_paths

    # making some assumptions here :)
    if steps % 2 == 0:
        op = operator.eq
    else:
        op = operator.ne
    return len({
        (x, y)
        for x, y in seen
        if op((x + y) % 2, (start[0] + start[1]) % 2)
    })


INPUT_S = '''\
...........
.....###.#.
.###.##..#.
..#.#...#..
....#.#....
.##..S####.
.##..#...#.
.......##..
.##.#.####.
.##..##.##.
...........
'''


@pytest.mark.parametrize(
    ('input_s', 'steps', 'expected'),
    (
        (INPUT_S, 1, 2),
        (INPUT_S, 3, 6),
        (INPUT_S, 6, 16),
        (INPUT_S, 50, 1594),
        (INPUT_S, 100, 6536),
    ),
)
def test(input_s: str, steps: int, expected: int) -> None:
    assert compute(input_s, steps=steps) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
