from __future__ import annotations

import argparse
import heapq
import os.path

import pytest

import support
from support import Direction4

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    coords = support.parse_coords_int(s)
    seen = set()
    end = next(reversed(coords))

    q = [(0, (0, 0), Direction4.DOWN), (0, (0, 0), Direction4.RIGHT)]
    while q:
        cost, pos, d = heapq.heappop(q)
        if pos == end:
            return cost
        elif (d, pos) in seen:
            continue
        else:
            seen.add((d, pos))

        def do(d_d: Direction4) -> None:
            cost_d = cost
            pos_d = pos
            for _ in range(3):
                pos_d = d_d.apply(*pos_d)
                if pos_d not in coords:
                    return

                cost_d += coords[pos_d]
                heapq.heappush(q, (cost_d, pos_d, d_d))

        do(d.ccw)
        do(d.cw)

    raise AssertionError('unreachable!')


INPUT_S = '''\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
'''
EXPECTED = 102


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
