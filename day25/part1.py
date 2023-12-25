from __future__ import annotations

import argparse
import collections
import copy
import math
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def _connected_components(nodes: dict[str, set[str]]) -> list[int]:
    ret = []

    while nodes:
        done = set()
        node = next(iter(nodes))
        processing = [node]
        while processing:
            node = processing.pop()
            for other in nodes[node]:
                processing.append(other)
                nodes[other].remove(node)
            del nodes[node]
            done.add(node)
        ret.append(len(done))

    return ret


def compute(s: str) -> int:
    connections_s = set()
    nodes = collections.defaultdict(set)
    for line in s.splitlines():
        src, dests = line.split(': ')
        for dest in dests.split():
            nodes[src].add(dest)
            nodes[dest].add(src)
            connections_s.add((src, dest))

    # lmao: determined empirically with `dot`
    # for k, v in connections_s:
    #     print(f'{k} -> {v} [dir=both]')
    if s != INPUT_S:
        cand = copy.deepcopy(nodes)
        for src, dest in (
            ('gqr', 'vbk'), ('klj', 'scr'), ('sdv', 'mxv'),
        ):
            cand[src].remove(dest)
            cand[dest].remove(src)
        return math.prod(_connected_components(cand))

    connections = list(connections_s)
    for i, c1 in enumerate(connections):
        for j, c2 in enumerate(connections[i + 1:], start=i + 1):
            for c3 in connections[j + 1:]:
                cand = copy.deepcopy(nodes)
                for src, dest in (c1, c2, c3):
                    cand[src].remove(dest)
                    cand[dest].remove(src)
                components = _connected_components(cand)
                if len(components) == 2:
                    return math.prod(components)

    raise AssertionError('unreachable')


INPUT_S = '''\
jqt: rhn xhk nvd
rsh: frs pzl lsr
xhk: hfx
cmg: qnr nvd lhk bvb
rhn: xhk bvb hfx
bvb: xhk hfx
pzl: lsr hfx nvd
qnr: nvd
ntq: jqt hfx bvb xhk
nvd: lhk
lsr: lhk
rzs: qnr cmg lsr rsh
frs: qnr lhk lsr
'''
EXPECTED = 54


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
