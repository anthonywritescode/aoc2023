from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()

    empty_y = []
    for y, line in enumerate(lines):
        if '#' not in line:
            empty_y.append(y)
    empty_x = []
    for x in range(len(lines[0])):
        if all(line[x] == '.' for line in lines):
            empty_x.append(x)

    points = []
    for y, line in enumerate(lines):
        for x, c in enumerate(line):
            if c == '#':
                points.append((
                    x + sum(1 for c_x in empty_x if c_x < x),
                    y + sum(1 for c_y in empty_y if c_y < y),
                ))

    total = 0
    for i, (px, py) in enumerate(points):
        for (ox, oy) in points[i + 1:]:
            total += abs(ox - px) + abs(oy - py)
    return total


INPUT_S = '''\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
'''
EXPECTED = 374


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
