from utils.helpers import read_input_files, submit_answer


def part1(submit: bool):
    print("day 11 part 1")
    test_input, input = read_input_files(__file__)
    test_res = _solve1(test_input)
    print(f"Test: {test_res}")
    res = _solve1(input)
    print(f"Result: {res}")
    # if submit:
    #     resp = submit_answer(res, 11, 1)
    #     print(resp)


def part2(submit: bool):
    print("day 11 part 2")
    test_input, input = read_input_files(__file__)
    test_res = _solve2(test_input)
    print(f"Test: {test_res}")
    res = _solve2(input)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 11, 2)
        print(resp)


def _solve1(input):
    stones = [int(x) for x in input[0].split(" ")]
    return _blink_stones(stones, 25)


def _solve2(input):
    stones = [int(x) for x in input[0].split(" ")]
    return _blink_stones(stones, 75)


def _blink_stones(stones, blinks):
    # We don't have to keep track of each stone, just the number of stones with each unique value
    # Then on each transformation we just store the new_stone(s) * the count of that stone value
    stone_number_map = {}
    for stone in stones:
        stone_number_map[stone] = stone_number_map.get(stone, 0) + 1

    for _ in range(blinks):
        new_stone_number_map = {}
        for stone in stone_number_map:
            if stone == 0:
                new_stone_number_map[1] = new_stone_number_map.get(
                    1, 0) + stone_number_map[stone]
            elif len(str(stone)) % 2 == 0:
                stone_str = str(stone)
                half_one, half_two = int(
                    stone_str[:len(stone_str) // 2]), int(stone_str[len(stone_str) // 2:])
                new_stone_number_map[half_one] = new_stone_number_map.get(
                    half_one, 0) + stone_number_map[stone]
                new_stone_number_map[half_two] = new_stone_number_map.get(
                    half_two, 0) + stone_number_map[stone]
            else:
                new_stone = stone*2024
                new_stone_number_map[new_stone] = new_stone_number_map.get(
                    new_stone, 0) + stone_number_map[stone]
        stone_number_map = new_stone_number_map
    res = 0
    for count in stone_number_map.values():
        res += count
    return res
