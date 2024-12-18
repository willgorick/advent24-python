from utils.helpers import read_input_files, submit_answer
from collections import deque


def part1(submit: bool):
    print("day 18 part 1")
    test_input, input = read_input_files(__file__)
    test_res = _solve1(test_input, True)
    print(f"Test: {test_res}")
    res = _solve1(input)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 18, 1)
        print(resp)


def part2(submit: bool):
    print("day 18 part 2")
    test_input, input = read_input_files(__file__)
    test_res = _solve2(test_input, True)
    print(f"Test: {test_res}")
    res = _solve2(input)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 18, 2)
        print(resp)


def _solve1(input, test=False):
    grid = _initialize_grid(test)
    for i in range(len(input)):
        if test and i == 12 or i == 1024:
            break
        x, y = input[i].split(",")
        grid[int(y)][int(x)] = "#"
    return _bfs(grid)


def _solve2(input, test=False):
    grid = _initialize_grid(test)
    for i in range(len(input)):
        x, y = input[i].split(",")
        grid[int(y)][int(x)] = "#"
        attempt = _bfs(grid)
        if not attempt:
            return f"{x},{y}"


def _bfs(grid):
    queue = deque([(0, 0, 0)])
    steps = 0
    target = (len(grid)-1, len(grid)-1)
    best = {}
    while queue:
        x, y, steps = queue.popleft()
        if not _is_in_bounds(x, y, grid) or grid[y][x] == "#" or ((x, y) in best and best[(x, y)] <= steps):
            continue
        if (x, y) == target:
            return steps

        best[(x, y)] = steps
        for dir in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            queue.append((x+dir[0], y+dir[1], steps+1))
    return False


def _is_in_bounds(x, y, grid):
    return 0 <= x < len(grid) and 0 <= y < len(grid)


def _initialize_grid(test=False):
    grid_size = 7 if test else 71
    grid = [["." for _ in range(grid_size)] for _ in range(grid_size)]
    return grid
