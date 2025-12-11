from aoc import parse_file, InputType, timer
from dataclasses import dataclass
from sympy import linsolve, Symbol
from sympy.abc import symbols
from itertools import product
from pulp import (LpProblem, LpVariable, lpSum, LpMinimize, LpInteger,
                  PULP_CBC_CMD)


@dataclass(frozen=True)
class Button:
    target: list[int]

    @classmethod
    def from_string(cls, string: str) -> 'Button':
        string = string.replace('(',
                                '').replace(')',
                                            '')
        nums = [int(c) for c in string.split(',')]
        return cls(nums)

    def press(self, state: tuple[bool, ...]) -> tuple[bool, ...]:
        return tuple([not v if i in self.target else v
                      for i, v in enumerate(state)])

    def jpress(self, state: tuple[int, ...]) -> tuple[int, ...]:
        return tuple([v + 1 if i in self.target else v
                      for i, v in enumerate(state)])


@dataclass
class Machine:
    target: list[bool]
    state: list[bool] = None
    buttons: list[Button] = None

    @classmethod
    def from_string(cls, string: str) -> 'Machine':
        string = string.replace('[','').replace(']','')
        pieces = string.split(' ')
        lights = pieces.pop(0)
        joltage = pieces.pop(-1)
        buttons = [Button.from_string(b) for b in pieces]
        length = len(lights)
        state = [False] * length
        target = [c == '#' for c in lights]
        return cls(target, state, buttons)

    def get_optimal_presses(self) -> int:
        start_state = tuple(self.state)
        target = tuple(self.target)
        explored = {start_state}
        queue = [(start_state, 0)]
        while queue:
            state, steps = queue.pop(0)
            if state == target:
                return steps
            for possible_state in self.buttons_press(state):
                if possible_state not in explored:
                    explored.add(possible_state)
                    queue.append((possible_state, steps+1))
        raise Exception('No solution found')

    def buttons_press(self, state: tuple[bool, ...]) -> set[tuple[bool, ...]]:
        new_states = set()
        for button in self.buttons:
            new_states.add(button.press(state))
        return new_states

    def joltage_press(self, state: tuple[int, ...]) -> set[tuple[int, ...]]:
        new_states = set()
        for button in self.buttons:
            new_states.add(button.jpress(state))


@dataclass
class EquationSet:
    target: list[int]
    buttons: list[tuple[int, ...]]

    @classmethod
    def from_string(cls, string: str) -> 'EquationSet':
        string = string.replace('{','').replace('}','').replace('(','').replace(')','')
        pieces = string.split(' ')
        pieces.pop(0)
        joltage = pieces.pop(-1)
        target = [int(j) for j in joltage.split(',')]
        buttons = []
        for button in pieces:
            vec = [0 for _ in target]
            for index in button.split(','):
                vec[int(index)] = 1
            buttons.append(vec)
        return cls(target, buttons)

    def get_optimal_presses(self) -> int:
        equations = []
        n_buttons = len(self.buttons)
        x = symbols(f'x0:{n_buttons}', integer=True, nonnegative=True)
        for j in range(len(self.target)):
            eq = sum(self.buttons[i][j] * x[i] for i in range(n_buttons)) - self.target[j]
            equations.append(eq)

        # Solve
        solution = linsolve(equations, x)
        # linsolve returns a FiniteSet of tuples; extract the first solution
        sol = list(solution)[0]

        # If solution contains free parameters (symbols), we need to minimize total presses
        free_symbols = [s for s in sol if isinstance(s, Symbol)]
        if free_symbols:
            target_max = max(self.target)
            min_total = None
            best_solution = None

            for vals in product(range(target_max + 1), repeat=len(free_symbols)):
                subs = dict(zip(free_symbols, vals))
                concrete_sol = [int(s.subs(subs)) for s in sol]
                if all(v >= 0 for v in concrete_sol):
                    total = sum(concrete_sol)
                    if (min_total is None) or (total < min_total):
                        min_total = total
                        best_solution = concrete_sol
            if best_solution is None:
                raise ValueError("No valid integer solution found within the search range")
            return sum(best_solution)
        else:
            # Fully determined solution
            concrete_sol = [int(v) for v in sol]
            return sum(concrete_sol)

    def minimal_presses(self):
        num_buttons = len(self.buttons)
        num_coords = len(self.target)
        prob = LpProblem("MinimalPresses", LpMinimize)
        x = [LpVariable(f"x{i}", lowBound=0, cat=LpInteger) for i in range(num_buttons)]
        # Objective
        prob += lpSum(x)
        # Constraints
        for j in range(num_coords):
            prob += lpSum(self.buttons[i][j] * x[i] for i in range(num_buttons)) == self.target[j]
        prob.solve(PULP_CBC_CMD(msg=0))
        solution = [v.varValue for v in x]
        return sum(solution)


