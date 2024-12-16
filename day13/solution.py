import time
from utils.helpers import read_input_files, submit_answer
import re
from heapq import heappush, heappop
from math import ceil

REG_A = "Button A: X\+([0-9]*), Y\+([0-9]*)"
REG_B = "Button B: X\+([0-9]*), Y\+([0-9]*)"
REG_PRIZE = "Prize: X=([0-9]*), Y=([0-9]*)"


def part1(submit: bool):
    print("day 13 part 1")
    test_input, input = read_input_files(__file__)
    test_res = _solve1(test_input)
    print(f"Test: {test_res}")
    # res = _solve1(input)
    # print(f"Result: {res}")
    # if submit:
    #     resp = submit_answer(res, 13, 1)
    #     print(resp)


def part2(submit: bool):
    print("day 13 part 2")
    test_input, input = read_input_files(__file__)
    test_res = _solve1(test_input, 10000000000000)
    print(f"Test: {test_res}")
    res = _solve1(input, 10000000000000)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 13, 2)
        print(resp)


def _solve1(input, offset=0):
    res = 0
    games = []
    curr_game = []
    for line in input:
        a_match = re.match(REG_A, line)
        b_match = re.match(REG_B, line)
        prize_match = re.match(REG_PRIZE, line)
        if a_match:
            curr_game.append((int(a_match.group(1)), int(a_match.group(2))))
        elif b_match:
            curr_game.append((int(b_match.group(1)), int(b_match.group(2))))
        elif prize_match:
            curr_game.append((int(prize_match.group(1)),
                             int(prize_match.group(2))))
            games.append(curr_game)
            curr_game = []
    start = time.time()
    for game in games:
        a_presses, b_presses = _different_play(game, offset)
        if a_presses != None and b_presses != None:
            res += (a_presses*3)+b_presses
    end = time.time()
    print(f"TOTAL TIME: {end-start}")
    return res


"""
A*A_X + B*B_X = P_X
A*A_Y + B*B_Y = P_Y
A = (P_X - B*B_X) / A_X

A*A_Y + B*B_Y = P_Y
((P_X - B*B_X)/A_X) * A_Y + B*B_Y = P_Y
(P_X - B*B_X)/ AX + (B*B_Y) / A_Y = P_Y/A_Y
P_X - B*B_X + (B * B_Y * A_X) / A_Y = (P_Y*A_X) / A_Y
(B * B_Y * A_X)/A_Y - B*B_X = (P_Y*A_X)/A_Y - P_X 
B*((B_Y*A_X)/A_Y - B_X) = (P_Y*A_X)/A_Y - P_X 
B = ((P_Y*A_X)/A_Y - P_X) / ((B_Y*A_X)/A_Y - B_X)
B + (P_Y*A_X - P_X*A_Y) / (B_Y*A_X - B_X*A_Y)
"""


def _different_play(game, offset=0):
    a, b, prize = game
    p_x, p_y = prize
    p_x += offset
    p_y += offset
    a_x, a_y = a
    b_x, b_y = b
    B = (p_y*a_x - p_x*a_y) / (b_y*a_x - b_x * a_y)
    A = (p_x - B*b_x) / a_x
    return int(A) if A.is_integer() else None, int(B) if B.is_integer() else None


def _play(game):
    # keep track of the optimal routes to
    # optimal_routes = [[float('inf') for _ in range(100)] for _ in range(100)]
    # BFS, where heap is the cost in tokens, and the current position
    min_token_positions = {}
    a, b, prize = game
    prize_x, prize_y = prize[0], prize[1]
    heap = []
    # cost, x, y, a_presses, b_presses
    heappush(heap, (0, 0, 0, 0, 0))
    # i = 0
    while heap:
        cost, x, y, a_presses, b_presses = heappop(heap)
        # because we're using a heap, the first time we get a valid x and y we should return
        # the cost, because it is the minimum cost to reach the prize
        if x == prize_x and y == prize_y:
            return cost
        # if we've passed the target in the x or y direction, or we are at over 100 presses for
        # either button, or we've already reached this point for a lesser or equal cost, then skip
        if (x > prize_x or y > prize_y) or (a_presses > 100) or (b_presses > 100) or (min_token_positions.get((x, y), float('inf')) <= cost):
            continue

        min_token_positions[(x, y)] = cost
        heappush(heap, (cost+3, x+a[0], y+a[1], a_presses+1, b_presses))
        heappush(heap, (cost+1, x+b[0], y+b[1], a_presses, b_presses+1))
    # print(i)
    return 0


def _solve2(input):
    pass
