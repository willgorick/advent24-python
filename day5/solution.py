from utils.helpers import read_input_files, submit_answer
from collections import defaultdict, deque
from math import ceil


def part1(submit: bool):
    print("day 5 part 1")
    test_input, input = read_input_files(__file__)
    test_res = _solve1(test_input)
    print(f"Test: {test_res}")
    res = _solve1(input)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 5, 1)
        print(resp)


def part2(submit: bool):
    print("day 5 part 2")
    test_input, input = read_input_files(__file__)
    test_res = _solve2(test_input)
    print(f"Test: {test_res}")
    res = _solve2(input)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 5, 2)
        print(resp)


def _solve1(input):
    res = 0
    rules, orders = _parse_rules_and_input(input)
    rules_by_end_page = _parse_rules_by_end(rules)
    for order in orders:
        in_order = True
        order_set = set(order)
        for page in order:
            prerequisites = rules_by_end_page[page]
            for prereq in prerequisites:
                if prereq in order_set:
                    in_order = False
            order_set.remove(page)
        if in_order:
            middle_index = len(order) // 2
            res += order[middle_index]
    return res


def _solve2(input):
    res = 0
    rules, orders = _parse_rules_and_input(input)
    rules_by_end_page = _parse_rules_by_end(rules)
    for order in orders:
        in_order = True
        order_set = set(order)
        for page in order:
            prerequisites = rules_by_end_page[page]
            for prereq in prerequisites:
                if prereq in order_set:
                    in_order = False
            order_set.remove(page)
        if not in_order:
            relevant_rules = _get_relevant_rules(order, rules_by_end_page)
            sorted_order = _topological_sort(relevant_rules)
            middle_index = len(order) // 2
            res += sorted_order[middle_index]
    return res


def _get_relevant_rules(order, rules_by_end_page):
    order_set = set(order)
    relevant_rules = []
    # relevant_rules = [[start_page, end_page]
    #                   for end_page in order for start_page in rules_by_end_page[end_page] if start_page in order_set]
    for end_page in order:
        for start_page in rules_by_end_page[end_page]:
            if start_page in order_set:
                relevant_rules.append([start_page, end_page])
    return relevant_rules


def _topological_sort(rules):
    sorted_order = []
    all_pages = set(page for rule in rules for page in rule)
    in_degree = {page: 0 for page in all_pages}
    graph = {page: [] for page in all_pages}

    for before, after in rules:
        graph[before].append(after)
        in_degree[after] += 1

    sources = deque()
    for page in in_degree:
        if in_degree[page] == 0:
            sources.append(page)
    while sources:
        page = sources.popleft()
        sorted_order.append(page)
        for child in graph[page]:
            in_degree[child] -= 1
            if in_degree[child] == 0:
                sources.append(child)
    return sorted_order


def _parse_rules_and_input(input):
    i = 0
    rules, orders = [], []
    while input[i] != "":
        before, after = input[i].split("|")
        rules.append([int(before), int(after)])
        i += 1
    # skip blank line
    i += 1
    while i < len(input):
        order = input[i].split(",")
        orders.append([int(page) for page in order])
        i += 1
    return rules, orders


def _parse_rules_by_end(rules):
    rules_by_end = defaultdict(list)
    for rule in rules:
        rules_by_end[rule[1]].append(rule[0])
    return rules_by_end
