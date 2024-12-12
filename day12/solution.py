from utils.helpers import read_input_files, submit_answer
from collections import deque


def part1(submit: bool):
    print("day 12 part 1")

    test_input, input = read_input_files(__file__)
    test_solution = Solution(test_input)
    test_res = test_solution.solve1()
    print(f"Test: {test_res}")
    solution = Solution(input)
    res = solution.solve1()
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 12, 1)
        print(resp)


def part2(submit: bool):
    print("day 12 part 2")
    test_input, input = read_input_files(__file__)
    test_solution = Solution(test_input)
    test_res = test_solution.solve2()
    print(f"Test: {test_res}")
    solution = Solution(input)
    res = solution.solve2()
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 12, 2)
        print(resp)


class Solution:
    def __init__(self, input):
        self.input = input
        self.rows, self.cols = len(input), len(input[0])
        self.visited = set()
        self.dirs = {"R": (0, 1), "L": (0, -1), "D": (1, 0), "U": (-1, 0)}

    def solve1(self):
        res = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) not in self.visited:
                    area, perimeter = self._bfs(row, col)
                    res += area*perimeter
        return res

    def solve2(self):
        res = 0
        for row in range(self.rows):
            for col in range(self.cols):
                if (row, col) not in self.visited:
                    area, sides = self._bfs2(row, col)
                    res += area*sides
        return res

    def _bfs(self, row, col):
        plant_type = self.input[row][col]
        area, perimeter = 0, 0
        queue = deque([(row, col)])
        self.visited.add((row, col))

        while queue:
            i, j = queue.popleft()
            area += 1
            for dir in self.dirs.values():
                new_i, new_j = i+dir[0], j+dir[1]
                # can't expand the region in this direction, build a fence here
                if (not self._is_in_bounds(new_i, new_j)) or self.input[new_i][new_j] != plant_type:
                    perimeter += 1
                # can expand the region in this direction
                elif (new_i, new_j) not in self.visited:
                    queue.append((new_i, new_j))
                    self.visited.add((new_i, new_j))
        return area, perimeter

    def _bfs2(self, row, col):
        plant_type = self.input[row][col]
        area, sides = 0, 0
        # Keep track of where we've built fence (which direction we came from and which coordinate the fence is at)
        perimeter_set = set()
        queue = deque([(row, col)])
        self.visited.add((row, col))

        while queue:
            i, j = queue.popleft()
            area += 1
            for letter, dir in self.dirs.items():
                new_i, new_j = i+dir[0], j+dir[1]
                # can't expand the region in this direction, build a fence here
                if (not self._is_in_bounds(new_i, new_j)) or self.input[new_i][new_j] != plant_type:
                    # check if there is a neighboring fence piece, if not increment the number of sides
                    if letter == "U" or letter == "D":
                        if not (letter, new_i, new_j-1) in perimeter_set and not (letter, new_i, new_j+1) in perimeter_set:
                            sides += 1
                    else:
                        if not (letter, new_i-1, new_j) in perimeter_set and not (letter, new_i+1, new_j) in perimeter_set:
                            sides += 1
                    perimeter_set.add((letter, new_i, new_j))
                # can expand the region in this direction
                elif (new_i, new_j) not in self.visited:
                    queue.append((new_i, new_j))
                    self.visited.add((new_i, new_j))
        return area, sides

    def _is_in_bounds(self, i, j):
        return 0 <= i < self.rows and 0 <= j < self.cols
