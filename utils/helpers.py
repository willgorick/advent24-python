def parse_args(args: list[str]):
    day, part = None, None

    for arg in args:
        if arg.startswith("--day="):
            day = arg.split("=")[1]
        if arg.startswith("--part="):
            part = arg.split("=")[1]

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

    return dayInt, partInt


def read_local_input(calling_file: str) -> list[str]:
    local_input_file = _find_local_input_file(calling_file)
    try:
        f = open(local_input_file)
        return f.read().splitlines()
    except:
        print(f"Unable to find or open the input file {local_input_file}")
        exit(1)


def _find_local_input_file(calling_file: str) -> str:
    file_path_list = calling_file.split('/')
    file_path_list[-1] = 'input.txt'
    return "/".join(file_path_list)
