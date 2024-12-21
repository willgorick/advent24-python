from utils.helpers import read_input_files, submit_answer
from collections import defaultdict

def part1(submit: bool):
    print("day 19 part 1")
    test_input, input = read_input_files(__file__)
    test_solution = Solution(test_input)
    test_res = test_solution._solve1()
    print(f"Test: {test_res}")
    solution = Solution(input)
    res = solution._solve1()
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 19, 1)
        print(resp)


def part2(submit: bool):
    print("day 19 part 2")
    test_input, input = read_input_files(__file__)
    test_solution = Solution(test_input)
    test_res = test_solution._solve2()
    print(f"Test: {test_res}")
    solution = Solution(input)
    res = solution._solve2()
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 19, 2)
        print(resp)

class Solution:
    def __init__(self, input):
        self._parse_input(input)
        self.invalid_patterns = set()
        self.chunk_result_map = {}

    def _solve1(self): 
        return sum([1 if self.recurse_design(towel) else 0 for towel in self.towels])


    def _solve2(self):
        return sum([self.recurse_design_2(towel) for towel in self.towels])

    def recurse_design(self, design, prev_design=""):
        if design in self.invalid_patterns:
            return False
        if len(design) == 0:
            return True
        # greedily try to match the entire design first, 
        # then pick smaller slices
        for i in range(len(design), 0, -1):
            # if a chunk of the design matches a pattern we have,
            # remove that chunk and try to match the remainder of the design
            if self.pattern_map.get(i, False) and design[:i] in self.pattern_map[i]:
                # add all previously found designs to the map to 
                # avoid recalculating work
                prev_design = prev_design + design[:i]
                self.pattern_map[len(prev_design)].add(prev_design)

                valid_design = self.recurse_design(design[i:], prev_design)
                # if this results in a valid design, return true
                # otherewise try again with a smaller chunk of the design
                if valid_design:
                    return True
        # unable to create the design
        self.invalid_patterns.add(design)
        return False
    
    def recurse_design_2(self, design):
        #base cases
        if design in self.invalid_patterns:
            return 0
        if len(design) == 0:
            return 1
        
        sub_result = 0
        for i in range(len(design), 0, -1):
            if self.pattern_map.get(i, False) and design[:i] in self.pattern_map[i]:
                chunk = design[i:]
                # cache the results of each chunk we try
                if self.chunk_result_map.get(chunk, False):
                    chunk_result = self.chunk_result_map[chunk]
                else:
                    chunk_result = self.recurse_design_2(chunk)
                    self.chunk_result_map[chunk] = chunk_result
                sub_result += chunk_result

        # no possible valid solution for this design
        if sub_result == 0:
            self.invalid_patterns.add(design)
        return sub_result
    
    def _parse_input(self, input):
        patterns = input[0].split(", ")
        towels = [input[i] for i in range(2, len(input))]
        pattern_map = defaultdict(set)
        for pattern in patterns:
            pattern_map[len(pattern)].add(pattern)
        self.pattern_map, self.towels = pattern_map, towels