from __future__ import annotations

import argparse
import os.path
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Range(NamedTuple):
    dest: int
    src: int
    length: int

    def apply(
            self,
            ranges: list[tuple[int, int]],
    ) -> tuple[list[tuple[int, int]], list[tuple[int, int]]]:
        done, todo = [], []

        self_start = self.src
        self_end = self.src + self.length - 1

        for start, end in ranges:
            if self_start <= start <= self_end < end:
                # rrrrrr
                #    ccccc
                done.append((self.convert(start), self.convert(self_end)))
                todo.append((self_end + 1, end))
            elif self_start <= start <= end <= self_end:
                # rrrrrr
                #  ccc
                done.append((self.convert(start), self.convert(end)))
            elif start < self_start < end < self_end:
                #    rrrrrr
                #  cccc
                todo.append((start, self_start - 1))
                done.append((self.convert(self_start), self.convert(end)))
            elif start < self_start <= self_end < end:
                #    rrr
                # cccccccc
                todo.append((start, self_start - 1))
                done.append((self.convert(self_start), self.convert(self_end)))
                todo.append((self_end + 1, end))
            else:
                todo.append((start, end))

        return done, todo

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

    ns = [int(n_s) for n_s in seeds.split(': ')[1].split()]
    it = iter(ns)
    ranges = [(start, start + length - 1) for start, length in zip(it, it)]

    for mapping in mappings:
        completed = []
        for r in mapping:
            done, ranges = r.apply(ranges)
            completed.extend(done)

        ranges = completed + ranges

    return min(start for start, _ in ranges)


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
EXPECTED = 46


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
