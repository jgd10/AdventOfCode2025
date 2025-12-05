from aoc import parse_file, InputType
from dataclasses import dataclass


@dataclass(frozen=True)
class Interval:
    start: int
    end: int

    def overlaps(self,
                 other: 'Interval') -> bool:
        return self.start <= other.end and self.end >= other.start


    def is_in(self, value: int) -> bool:
        return self.start <= value <= self.end


    def combine_overlapping(self, other: 'Interval') -> 'Interval':
        new_start = min(self.start, other.start)
        new_end = max(self.end, other.end)
        return Interval(new_start, new_end)

    def calc_valid_count(self) -> int:
        return self.end - self.start + 1


def test_interval_overlaps():
    a = Interval(12, 20)
    b = Interval(20, 23)

    c = Interval(3, 5)
    d = Interval(4, 4)

    assert a.overlaps(b) is True
    assert c.overlaps(d) is True
    assert d.overlaps(c) is True


@dataclass
class IntervalCollection:
    intervals: set[Interval]

    @property
    def count(self) -> int:
        return len(self.intervals)

    def add_interval(self, interval: Interval):
        initial_intervals = self.intervals.copy()
        overlaps = False
        for existing in initial_intervals:
            if existing.overlaps(interval):
                overlaps = True
                new = existing.combine_overlapping(interval)
                self.intervals.remove(existing)
                self.intervals.add(new)
        if not overlaps:
            self.intervals.add(interval)

    def consolidate_intervals(self):
        num_intervals = self.count
        while True:
            self._consolidate_intervals_once()
            if self.count == num_intervals:
                break
            num_intervals = self.count

    def _consolidate_intervals_once(self):
        consolidated = IntervalCollection(set())
        for interval in self.intervals:
            consolidated.add_interval(interval)
        self.intervals = consolidated.intervals


def part1(database: set[Interval], id_list: set[int]) -> int:
    fresh = set()
    for id_value in id_list:
        for interval in database:
            if interval.is_in(id_value):
                fresh.add(id_value)
                break
    return len(fresh)


def part2(database: set[Interval]) -> int:
    interval_collection = IntervalCollection(database)
    interval_collection.consolidate_intervals()
    valid_num_ids = [interval.calc_valid_count() for
                     interval in interval_collection.intervals]
    return sum(valid_num_ids)


def main():
    test_interval_overlaps()
    input_data = parse_file(InputType.INPUT)

    database: set[Interval] = set()
    id_list: set[int] = set()

    for line in input_data:
        if '-' in line:
            start_str, end_str = line.split('-')
            assert int(start_str) <= int(end_str), f"Invalid interval: {line}"
            interval = Interval(int(start_str), int(end_str))
            database.add(interval)
        elif line.isdigit():
            id_list.add(int(line))

    result_part1 = part1(database, id_list)
    print(f"Part 1: {result_part1}")

    result_part2 = part2(database)
    print(f"Part 2: {result_part2}")


if __name__ == "__main__":
    main()