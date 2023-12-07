from __future__ import annotations

import argparse
import os.path
import sys
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Range(NamedTuple):
    dest: int
    src: int
    length: int

    def contains(self, n: int) -> bool:
        return self.src <= n < self.src + self.length

    def convert(self, n: int) -> int:
        return (n - self.src) + self.dest

    @classmethod
    def parse(cls, s: str) -> Range:
        dest_s, src_s, length_s = s.split()
        return cls(int(dest_s), int(src_s), int(length_s))


def compute(s: str) -> int:
    seeds, *rest = s.strip().split('\n\n')
    mappings = [
        [Range.parse(line) for line in part.splitlines()[1:]]
        for part in rest
    ]

    min_loc = sys.maxsize
    for n_s in seeds.split(': ')[1].split():
        n = int(n_s)
        for mapping in mappings:
            for r in mapping:
                if r.contains(n):
                    n = r.convert(n)

                    break

        min_loc = min(min_loc, n)

    return min_loc


INPUT_S = '''\
seeds: 79 14 55 13

seed-to-soil map:
50 98 2
52 50 48

soil-to-fertilizer map:
0 15 37
37 52 2
39 0 15

fertilizer-to-water map:
49 53 8
0 11 42
42 0 7
57 7 4

water-to-light map:
88 18 7
18 25 70

light-to-temperature map:
45 77 23
81 45 19
68 64 13

temperature-to-humidity map:
0 69 1
1 0 69

humidity-to-location map:
60 56 37
56 93 4
'''
EXPECTED = 35


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
