from utils.helpers import read_input_files, submit_answer


def part1(submit: bool):
    print("day 25 part 1")
    test_input, input = read_input_files(__file__)
    test_res = _solve1(test_input)
    print(f"Test: {test_res}")
    res = _solve1(input)
    print(f"Result: {res}")
    # if submit:
    #     resp = submit_answer(res, 25, 1)
    #     print(resp)


def part2(submit: bool):
    print("day 25 part 2")
    test_input, input = read_input_files(__file__)
    test_res = _solve2(test_input)
    print(f"Test: {test_res}")
    # res = _solve2(input)
    # print(f"Result: {res}")
    # if submit:
    #     resp = submit_answer(res, 25, 2)
    #     print(resp)


def _solve1(input):
    keys, locks = _parse_input(input)
    fits = 0
    for key in keys:
        for lock in locks:
            valid_pair = True
            for i in range(len(key)):
                if key[i]+lock[i] > 5:
                    valid_pair = False
            fits +=1 if valid_pair else 0
    return fits


def _solve2(input):
    pass

def _parse_input(input) -> tuple[list[tuple], list[tuple]]:
    keys = []
    locks = []
    current = []
    isKey = None
    for line in input:
        if line == "" or line == "\n":
            counts = []
            for col in range(len(current[0])):
                count = sum(1 if current[row][col] == "#" else 0 for row in range(len(current)))
                counts.append(count-1)
            if isKey:
                keys.append(counts)
            else: 
                locks.append(counts)
            current = []
            continue

        if not len(current):
            isKey = line == "#####"
        current.append(line)
    if len(current):
        counts = []
        for col in range(len(current[0])):
            count = sum(1 if current[row][col] == "#" else 0 for row in range(len(current)))
            counts.append(count-1)
        if isKey:
            keys.append(counts)
        else: 
            locks.append(counts)
    return keys, locks