@dataclass
class MachineJoltage:
    target: tuple[int, ...]
    state: tuple[int, ...] = None
    buttons: list[tuple[int, ...]] = None

    @classmethod
    def from_string(cls, string: str) -> 'MachineJoltage':
        string = string.replace('{','').replace('}','').replace('(','').replace(')','')
        pieces = string.split(' ')
        lights = pieces.pop(0)
        joltage = pieces.pop(-1)
        target = tuple([int(j) for j in joltage.split(',')])
        state = tuple([0 for _ in target])
        buttons = []
        for button in pieces:
            vec = [0 for _ in target]
            for index in button.split(','):
                vec[int(index)] = 1
            buttons.append(vec)
        return cls(target, state, buttons)

    def minimal_presses2(self) -> int:
        """
        Computes the minimal number of button presses to reach the target.
        target: list of ints (remaining increments needed)
        buttons: list of lists of 0/1 indicating which coordinates each button affects
        """
        target = list(self.target)[:]  # make a mutable copy
        presses = [0] * len(self.buttons)

        while any(t > 0 for t in target):
            # Compute coverage of each button (number of coordinates it can increment >0)
            coverage = [
                sum([1 for j, b in enumerate(self.buttons[i]) if b and target[j] > 0])
                for i in range(len(self.buttons))
            ]

            if max(coverage) == 0:
                # No button can increment remaining coordinates → impossible
                raise ValueError("Some coordinates cannot be reached by any button")

            # Pick the button that covers the most needed increments
            best_index = coverage.index(max(coverage))

            # Press it once
            presses[best_index] += 1
            for j, b in enumerate(self.buttons[best_index]):
                if b and target[j] > 0:
                    target[j] -= 1

        return sum(presses)

    def minimal_presses(self):
        target = list(self.target)
        presses = [0] * len(self.buttons)

        while any(t > 0 for t in target):
            # Select button that covers most remaining needed increments
            max_button_vals = [sum(1 for j, b in enumerate(self.buttons[i]) if b and target[j] > 0) for i in range(len(self.buttons))]
            best_index = max_button_vals.index(max(max_button_vals))

            # Determine how many times to press it
            max_needed = min([target[j]
                              for j, b in enumerate(self.buttons[best_index])
                              if b and target[j] > 0], default=0)
            if max_needed == 0:
                # pick 1 by default if all covered partially
                continue

            # Press button
            presses[best_index] += max_needed
            for j, b in enumerate(self.buttons[best_index]):
                if b:
                    target[j] -= max_needed

        return sum(presses)

@timer()
def part1(data: str) -> int:
    machines = [Machine.from_string(row) for row in data]
    #optimal_presses = [m.get_optimal_presses() for m in machines]
    optimal_presses = []
    for m in machines:
        presses = m.get_optimal_presses()
        optimal_presses.append(presses)
    return sum(optimal_presses)


@timer()
def part2(data: str) -> int:
    machines = [EquationSet.from_string(row) for row in data]
    optimal_presses = []
    for m in machines:
        presses = m.minimal_presses()
        optimal_presses.append(presses)
    return sum(optimal_presses)


def main():
    data = parse_file(InputType.INPUT)
    result1 = part1(data)
    print(f'Part 1: {result1}')
    data = parse_file(InputType.INPUT)
    result2 = part2(data)
    print(f'Part 2: {result2}')


if __name__ == '__main__':
    main()
