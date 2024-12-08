from utils.helpers import read_input_files, submit_answer
from fractions import Fraction
from collections import defaultdict


def part1(submit: bool):
    solutionTest, solutionFull = Solution(), Solution()
    print("day 8 part 1")
    test_input, input = read_input_files(__file__)
    test_res = solutionTest._solve1(test_input)
    print(f"Test: {test_res}")
    res = solutionFull._solve1(input)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 8, 1)
        print(resp)


def part2(submit: bool):
    print("day 8 part 2")
    solutionTest, solutionFull = Solution(), Solution()
    test_input, input = read_input_files(__file__)
    test_res = solutionTest._solve2(test_input)
    print(f"Test: {test_res}")
    res = solutionFull._solve2(input)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 8, 2)
        print(resp)


class Solution:
    def __init__(self):
        self.antinodes = set()
        self.rows, self.cols = 0, 0

    def _solve1(self, input):
        node_map = self._create_node_map(input)
        for char in node_map:
            char_nodes = node_map[char]
            for i in range(len(char_nodes)):
                for j in range(i+1, len(char_nodes)):
                    self._process_pair(char_nodes[i], char_nodes[j])
        return len(self.antinodes)

    def _solve2(self, input):
        node_map = self._create_node_map(input)
        for char in node_map:
            char_nodes = node_map[char]
            for i in range(len(char_nodes)):
                for j in range(i+1, len(char_nodes)):
                    self._process_pair(char_nodes[i], char_nodes[j], True)
        return len(self.antinodes)

    def _create_node_map(self, input) -> dict[str, list[str]]:
        node_map = defaultdict(list)
        self.rows, self.cols = len(input), len(input[0])
        for row in range(self.rows):
            for col in range(self.cols):
                char = input[row][col]
                if char != ".":
                    node_map[char].append((row, col))
        return node_map

    def _process_pair(self, a, b, part2=False):
        dx, dy = b[0]-a[0], b[1]-a[1]
        # minimize the fraction for the slope
        m = Fraction(dy, dx)
        if part2:
            self._find_antinodes_2(a, b, m)
            return
        self._find_antinodes(a, b, m)
        return

    def _find_antinodes(self, a: tuple[int, int], b: tuple[int, int], m: Fraction):
        antinode_1 = (b[0]+m.denominator, b[1]+m.numerator)
        antinode_2 = (a[0]-m.denominator, a[1]-m.numerator)

        if 0 <= antinode_1[0] < self.rows and 0 <= antinode_1[1] < self.cols and antinode_1 not in self.antinodes:
            self.antinodes.add(antinode_1)
        if 0 <= antinode_2[0] < self.rows and 0 <= antinode_2[1] < self.cols and antinode_2 not in self.antinodes:
            self.antinodes.add(antinode_2)
        return

    def _find_antinodes_2(self, a: tuple[int, int], b: tuple[int, int], m: Fraction):
        # continue the line in the direction of a -> b
        while 0 <= b[0] < self.rows and 0 <= b[1] < self.cols:
            self.antinodes.add(b)
            b = (b[0]+m.denominator, b[1]+m.numerator)

        # continue the line in the direction of b -> a
        while 0 <= a[0] < self.rows and 0 <= a[1] < self.cols:
            self.antinodes.add(a)
            a = (a[0]-m.denominator, a[1]-m.numerator)

        return
