from utils.helpers import read_input_files, submit_answer


def part1(submit: bool):
    print("day 0 part 1")
    test_input, input = read_input_files(__file__)
    test_res = _solve1(test_input)
    print(f"Test: {test_res}")
    # res = _solve1(input)
    # print(f"Result: {res}")
    # if submit:
    #     resp = submit_answer(res, 0, 1)


def part2(submit: bool):
    print("day 0 part 2")
    test_input, input = read_input_files(__file__)
    test_res = _solve2(test_input)
    print(f"Test: {test_res}")
    # res = _solve2(input)
    # print(f"Result: {res}")
    # if submit:
    #     resp = submit_answer(res, 0, 2)


def _solve1(input):
    pass


def _solve2(input):
    pass
