from aoc import parse_file, Point, Direction, InputType
from dataclasses import dataclass
import paintbychar as pbc



@dataclass
class Node:
    point: Point
    parent: 'Node' = None
    children: set['Node'] = None


@dataclass
class TachyonManifold:
    start: Point
    splitters: set[Point]
    spaces: set[Point]
    tree: Node = None
    
    def evolve_beam(self):
        split_counter = 0
        beams = {self.start.point_in_direction(Direction.S)}
        new_beams = beams.copy()
        while new_beams.intersection(self.spaces):
            next_step = set()
            for beam in new_beams:
                new = beam.point_in_direction(Direction.S)
                if new in self.splitters:
                    split_counter += 1
                    a, b = (new.point_in_direction(Direction.W), 
                            new.point_in_direction(Direction.E))
                    next_step.add(a)
                    next_step.add(b)
                else:
                    next_step.add(new)
            new_beams = next_step
            beams.update(new_beams.intersection(self.spaces))
        return split_counter, beams
    
    def build_tree(self):
        ymax = max(p.y for p in self.spaces)
        paths = {self.start: 1}
        iteration = 0
        save_state_as_image(paths, ymax, self, iteration)
        # process row by row (y increases monotonically), so parents are handled before children
        for y in range(self.start.y, ymax):
            row_points = [p for p in paths if p.y == y]
            for p in row_points:
                count = paths[p]
                downward = p.point_in_direction(Direction.S)

                # splitter is at the downward position; children are lateral from that splitter
                if downward in self.splitters:
                    left = downward.point_in_direction(Direction.W)
                    right = downward.point_in_direction(Direction.E)
                    if left in paths:
                        paths[left] += count
                    else:
                        paths[left] = count
                    if right in paths:
                        paths[right] += count
                    else:
                        paths[right] = count
                elif downward in self.spaces:
                    if downward in paths:
                        paths[downward] += count
                    else:
                        paths[downward] = count
            iteration += 1
            save_state_as_image(paths, ymax, self, iteration)
        return paths, ymax
    
    @classmethod
    def from_data(cls, data: list[str]) -> 'TachyonManifold':
        splitters = set()
        spaces = set()
        start = None
        for y, line in enumerate(data):
            for x, char in enumerate(line):
                point = Point(x, y)
                match char:
                    case 'S':
                        start = point
                    case '^':
                        splitters.add(point)
                    case '.':
                        spaces.add(point)
        return cls(start=start, splitters=splitters, spaces=spaces)
        


def part1(data: list[str]) -> int:
    tm = TachyonManifold.from_data(data)
    splits, _ = tm.evolve_beam()
    return splits
                

def part2(data: list[str]) -> int:
    tm = TachyonManifold.from_data(data)
    paths, ymax = tm.build_tree()
    return sum(v for k, v in paths.items() if k.y == ymax)


def save_state_as_image(paths, ymax, tm, iteration: int):
    string = redraw(paths, ymax, tm)
    img = pbc.string_to_image(string, preset='plasma', bg_color='white',
                              fill_option=pbc.FillOption.CHARS)
    pbc.save_image(img, f'part2/timeline_density{iteration:04d}.png')


def redraw(paths: dict, ymax: int, tm: TachyonManifold) -> str:
    data = [['.' for _ in range(ymax+1)] for __ in range(ymax+1)]
    max_value = 547847144422  # max(paths.values()), hardcoded for plotting
    for path, value in paths.items():
        match value:
            case value if value < max_value*.000000001:
                char = '0'
            case value if max_value *.000000001 < value <= max_value*.00000001:
                char = '1'
            case value if max_value *.00000001 < value <= max_value*.0000001:
                char = '2'
            case value if max_value *.0000001 < value <= max_value*.000001:
                char = '3'
            case value if max_value *.000001 < value <= max_value*.00001:
                char = '4'
            case value if max_value *.00001 < value <= max_value*.0001:
                char = '5'
            case value if max_value *.0001 < value <= max_value*.001:
                char = '6'
            case value if max_value *.001 < value <= max_value*.01:
                char = '7'
            case value if max_value *.01 < value <= max_value*.1:
                char = '8'
            case value if max_value *.1 < value <= max_value:
                char = '9'
            case _:
                raise ValueError
        data[path.y][path.x] = char
    for splitter in tm.splitters:
        data[splitter.y][splitter.x] = '^'
    data[tm.start.y][tm.start.x] = 'S'
    rows = []
    for row in data:
        rows.append(''.join(row))
    string = '\n'.join(rows)
    return string


def main():
    data = parse_file(InputType.INPUT)
    result1 = part1(data)
    print(f'Part 1: {result1}')
    result2 = part2(data)
    print(f'Part 2: {result2}')
    

if __name__ == '__main__':
    main()
