from utils.helpers import read_input_files, submit_answer


def part1(submit: bool):
    print("day 2 part 1")
    test_input, input = read_input_files(__file__)
    test_safety = _check_safety(test_input)
    res = _check_safety(input)
    print(f"Test: {test_safety}")
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 2, 1)
        print(resp)


def part2(submit: bool):
    print("day 2 part 2")
    test_input, input = read_input_files(__file__)
    test_safety = _check_safety_2(test_input)
    res = _check_safety_2(input)
    print(f"Test: {test_safety}")
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 2, 2)
        print(resp)


def _check_safety(input):
    safety_count = 0
    for line in input:
        levels = [int(x) for x in line.split(" ")]
        safety_count += 1 if _safe_report(levels) else 0

    return safety_count


def _check_safety_2(input):
    safety_count = 0
    for line in input:
        levels = [int(x) for x in line.split(" ")]
        report_is_safe = any([_safe_report(levels[:i] +
                                           levels[i+1:]) for i in range(len(levels))])
        safety_count += 1 if report_is_safe else 0
    return safety_count


def _safe_report(levels):
    strict_increasing = {1, 2, 3}
    strict_decreasing = {-1, -2, -3}
    diffs = set()
    for i in range(1, len(levels)):
        diffs.add(levels[i] - levels[i-1])
    return diffs.issubset(
        strict_increasing) or diffs.issubset(strict_decreasing)
