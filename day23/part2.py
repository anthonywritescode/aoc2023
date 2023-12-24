from __future__ import annotations

import argparse
import collections
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    coords = {}
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c == '#':
                coords[(x, y)] = c
            else:
                coords[(x, y)] = '.'

    connections: dict[tuple[int, int], list[tuple[int, tuple[int, int]]]]
    connections = collections.defaultdict(list)

    start = (1, 0)
    dest = (x - 1, y)
    nodes = [start, dest]

    bx, by = support.bounds(coords)
    for y in by.range:
        for x in bx.range:
            if coords[(x, y)] != '.':
                continue
            n_possible = 0
            for cand in support.adjacent_4(x, y):
                if coords.get(cand, '#') == '.':
                    n_possible += 1
            if n_possible > 2:
                nodes.append((x, y))

    def _find_connections(node: tuple[int, int]) -> None:
        paths = [(node, {node})]
        while paths:
            new_paths = []
            for pos, seen in paths:
                for d in support.Direction4:
                    cand = d.apply(*pos)
                    if cand in seen:
                        continue
                    elif cand in nodes:
                        assert cand not in {t for _, t in connections}, cand
                        connections[node].append((len(seen), cand))
                    elif cand not in seen and coords.get(cand, '#') == '.':
                        new_paths.append((cand, {*seen, cand}))
            paths = new_paths

    for node in nodes:
        _find_connections(node)

    maximum = 0
    paths = [(0, start, {start})]
    while paths:
        size, pos, seen = paths.pop()
        for cost, node in connections[pos]:
            total_cost = size + cost
            if node == dest:
                if total_cost > maximum:
                    maximum = total_cost
            elif node not in seen:
                paths.append((total_cost, node, {*seen, node}))

    return maximum


INPUT_S = '''\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
'''
EXPECTED = 154


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
