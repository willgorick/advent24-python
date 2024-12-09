from utils.helpers import read_input_files, submit_answer

# Why did I do this with a doubly linked list?


class DoublyLinkedListNode:
    def __init__(self, is_file: bool, start_index: int, size: int, file_index: int = -1):
        self.is_file = is_file
        self.start_index = start_index
        self.size = size
        self.file_index = file_index
        self.next, self.prev = None, None

    def __repr__(self):
        return f"{'File' if self.is_file else 'Empty'}{self.file_index if self.file_index >= 0 else ''}: size {self.size}, starting at index {self.start_index}"


def part1(submit: bool):
    print("day 9 part 1")
    test_input, input = read_input_files(__file__)
    test_res = _solve1(test_input[0])
    print(f"Test: {test_res}")
    res = _solve1(input[0])
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 9, 1)
        print(resp)


# for ƒree space blocks keep a map of free space block size to a heap of indices (where the blocks of memory of that size start).  When you fill each block heappop that index from the list (so the next lowest index is next), and then heappush the difference between the free space block size and the file block size
def part2(submit: bool):
    print("day 9 part 2")
    test_input, input = read_input_files(__file__)
    test_res = _solve2(test_input[0])
    print(f"Test: {test_res}")
    res = _solve2(input[0])
    print(f"Result: {res}")
    if submit:
        resp = submit_answer(res, 9, 2)
        print(resp)


def _solve1(input):
    memory_map, next_to_move_index, next_free_space_index = _setup_memory(
        input)
    _shift_memory(memory_map, next_to_move_index, next_free_space_index)
    return _checksum(memory_map)


def _solve2(input):
    head = _setup_memory_2(input)
    curr = head
    while curr != None:
        prev = curr
        curr = curr.next
    l = head
    _try_to_move_chunks(l, prev)
    res = _checksum_chunks(head)
    return res


def _setup_memory_2(input):
    is_file = True
    file_index, memory_index = 0, 0
    prev = None
    head = None
    for char in input:
        node = DoublyLinkedListNode(is_file, memory_index, int(
            char), file_index if is_file else -1)
        if not head:
            head = node
        if prev:
            node.prev = prev
            prev.next = node

        prev = node
        memory_index += int(char)
        file_index += 1 if is_file else 0
        is_file = not is_file

    return head


def _checksum_chunks(curr: DoublyLinkedListNode):
    res = 0
    while curr:
        if curr.is_file:
            for i in range(curr.start_index, curr.start_index+curr.size):
                res += i * curr.file_index
        curr = curr.next
    return res


def _try_to_move_chunks(l: DoublyLinkedListNode, r: DoublyLinkedListNode):
    head = l
    swapped_set = set()
    while r:
        # unable to perform a swap, reset l and shift to next earlier block for r
        if not l or r.file_index in swapped_set or r.start_index < l.start_index:
            l = head
            r = r.prev
            continue

        # find the next file
        if not r.is_file:
            r = r.prev
            continue

        # can't move to a block that is already a file
        # can't swap the file r to empty block l if l is smaller
        if l.is_file or l.size < r.size:
            l = l.next
            continue

        # valid swap!
        # easy case - swap the file_index and is_file flag
        swapped_set.add(r.file_index)
        if l.size == r.size:
            l.is_file, r.is_file = r.is_file, l.is_file
            l.file_index, r.file_index = r.file_index, l.file_index
        # tricky case, we're swapping r into a space larger than it
        else:
            size_diff = l.size - r.size
            # swap the file_index and is_file flag
            l.is_file, r.is_file = r.is_file, l.is_file
            l.file_index, r.file_index = r.file_index, l.file_index
            # decrease the size of the new l block to the r block's size
            l.size = r.size
            new_block = DoublyLinkedListNode(
                False, l.start_index+l.size, size_diff, -1)
            l_next = l.next
            # insert new_block between l and l's next
            new_block.next = l_next
            l_next.prev = new_block
            new_block.prev = l
            l.next = new_block
        # move on to next chunk
        r = r.prev
        # reset l to the head
        l = head


def _setup_memory(input):
    memory_map = {}
    memory_index, file_id = 0, 0
    # next_free_space_index is set to the first free block of space (note this works because my second number is not a 0)
    next_free_space_index, next_to_move_index = int(input[0]), None
    is_file = True
    for char in input:
        for _ in range(int(char)):
            # set value in memory_map
            memory_map[memory_index] = file_id if is_file else "."
            # if we're looking at a file, update our next_to_move_index
            next_to_move_index = memory_index if is_file else next_to_move_index
            # memory_index keeps track of where in memory we're updating
            memory_index += 1
        # increase the file_id if we just wrote a file
        file_id += 1 if is_file else 0
        # flip the is_file boolean
        is_file = not is_file

    return memory_map, next_to_move_index, next_free_space_index


def _shift_memory(memory_map, next_to_move_index, next_free_space_index):
    while next_to_move_index > next_free_space_index:
        # grab current value to move
        val_to_move = memory_map[next_to_move_index]

        # move value to next free space, update its prev space to be "."
        memory_map[next_free_space_index] = val_to_move
        memory_map[next_to_move_index] = "."

        # get next non-empty index from the right (next file piece)
        while next_to_move_index >= next_free_space_index and memory_map[next_to_move_index] == ".":
            next_to_move_index -= 1

        # get next empty index from the left (next free space)
        while next_free_space_index <= next_to_move_index and memory_map[next_free_space_index] != ".":
            next_free_space_index += 1


def _checksum(memory_map):
    res = 0
    for [key, val] in memory_map.items():
        res += key*val if val != "." else 0
    return res
