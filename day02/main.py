from xmlrpc.client import FastUnmarshaller

from aoc import parse_file, InputType, timer
import functools



def is_valid_id(id_: str) -> bool:
    length = len(id_)
    if length % 2 != 0:
        return True
    return id_[:length // 2] != id_[length // 2:]


@functools.cache
def is_valid_id_recursive(id_: str) -> bool:
    """Did not work.

    product of not understanding the question correctly."""
    if id_[0] == '0':
        return True
    length = len(id_)
    if length == 1:
        return True
    half_length = length // 2
    if length % 2 != 0:
        s1, s2, s3, s4 = (id_[:half_length], id_[half_length:],
                          id_[:half_length+1], id_[half_length+1:])
        return ((is_valid_id_recursive(s1) and is_valid_id_recursive(s2)) and
                is_valid_id_recursive(s3) and is_valid_id_recursive(s4))
    s4, s5 = id_[:length // 2], id_[length // 2:]
    if s4 == s5:
        return False
    return is_valid_id_recursive(s4) and is_valid_id_recursive(s5)


# Taken from https://stackoverflow.com/questions/29481088/
# Made sure to understand the answer before using it.
def principal_period(s):
    i = (s+s).find(s, 1, -1)
    return 0 if i == -1 else int(s)


# My version of principal period below. This is more intuitive and
# comparable in speed (tbh there's not much in it)
def is_id_invalid(id_: str):
    combined = id_ + id_
    return id_ in combined[1:-1]


@timer()
def part1(data: str) -> int:
    id_ranges = data.pop().split(',')
    all_invalids = set()
    for id_range in id_ranges:
        start_id, end_id = id_range.split('-')
        invalids = {
            id_num for id_num in range(int(start_id), int(end_id) + 1)
            if not is_valid_id(str(id_num))
        }
        all_invalids.update(invalids)
    return sum(all_invalids)


@timer()
def part2(data: str, use_my_func: bool = True) -> int:
    id_ranges = data.pop().split(',')
    all_invalids = set()
    for id_range in id_ranges:
        start_id, end_id = id_range.split('-')
        if use_my_func:
            invalids = {id_num for id_num in range(int(start_id), int(end_id) + 1)
                        if is_id_invalid(str(id_num))}
        else:
            invalids = {principal_period(str(id_num))
                       for id_num in range(int(start_id), int(end_id) + 1)}
        all_invalids.update(invalids)
    return sum(all_invalids)


def main():
    print(f'Part 1: {part1(parse_file(InputType.INPUT))}')
    print(f'Part 2: {part2(parse_file(InputType.INPUT))}')
    print(f'Part 2: {part2(parse_file(InputType.INPUT), use_my_func=False)} (using principal period)')




if __name__ == '__main__':
    main()
