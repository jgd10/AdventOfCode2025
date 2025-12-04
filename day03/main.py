from aoc import parse_file, InputType


def part1(data: str) -> int:
    joltages = []
    for row in data:
        batteries = list(row)
        best_combo = [batteries[0],
                      batteries[1]]
        for i, bat in enumerate(batteries[1:-1]):
            if int(bat) > int(best_combo[0]):
                best_combo[0] = bat
                best_combo[1] = batteries[i + 2]
            elif int(bat) > int(best_combo[1]):
                best_combo[1] = bat
        if int(batteries[-1]) > int(best_combo[1]):
            best_combo[1] = batteries[-1]
        joltage = int(''.join(best_combo))
        joltages.append(joltage)
    return sum(joltages)


def part2(data: list[str]) -> int:
    vals = find_max_joltages(data, 12)
    return sum(vals)


def find_max_joltages(data: list[str], digits: int) -> list[int]:
    joltages = []

    for ii, row in enumerate(data):
        batteries = [int(i) for i in list(row)]
        best_combo = []
        index = -1
        while len(best_combo) < digits:
            j = len(best_combo)
            h = digits - j
            end_index = -(h - 1)
            if end_index == 0:
                end_index = len(batteries)
            viable = batteries[index+1:end_index]
            best_battery = max(viable)
            best_index = viable.index(best_battery)
            for i in range(best_index+1):
                viable[i] = 0
            batteries[index+1:end_index] = viable
            if index == -1:
                index = 0
            index += best_index
            best_combo.append(best_battery)
            line_viz = ''.join([str(b) for b in batteries]) + ' - ' + ''.join([str(c) for c in best_combo])
            print(line_viz)
        joltage = int(''.join([str(i) for i in best_combo]))
        joltages.append(joltage)
    return joltages


def main():
    data = parse_file(InputType.INPUT)

    result1 = part1(data)
    print(f"Part 1: {result1}")
    print(f"Part 1: {sum(find_max_joltages(data, 12))}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()
