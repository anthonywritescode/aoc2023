from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _compute_line(s: tuple[str, ...]) -> int:
    line = list(s)
    length = len(s)
    target = 0
    looking = 0
    while target < length:
        if line[target] == 'O':
            target += 1
        elif line[target] == '#':
            target += 1
        elif line[target] == '.':
            looking = max(looking, target + 1)
            for looking in range(looking, length):
                if line[looking] == '#':
                    target = looking + 1
                    break
                elif line[looking] == 'O':
                    line[target], line[looking] = line[looking], line[target]
                    target += 1
                    looking += 1
                    break
            else:
                break
        else:
            target += 1

    return sum(length - i for i, c in enumerate(line) if c == 'O')


def compute(s: str) -> int:
    return sum(_compute_line(column) for column in zip(*s.splitlines()))


INPUT_S = '''\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
'''
EXPECTED = 136


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
