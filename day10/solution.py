from utils.helpers import read_input_files, submit_answer
from collections import deque

DIRS = [(0, 1), (0, -1), (1, 0), (-1, 0)]
NUM_SET = {"0", "1", "2", "3", "4", "5", "6", "7", "8", "9"}


def part1(submit: bool):
    print("day 10 part 1")
    test_input, input = read_input_files(__file__)
    test_solution = Solution(test_input)
    test_res = test_solution.solve()
    print(f"Test: {test_res}")
    solution = Solution(input)
    res = solution.solve()
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 10, 1)
        print(resp)


def part2(submit: bool):
    print("day 10 part 2")
    test_input, input = read_input_files(__file__)
    test_solution = Solution(test_input)
    test_res = test_solution.solve(True)
    print(f"Test: {test_res}")
    solution = Solution(input)
    res = solution.solve(True)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 10, 2)
        print(resp)


class Solution:
    def __init__(self, input):
        self.input = [[int(col) for col in row]
                      for row in input]

    def solve(self, part2=False):
        res = 0
        for i in range(len(self.input)):
            for j in range(len(self.input[0])):
                if self.input[i][j] == 0:
                    res += self._bfs(i, j, 0, part2)
        return res

    def _bfs(self, i, j, elevation, part2=False):
        trail_score = 0
        trailhead_map = set()
        queue = deque([(i, j, elevation)])
        while queue:
            i, j, elevation = queue.popleft()
            # not a valid hike
            if not self._is_in_bounds(i, j) or self.input[i][j] != elevation:
                continue

            # reached the end of a valid hike
            if elevation == 9:
                if part2:
                    trail_score += 1
                elif (i, j) not in trailhead_map:
                    trailhead_map.add((i, j))
                    trail_score += 1
                    continue

            # continue trying to hike in each direction
            for dir in DIRS:
                queue.append((i+dir[0], j+dir[1], elevation+1))
        return trail_score

    def _is_in_bounds(self, i, j):
        return 0 <= i < len(self.input) and 0 <= j < len(self.input[0])
