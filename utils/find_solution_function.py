
from day1.solution import part1 as day1part1, part2 as day1part2
from day2.solution import part1 as day2part1
SOLUTIONS = {
    1: {
        1: day1part1,
        2: day1part2
    },
    2: {
        1: day2part1
    }
}


def find_solution_function(day: int, part: int):
    try:
        solution = SOLUTIONS.get(day).get(part)
    except:
        print("Solution either not yet written or not imported")
        exit(1)
    return solution
