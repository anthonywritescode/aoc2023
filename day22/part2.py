from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


class Brick:
    def __init__(
            self,
            x1: int, y1: int, z1: int,
            x2: int, y2: int, z2: int,
    ) -> None:
        self.x1, self.y1, self.z1 = x1, y1, z1
        self.x2, self.y2, self.z2 = x2, y2, z2

    def __repr__(self) -> str:
        return (
            f'Brick('
            f'*({self.x1}, {self.y1}, {self.z1}), '
            f'*({self.x2}, {self.y2}, {self.z2})'
            f')'
        )

    def supported_by(self, brick: Brick) -> bool:
        return (
            self.z1 == brick.z2 + 1 and
            self.x1 <= brick.x2 and
            self.x2 >= brick.x1 and
            self.y1 <= brick.y2 and
            self.y2 >= brick.y1
        )


def _would_move(bricks: list[Brick]) -> int:
    total = 0
    done = []
    for brick in bricks:
        if brick.z1 == 1:
            done.append(brick)
        elif any(brick.supported_by(other) for other in done):
            done.append(brick)
        else:
            total += 1
    return total


def compute(s: str) -> int:
    bricks = []
    for line in s.splitlines():
        c1_s, c2_s = line.split('~')
        bricks.append(
            Brick(
                *support.parse_numbers_comma(c1_s),
                *support.parse_numbers_comma(c2_s),
            ),
        )
    bricks.sort(key=lambda brick: brick.z1)

    done = []
    while bricks:
        new_bricks = []
        for brick in bricks:
            if brick.z1 == 1:
                done.append(brick)
            elif any(brick.supported_by(other) for other in done):
                done.append(brick)
            else:
                brick.z1 -= 1
                brick.z2 -= 1
                new_bricks.append(brick)

        bricks = new_bricks

    done.sort(key=lambda brick: brick.z1)

    total = 0
    for i in range(len(done)):
        total += _would_move(done[:i] + done[i + 1:])
    return total


INPUT_S = '''\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
'''
EXPECTED = 7


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
