from aoc import parse_file, Point, InputType
import paintbychar as pbc

def printers_to_txt(printers: set[Point], marked: set[Point], size: int) -> str:
    rows = []
    for i in range(size):
        row = []
        for j in range(size):
            if Point(i, j) in marked:
                char = 'x'
            elif Point(i, j) in printers:
                char = '@'
            else:
                char = '.'
            row.append(char)
        rows.append(''.join(row))
    string = '\n'.join(rows)
    return string


def printers_to_file(printers: set[Point], marked: set[Point], size: int, num: int) -> None:
    string = printers_to_txt(printers, marked, size)
    img = pbc.string_to_image(string, fill_option=pbc.FillOption.CHARS,
                          char_color_map={'@': 'red',
                                          'x': 'white',
                                          '.': 'gray'}, bg_color=(0,0,0))
    pbc.save_image(img, f'part2/printers{num:04}.png')


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
    iteration = 0
    printers_to_file(printers, set(), len(data), iteration)
    while len(accessible) > 0:
        accessible = get_accessible_printers(printers)
        total += len(accessible)
        iteration += 1
        printers_to_file(printers, accessible, len(data), iteration)
        printers.difference_update(accessible)
        iteration += 1
        printers_to_file(printers, set(), len(data), iteration)
    return total


def main():
    data = parse_file(InputType.INPUT)
    result1 = part1(data)
    print(f"Part 1: {result1}")
    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
