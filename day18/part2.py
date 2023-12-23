from __future__ import annotations

import argparse
import operator
import os.path
import re
import sys
from typing import Callable
from typing import Iterable
from typing import NamedTuple

import pytest

import support
from support import Direction4

PAT = re.compile(r'^[ULRD] [0-9]+ \(#([a-f0-9]{5})([0123])\)$')

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

DIRS = {
    '0': Direction4.RIGHT,
    '1': Direction4.DOWN,
    '2': Direction4.LEFT,
    '3': Direction4.UP,
}


class Choice(NamedTuple):
    keep: int
    change: int
    compare: Callable[[int, int], bool]


CHOICES = {
    (Direction4.UP, Direction4.RIGHT, Direction4.DOWN): Choice(
        keep=0,
        change=1,
        compare=operator.lt,
    ),
    (Direction4.RIGHT, Direction4.DOWN, Direction4.LEFT): Choice(
        keep=1,
        change=0,
        compare=operator.gt,
    ),
    (Direction4.DOWN, Direction4.LEFT, Direction4.UP): Choice(
        keep=0,
        change=1,
        compare=operator.gt,
    ),
    (Direction4.LEFT, Direction4.UP, Direction4.RIGHT): Choice(
        keep=1,
        change=0,
        compare=operator.lt,
    ),
}


class P(NamedTuple):
    x: int
    y: int


def _find_dir(p1: tuple[int, int], p2: tuple[int, int]) -> Direction4:
    p1x, p1y = p1
    p2x, p2y = p2
    if p2x > p1x:
        return Direction4.RIGHT
    elif p2x < p1x:
        return Direction4.LEFT
    elif p2y > p1y:
        return Direction4.DOWN
    elif p2y < p1y:
        return Direction4.UP
    else:
        raise AssertionError(f'unreachable!: {p1=} {p2=}')


def _reverse(forward: dict[P, P], p: P) -> P:
    for k, v in forward.items():
        if v == p:
            return k
    else:
        raise AssertionError('unreachable!')


def _contains_point(
        c1: tuple[int, int],
        c2: tuple[int, int],
        pts: Iterable[P],
        allowed: set[P],
) -> bool:
    bx, by = support.bounds((c1, c2))
    for p in pts:
        if p in allowed:
            continue
        elif bx.min <= p.x <= bx.max and by.min <= p.y <= by.max:
            return True
    else:
        return False


def _fixup(forward: dict[P, P]) -> None:
    while True:
        for p1 in forward:
            p2 = forward[p1]
            p3 = forward[p2]

            if _find_dir(p1, p2) == _find_dir(p2, p3):
                del forward[p2]
                forward[p1] = p3
                break
        else:
            break


def _check_ok(forward: dict[P, P]) -> None:
    for p1 in forward:
        p2 = forward[p1]
        p3 = forward[p2]

        d1 = _find_dir(p1, p2)
        d2 = _find_dir(p2, p3)
        assert d1 in (d2.cw, d2.ccw)


def compute(s: str) -> int:
    max_x = -sys.maxsize
    max_d = Direction4.RIGHT
    pos = (0, 0)
    forward = {}
    for line in s.splitlines():
        match = PAT.match(line)
        assert match is not None
        n, d = int(match[1], 16), DIRS[match[2]]

        prev = pos
        pos = d.apply(*pos, n=n)
        forward[P(*prev)] = P(*pos)

        if prev[0] > max_x:
            max_x = prev[0]
            max_d = d

    _fixup(forward)

    # XXX: code only works for right-hand-is-inside
    assert max_d is Direction4.DOWN

    rects = []
    while True:
        if len(forward) == 4:
            c1 = next(iter(forward))
            c2 = forward[forward[c1]]
            dx = abs(c2[0] - c1[0]) + 1
            dy = abs(c2[1] - c1[1]) + 1
            rects.append(dx * dy)
            break

        for p1 in forward:
            p2 = forward[p1]
            p3 = forward[p2]
            p4 = forward[p3]

            d1 = _find_dir(p1, p2)
            d2 = _find_dir(p2, p3)
            d3 = _find_dir(p3, p4)

            cfg = CHOICES.get((d1, d2, d3))
            if cfg is None:
                continue

            c2_l: list[int | None] = [None, None]

            if cfg.compare(p1[cfg.change], p4[cfg.change]):
                c1 = p2
                c2_l[cfg.keep] = p4[cfg.keep]
                c2_l[cfg.change] = p1[cfg.change]
            else:
                c1 = p3
                c2_l[cfg.keep] = p1[cfg.keep]
                c2_l[cfg.change] = p4[cfg.change]

            c2_x, c2_y = c2_l
            assert c2_x is not None
            assert c2_y is not None
            c2 = P(c2_x, c2_y)

            if not _contains_point(c1, c2, forward, {p1, p2, p3, p4}):
                d_change = abs(c2[cfg.change] - c1[cfg.change])
                d_keep = 1 + abs(c2[cfg.keep] - c1[cfg.keep])
                forward[p1] = c2
                del forward[p2]
                del forward[p3]
                forward[c2] = p4
                _fixup(forward)
                _check_ok(forward)

                rects.append(d_change * d_keep)
                break
        else:
            raise AssertionError('did not find any to eliminate!')

    return sum(rects)


SIMPLE_S = '''\
R 1 (#000050)
R 1 (#0000a1)
R 1 (#000052)
R 1 (#0000a3)
'''

INPUT_SMALL = '''\
R 1 (#000060)
R 1 (#000051)
R 1 (#000022)
R 1 (#000021)
R 1 (#000020)
R 1 (#000021)
R 1 (#000052)
R 1 (#000023)
R 1 (#000012)
R 1 (#000023)
R 1 (#000020)
R 1 (#000033)
R 1 (#000022)
R 1 (#000023)
'''

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
EXPECTED = 952408144115


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (SIMPLE_S, 66),
        (INPUT_SMALL, 62),
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
