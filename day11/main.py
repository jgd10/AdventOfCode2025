import functools

from aoc import parse_file, InputType
from functools import cache
import networkx as nx
from igraph import Graph
from dataclasses import dataclass

def count_all_paths(graph: dict[str, str], start: str, end: str) -> int:
    paths = set()
    dfs(graph, start, end, paths, [])
    return len(paths)


def all_paths(graph: dict[str, str], start: str, end: str, via: set[str] = None):
    paths = set()
    dfs(graph, start, end, paths, [], via)
    return paths


def dfs(graph, start: str, end: str, paths: set[tuple[str, ...]], path: list[str], via: set[str] = None) -> None:
    path.append(start)
    if start == end:
        if via is not None and all(v in path for v in via):
            paths.add(tuple(path))
        elif via is None:
            paths.add(tuple(path))
        else:
            pass
        return
    if start not in graph:
        return
    for node in graph[start]:
        dfs(graph, node, end, paths, path[:], via)
    return


@dataclass(frozen=True)
class MemoGraph:
    graph: frozenset[tuple[str, tuple[str, ...]]]

    @classmethod
    def from_dict(cls, graph: dict[str, str]) -> 'MemoGraph':
        new = frozenset((k, tuple(v)) for k, v in graph.items())
        return cls(new)

    def get_next_nodes(self, node: str):
        for n, vals in self.graph:
            if n == node:
                return vals
        return ()

    @functools.lru_cache(maxsize=None)
    def dfs(self, start: str, end: str) -> int:
        counter = 0
        if start == end:
            return 1
        for node in self.get_next_nodes(start):
            counter += self.dfs(node, end)
        return counter


def part1():
    data = parse_file(InputType.INPUT)
    graph = {}
    for row in data:
        nodes = row.split(' ')
        graph[nodes[0].replace(':', '')] = set(nodes[1:])
    mg = MemoGraph.from_dict(graph)
    return mg.dfs('you', 'out')


def part2():
    data = parse_file(InputType.INPUT)
    graph = {}
    for row in data:
        nodes = row.split(' ')
        graph[nodes[0].replace(':', '')] = set(nodes[1:])
    mg = MemoGraph.from_dict(graph)
    paths_to_fft = mg.dfs('svr', 'fft')
    paths_fft_dac = mg.dfs('fft', 'dac')
    paths_dac_fft = mg.dfs('dac', 'fft')
    paths_to_out = mg.dfs('dac', 'out')

    middle_paths = max(paths_fft_dac, paths_dac_fft)
    #net = Network(directed=True)
    #net.from_nx(G)
    #net.show('test.html', notebook=False)
    #paths1 = all_paths(graph, 'dac', 'fft', via=None)
    #paths2 = all_paths(graph, 'fft', 'dac', via=None)
    return paths_to_fft*middle_paths*paths_to_out #len(paths1), len(paths2)

def main():
    print(f'Part 1: {part1()}')
    print(f'Part 2: {part2()}')


if __name__ == '__main__':
    main()
