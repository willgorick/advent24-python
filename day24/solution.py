from utils.helpers import read_input_files, submit_answer

def part1(submit: bool):
    print("day 0 part 1")
    test_input, input = read_input_files(__file__, "test2.txt")
    test_res = _solve1(test_input)
    print(f"Test: {test_res}")
    res = _solve1(input)
    print(f"Result: {res}")
    # if submit:
    #     resp = submit_answer(res, 0, 1)
    #     print(resp)


def part2(submit: bool):
    print("day 0 part 2")
    test_input, input = read_input_files(__file__, "test3.txt")
    # test_res = _solve2(test_input, True)
    # print(f"Test: {test_res}")
    res = _solve2(input)
    print(f"Result: {res}")
    # if submit:
    #     resp = submit_answer(res, 0, 2)
    #     print(resp)


def _solve1(input):
    wires, operations, wires_to_solve, _ = _parse_input(input)
    solved_zs = _solve_zs(wires, operations, wires_to_solve)
    return _convert_binary_to_decimal(solved_zs, "z")

def _solve2(input, test=False):
    _, operations, _, highest_z = _parse_input(input)

    wrong = set()
    for res, (op1, op, op2) in operations.items():
        # op must be an XOR for any z wire result other than the most significant bit in order to be a proper adder
        if res.startswith("z") and op != "XOR" and res != highest_z:
            wrong.add(res)

        #if we have an XOR that isn't the final step of adding X+Y -> Z
        if (
            op == "XOR"
            and res[0] not in ["z"]
            and op1[0] not in ["x", "y"]
            and op2[0] not in ["x", "y"]
        ):
            wrong.add(res)

        # an and not involving the LSB
        if op == "AND" and "x00" not in [op1, op2]:
            # the same result being used previously in an operation other than an OR
            for subop1, subop, subop2 in operations.values():
                if (res == subop1 or res == subop2) and subop != "OR":
                    wrong.add(res)
        # an XOR where the result previoulsy was an OR
        if op == "XOR":
            for subop1, subop, subop2 in operations.values():
                if (res == subop1 or res == subop2) and subop == "OR":
                    wrong.add(res)
    return ",".join(sorted(wrong))


def _solve_zs(wires: dict[str, int], operations: dict[str, str], wires_to_solve: set[str]):
    solved_zs = {}
    while len(wires_to_solve):
        solved_wires = set()
        for wire in wires_to_solve:
            # both a and b are present
            needed_a = wires.get(operations[wire][0], None)
            needed_b = wires.get(operations[wire][2], None)
            if needed_a != None and needed_b != None:
                op = operations[wire][1]
                if op == "AND":
                    wires[wire] = needed_a & needed_b
                elif op == "OR":
                    wires[wire] = needed_a | needed_b
                else:
                    wires[wire] = needed_a ^ needed_b
                if wire.startswith("z"):
                    solved_zs[wire] = wires[wire]
                solved_wires.add(wire)
        wires_to_solve -= solved_wires

    return solved_zs

def _convert_binary_to_decimal(solved_values, letter):
    res = 0
    i = 0
    while True:
        ind = str(i)
        if i < 10:
            ind = "0"+str(i)
        if solved_values.get(f"{letter}{ind}", None) != None:
            res += (2**i) * solved_values[f"{letter}{ind}"]
            i += 1
            continue
        break
    return res

def _parse_input(input) -> tuple[dict[str, int], dict[str, tuple[str, str, str]], set[str], str]:
    i = 0
    wires = {}
    while input[i] != "":
        wire, value = input[i].split(": ")
        wires[wire] = int(value)
        i += 1
    i += 1
    operations = {}
    wires_to_solve = set()
    highest_z = 0
    while i < len(input):
        inp, out = input[i].split(" -> ")
        a_wire, operation, b_wire = inp.split(" ")
        operations[out] = (a_wire, operation, b_wire)
        wires_to_solve.add(out)
        if out.startswith("z") and int(out[1:]) > highest_z:
            highest_z = int(out[1:])
        i += 1

    return wires, operations, wires_to_solve, f"z{highest_z}"



def _convert_decimal_to_binary(decimal_number, letter, digits=46):
    wires = {}
    for i in range(digits):
        remainder = decimal_number%2
        decimal_number //=2
        ind = str(i)
        if i < 10:
            ind = f"0{ind}"
        wires[f"{letter}{ind}"] = remainder
    return wires