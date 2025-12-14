import copy
import functools
import paintbychar as pbc
from aoc import parse_file, InputType, Direction, timer, TimeUnit
from dataclasses import dataclass


EXAMPLES = (
    """### 
    ##.
    ##.""",
    """###
    ##.
    .##""",
    """.##
    ###
    ##.""",
    """##.
    ###
    ##.""",
    """###
    #..
    ###""",
    """###
    .#.
    ###""")


INPUTS = ("""###
#.#
#.#""",
"""#..
##.
###""",
"""###
###
..#""",
""".##
##.
###""",
"""###
.#.
###""",
""".##
##.
#..""")


@dataclass(frozen=True)
class Present:
    coords: frozenset[tuple[int, int]]
    origin: tuple[int, int]
    shape_char: str = 'U'

    @classmethod
    def from_string(cls, s: str, char: str) -> "Present":
        rows = s.split('\n')
        coords = set()
        for j, row in enumerate(rows):
            for i, c in enumerate(row.strip()):
                if c == '#':
                    coords.add((i, j))
        return Present(frozenset(coords), (0, 0), shape_char=char)

    def move_origin(self, new_origin: tuple[int, int]) -> 'Present':
        return Present(self.coords, new_origin, self.shape_char)

    def move_in_direction(self, direction: Direction) -> 'Present':
        match direction:
            case Direction.N:
                return Present(self.coords, (self.origin[0], self.origin[
                    1]-1), self.shape_char)
            case Direction.E:
                return Present(self.coords, (self.origin[0]+1, self.origin[1]), self.shape_char)
            case Direction.W:
                return Present(self.coords, (self.origin[0]-1, self.origin[1]), self.shape_char)
            case Direction.S:
                return Present(self.coords, (self.origin[0], self.origin[1]+1), self.shape_char)
            case _:
                raise Exception(f"Unknown direction {direction}")


    @functools.cached_property
    def relative_coords(self):
        return frozenset({(x + self.origin[0], y + self.origin[1])
                           for x, y in self.coords})

    @functools.cached_property
    def area(self) -> int:
        return len(self.coords)

    @functools.cached_property
    def rotate_cw(self) -> 'Present':
        new = {(y, 2-x) for x, y in self.coords}
        return Present(frozenset(new), self.origin, self.shape_char)

    def visualise(self):
        rows = []
        for j in range(3):
            row = []
            for i in range(3):
                if (i,j) in self.coords:
                    row.append('#')
                else:
                    row.append('.')
            rows.append(''.join(row))
        return '\n'.join(rows)


@dataclass
class TreeSpace:
    size: tuple[int, ...]
    coords: frozenset[tuple[int, int]]
    present_requirements: tuple[int, ...]
    presents: tuple[Present, ...]
    placed_presents: set[Present] = None

    @classmethod
    def from_string(cls, s: str, presents: tuple[Present, ...]) -> "TreeSpace":
        pieces = s.split(' ')
        size = [int(z) for z in pieces.pop(0).replace(':', '').split('x')]
        coords = {(i, j) for j in range(size[0]) for i in range(size[1])}
        presents_ = [int(p) for p in pieces]
        return TreeSpace(tuple(size), frozenset(coords), tuple(presents_), presents)

    @functools.cached_property
    def placed_present_coords(self) -> frozenset[tuple[int, int]]:
        if self.placed_presents is None:
            self.placed_presents = set()
            return frozenset()
        new = set()
        for present in self.placed_presents:
            new.add(present.relative_coords)
        return frozenset(new)

    def visualise(self):
        string = [['.' for _ in range(self.size[0])] for _ in range(self.size[1])]
        for (i, j) in self.coords:
            for p in self.placed_presents:
                if (i, j) in p.relative_coords:
                    string[i][j] = p.shape_char
        rows = []
        for row in string:
            rows.append(''.join(row))
        return '\n'.join(rows)

    def possible_to_fill_space(self) -> bool:
        min_area = sum(pr*p.area
                       for p, pr in zip(self.presents,
                                        self.present_requirements))
        
        if len(self.coords) < min_area:
            return False
        # For my input this check was sufficient
        # else:
        #     return True
        presents_to_place = []
        for index, number in enumerate(self.present_requirements):
            for _ in range(number):
                presents_to_place.append(copy.deepcopy(self.presents[index]))

        self.placed_presents = set()
        placed_coords = set()
        counter = 0
        while presents_to_place:
            img = pbc.string_to_image(self.visualise(),
                                      char_color_map={'0': (195, 15, 22),
                                                      '1': (31, 39, 102),
                                                      '2': (241, 217, 0),
                                                      '3': (30, 121, 44),
                                                      '4': 'white',
                                                      '5': 'pink'},
                                      fill_option=pbc.FillOption.BOTH)
            pbc.save_image(img, f'./visualisation/tree_{self.size}_'
                                f'{counter:04d}.png')
            counter += 1
            current = presents_to_place.pop(0)
            for (i, j) in self.coords:
                current = current.move_origin((i, j))
                if not current.relative_coords.issubset(self.coords):
                    continue
                if not current.relative_coords.intersection(placed_coords):
                    placed_coords.update(current.relative_coords)
                    self.placed_presents.add(current)
                    break
                else:
                    fit_found = False
                    for _ in range(3):
                        current = current.rotate_cw
                        if not fit_found and not current.relative_coords.intersection(placed_coords):
                            placed_coords.update(current.relative_coords)
                            self.placed_presents.add(current)
                            fit_found = True

        return len(self.placed_presents) == sum(self.present_requirements)


@timer(TimeUnit.ms)
def part1():
    data = parse_file(InputType.INPUT)
    trees = []
    presents = tuple([Present.from_string(p, s) for s, p in zip('012345', INPUTS)])
    counter = 0
    for row in data:
        if 'x' in row:
            trees.append(TreeSpace.from_string(row, presents))
    for i, tree in enumerate(trees):
        if tree.possible_to_fill_space():
            counter += 1
        if tree.placed_presents is None:
            tree.placed_presents = set()
    return counter


def main():
    print(f'Part 1: {part1()}')


if __name__ == '__main__':
    main()
