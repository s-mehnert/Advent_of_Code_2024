from itertools import combinations

# import puzzle input

imported_data = list()

with open("08_input.txt") as input:
    for line in input.readlines():
        imported_data.append([pos for pos in line.strip("\n")])

helper_grid = [[(i, j) for j in range(len(imported_data[0]))] for i in range(len(imported_data))]


# helper functions


def print_grid(grid):
    print()
    for line in grid:
        for pos in line:
            print(pos, end="")
        print()
    print()


def evaluate_grid(grid: list) -> list:
    frequencies = list()

    for line in grid:
        for pos in line:
            if pos != "." and pos not in frequencies:
                frequencies.append(pos)

    return frequencies


def find_antennas(grid: list, frequency: str) -> list:
    antennas = list()

    for i, line in enumerate(grid):
        for j, pos in enumerate(line):
            if pos == frequency:
                antennas.append((i, j))

    return antennas


def find_antipodes(grid: list, antennas: list) -> int:
    antipodes = list()
    antenna_combos = combinations(antennas, 2)

    for combo in antenna_combos:
        a1, a2 = combo
        a1_row, a1_col = a1
        a2_row, a2_col = a2
        diff_rows = a1_row-a2_row
        diff_cols = a1_col-a2_col

        antipode_1 = (a1_row + diff_rows, a1_col + diff_cols)
        antipode_2 = (a2_row - diff_rows, a2_col - diff_cols)

        for antipode in [antipode_1, antipode_2]:
            if antipode[0] in range(len(grid)) and antipode[1] in range(len(grid[0])):
                antipodes.append(antipode)

    return antipodes


# --- Part 2 ---

# calculate the patterns further as long as they are within bounds of grid
# count antenna positions as antinodes as well
# do this in a new function


def find_antipodes_v2(grid: list, antennas: list) -> int:
    antipodes = list()
    antenna_combos = combinations(antennas, 2)

    for combo in antenna_combos:
        a1, a2 = combo
        a1_row, a1_col = a1
        a2_row, a2_col = a2
        diff_rows = a1_row-a2_row
        diff_cols = a1_col-a2_col

        antipodes.extend([a1, a2])

        new_antipode_row = a1_row
        new_antipode_col = a1_col

        while new_antipode_row in range(len(grid)) and new_antipode_col in range(len(grid[0])):
            antipodes.append((new_antipode_row, new_antipode_col))
            new_antipode_row += diff_rows
            new_antipode_col += diff_cols

        new_antipode_row = a2_row - diff_rows
        new_antipode_col = a2_col - diff_cols

        while new_antipode_row in range(len(grid)) and new_antipode_col in range(len(grid[0])):
            antipodes.append((new_antipode_row, new_antipode_col))
            new_antipode_row -= diff_rows
            new_antipode_col -= diff_cols

    return list(set(antipodes))


# calculate result

antipodes = list()
antipodes_v2 = list()

for frequency in evaluate_grid(imported_data):
    new_antipodes = find_antipodes(imported_data, find_antennas(imported_data, frequency))
    new_antipodes_v2 = find_antipodes_v2(imported_data, find_antennas(imported_data, frequency))
    for antipode in new_antipodes:
        if antipode not in antipodes:
            antipodes.append(antipode)
    for antipode_v2 in new_antipodes_v2:
        if antipode_v2 not in antipode_v2:
            antipodes_v2.append(antipode_v2)

result_1 = len(antipodes)

print_grid(imported_data)
print("Number of antipodes on map:", result_1)

result_2 = len(list(set(antipodes_v2)))

print("\nNumber of antipodes on map with new rules:", result_2)
