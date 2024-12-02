import sys
from utils.helpers import parse_args
from utils.find_solution_function import find_solution_function


def main():
    day, part, submit = parse_args(sys.argv)
    solution_function = find_solution_function(day, part)
    solution_function(submit)


if __name__ == "__main__":
    main()
