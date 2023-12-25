from __future__ import annotations

import argparse
import fractions
import operator
import os.path
import sys

import pytest
import z3

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def quadratic_fit(
        pts: tuple[tuple[int, int], ...],
) -> tuple[fractions.Fraction, fractions.Fraction, fractions.Fraction]:
    solver = z3.Solver()
    a = z3.Real('a')
    b = z3.Real('b')
    c = z3.Real('c')
    for x, y in pts:
        solver.add(y == a * (x ** 2) + b * x + c)
    assert solver.check() == z3.sat
    model = solver.model()
    return (
        model[a].as_fraction(),
        model[b].as_fraction(),
        model[c].as_fraction(),
    )


def compute(s: str, *, steps: int = 26501365) -> int:
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c == 'S':
                start = (x, y)

    width = len(s.splitlines()[0])
    height = len(s.splitlines())

    seen = {start}
    coords = support.parse_coords_hash(s)
    paths = [start]

    go_until = sys.maxsize
    points: list[tuple[int, int]] = []
    i = 0
    while True:
        i += 1
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

        if i % 2 == 0:
            op = operator.eq
        else:
            op = operator.ne
        n = len({
            (x, y)
            for x, y in seen
            if op((x + y) % 2, (start[0] + start[1]) % 2)
        })

        if i == steps:  # for non-extrapolated!
            return n

        points.append((i, n))

        if len(points) >= width * 4:
            fit_points = tuple(points[-1 - width * i] for i in range(1, 4))
            A, B, C = quadratic_fit(fit_points)
            if (A * i * i + B * i + C) == n:
                works_at = fit_points[0][0]
                go_until = i + (steps - works_at) % width

            if i == go_until:
                ret = A * steps * steps + B * steps + C
                assert ret.denominator == 1
                return ret.numerator

    raise AssertionError('unreachable!')


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
        (INPUT_S, 5000, 16733044),
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
