from aoc import parse_file, InputType, timer
from dataclasses import dataclass
from copy import deepcopy


@dataclass(frozen=True)
class Vector3D:
    x: int
    y: int
    z: int
    
    def distance(self, other):
        return ((self.x - other.x)**2 
                + (self.y - other.y)**2 
                + (self.z - other.z)**2)

    @classmethod
    def from_str(cls, string):
        nums = string.split(',')
        return cls(int(nums[0]), int(nums[1]), int(nums[2]))


def connect_closest_pairs(points: set[Vector3D], number: int):
    pairs = find_closest_pairs(points)
    connected_pairs = set()
    connected_junctions = set()
    for _, pair in zip(range(number), pairs):
        #if len(pair[0].intersection(connected_junctions)) == 2:
        #    continue
        connected_pairs.add(pair[0])
        connected_junctions.update(pair[0])
    return connected_pairs


def find_closest_pairs(points: set[Vector3D]) -> list[
    tuple[frozenset[Vector3D], int]]:
    pairs = find_distances_between_pairs(points)
    pairs = [(k, v) for k, v in sorted(pairs.items(),
                                       key=lambda item: item[1])]
    return pairs


def consolidate_circuits(circuits: list[set[Vector3D]]):
    circuits_updating = True
    old_circuits = deepcopy(circuits)
    while circuits_updating:
        for circuit1 in circuits:
            for circuit2 in circuits:
                if circuit1.intersection(circuit2):
                    circuit1.update(circuit2)
        if circuits == old_circuits:
            circuits_updating = False
        else:
            old_circuits = deepcopy(circuits)


def connect_until_mega_circuit(points):
    pairs = find_closest_pairs(points)
    circuits = []
    biggest_circuit = set()
    all_junctions = set()
    for p in pairs:
        all_junctions.update(p[0])
    while len(biggest_circuit) != len(all_junctions):
        pair, _ = pairs.pop(0)
        pair_in_circuit = False
        intersecting_circuits = []
        for circuit in circuits:
            if circuit.intersection(pair):
                intersecting_circuits.append(circuit)
                intersecting_circuits.append(pair)
                pair_in_circuit = True
        if intersecting_circuits:
            for c in circuits:
                for c2 in intersecting_circuits:
                    if c.intersection(c2):
                        c.update(c2)
        if not pair_in_circuit:
            circuits.append(set(pair))
        circuits = [set(s) for s in {frozenset(d) for d in circuits}]
        len_circuits = sorted(circuits, reverse=True, key=len)
        biggest_circuit = set(len_circuits[0])
    p1, p2 = pair
    return p1.x * p2.x 


def find_circuits(pairs: set[frozenset[Vector3D]]):
    circuits = [set(p) for p in pairs]
    old_circuits = deepcopy(circuits)
    length_circuits = [len(c) for c in circuits]
    circuits_updating = True
    while circuits_updating:
        for pair1 in pairs:
            for circuit in circuits:
                if circuit.intersection(pair1):
                    circuit.update(pair1)
        if circuits == old_circuits:
            circuits_updating = False
        else:
            old_circuits = deepcopy(circuits)
            
    len_circuits = [len(c) for c in {frozenset(d) for d in circuits}]
    len_circuits = sorted(len_circuits, reverse=True)
    return len_circuits[0] * len_circuits[1] * len_circuits[2]


def find_distances_between_pairs(points: set[Vector3D]) -> dict[frozenset[
    Vector3D], int]:
    pairs = {}
    for point1 in points:
        for point2 in points:
            key = frozenset({point1, point2})
            if len(key) == 2 and not key in pairs:
                dist = point1.distance(point2)
                pairs[key] = dist
    return pairs


def part1(data: list[str], n: int) -> int:
    points = set()
    for row in data:
        point = Vector3D.from_str(row)
        points.add(point)
    pairs = connect_closest_pairs(points, n)
    result = find_circuits(pairs)
    return result


def part2(data: list[str]) -> int:
    points = set()
    for row in data:
        point = Vector3D.from_str(row)
        points.add(point)
    result = connect_until_mega_circuit(points)
    return result


@timer()
def part1_for_timer():
    data = parse_file(InputType.INPUT)
    result1 = part1(data, 1000)
    return result1


@timer()
def part2_for_timer():
    data = parse_file(InputType.INPUT)
    result2 = part2(data)
    return result2


def main():
    result1 = part1_for_timer()
    print(f'Part 1: {result1}')
    result2 = part2_for_timer()
    print(f'Part 2: {result2}')
    
    
if __name__ == '__main__':
    main()
