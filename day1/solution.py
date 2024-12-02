from utils.helpers import read_input_files, submit_answer
from heapq import heappop, heappush
from collections import defaultdict


def part1(submit: bool):
    print("day 1 part 1")
    test_input, input = read_input_files(__file__)
    test_dist = _heapify_and_calculate_distance(test_input)
    dist = _heapify_and_calculate_distance(input)
    print(f"Test: {test_dist}")
    print(f"Result: {dist}")
    if submit:
        resp = submit_answer(dist, 1, 1)
        print(resp)


def _heapify_and_calculate_distance(input):
    left, right = [], []
    total_dist = 0
    for i in range(len(input)):
        l, r = input[i].split("   ")
        heappush(left, int(l))
        heappush(right, int(r))
    while left:
        total_dist += abs(heappop(left) - heappop(right))
    return total_dist


def part2(submit: bool):
    print("day 2 part 2")
    test_input, input = read_input_files(__file__)
    test_score = _calculate_similarity_score(test_input)
    score = _calculate_similarity_score(input)
    print(f"Test: {test_score}")
    print(f"Result: {score}")
    if submit:
        resp = submit_answer(score, day=1, part=2)
        print(resp)


def _calculate_similarity_score(input):
    l_count, r_count = defaultdict(int), defaultdict(int)
    similarity_score = 0
    for line in input:
        l, r = line.split("   ")
        l_count[int(l)] += 1
        r_count[int(r)] += 1

    for id, count in l_count.items():
        similarity_score += id*count * r_count[id]
    return similarity_score
