# import puzzle input

imported_data = list()

with open("09_input.txt") as input:
    imported_data = list(input.read())


# helper functions


def decompress_diskmap(diskmap: str) -> list:
    files = list()
    freespaces = list()

    for i in range(0, len(diskmap), 2):
        idx = i
        if i > 1:
            idx = i//2
        files.append((idx, int(diskmap[i])))

    for j in range(1, len(diskmap), 2):
        freespaces.append((-1, int(diskmap[j])))

    return files, freespaces


def fill_freespace(file: tuple, freespace: tuple) -> tuple:
    new_file_tup = None
    remaining_file_tup = None
    remaining_freespace_tup = None
    space_diff = file[1] - freespace[1]

    if space_diff > 0:
        remaining_file_tup = (file[0], abs(space_diff))
        new_file_tup = (file[0], freespace[1])

    elif space_diff <= 0:
        new_file_tup = file
        if space_diff != 0:
            remaining_freespace_tup = (freespace[0], abs(space_diff))

    return new_file_tup, [remaining_file_tup, remaining_freespace_tup]


def move_blocks(files: list, freespaces: list) -> list:
    new_diskmap = [files.pop(0)]
    next_block = None
    next_free = None

    while files:
        if not next_block:
            next_block = files.pop()
        if not next_free:
            next_free = freespaces.pop(0)

        to_be_added, rest = fill_freespace(next_block, next_free)
        new_diskmap.append(to_be_added)

        if rest[0]:
            next_block = rest[0]
            new_diskmap.append(files.pop(0))
        else:
            next_block = None
        if rest[1]:
            next_free = rest[1]
        else:
            next_free = None
        if not rest[0] and not rest[1]:
            new_diskmap.append(files.pop(0))

    if next_block:
        new_diskmap.append(next_block)

    return new_diskmap


def move_whole_blocks(files: list, freespaces: list) -> list:
    new_diskmap = [files.pop(0)]
    blocks_remaining_at_end = list()
    # decompressed_diskmap = [tuple for pair in zip(freespaces, files) for tuple in pair]
    # next = None
    next_block = None
    # next_free = None

    while files:
        if next_block:
            blocks_remaining_at_end.insert(0, next_block)
            print("--> adding file", next_block, "to beginning of remaining blocks:", blocks_remaining_at_end)          
            blocks_remaining_at_end.insert(0, freespaces.pop())
            print("--> adding freespace to beginning of remaining blocks:", blocks_remaining_at_end)
        next_block = files.pop()
        found_space = False

        for index, item in enumerate(new_diskmap):
            if item[0] == -1:
                if next_block[1] == item[1]:
                    print("found free space in diskmap --> EXACT FIT")
                    new_diskmap[index] = next_block
                    print("--> inserting file", next_block, "to diskmap:", new_diskmap)
                    if blocks_remaining_at_end:
                        blocks_remaining_at_end.insert(0, (-1, next_block[1]))
                        print("--> adding freespace", (-1, next_block[1]), "to beginning of remaining blocks:", blocks_remaining_at_end)
                    next_block = None
                    found_space = True
                    break
                if next_block[1] < item[1]:
                    print("found free space in diskmap --> FREESPACE REMAINING")
                    new_diskmap.insert(index, next_block)
                    new_diskmap[index+1] = (item[0], item[1]-next_block[1])
                    print("--> inserting file", next_block, "to diskmap:", new_diskmap)
                    if blocks_remaining_at_end:
                        blocks_remaining_at_end.insert(0, (-1, next_block[1]))
                        print("--> adding freespace", (-1, next_block[1]), "to beginning of remaining blocks:", blocks_remaining_at_end)
                    next_block = None
                    found_space = True
                    break

        if not found_space:

            for idx, free in enumerate(freespaces):
                if next_block[1] <= free[1]:
                    new_diskmap.append(next_block)
                    print("--> adding file", next_block, "to diskmap:", new_diskmap)
                    print("--> adding freespace to beginning of remaining blocks:", blocks_remaining_at_end)
                    blocks_remaining_at_end.insert(0, (-1, next_block[1]))
                    print("--> adding freespace", (-1, next_block[1]), "to beginning of remaining blocks:", blocks_remaining_at_end)
                    if next_block[1] < free[1]:
                        freespaces[idx] = (-2, free[1] - next_block[1])
                    next_block = None
                    break

    if next_block:
        blocks_remaining_at_end.insert(0, next_block)

    remaining_freecpaces = [free for free in freespaces if free[0] == -1]
    while remaining_freecpaces:
        blocks_remaining_at_end.insert(0, remaining_freecpaces.pop())

    return new_diskmap + blocks_remaining_at_end


files, freespaces = decompress_diskmap(imported_data)
print(files)
print(freespaces)
print(move_whole_blocks(files, freespaces))


def calculate_filesystem_checksum(new_diskmap: list) -> int:
    idx = -1
    checksum = 0

    for block in new_diskmap:
        for i in range(block[1]):
            idx += 1
            checksum += idx * block[0]

    return checksum


# calculate result

# files, freespaces = decompress_diskmap(imported_data)
# new_diskmap = move_blocks(files, freespaces)
# result_1 = calculate_filesystem_checksum(new_diskmap)

# print("Checksum of filesystem:", result_1)

# new_diskmap = move_whole_blocks(files, freespaces)
# result_2 = calculate_filesystem_checksum(new_diskmap)

# print("\nChecksum of filesystem:", result_2)
