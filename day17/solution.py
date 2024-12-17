from utils.helpers import read_input_files, submit_answer

COMBO_INSTRUCTIONS = {0, 2, 5, 6, 7}
LITERAL_INSTRUCTIONS = {1, 3}

def part1(submit: bool):
    print("day 17 part 1")
    test_input, input = read_input_files(__file__)
    test_res = _solve1(test_input)
    print(f"Test: {test_res}")
    res = _solve1(input)
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 17, 1)
        print(resp)


def part2(submit: bool):
    print("day 17 part 2")
    test_input, input = read_input_files(__file__, "test2.txt")
    # test_res = _solve2(test_input)
    # print(f"Test: {test_res}")
    res = _solve2(input)
    print(f"Result: {res}")
    # if submit:
    #     resp = submit_answer(res, 17, 2)
    #     print(resp)


def _solve1(input):
    reg_a, reg_b, reg_c, program = _parse_input(input)
    output = _run_program(reg_a, reg_b, reg_c, program)
    return ",".join([str(out) for out in output])

# going to be honest, I don't fully understand this
def _solve2(input):
    _, _, _, program = _parse_input(input)
    # each next state will be a three bit number added to the end of the current number
    def find_reg_a(n=0,d=15):
        res = [1E20]
        print(n)
        if d == -1: 
            return n
        for i in range(8):
            # i*(8**d) starts with 8**15, then goes to 2*8^15, etc.
            # the n value is the current register
            reg_a = n+(i*(8**d))
            # print(reg_a)
            output = _run_program(reg_a, 0, 0, program)
            # get bigger until we reach the proper length
            if len(output) != len(program):
                continue
            if output[d] == program[d]: 
                res.append(find_reg_a(reg_a, d-1))
        print(len(res))
        return min(res)
    res = find_reg_a()
    print(res)
    return res

def _run_program(reg_a, reg_b, reg_c, program):
    instr_ptr = 0
    output = []
    while instr_ptr < len(program):
        instruction = program[instr_ptr]
        operand = None
        if instruction in COMBO_INSTRUCTIONS:
            operand = _get_combo_operand(reg_a, reg_b, reg_c, program, instr_ptr)
        elif instruction in LITERAL_INSTRUCTIONS:
            operand = program[instr_ptr+1]
        reg_a, reg_b, reg_c, instr_ptr, output = _process_instruction(reg_a, reg_b, reg_c, instruction, operand, instr_ptr, output)
    return output
    

def _process_instruction(reg_a, reg_b, reg_c, instruction, operand, instr_ptr, output):
    jumped = False
    if instruction == 0:
        reg_a = reg_a // (2**operand)
    elif instruction == 1:
        reg_b = reg_b^operand
    elif instruction == 2:
        reg_b = operand%8
    elif instruction == 3:
        if reg_a != 0:
            jumped = True
            instr_ptr = operand
    elif instruction == 4:
        reg_b = reg_b^reg_c
    elif instruction == 5:
        output.append(operand%8)
    elif instruction == 6:
        reg_b = reg_a // (2**operand)
    elif instruction == 7:
        reg_c = reg_a // (2**operand)


    instr_ptr += 2 if not jumped else 0
    return reg_a, reg_b, reg_c, instr_ptr, output

def _get_combo_operand(reg_a, reg_b, reg_c, program, instr_ptr):
    operand = None
    potential_operand = program[instr_ptr+1]
    if potential_operand <= 3:
        operand = potential_operand
    elif potential_operand == 4:
        operand = reg_a
    elif potential_operand == 5:
        operand = reg_b
    elif potential_operand == 6:
        operand = reg_c
    return operand
def _parse_input(input):
    reg_a = int(input[0].split(": ")[1])
    reg_b = int(input[1].split(": ")[1])
    reg_c = int(input[2].split(": ")[1])
    program = [int(x) for x in input[4].split(": ")[1].split(",")]
    return reg_a, reg_b, reg_c, program
