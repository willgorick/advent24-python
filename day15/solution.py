from utils.helpers import read_input_files, submit_answer
from typing import List

MOVE_MAP = {"<": (0, -1), ">": (0, 1), "^": (-1, 0), "v": (1, 0)}


def part1(submit: bool):
    print("day 15 part 1")
    test_input, input = read_input_files(__file__, "test2.txt")
    test_res = _solve1(test_input)
    print(f"Test: {test_res}")
    res = _solve1(input)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 15, 1)
        print(resp)


# distances are measured from the edge of the map to the closest edge of the box in question (top left)
def part2(submit: bool):
    print("day 15 part 2")
    test_input, input = read_input_files(__file__, "test2.txt")
    test_res = _solve2(test_input)
    print(f"Test: {test_res}")
    res = _solve2(input)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 15, 2)
        print(resp)


def _solve1(input):
    res = 0
    grid, moves, robot = _parse_input(input)
    grid = _move_robot(grid, moves, robot)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "O":
                res += 100*i + j
    return res


def _solve2(input):
    res = 0
    grid, moves, robot = _parse_input_2(input)
    grid = _move_robot_recursive(grid, moves, robot)
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "[":
                res += 100*i + j
    return res


def _parse_input_2(input):
    i = 0
    grid, moves = [], []
    robot = None
    while input[i] != "":
        row = []
        for j in range(len(input[i])):
            if input[i][j] == "@":
                row.append("@")
                row.append(".")
            elif input[i][j] == "O":
                row.append("[")
                row.append("]")
            else:
                row.append(input[i][j])
                row.append(input[i][j])
        grid.append(row)
        i += 1
    i += 1
    for row in range(len(grid)):
        for col in range(len(grid[0])):
            if grid[row][col] == "@":
                robot = (row, col)

    while i < len(input):
        for char in input[i]:
            moves.append(char)
        i += 1
    return grid, moves, robot


def _parse_input(input):
    i = 0
    grid, moves = [], []
    robot = None
    while input[i] != "":
        row = []
        for j in range(len(input[i])):
            if input[i][j] == "@":
                robot = (i, j)
                row.append("@")
            else:
                row.append(input[i][j])
        grid.append(row)
        i += 1
    i += 1

    while i < len(input):
        for char in input[i]:
            moves.append(char)
        i += 1
    return grid, moves, robot


def _move_robot_recursive(grid: List[List[str]], moves: List[str], robot: tuple[int, int]):
    for move in moves:
        offset_i, offset_j = MOVE_MAP[move]
        move_to_i, move_to_j = robot[0]+offset_i, robot[1] + offset_j
        potential_robot = (move_to_i, move_to_j)
        # if the next space is a wall, we can't move
        if grid[move_to_i][move_to_j] == "#":
            continue
        # if the space is empty, move the robot there
        elif grid[move_to_i][move_to_j] == ".":
            grid[robot[0]][robot[1]] = "."
            grid[move_to_i][move_to_j] = "@"
            robot = (move_to_i, move_to_j)
        # trying to move to a space with a box, evaluate if possible
        else:
            # it's possible to move the robot here
            if _box_can_move_recursive(move, grid, move_to_i, move_to_j):
                grid = _move_boxes_recursive(move, grid, move_to_i, move_to_j)
                grid[move_to_i][move_to_j] = "@"
                grid[robot[0]][robot[1]] = "."
                robot = (move_to_i, move_to_j)

    return grid


def _move_boxes_recursive(move: tuple[int, int],  grid: List[List[str]], i, j):
    if grid[i][j] == ".":
        return True
    offset_i, offset_j = MOVE_MAP[move]
    next_i, next_j = i+offset_i, j+offset_j
    if move == ">" or move == "<":
        _move_boxes_recursive(move, grid, next_i, next_j)
        grid[next_i][next_j] = grid[i][j]
    else:
        if grid[i][j] == "[":
            _move_boxes_recursive(move, grid, next_i, next_j) and _move_boxes_recursive(
                move, grid, next_i, next_j+1)
            grid[next_i][next_j] = grid[i][j]
            grid[next_i][next_j+1] = grid[i][j+1]
            grid[i][j] = "."
            grid[i][j+1] = "."
        else:
            _move_boxes_recursive(move, grid, next_i, next_j) and _move_boxes_recursive(
                move, grid, next_i, next_j-1)
            grid[next_i][next_j] = grid[i][j]
            grid[next_i][next_j-1] = grid[i][j-1]
            grid[i][j] = "."
            grid[i][j-1] = "."
    return grid


