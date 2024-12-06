from utils.helpers import read_input_files, submit_answer
from typing import List
from collections import defaultdict

DIR_MAP = {"^": (-1, 0), "v": (1, 0), ">": (0, 1), "<": (0, -1)}
NEXT_DIR = {"^": ">", ">": "v", "v": "<", "<": "^"}
ROW, COLS = None, None
ORIGINAL_PATH = set()


def part1(submit: bool):
    print("day 6 part 1")
    test_input, input = read_input_files(__file__)
    test_res = _solve1(test_input)
    print(f"Test: {test_res}")
    res = _solve1(input)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 6, 1)
        print(resp)


def part2(submit: bool):
    print("day 6, part 2")
    test_input, input = read_input_files(__file__)
    test_res = _solve2(test_input)
    print(f"Test: {test_res}")
    res = _solve2(input)
    print(f"Result: {res}")
    # if submit:
    #     resp = submit_answer(res, 0, 2)
    #     print(resp)


def _solve1(grid: List[List[str]]):
    curr_loc, grid = _setup(grid)
    return _original_path(curr_loc, grid)


def _solve2(grid: List[List[str]]):
    curr_loc, grid = _setup(grid)
    original_path = _original_path(curr_loc, grid, True)
    res = 0
    # check every spot on the original path to determine
    # if an obstruction will cause a cycle
    tenth = len(original_path) // 10
    i = 0
    for (row, col) in original_path:
        if i % tenth == 0:
            print(f"{(i // tenth)*10}%")
        i += 1
        curr_spot = grid[row][col]
        # don't try to place a new obstacle at the start
        # spot or where an obstacle already is
        if curr_spot not in {"^", "#"}:
            grid[row][col] = "#"
            res += _check_for_cycle(grid, curr_loc)
            grid[row][col] = "."

    return res


def _check_for_cycle(grid: List[List[str]], curr_loc: tuple):
    travel_direction = "^"
    visited_map = defaultdict(set)

    while True:
        # if we've reached this location going in this direction
        # # already, we've caused a loop
        if travel_direction in visited_map[curr_loc]:
            return 1

        # add this direction to this location's entry in the map
        visited_map[curr_loc].add(travel_direction)
        move = DIR_MAP[travel_direction]
        next_loc = (curr_loc[0]+move[0], curr_loc[1]+move[1])
        # if we're about to go out of bounds, end the loop
        if not _check_if_in_bounds(next_loc):
            break
        # if the next location is an obstacle, turn right 90 degrees
        if grid[next_loc[0]][next_loc[1]] == "#":
            travel_direction = NEXT_DIR[travel_direction]
        # if no obstacle and inbounds, move to the new location
        else:
            curr_loc = next_loc
    return 0


def _original_path(curr_loc, grid, return_path=False):
    visited_set = set()
    travel_direction = "^"

    while True:
        visited_set.add(curr_loc)
        move = DIR_MAP[travel_direction]
        next_loc = (curr_loc[0]+move[0], curr_loc[1]+move[1])
        # if we're about to go out of bounds, end the loop
        if not _check_if_in_bounds(next_loc):
            break
        # if the next location is an obstacle, turn right 90 degrees
        if grid[next_loc[0]][next_loc[1]] == "#":
            travel_direction = NEXT_DIR[travel_direction]
        # if no obstacle and inbounds, move to the new location
        else:
            curr_loc = next_loc
    return visited_set if return_path else len(visited_set)


def _setup(grid: List[List[str]]):
    global ROWS
    global COLS
    ROWS, COLS = len(grid), len(grid[0])
    new_grid = [[x for x in line] for line in grid]
    for row in range(ROWS):
        for col in range(COLS):
            if new_grid[row][col] == "^":
                return (row, col), new_grid


def _check_if_in_bounds(loc: tuple):
    return loc[0] >= 0 and loc[1] >= 0 and loc[0] < ROWS and loc[1] < COLS
