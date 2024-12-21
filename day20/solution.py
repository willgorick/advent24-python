from utils.helpers import read_input_files, submit_answer

FLIP_MAP = {(0, 1): (0, -1), (0, -1): (0, 1), (1, 0): (-1, 0), (-1, 0): (1, 0)}

def part1(submit: bool):
    print("day 20 part 1")
    test_input, input = read_input_files(__file__)
    test_res = _solve(test_input, test=True)
    print(f"Test: {test_res}")
    res = _solve(input)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 20, 1)
        print(resp)


def part2(submit: bool):
    print("day 20 part 2")
    test_input, input = read_input_files(__file__)
    test_res = _solve(test_input, part=2, test=True)
    print(f"Test: {test_res}")
    res = _solve(input, part=2)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 20, 2)
        print(resp)
    
def _solve(input, part=1, test=False):
    start, end, grid = _parse_input(input)
    best_path = _non_cheat_path(start, end, grid)
    distance_to_end_map = {}
    for i in range(len(best_path)):
        row, col = best_path[i]
        distance_to_end_map[(row, col)] = len(best_path)-i
    cheat_paths = _cheat(end, grid, best_path, distance_to_end_map, part, test)
    return cheat_paths

def _cheat(end, grid, best_non_cheat_path, distance_to_end_map, part=2, test=False):
    SAVINGS = 50 if test and part==2 else (2 if test else 100)
    GOAL_TIME = len(best_non_cheat_path) - SAVINGS
    CHEATS = 20 if part == 2 else 2
    cheat_paths = 0
    time = 0
    for origin in best_non_cheat_path:
        # no cheats starting after this point are worth it, because we can't 
        # reach the end in our goal time
        if _manhattan_distance(origin, end) + time > GOAL_TIME:
            break

        # this double for loop gets every possible location we could get to by cheating
        for i in range(origin[0]-CHEATS, origin[0]+CHEATS+1, 1):
            # however many steps we're taking in the i direction, we have 
            # total steps - that number to take in the j direction
            distance_in_i = abs(origin[0]-i)
            j_distance = CHEATS - distance_in_i
            for j in range(origin[1]-j_distance, origin[1]+j_distance+1, 1):
                # skip out of bounds points, don't end a cheat in a wall
                if not _is_in_bounds(i, j, grid) or (not grid[i][j] in {".", "E"}):
                    continue
                if (i, j) == end:
                    cheat_paths += 1
                elif time + _manhattan_distance(origin, (i, j)) + distance_to_end_map[(i, j)] <= GOAL_TIME:
                    cheat_paths += 1

        time += 1

    return cheat_paths

def _non_cheat_path(start, end, grid):
    path = []
    i, j, prev_dir = start[0], start[1], None
    while (i, j) != end:            
        correct_dir = None
        for dir in [(0,1), (0,-1), (1,0), (-1, 0)]:
            # Never go back the way you came
            if prev_dir != FLIP_MAP[dir] and grid[i+dir[0]][j+dir[1]] in {".", "E"}:
                correct_dir = dir
                break
        path.append((i,j))
        i, j = i+correct_dir[0], j+correct_dir[1]
        prev_dir = correct_dir    
    return path

def _parse_input(input):
    start, end = None, None
    grid = []
    for row in range(len(input)):
        grid_row = []
        for col in range(len(input[0])):
            if input[row][col] == "S":
                start = (row, col)
            elif input[row][col] == "E":
                end = (row, col)
            grid_row.append(input[row][col])
        grid.append(grid_row)
    return start, end, grid

def _is_in_bounds(i, j, grid):
    return i >= 0 and j >= 0 and i < len(grid) and j < len(grid[0])

def _manhattan_distance(point1, point2):
    return abs(point1[0] - point2[0]) + abs(point1[1]-point2[1])