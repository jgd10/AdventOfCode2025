from aoc import parse_file, Point, InputType


def locate_printers(data: list[str]) -> set[Point]:
    printers = set()
    for y, line in enumerate(data):
        for x, char in enumerate(line):
            if char == "@":
                printers.add(Point(x, y))
    return printers


def part1(data: list[str]) -> int:
    printers = locate_printers(data)
    total = sum(len(p.all_neighbors.intersection(printers)) < 4 for p in
                printers)
    return total


def get_accessible_printers(printers: set[Point]) -> set[Point]:
    accessible = set()
    for p in printers:
        if len(p.all_neighbors.intersection(printers)) < 4:
            accessible.add(p)
    return accessible


def part2(data: list[str]) -> int:
    printers = locate_printers(data)
    total = 0
    accessible = get_accessible_printers(printers)
    while len(accessible) > 0:
        accessible = get_accessible_printers(printers)
        total += len(accessible)
        printers.difference_update(accessible)
    return total


def main():
    data = parse_file(InputType.INPUT)
    result1 = part1(data)
    print(f"Part 1: {result1}")
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()