from utils.helpers import read_input_files, submit_answer


def part1(submit: bool):
    print("day 7 part 1")
    test_input, input = read_input_files(__file__)
    test_res = _solve1(test_input)
    print(f"Test: {test_res}")
    res = _solve1(input)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 7, 1)
        print(resp)


def part2(submit: bool):
    print("day 7 part 2")
    test_input, input = read_input_files(__file__)
    test_res = _solve2(test_input)
    print(f"Test: {test_res}")
    res = _solve2(input)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 7, 2)
        print(resp)


def _solve1(input):
    res = 0
    for line in input:
        res += _evaluate_if_possible(line)
    return res


def _solve2(input):
    res = 0
    for line in input:
        res += _evaluate_if_possible(line, True)
    return res


def _evaluate_if_possible(line, part2=False):
    total, parts = line.split(": ")
    total = int(total)
    parts = [int(x) for x in parts.split(" ")]
    return total if _bfs(total, parts, 1, parts[0], part2) else 0


def _bfs(total, parts, index, curr_sum, part2=False):
    # processed all parts, return true if a valid equation was found
    if index == len(parts):
        return curr_sum == total
    # if we've already gone over, stop progressing down this path
    if curr_sum > total:
        return False
    # proceed with bfs trying both addition and multiplication (and concatenation if part 2)
    if part2:
        return _bfs(total, parts, index+1, curr_sum+parts[index], True) or _bfs(total, parts, index+1, curr_sum*parts[index], True) or _bfs(total, parts, index+1, int(str(curr_sum)+str(parts[index])), True)

    return _bfs(total, parts, index+1, curr_sum+parts[index]) or _bfs(total, parts, index+1, curr_sum*parts[index])
