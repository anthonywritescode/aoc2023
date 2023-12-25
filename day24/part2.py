from __future__ import annotations

import argparse
import os.path
from typing import NamedTuple

import pytest
import z3

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Collision2d(NamedTuple):
    t0: float
    t1: float
    x: float
    y: float


class Hailstone(NamedTuple):
    x0: int
    y0: int
    z0: int
    vx: int
    vy: int
    vz: int

    @property
    def m_2d(self) -> float:
        return self.vy / self.vx

    @property
    def c_2d(self) -> float:
        return self.y0 - (self.vy / self.vx) * self.x0

    def intersect_non_z(self, other: Hailstone) -> Collision2d | None:
        try:
            x = (other.c_2d - self.c_2d) / (self.m_2d - other.m_2d)
            t0 = (x - self.x0) / self.vx
            t1 = (x - other.x0) / other.vx
            y = self.vy * t0 + self.y0
        except ZeroDivisionError:
            return None
        else:
            return Collision2d(t0, t1, x, y)


def compute(s: str) -> int:
    hailstones = []
    for line in s.splitlines():
        pos, v = line.split(' @ ')
        hailstones.append(
            Hailstone(
                *support.parse_numbers_comma(pos),
                *support.parse_numbers_comma(v),
            ),
        )

    solver = z3.Solver()

    rock_x0 = z3.Int('rock_x0')
    rock_y0 = z3.Int('rock_y0')
    rock_z0 = z3.Int('rock_z0')
    rock_vx = z3.Int('rock_vx')
    rock_vy = z3.Int('rock_vy')
    rock_vz = z3.Int('rock_vz')

    for i, hailstone in enumerate(hailstones):
        collision_t = z3.Int(f't_{i}')
        solver.add(collision_t >= 0)
        solver.add(
            rock_x0 + collision_t * rock_vx ==
            hailstone.x0 + collision_t * hailstone.vx,
        )
        solver.add(
            rock_y0 + collision_t * rock_vy ==
            hailstone.y0 + collision_t * hailstone.vy,
        )
        solver.add(
            rock_z0 + collision_t * rock_vz ==
            hailstone.z0 + collision_t * hailstone.vz,
        )

    assert solver.check() == z3.sat
    model = solver.model()

    return (
        model[rock_x0].as_long() +
        model[rock_y0].as_long() +
        model[rock_z0].as_long()
    )


INPUT_S = '''\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
'''
EXPECTED = 47


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
