from __future__ import annotations

import argparse
import operator
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

OP = {
    '>': operator.gt,
    '>=': operator.ge,
    '<': operator.lt,
    '<=': operator.le,
}
OPPOSITE = {'<': '>=', '>': '<='}


def compute(s: str) -> int:
    progs_s, _ = s.split('\n\n')

    todo = []
    routes = {}
    for line in progs_s.splitlines():
        name, rest = line.rstrip('}').split('{')
        beg, default = rest.rsplit(',', 1)

        failures: list[tuple[str, str, int]] = []
        for part in beg.split(','):
            comp_s, dest = part.split(':')
            key = comp_s[0]
            comp = comp_s[1]
            val = int(comp_s[2:])

            move = (name, (*failures, (key, comp, val)))

            if dest == 'A':
                todo.append(move)
            elif dest != 'R':
                routes[dest] = move

            failures.append((key, OPPOSITE[comp], val))

        move = (name, tuple(failures))
        if default == 'A':
            todo.append(move)
        elif default != 'R':
            routes[default] = move

    total = 0
    for target, conditions in todo:
        while target != 'in':
            target, more_conditions = routes[target]
            conditions += more_conditions

        for_path = 1
        for c in 'xmas':
            for_num = 0
            for i in range(1, 4001):
                if all(s != c or OP[op](i, val) for s, op, val in conditions):
                    for_num += 1

            for_path *= for_num

        total += for_path

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
EXPECTED = 167409079868000


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
