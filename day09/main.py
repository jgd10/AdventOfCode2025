from aoc import parse_file, InputType, Vector, timer
from shapely import Point, Polygon
import copy


@timer()
def part1():
    vectors = get_vectors()
    areas = {}
    for vector1 in vectors:
        for vector2 in vectors:
            if vector1 != vector2:
                key = frozenset((vector1, vector2))
                if key in areas:
                    continue
                areas[key] = vector1.rectangle_area(vector2)
    sorted_areas = sorted(areas.values(), reverse=True)
    return sorted_areas[0]


def get_vectors():
    data = parse_file(InputType.INPUT)
    vectors = []
    for row in data:
        vals = row.split(',')
        vectors.append(Vector(int(vals[0]), int(vals[1])))
    return vectors


def draw_line_to_point(vector: Vector, start: Vector = None) -> set[Vector]:
    if start is None:
        start = Vector(0, vector.y)

    vectors = set()
    if vector.x == start.x:
        starty, stopy = min([start.y, vector.y]), max([start.y, vector.y])
        for y in range(starty, stopy+1):
            vectors.add(Vector(vector.x, y))
    elif vector.y == start.y:
        startx, stopx = min([start.x, vector.x]), max([start.x, vector.x])
        for x in range(startx, stopx+1):
            vectors.add(Vector(x, vector.y))
    return vectors

def get_green_vectors(vectors: list[Vector]):
    temp_vectors = copy.deepcopy(vectors)
    v1 = temp_vectors.pop(0)
    green_lines = []
    polygon_sides = set()
    while len(temp_vectors) > 0:
        v2 = temp_vectors.pop(0)
        green_lines.append(draw_line_to_point(v1, v2))
        polygon_sides.add(frozenset([v1, v2]))
        v1 = v2
    green_lines.append(draw_line_to_point(v1, vectors[0]))
    polygon_sides.add(frozenset([v1, vectors[0]]))

    green_area = set()
    green_vectors = set()
    for line in green_lines:
        green_vectors.update(line)
    green_vectors.update(green_area)
    return green_vectors

@timer()
def part2():
    vectors = get_vectors()
    polygon = Polygon([(v.x, v.y) for v in vectors+[vectors[0]]])
    green_vectors = get_green_vectors(vectors)
    green_vectors.update(vectors)
    #visualise(set(vectors), green_vectors)
    areas = {}
    for vector1 in vectors:
        for vector2 in vectors:
            if vector1 != vector2:
                key = frozenset((vector1, vector2))
                if key in areas:
                    continue
                areas[key] = vector1.rectangle_area(vector2)
    filtered_areas = {}
    for key, area in areas.items():
        v1, v2 = key
        xmin, xmax = min(v1.x, v2.x), max(v1.x, v2.x)
        ymin, ymax = min(v1.y, v2.y), max(v1.y, v2.y)
        rectangle : Polygon = Polygon([(xmin, ymin), (xmax, ymin), (xmax, ymax), (xmin, ymax), (xmin, ymin)])
        if rectangle.within(polygon):
            filtered_areas[key] = area
    sorted_areas = sorted(filtered_areas.values(), reverse=True)
    return sorted_areas[0]


def visualise(red_vectors: set[Vector], green_vectors: set[Vector]):
    vectors = red_vectors.union(green_vectors)
    xs = {v.x for v in vectors}
    ys = {v.y for v in vectors}
    ymin, ymax = min(xs), max(xs)
    xmin, xmax = min(ys), max(ys)
    rows = []
    for j in range(0, xmax+1):
        row = []
        for i in range(0, ymax+1):
            vector = Vector(i, j)
            if vector in red_vectors:
                char = '#'
            elif vector in green_vectors:
                char = 'X'
            elif vector == Vector(xmin, ymin):
                char = '.'
            else:
                char = '.'
            row.append(char)
        rows.append(''.join(row))
    string = '\n'.join(rows)
    print(string)


def main():
    result = part1()
    print(f'Part 1: {result}')
    result = part2()
    print(f'Part 2: {result}')


if __name__ == '__main__':
    main()
