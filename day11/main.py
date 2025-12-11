from aoc import parse_file, InputType
from functools import cache


def count_all_paths(graph: dict[str, str], start: str, end: str) -> int:
    paths = set()
    dfs(graph, start, end, paths, [])
    return len(paths)


def all_paths(graph: dict[str, str], start: str, end: str, via: set[str] = None):
    paths = set()
    dfs(graph, start, end, paths, [], via)
    return paths


@cache
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


def part1():
    data = parse_file(InputType.INPUT)
    graph = {}
    for row in data:
        nodes = row.split(' ')
        graph[nodes[0].replace(':', '')] = set(nodes[1:])
    count = count_all_paths(graph, 'you', 'out')
    return count


def part2():
    data = parse_file(InputType.INPUT)
    graph = {}
    for row in data:
        nodes = row.split(' ')
        graph[nodes[0].replace(':', '')] = set(nodes[1:])

    paths = all_paths(graph, 'svr', 'out', via={'fft', 'dac'})
    return len(paths)


def main():
    print(f'Part 1: {part1()}')
    print(f'Part 2: {part2()}')


if __name__ == '__main__':
    main()
