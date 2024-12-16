from utils.helpers import read_input_files, submit_answer
from heapq import heappush, heappop

GRID = None
DIRS = [(0, 1), (1, 0), (0, -1), (-1, 0)]


def part1(submit: bool):
    print("day 16 part 1")
    test_input, input = read_input_files(__file__, "test2.txt")
    test_res = _solve1(test_input)
    print(f"Test: {test_res}")
    res = _solve1(input)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 16, 1)
        print(resp)


def part2(submit: bool):
    print("day 16 part 2")
    test_input, input = read_input_files(__file__, "test2.txt")
    test_res = _solve2(test_input)
    print(f"Test: {test_res}")
    res = _solve2(input)
    print(f"Result: {res}")
    # if submit:
    #     resp = submit_answer(res, 16, 2)
    #     print(resp)


def _solve1(input):
    grid, start = _construct_grid(input)
    _, best_cost = _bfs(start, grid)
    return best_cost


def _solve2(input):
    grid, start = _construct_grid(input)
    best_paths, _ = _bfs(start, grid)
    best_path_seats = set()
    for path in best_paths:
        for seat in path.split("|"):
            best_path_seats.add(seat)
    return len(best_path_seats)


def _bfs(start, grid):
    visited_map = {}
    heap = [(0, start, (0, 1), "")]
    best_paths = []
    best_cost = float('inf')
    while heap:
        cost, pos, direction, path = heappop(heap)
        if path == "":
            path += f"{pos}"
        else:
            path += f"|{pos}"
        # we've reached the end, and this is the optimal route because heaps
        if grid[pos[0]][pos[1]] == "E":
            # first best path
            if cost < best_cost:
                best_cost = cost
            # no longer an optimal path reaching the end
            if cost > best_cost:
                return best_paths, best_cost
            best_paths.append(path)
        # we've hit a wall, can't go this way
        if grid[pos[0]][pos[1]] == "#":
            continue
        # we've already reached this point for equal or lesser cost
        if (pos, direction) in visited_map and visited_map.get((pos, direction)) < cost:
            continue
        visited_map[(pos, direction)] = cost
        # try to keep going in the same direction
        heappush(
            heap, (cost+1, (pos[0]+direction[0], pos[1]+direction[1]), direction, path))
        # if we're going  East or West, try North and South
        if direction[0] == 0:
            heappush(
                heap, (cost+1001, (pos[0]+1, pos[1]), (1, 0), path))
            heappush(
                heap, (cost+1001, (pos[0]-1, pos[1]), (-1, 0), path))
        # if we're going North or South, try East and West
        else:
            heappush(
                heap, (cost+1001, (pos[0], pos[1]+1), (0, 1), path))
            heappush(
                heap, (cost+1001, (pos[0], pos[1]-1), (0, -1), path))
    # this would mean the maze has no solution
    return -1


def _construct_grid(input):
    grid = []
    start, end = None, None
    for i in range(len(input)):
        row = []
        for j in range(len(input[0])):
            if input[i][j] == "S":
                start = (i, j)
            row.append(input[i][j])
        grid.append(row)

    return grid, start
