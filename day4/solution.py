from utils.helpers import read_input_files, submit_answer


DIRS = [[0, 1], [0, -1], [1, 1], [1, 0], [1, -1], [-1, 1], [-1, 0], [-1, -1]]
WORD = "XMAS"
INPUT = []


def part1(submit: bool):
    print("day 4 part 1")
    test_input, input = read_input_files(__file__)
    test_res = _solve1(test_input)
    print(f"Test: {test_res}")
    res = _solve1(input)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 4, 1)
        print(resp)


def part2(submit: bool):
    print("day 4 part 2")
    test_input, input = read_input_files(__file__)
    test_res = _solve2(test_input)
    print(f"Test: {test_res}")
    res = _solve2(input)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 4, 2)
        print(resp)


def _solve1(input):
    res = 0
    global INPUT
    INPUT = input
    ROWS, COLS = len(input), len(input[0])
    for i in range(ROWS):
        for j in range(COLS):
            # only search around if we find an X first
            if input[i][j] == "X":
                # search in each of the 8 directions
                for dir_ind in range(len(DIRS)):
                    res += _search(i+DIRS[dir_ind][0], j +
                                   DIRS[dir_ind][1], 1, dir_ind, ROWS, COLS)
    return res


def _solve2(input):
    res = 0
    global INPUT
    INPUT = input
    ROWS, COLS = len(input), len(input[0])
    MS = {"M", "S"}
    for i in range(ROWS):
        for j in range(COLS):
            # find possible centers of X-MASes
            if input[i][j] == "A":
                # if any of the four corners are out of bounds no X MAS
                if not _corners_in_bounds(i, j, ROWS, COLS):
                    continue

                # find the values at the four corners
                corner_indices = [[i-1, j-1],
                                  [i-1, j+1], [i+1, j+1], [i+1, j-1]]
                corners = [INPUT[corner_index[0]][corner_index[1]]
                           for corner_index in corner_indices]

                # all four corners must be either M or S
                if any(corner not in MS for corner in corners):
                    continue

                # if opposing corners are the same, we can't have a X MAS
                if corners[0] == corners[2] or corners[1] == corners[3]:
                    continue
                res += 1

    return res


def _search(i, j, word_ind, dir_ind, rows, cols):
    next_letter_to_find = WORD[word_ind]
    # no matches this direction
    if not _is_in_bounds(i, j, rows, cols) or not INPUT[i][j] == next_letter_to_find:
        return 0
    # we've just matched the last letter
    if word_ind == len(WORD)-1:
        return 1

    # check next letter
    return _search(i+DIRS[dir_ind][0], j+DIRS[dir_ind][1], word_ind+1, dir_ind, rows, cols)


def _is_in_bounds(i, j, rows, cols):
    return i >= 0 and j >= 0 and i < rows and j < cols


def _corners_in_bounds(i, j, rows, cols):
    return i >= 1 and j >= 1 and i < rows-1 and j < cols-1
