import copy
import functools
import paintbychar as pbc
from aoc import parse_file, InputType, Direction, timer, TimeUnit
from dataclasses import dataclass
from PIL import Image, ImageDraw, ImageFont
import random


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

    def move_in_direction(self, direction: Direction, steps: int = 1) -> 'Present':
        match direction:
            case Direction.N:
                return Present(self.coords, (self.origin[0], self.origin[
                    1]-steps), self.shape_char)
            case Direction.E:
                return Present(self.coords, (self.origin[0]+steps, self.origin[1]), self.shape_char)
            case Direction.W:
                return Present(self.coords, (self.origin[0]-steps, self.origin[1]), self.shape_char)
            case Direction.S:
                return Present(self.coords, (self.origin[0], self.origin[1]+steps), self.shape_char)
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
    image_counter: int = 0

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

    def visualise(self, extra_shape: Present = None):
        string = [['.' for _ in range(self.size[0])] for _ in range(self.size[1])]
        for (i, j) in self.coords:
            for p in self.placed_presents:
                if (i, j) in p.relative_coords:
                    string[i][j] = p.shape_char
            if extra_shape is not None and (i,j) in extra_shape.relative_coords:
                string[i][j] = '6'
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
        random.shuffle(presents_to_place)
        self.placed_presents = set()
        placed_coords = set()
        counter = 0
        while presents_to_place:
            counter += 1
            self.random_movement(placed_coords, presents_to_place)

        return len(self.placed_presents) == sum(self.present_requirements)

    def random_placement(self, placed_coords, presents_to_place):
        current = presents_to_place.pop(0)
        fraction = float(sum([p.area for p in self.placed_presents]))*100./(self.size[0]*self.size[1])
        title = f'Space Filled = {fraction:.2f}%'
        self.save_treespace_image(len(self.placed_presents), title)
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
                    if not fit_found and not current.relative_coords.intersection(
                            placed_coords):
                        placed_coords.update(current.relative_coords)
                        self.placed_presents.add(current)
                        fit_found = True

    def random_movement(self, placed_coords, presents_to_place):
        current = presents_to_place.pop(0)
        if placed_coords:
            current = current.move_origin(random.choice(list(placed_coords)))
        rotations = 3
        iterations = 0
        while True:
            fraction = float(sum([p.area for p in self.placed_presents]))*100./(self.size[0]*self.size[1])
            title = f'Space Filled = {fraction:.3f}% - Placing Shape #{len(self.placed_presents)+1:03d}/{sum(self.present_requirements)} Attempt #{iterations+1:03d}'
            counter = f'{len(self.placed_presents):04d}-{iterations:04d}'
            self.save_treespace_image(counter, title, current)
            print(f'Saved {counter}')
            iterations += 1
            if (current.relative_coords.issubset(self.coords)
                    and not current.relative_coords.intersection(placed_coords)):
                placed_coords.update(current.relative_coords)
                self.placed_presents.add(current)
                break
            else:
                if rotations < 3:
                    current = current.rotate_cw
                    rotations += 1
                    continue
                else:
                    possibles = []
                    steps = 1
                    max_steps = max(self.size)
                    while not possibles:
                        tests = {direction: current.move_in_direction(direction, steps) for direction in Direction}
                        possibles = [p for p in tests.values() if p.relative_coords.issubset(self.coords - placed_coords)]
                        steps += 1
                        if steps > max_steps:
                            break
                    if steps > max_steps:
                        current = current.move_origin(random.choice(list(placed_coords)))
                    else:
                        current = random.choice(possibles)
                    rotations = 0
        fraction = float(sum([p.area for p in self.placed_presents]))*100./(self.size[0]*self.size[1])
        title = f'Space Filled = {fraction:.3f}% - Placing Shape #{len(self.placed_presents):03d}/{sum(self.present_requirements)} Attempt #{iterations+1:03d}'
        counter = f'{len(self.placed_presents):04d}-{iterations:04d}'
        self.save_treespace_image(counter, title, None)
        print(f'Saved {counter}')

    def save_treespace_image(self, counter: str | int, title: str, poised_shape: Present = None) -> None:
        img = pbc.string_to_image(self.visualise(poised_shape),
                                  char_color_map={'0': (195, 15, 22),
                                                  '1': (31, 39, 102),
                                                  '2': (241, 217, 0),
                                                  '3': (30, 121, 44),
                                                  '4': 'white',
                                                  '5': 'pink',
                                                  '6': (0, 255, 255)},
                                  fill_option=pbc.FillOption.BOTH,
                                  bg_color='beige')
        img_w, img_h = img.size
        title_height = 80
        padding = 20
        # Create a new image with space for title
        canvas_w = img_w + 2 * padding
        canvas_h = img_h + title_height + 2 * padding
        canvas = Image.new("RGB", (canvas_w, canvas_h), "white")
        # Paste plot into canvas
        plot_x = padding
        plot_y = title_height + padding
        canvas.paste(img, (plot_x, plot_y))
        # Draw text
        draw = ImageDraw.Draw(canvas)
        font_title = ImageFont.truetype("SourceCodePro-VariableFont_wght.ttf", 36)
        font_body = ImageFont.truetype("SourceCodePro-VariableFont_wght.ttf", 20)
        # Title text
        title_bbox = draw.textbbox((0, 0), title, font=font_title)
        title_w = title_bbox[2] - title_bbox[0]
        draw.text(
            ((canvas_w - title_w) // 2, padding),
            title,
            fill="black",
            font=font_title,
        )
        canvas.save(f'./visualisation/tree_{self.size}_{self.image_counter:04d}.png')
        self.image_counter += 1


@timer(TimeUnit.s)
def part1():
    data = parse_file(InputType.EXAMPLE3)
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
        print(f'Trees tested: {i+1}/{len(trees)}')
    return counter


def main():
    print(f'Part 1: {part1()}')


if __name__ == '__main__':
    main()
