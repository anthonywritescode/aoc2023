from __future__ import annotations

import argparse
import os.path
from typing import Iterable
from typing import Sequence

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _compute_line(s: Sequence[str]) -> str:
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

    return ''.join(line)


def _columns(s: str) -> Iterable[tuple[str, ...]]:
    return zip(*s.splitlines())


def _cycle(s: str) -> str:
    # north
    s = '\n'.join(_compute_line(line) for line in _columns(s))
    s = '\n'.join(''.join(line) for line in _columns(s))
    # west
    s = '\n'.join(_compute_line(line) for line in s.splitlines())
    # south
    s = '\n'.join(_compute_line(line[::-1])[::-1] for line in _columns(s))
    s = '\n'.join(''.join(line) for line in _columns(s))
    # east
    s = '\n'.join(_compute_line(line[::-1])[::-1] for line in s.splitlines())

    return s


def _load(s: str) -> int:
    return sum(
        sum(len(line) - i for i, c in enumerate(line) if c == 'O')
        for line in zip(*s.splitlines())
    )


N = 1000000000


def compute(s: str) -> int:
    seen = {s.rstrip(): 0}
    i = 0
    while True:
        i += 1
        s = _cycle(s)
        if s in seen:
            break
        else:
            seen[s] = i

    for _ in range((N - seen[s]) % (i - seen[s])):
        s = _cycle(s)
    return _load(s)


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
EXPECTED = 64


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
