from __future__ import annotations

import argparse
import os.path
from typing import NamedTuple

import pytest

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


def compute(
        s: str,
        *,
        low: int = 200000000000000,
        high: int = 400000000000000,
) -> int:
    hailstones = []
    for line in s.splitlines():
        pos, v = line.split(' @ ')
        hailstones.append(
            Hailstone(
                *support.parse_numbers_comma(pos),
                *support.parse_numbers_comma(v),
            ),
        )

    total = 0
    for i, hailstone in enumerate(hailstones):
        for other in hailstones[i + 1:]:
            collision = hailstone.intersect_non_z(other)
            if (
                    collision is not None and
                    collision.t0 >= 0 and
                    collision.t1 >= 0 and
                    low <= collision.x <= high and
                    low <= collision.y <= high
            ):
                total += 1

    return total


INPUT_S = '''\
19, 13, 30 @ -2,  1, -2
18, 19, 22 @ -1, -1, -2
20, 25, 34 @ -2, -2, -4
12, 31, 28 @ -1, -2, -1
20, 19, 15 @  1, -5, -3
'''
EXPECTED = 2


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s, low=7, high=27) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