def _box_can_move_recursive(move: tuple[int, int], grid: List[List[str]], i, j):
    # we've reached a wall
    if grid[i][j] == "#":
        return False
    # we've reached an empty space
    if grid[i][j] == ".":
        return True

    offset_i, offset_j = MOVE_MAP[move]
    next_i, next_j = i+offset_i, j+offset_j
    # less complicated moves
    if move == ">" or move == "<":
        return _box_can_move_recursive(move, grid, next_i, next_j)

    # more complicated up/down moves
    else:
        if grid[i][j] == "[":
            return _box_can_move_recursive(move, grid, next_i, next_j) and _box_can_move_recursive(move, grid, next_i, next_j+1)
        else:
            return _box_can_move_recursive(move, grid, next_i, next_j) and _box_can_move_recursive(move, grid, next_i, next_j-1)

    # def _move_robot_2(grid: List[List[str]], moves: List[str], robot: tuple[int, int]):
    #     for move in moves:
    #         offset_i, offset_j = MOVE_MAP[move]
    #         move_to_i, move_to_j = robot[0]+offset_i, robot[1] + offset_j
    #         potential_robot = (move_to_i, move_to_j)
    #         # if the next space is a wall, we can't move
    #         if grid[move_to_i][move_to_j] == "#":
    #             continue
    #         # if the space is empty, move the robot there
    #         elif grid[move_to_i][move_to_j] == ".":
    #             grid[robot[0]][robot[1]] = "."
    #             grid[move_to_i][move_to_j] = "@"
    #             robot = (move_to_i, move_to_j)
    #         # trying to move to a space with a box, evaluate if possible
    #         else:
    #             box_starts = []
    #             # sideways moves can be handled more normally
    #             if move == ">" or move == "<":
    #                 while grid[move_to_i][move_to_j] == "]" or grid[move_to_i][move_to_j] == "[":
    #                     if grid[move_to_i][move_to_j] == "[":
    #                         box_starts.append(move_to_j)
    #                     move_to_i += offset_i
    #                     move_to_j += offset_j
    #                 # if there is a wall after all the boxes, we cannot move the robot or the boxes
    #                 if grid[move_to_i][move_to_j] == "#":
    #                     continue
    #                 # if there is an empty space after the boxes
    #                 else:
    #                     # loop through the boxes and shift them either left or right
    #                     for i in range(len(box_starts)):
    #                         box_start = box_starts[i]
    #                         if move == ">":
    #                             # if moving right, set value where first box started to robot
    #                             if i == 0:
    #                                 grid[robot[0]][robot[1]] = "."
    #                                 grid[move_to_i][box_start] = "@'"
    #                                 robot = (move_to_i, box_start)
    #                             # set future box start values to a box close
    #                             else:
    #                                 grid[move_to_i][box_start] = "]"
    #                             # set the next value after the original box start to a box start
    #                             grid[move_to_i][box_start+1] = "["

    #                             # move a box to this empty space
    #                     grid[move_to_i][move_to_j] = "O"
    #                     # mark the robot's previous space as empty
    #                     grid[robot[0]][robot[1]] = "."
    #                     # move the robot
    #                     robot = potential_robot
    #                     grid[robot[0]][robot[1]] = "@"

    #                 # advance past all the boxes
    #             while grid[move_to_i][move_to_j] == "O":
    #                 move_to_i += offset_i
    #                 move_to_j += offset_j
    #             pass
    #     return grid


def _move_robot(grid: List[List[str]], moves: List[str], robot: tuple[int, int]):
    for move in moves:
        offset_i, offset_j = MOVE_MAP[move]
        move_to_i, move_to_j = robot[0]+offset_i, robot[1] + offset_j
        potential_robot = (move_to_i, move_to_j)
        # if the next space is a wall, we can't move
        if grid[move_to_i][move_to_j] == "#":
            continue
        # if the space is empty, move the robot there
        elif grid[move_to_i][move_to_j] == ".":
            grid[robot[0]][robot[1]] = "."
            grid[move_to_i][move_to_j] = "@"
            robot = (move_to_i, move_to_j)
        # trying to move to a space with a box, evaluate if possible
        else:
            # advance past all the boxes
            while grid[move_to_i][move_to_j] == "O":
                move_to_i += offset_i
                move_to_j += offset_j

            # if there is a wall after all the boxes, we cannot move the robot or the boxes
            if grid[move_to_i][move_to_j] == "#":
                continue
            # if there is an empty space after the boxes
            else:
                # move a box to this empty space
                grid[move_to_i][move_to_j] = "O"
                # mark the robot's previous space as empty
                grid[robot[0]][robot[1]] = "."
                # move the robot
                robot = potential_robot
                grid[robot[0]][robot[1]] = "@"
    return grid
