from utils.helpers import read_input_files, submit_answer
import re

DO_REGEX = "do\(\)"
DONT_REGEX = "don't\(\)"
MUL_REGEX = "mul\(([0-9]{1,3}),([0-9]{1,3})\)"


def part1(submit: bool):
    print("day 3 part 1")
    test_input, input = read_input_files(__file__)
    input = _smush_input_lines(input)
    test_input = _smush_input_lines(test_input)

    test_res = find_muls(test_input)
    print(f"Test: {test_res}")
    res = find_muls(input)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 3, 1)
        print(resp)


def part2(submit: bool):
    print("day 3 part 2")
    test_input, input = read_input_files(__file__, "test2.txt")
    input = _smush_input_lines(input)
    test_input = _smush_input_lines(test_input)
    test_res = find_muls2(test_input)
    print(f"Test: {test_res}")
    res = find_muls2(input)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 3, 2)
        print(resp)


def find_muls(input):
    return sum(int(match[0]) * int(match[1]) for match in re.findall(MUL_REGEX, input))


def find_muls2(input):
    res = 0
    mul_enabled = True

    dos = re.finditer(DO_REGEX, input)
    donts = re.finditer(DONT_REGEX, input)
    muls = re.finditer(MUL_REGEX, input)
    mul, do, dont = next(muls), next(dos), next(donts)

    while mul or do or dont:
        mul_index = mul.end() if mul else float('inf')
        do_index = do.end() if do else float('inf'),
        dont_index = dont.end() if dont else float('inf')
        next_instr = min(mul_index, do_index, dont_index)

        if do_index == next_instr:
            mul_enabled = True
            do = next(dos, False)
        elif dont_index == next_instr:
            mul_enabled = False
            dont = next(donts, False)
        else:
            res += int(mul.group(1)) * int(mul.group(2)) if mul_enabled else 0
            mul = next(muls, False)
    return res


def _smush_input_lines(input):
    singleline_input = ""
    for line in input:
        singleline_input += line
    return singleline_input
