from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

# Determine the ASCII code for the current character of the string.
# Increase the current value by the ASCII code you just determined.
# Set the current value to itself multiplied by 17.
# Set the current value to the remainder of dividing itself by 256.


def _hash(s: str) -> int:
    n = 0
    for c in s.strip():
        n += ord(c)
        n *= 17
        n %= 256
    return n


def compute(s: str) -> int:
    boxes: list[dict[str, int]] = [{} for _ in range(256)]
    for part in s.strip().split(','):
        if part.endswith('-'):
            label = part[:-1]
            box_id = _hash(label)
            boxes[box_id].pop(label, None)
        else:
            s, n_s = part.split('=')
            boxes[_hash(s)][s] = int(n_s)

    total = 0
    for i, box in enumerate(boxes, start=1):
        for j, n in enumerate(box.values(), start=1):
            total += i * j * n
    return total


INPUT_S = '''\
rn=1,cm-,qp=3,cm=2,qp-,pc=4,ot=9,ab=5,pc-,pc=6,ot=7
'''
EXPECTED = 145


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
