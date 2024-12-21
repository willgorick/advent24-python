from utils.helpers import read_input_files, submit_answer
from collections import deque, defaultdict

FLIP_MAP = {(0, 1): (0, -1), (0, -1): (0, 1), (1, 0): (-1, 0), (-1, 0): (1, 0)}
def part1(submit: bool):
    print("day 20 part 1")
    test_input, input = read_input_files(__file__)
    test_res = _solve1(test_input, True)
    print(f"Test: {test_res}")
    res = _solve1(input)
    print(f"Result: {res}")
    # if submit:
    #     resp = submit_answer(res, 20, 1)
    #     print(resp)


def part2(submit: bool):
    print("day 20 part 2")
    test_input, input = read_input_files(__file__)
    test_res = _solve2(test_input, True)
    print(f"Test: {test_res}")
    # res = _solve2(input)
    # print(f"Result: {res}")
    # if submit:
    #     resp = submit_answer(res, 20, 2)
    #     print(resp)


def _solve1(input, test=False):
    start, end, grid = _parse_input(input)
    best_non_cheat, best_path = _non_cheat_path(start, end, grid)
    distance_to_end_map = {}
    for i in range(len(best_path)):
        row, col = best_path[i]
        distance_to_end_map[(row, col)] = len(best_path)-i
    cheat_paths = _cheat_path(start, end, grid, best_non_cheat, distance_to_end_map, test)
    return cheat_paths
    
def _solve2(input, test=False):
    _cheat_20()
    return
    start, end, grid = _parse_input(input)
    best_non_cheat, best_path = _non_cheat_path(start, end, grid)
    distance_to_end_map = {}
    for i in range(len(best_path)):
        row, col = best_path[i]
        distance_to_end_map[(row, col)] = len(best_path)-i
    cheat_paths = _cheat_path_2(start, end, grid, best_non_cheat, distance_to_end_map, test)
    return cheat_paths

def _cheat_20():
    grid = [['.' for _ in range(11)] for _ in range(11)]
    origin = (5, 5)
    radius = 5
    for line in grid:
        print("".join(line))
    print()
    for i in range(origin[0]-radius, origin[0]+radius+1, 1):
        #however many steps we're taking in the i direction, we have total steps - that number to take in the j direction
        distance_in_i = abs(origin[0]-i)
        j_distance = radius - distance_in_i
        for j in range(origin[1]-j_distance, origin[1]+j_distance+1, 1):
            grid[i][j] = "*"
    for line in grid:
        print("".join(line))

    pass

def _non_cheat_path(start, end, grid):
    time = 0
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
        time += 1
    return time, path

def _cheat_path_2(start, end, grid, best_non_cheat, distance_to_end_map, test=False):
    goal_time = best_non_cheat - (50 if test else 100)
    cheat_starts = set()
    cheat_start_ends = set()
    cheat_paths = 0
    
    # i, j, cheats, prev_dir, cheat_start
    queue = deque([(start[0], start[1], 19, None, None)])
    time = 0
    while queue:
        # we don't care about any outcomes beyond this
        if time > goal_time:
            break

        for _ in range(len(queue)):
            i, j, cheats, prev_dir, cheat_start = queue.popleft()

            if not _is_in_bounds(i, j, grid):
                continue

            # don't try to progress further once we've reached the end
            if (i, j) == end:
                # handle cheats that start at the same spot and end at the end
                if cheat_start and (cheat_start, end) in cheat_start_ends:
                    continue
                if cheat_start:
                    cheat_start_ends.add((cheat_start, end))
                print(best_non_cheat - time)
                cheat_paths += 1
                continue

            if grid[i][j] == "#":
                # we're out of cheats so seg fault, or trying to start from the same spot we've already started from
                if cheats == 0 or (i,j) in cheat_starts:
                    continue

                # decrement cheats remaining
                if cheats == 19:
                    cheat_starts.add((i, j))
                    cheat_start = (i, j)
                cheats -= 1
            
            #if we were cheating but are now done cheating
            if cheats < 19 and grid[i][j] == "." and cheat_start:
                # there was another cheat that started and ended at the same spot
                if (cheat_start, (i,j)) in cheat_start_ends:
                    continue
                # no more cheating allowed
                # cheats = 0
                # cheat_start_ends.add((cheat_start, (i, j)))
                # cheat_start = None
                

            # if we have cheats remaining, or are in the process of cheating, continue BFS'ing
            if cheats or cheat_start:
                for dir in [(0,1), (0,-1), (1,0), (-1, 0)]:
                    # never go backwards
                    if dir != FLIP_MAP.get(prev_dir):
                        new_i, new_j = i+dir[0], j+dir[1]
                        queue.append((new_i, new_j, cheats, dir, cheat_start))
            # if no cheats remaining, stick to the optimal path
            else:
                finish_time = time + distance_to_end_map[(i, j)]
                if finish_time <= goal_time:
                    print(best_non_cheat - finish_time)
                    cheat_paths += 1
                
        time += 1
    return cheat_paths

def _cheat_path(start, end, grid, best_non_cheat, distance_to_end_map, test=False):
    goal_time = best_non_cheat - (2 if test else 100)
    cheat_starts = set()
    cheat_paths = 0
    # limiting cheats to 1 because we're only counting a "cheat" state as a state in which we are currently in the wall
    queue = deque([(start[0], start[1], 1, None)])
    time = 0
    while queue:
        # we don't care about any outcomes beyond this
        if time > goal_time:
            break

        for _ in range(len(queue)):
            currently_cheating = False
            i, j, cheats, prev_dir = queue.popleft()
            if not _is_in_bounds(i, j, grid):
                continue

            # don't try to progress further once we've reached the end
            if (i, j) == end:
                cheat_paths += 1
                continue

            if grid[i][j] == "#":
                # we're out of cheats so seg fault
                if not cheats or (i,j) in cheat_starts:
                    continue
                # decrement cheats remaining
                cheats -= 1
                cheat_starts.add((i, j))
                currently_cheating = True
            
            # if we have cheats remaining, or are in the process of cheating, continue BFS'ing
            if cheats or currently_cheating:
                for dir in [(0,1), (0,-1), (1,0), (-1, 0)]:
                    # never go backwards
                    if dir != FLIP_MAP.get(prev_dir):
                        queue.append((i+dir[0], j+dir[1], cheats, dir))
            # if no cheats remaining, stick to the optimal path
            else:
                finish_time = time + distance_to_end_map[(i, j)]
                if finish_time <= goal_time:
                    cheat_paths += 1
                
        time += 1
    return cheat_paths

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