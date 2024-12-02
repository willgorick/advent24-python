import requests
import os


def parse_args(args: list[str]):
    day, part, submit = None, None, False

    for arg in args:
        if arg.startswith("--day="):
            day = arg.split("=")[1]
        if arg.startswith("--part="):
            part = arg.split("=")[1]
        if arg.startswith("--submit"):
            submit = True

    if day == None or part == None:
        print("Required arguments are: --day and --part")
        exit(1)
    try:
        dayInt = int(day)
        partInt = int(part)
    except:
        print("Either day or part argument was not an int")
        exit(1)

    if not (0 < dayInt < 26) or not (0 < partInt < 3):
        print("Either day or part value out of bounds")
        exit(1)

    return dayInt, partInt, submit


def submit_answer(answer: int, day: int, part: int) -> str:
    print(f"Posting answer: {answer} for day {day} part {part}")
    headers = {
        'Cookie': f'session={os.getenv("session")}',
        'User-Agent': f'https://github.com/willgorick/advent24-python by {os.getenv("email")}'
    }
    url = f"https://adventofcode.com/2024/day/{day}/answer"
    params = {'level': part, 'answer': answer}
    resp = requests.post(url, data=params, headers=headers)
    return resp.text


def read_local_input(calling_file: str, test: bool) -> list[str]:
    local_input_file = _find_local_input_file(calling_file, test)
    try:
        f = open(local_input_file)
        return f.read().splitlines()
    except:
        print(f"Unable to find or open the input file {local_input_file}")
        exit(1)


def _find_local_input_file(calling_file: str, test: bool) -> str:
    file_path_list = calling_file.split('/')
    file_path_list[-1] = 'test.txt' if test else 'input.txt'
    return "/".join(file_path_list)
