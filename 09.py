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

    # temp = files.pop(0)
    # decompressed_diskmap = [tuple for pair in zip(freespaces, files) for tuple in pair]
    # decompressed_diskmap.insert(0, temp)

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


def calculate_filesystem_checksum(new_diskmap: list) -> int:
    idx = -1
    checksum = 0

    for block in new_diskmap:
        for i in range(block[1]):
            idx += 1
            checksum += idx * block[0]

    return checksum


# calculate result

files, freespaces = decompress_diskmap(imported_data)
new_diskmap = move_blocks(files, freespaces)
result_1 = calculate_filesystem_checksum(new_diskmap)

print("Checksum of filesystem:", result_1)

result_2 = 0

# print("\nNumber of antipodes on map with new rules:", result_2)
