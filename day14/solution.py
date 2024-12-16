from utils.helpers import read_input_files, submit_answer
import re
REGEX = "p=([0-9]*),([0-9]*) v=(-?[0-9]*),(-?[0-9]*)"


def part1(submit: bool):
    print("day 14 part 1")
    test_input, input = read_input_files(__file__)
    test_res = _solve1(test_input, True)
    print(f"Test: {test_res}")
    res = _solve1(input)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 14, 1)
        print(resp)


def part2(submit: bool):
    print("day 14 part 2")
    _, input = read_input_files(__file__)
    res = _solve2(input)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 14, 2)
        print(resp)


def _solve1(input, test=False):
    WIDE = 11 if test else 101
    TALL = 7 if test else 103

    q1, q2, q3, q4 = 0, 0, 0, 0
    for line in input:
        match = re.match(REGEX, line)
        x, y, v_x, v_y = int(match.group(1)), int(
            match.group(2)), int(match.group(3)), int(match.group(4))
        for _ in range(100):
            x += v_x
            y += v_y
        x = x % WIDE
        y = y % TALL
        if x < WIDE // 2 and y < TALL // 2:
            q1 += 1
        elif x > WIDE // 2 and y < TALL // 2:
            q2 += 1
        elif x < WIDE // 2 and y > TALL // 2:
            q3 += 1
        elif x > WIDE // 2 and y > TALL // 2:
            q4 += 1
    return q1*q2*q3*q4


def _solve2(input, test=False):
    WIDE = 11 if test else 101
    TALL = 7 if test else 103
    robots = []
    for line in input:
        match = re.match(REGEX, line)
        x, y, v_x, v_y = int(match.group(1)), int(
            match.group(2)), int(match.group(3)), int(match.group(4))
        robots.append((x, y, v_x, v_y))
    i = 0
    while True:
        i += 1
        robot_loc_map = {}
        new_robots = []
        unique_positions = True
        for x, y, v_x, v_y in robots:
            x += v_x
            y += v_y
            x = x % WIDE
            y = y % TALL
            new_robots.append((x, y, v_x, v_y))
            if (x, y) in robot_loc_map:
                unique_positions = False
            robot_loc_map[(x, y)] = True
        grid = [["." for _ in range(WIDE)] for _ in range(TALL)]
        if unique_positions:
            for x, y, _, _ in new_robots:
                grid[y][x] = "*"
            for row in grid:
                print("".join(row))
            return i
        robots = new_robots
