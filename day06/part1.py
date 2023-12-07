from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    ts = [int(n_s) for n_s in lines[0].split()[1:]]
    ds = [int(n_s) for n_s in lines[1].split()[1:]]

    mult = 1
    for time, min_dist in zip(ts, ds):
        n = 0
        for wait in range(1, time - 1):
            dist = (time - wait) * wait
            if dist > min_dist:
                n += 1
        mult *= n
        # wait >= 1
        # wait < time
        # (time - wait) * wait > min_dist
        # => wait * time - wait ** 2 > min_dist

    return mult


INPUT_S = '''\
Time:      7  15   30
Distance:  9  40  200
'''
EXPECTED = 288


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
