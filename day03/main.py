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


def part2(data: str) -> int:
    joltages = []
    for row in data:
        batteries = [int(i) for i in list(row)]
        best_combo = []  # batteries[:12]
        while len(best_combo) < 12:
            j = len(best_combo)
            batteries_remaining = len(batteries)
            index = min(batteries_remaining, 11) - j + 1
            viable_batteries = batteries[min(j, 12):batteries_remaining-index]
            best_battery = max(viable_batteries)
            best_battery_index = batteries.index(best_battery)
            best_combo.append(best_battery)
            batteries.pop(best_battery_index+min(j,12))
        print(row, best_combo)
        joltage = int(''.join([str(i) for i in best_combo]))
        joltages.append(joltage)

        #for i, bat in enumerate(batteries):
        #    digits_left = min(len(batteries), 12)
        #    best_battery = max(batteries[])
        #    for j in range(12 - digits_left, min(i, 12)):
        #        if int(bat) > int(best_combo[j]):
        #            best_combo[j:] = batteries[i:i+digits_left]
        #if int(batteries[-1]) > int(best_combo[1]):
        #    best_combo[1] = batteries[-1]
        #joltage = int(''.join(best_combo))
        #joltages.append(joltage)
    return sum(joltages)

def main():
    data = parse_file(InputType.EXAMPLE2)

    result1 = part1(data)
    print(f"Part 1: {result1}")

    result2 = part2(data)
    print(f"Part 2: {result2}")


if __name__ == "__main__":
    main()