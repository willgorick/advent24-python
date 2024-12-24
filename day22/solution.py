from utils.helpers import read_input_files, submit_answer
from collections import defaultdict, deque

def part1(submit: bool):
    print("day 0 part 1")
    test_input, input = read_input_files(__file__)
    test_res = _solve1(test_input)
    print(f"Test: {test_res}")
    res = _solve1(input)
    print(f"Result: {res}")
    # if submit:
    #     resp = submit_answer(res, 0, 1)
    #     print(resp)


def part2(submit: bool):
    print("day 0 part 2")
    test_input, input = read_input_files(__file__)
    test_res = _solve2(test_input)
    print(f"Test: {test_res}")
    res = _solve2(input)
    print(f"Result: {res}")
    # if submit:
    #     resp = submit_answer(res, 0, 2)
    #     print(resp)


def _solve1(input):
    res = 0
    for line in input:
        secret = int(line)
        for _ in range(2000):
            value = secret*64
            secret = _mix_prune(secret, value)
            value = secret // 32
            secret = _mix_prune(secret, value)
            value = secret * 2048
            secret = _mix_prune(secret, value)
        res += secret
    return res

def _mix_prune(secret, value):
    secret = value^secret
    return secret%16777216

def _solve2(input):
    res = 0
    super_map = {}
    unique_diff_sequences = set()
    for i, line in enumerate(input):
        if i % 100 == 0:
            print(i)
        secret = int(line)
        prev_ones = secret%10
        diffs = deque([])
        diff_map = {}
        for _ in range(2000):
            value = secret*64
            secret = _mix_prune(secret, value)
            value = secret // 32
            secret = _mix_prune(secret, value)
            value = secret * 2048
            secret = _mix_prune(secret, value)
            ones = secret%10
            diffs.append(ones-prev_ones)
            # once diffs is 4 in length
            if len(diffs) > 3:
                # create a tuple to be used as a dict key
                diff_sequence = tuple(diffs)
                # MONKEY ONLY BUYS THE FIRST TIME HE SEES THE SEQUENCE
                if diff_sequence not in diff_map:   
                    diff_map[diff_sequence] = ones
                    # add this sequence to a set with all the unique diff sequences for every starting secret
                    unique_diff_sequences.add(diff_sequence)

                # remove the leftmost diff to keep the length at 4 
                diffs.popleft()
            # set prev_ones to the current ones
            prev_ones = ones
        super_map[i] = diff_map

    for unique_sequence in unique_diff_sequences:
        sub_res = 0
        # get the best value for the sequence from each starting secret
        for i in range(len(input)):
            sub_res += super_map[i].get(unique_sequence, 0)
        res = max(res, sub_res)
        
    return res
# greater than 2233 but lower than 2416