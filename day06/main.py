from string import digits

from aoc import parse_file, InputType
from dataclasses import dataclass
from enum import StrEnum


class Operation(StrEnum):
    ADD = '+'
    MULTIPLY = '*'


@dataclass
class Expression:
    numbers: list[int]
    operation: Operation

    def evaluate(self) -> int:
        if not self.numbers:
            return 0
        match self.operation:
            case Operation.ADD:
                return sum(self.numbers)
            case Operation.MULTIPLY:
                result = 1
                for n in self.numbers:
                    result *= n
                return result
            case _:
                raise ValueError(f'Unknown operation: {self.operation}')


@dataclass
class Homework:
    data: list[list[str]]

    def get_expressions(self) -> list[Expression]:
        numbers_ = [list(row[::-1]) for row in zip(*reversed(self.data))]
        operations = [Operation(row.pop(-1)) for row in numbers_]
        expressions = []
        for numbers, operation in zip(numbers_, operations):
            expressions.append(Expression(numbers=[int(n) for n in numbers
                                                   if n != ''],
                                          operation=operation))
        return expressions

    def get_cephalopod_expressions(self) -> list[Expression]:
        numbers_ = [list(row[::-1]) for row in zip(*reversed(self.data))]
        operations = [Operation(row.pop(-1).strip()) for row in numbers_]
        numbers_ = [[n[::-1] for n in row] for row in numbers_ ]
        expressions = []
        for row, op in zip(numbers_, operations):
            nums = [[d for d in digits_ if d != '0'] for
                    digits_ in
                    zip(*row)]
            nums = [int(''.join(digits_)) for digits_ in nums if digits_]
            expressions.append(Expression(numbers=nums, operation=op))
        return expressions

    def evaluate(self, cephalopod: bool = False) -> int:
        if cephalopod:
            expressions = self.get_cephalopod_expressions()
        else:
            expressions = self.get_expressions()
        return sum(expr.evaluate() for expr in expressions)


def part1(data: list[str]) -> int:
    data = [row.split() for row in data]
    hw = Homework(data)
    return hw.evaluate()


def part2(data: str) -> int:
    for row in data:
        print(row[0])
    data = [row+'      ' for row in data]
    data = [list(row[::-1]) for row in zip(*reversed(data))]
    expressions = []
    nums = []
    for row in data:
        new_op = row.pop(-1)
        op = new_op if new_op in ('+', '*') else op
        if set(row) == {' '}:
            expressions.append(Expression(numbers=[int(n) for n in nums],
                                          operation=Operation(op)))
            nums = []
        else:
            nums.append(''.join(row).strip())
    expressions.append(Expression(numbers=[int(n) for n in nums],
                                  operation=Operation(op)))

    return sum(expr.evaluate() for expr in expressions)


def main(input_type: InputType) -> None:
    data = parse_file(input_type)

    #result1 = part1(data)
    #print(f'Part 1: {result1}')

    result2 = part2(data)
    print(f'Part 2: {result2}')


if __name__ == '__main__':
    main(InputType.INPUT)