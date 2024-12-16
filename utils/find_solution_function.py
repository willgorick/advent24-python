import importlib

def find_solution_function(day: int, part: int):
    try:
        solution = importlib.import_module(f"day{day}.solution")
    except ImportError:
        print(f"Error: day{day} not found.")
        exit(1)

    try:
        function = getattr(solution, f"part{part}")
    except AttributeError:
        print(f"Error: part{part} not found in day{day}.")
        exit(1)

    return function