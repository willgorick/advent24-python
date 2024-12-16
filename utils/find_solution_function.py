
from day1.solution import part1 as day1part1, part2 as day1part2
from day2.solution import part1 as day2part1, part2 as day2part2
from day3.solution import part1 as day3part1, part2 as day3part2
from day4.solution import part1 as day4part1, part2 as day4part2
from day5.solution import part1 as day5part1, part2 as day5part2
from day6.solution import part1 as day6part1, part2 as day6part2
from day7.solution import part1 as day7part1, part2 as day7part2
from day8.solution import part1 as day8part1, part2 as day8part2
from day9.solution import part1 as day9part1, part2 as day9part2
from day10.solution import part1 as day10part1, part2 as day10part2
from day11.solution import part1 as day11part1, part2 as day11part2
from day12.solution import part1 as day12part1, part2 as day12part2
from day13.solution import part1 as day13part1, part2 as day13part2
from day14.solution import part1 as day14part1, part2 as day14part2
from day15.solution import part1 as day15part1, part2 as day15part2

SOLUTIONS = {
    1: {
        1: day1part1,
        2: day1part2
    },
    2: {
        1: day2part1,
        2: day2part2
    },
    3: {
        1: day3part1,
        2: day3part2
    },
    4: {
        1: day4part1,
        2: day4part2
    },
    5: {
        1: day5part1,
        2: day5part2
    },
    6: {
        1: day6part1,
        2: day6part2
    },
    7: {
        1: day7part1,
        2: day7part2
    },
    8: {
        1: day8part1,
        2: day8part2
    },
    9: {
        1: day9part1,
        2: day9part2
    },
    10: {
        1: day10part1,
        2: day10part2
    },
    11: {
        1: day11part1,
        2: day11part2
    },
    12: {
        1: day12part1,
        2: day12part2
    },
    13: {
        1: day13part1,
        2: day13part2
    },
    14: {
        1: day14part1,
        2: day14part2
    },
    15: {
        1: day15part1,
        2: day15part2
    }
}


def find_solution_function(day: int, part: int):
    try:
        solution = SOLUTIONS.get(day).get(part)
    except:
        print("Solution either not yet written or not imported")
        exit(1)
    return solution
