from __future__ import annotations

import argparse
import operator
import os.path
from typing import Callable
from typing import NamedTuple

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

OP = {'<': operator.lt, '>': operator.gt}


class Check(NamedTuple):
    key: str
    comp: Callable[[int, int], bool]
    val: int
    dest: str


class Prog(NamedTuple):
    checks: tuple[Check, ...]
    default: str

    def run(self, d: dict[str, int]) -> str:
        for check in self.checks:
            if check.comp(d[check.key], check.val):
                return check.dest
        else:
            return self.default


def compute(s: str) -> int:
    progs_s, parts_s = s.split('\n\n')

    total = 0

    progs = {}
    for line in progs_s.splitlines():
        name, rest = line.rstrip('}').split('{')
        beg, default = rest.rsplit(',', 1)
        checks = []
        for part in beg.split(','):
            comp_s, dest = part.split(':')
            key = comp_s[0]
            comp = OP[comp_s[1]]
            val = int(comp_s[2:])
            checks.append(Check(key, comp, val, dest))
        progs[name] = Prog(tuple(checks), default)

    for line in parts_s.splitlines():
        item = {}
        for part in line.strip('{}').split(','):
            k, val_s = part.split('=')
            item[k] = int(val_s)

        s = 'in'
        while s not in {'A', 'R'}:
            s = progs[s].run(item)

        if s == 'A':
            total += sum(item.values())

    return total


INPUT_S = '''\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
'''
EXPECTED = 19114


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
