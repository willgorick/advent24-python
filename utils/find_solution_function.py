
from day1.solution import part1 as day1part1, part2 as day1part2
from day2.solution import part1 as day2part1, part2 as day2part2
from day3.solution import part1 as day3part1, part2 as day3part2
from day4.solution import part1 as day4part1, part2 as day4part2
from day5.solution import part1 as day5part1, part2 as day5part2
from day6.solution import part1 as day6part1, part2 as day6part2
from day7.solution import part1 as day7part1, part2 as day7part2
from day8.solution import part1 as day8part1, part2 as day8part2

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
    }
}


def find_solution_function(day: int, part: int):
    try:
        solution = SOLUTIONS.get(day).get(part)
    except:
        print("Solution either not yet written or not imported")
        exit(1)
    return solution
