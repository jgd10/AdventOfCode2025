from aoc import InputType, parse_file
from dataclasses import dataclass


@dataclass
class Dial:
    needle: int = 50
    max: int = 99
    min: int = 0
    counter: int = 0
    part2: bool = False

    def reduce_by(self, value: int) -> None:
        if self.part2:
            self.counter += value // (self.max + 1)
        value = value % (self.max + 1)
        if (self.needle - value) < self.min:
            if self.part2 and self.needle != 0: self.counter += 1
            self.needle = (self.max+1) - abs(self.needle - value)
        else:
            self.needle = self.needle - value
        if self.needle == 0:
            self.counter += 1

    def increase_by(self, value: int) -> None:
        if self.part2:
            self.counter += value // (self.max + 1)
        value = value % (self.max + 1)
        if self.max < (self.needle + value):
            self.needle = self.min + (self.needle + value - (self.max+1))
            if self.part2 and self.needle != 0: self.counter += 1

        else:
            self.needle = self.needle + value
        if self.needle == 0:
            self.counter += 1


def part1():
    data = parse_file(InputType.INPUT)
    safe = Dial()
    for row in data:
        if 'R' in row:
            safe.increase_by(int(row.replace('R', '')))
        elif 'L' in row:
            safe.reduce_by(int(row.replace('L', '')))
    print(safe.counter)
    return


def part2():
    data = parse_file(InputType.INPUT)
    safe = Dial(part2=True)
    for row in data:
        if 'R' in row:
            safe.increase_by(int(row.replace('R', '')))
        elif 'L' in row:
            safe.reduce_by(int(row.replace('L', '')))
        print(row, safe.needle, safe.counter)
    print(f'Part2: {safe.counter}')
    return


def main():
    part1()
    part2()


if __name__ == '__main__':
    main()
