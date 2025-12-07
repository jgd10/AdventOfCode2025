from aoc import parse_file, Point, Direction, InputType
from dataclasses import dataclass


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
        return sum(v for k, v in paths.items() if k.y == ymax)
    
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
    timelines = tm.build_tree()
    return timelines


def main():
    data = parse_file(InputType.INPUT)
    result1 = part1(data)
    print(f'Part 1: {result1}')
    result2 = part2(data)
    print(f'Part 2: {result2}')
    

if __name__ == '__main__':
    main()