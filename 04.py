# import puzzle input
imported_data = list()

with open("04_input.txt") as input:
    for line in input.readlines():
        imported_data.append(line.strip("\n"))


# format data

puzzle_grid = [[imported_data[j][i] for i in range(len(imported_data[0]))] for j in range(len(imported_data))]
pos_grid = [[(j, i) for i in range(len(imported_data[0]))] for j in range(len(imported_data))]

# helper functions


def check_right(grid: list, pos: tuple) -> int:
    row, col = pos
    xmas_count = 0

    if grid[row][col+1] == "M":
        if grid[row][col+2] == "A":
            if grid[row][col+3] == "S":
                xmas_count += 1

    return xmas_count


def check_left(grid: list, pos: tuple) -> int:
    row, col = pos
    xmas_count = 0

    if grid[row][col-1] == "M":
        if grid[row][col-2] == "A":
            if grid[row][col-3] == "S":
                xmas_count += 1

    return xmas_count


def check_down(grid: list, pos: tuple) -> int:
    row, col = pos
    xmas_count = 0

    if grid[row+1][col] == "M":
        if grid[row+2][col] == "A":
            if grid[row+3][col] == "S":
                xmas_count += 1

    return xmas_count


def check_up(grid: list, pos: tuple) -> int:
    row, col = pos
    xmas_count = 0

    if grid[row-1][col] == "M":
        if grid[row-2][col] == "A":
            if grid[row-3][col] == "S":
                xmas_count += 1

    return xmas_count


def check_diag_ur(grid: list, pos: tuple) -> int:
    row, col = pos
    xmas_count = 0

    if grid[row-1][col+1] == "M":
        if grid[row-2][col+2] == "A":
            if grid[row-3][col+3] == "S":
                xmas_count += 1

    return xmas_count


def check_diag_ul(grid: list, pos: tuple) -> int:
    row, col = pos
    xmas_count = 0

    if grid[row-1][col-1] == "M":
        if grid[row-2][col-2] == "A":
            if grid[row-3][col-3] == "S":
                xmas_count += 1

    return xmas_count


def check_diag_dr(grid: list, pos: tuple) -> int:
    row, col = pos
    xmas_count = 0

    if grid[row+1][col+1] == "M":
        if grid[row+2][col+2] == "A":
            if grid[row+3][col+3] == "S":
                xmas_count += 1

    return xmas_count


def check_diag_dl(grid: list, pos: tuple) -> int:
    row, col = pos
    xmas_count = 0

    if grid[row+1][col-1] == "M":
        if grid[row+2][col-2] == "A":
            if grid[row+3][col-3] == "S":
                xmas_count += 1

    return xmas_count


direction_dict = {
    "right": check_right,
    "left": check_left,
    "down": check_down,
    "up": check_up,
    "diag_ur": check_diag_ur,
    "diag_ul": check_diag_ul,
    "diag_dr": check_diag_dr,
    "diag_dl": check_diag_dl
}


def filter_directions(grid: list, pos: tuple) -> list:
    row, col = pos
    dirs = list()

    if col > 2:
        dirs.append("left")
        if row > 2:
            dirs.append("diag_ul")
    if row > 2:
        dirs.append("up")
        if col < (len(grid[0])-3):
            dirs.append("diag_ur")
    if col < (len(grid[0])-3):
        dirs.append("right")
        if row < (len(grid)-3):
            dirs.append("diag_dr")
    if row < (len(grid)-3):
        dirs.append("down")
        if col > 2:
            dirs.append("diag_dl")

    return dirs


def check_for_xmas(grid: list, pos: tuple, dirs: list) -> int:
    row, col = pos
    xmas_count = 0

    if grid[row][col] == "X":
        for dir in dirs:
            xmas_count += direction_dict[dir](grid, pos)

    # if xmas_count > 0:
    #     print(f"Adding {xmas_count} at {pos}")

    return xmas_count


# --- PART 2 ---


def check_for_mas_diag_dr(grid: list, pos: tuple) -> bool:
    row, col = pos
    if grid[row+1][col+1] == "A":
        if grid[row+2][col+2] == "S":
            return True
    return False


def check_for_sam_diag_dr(grid: list, pos: tuple) -> bool:
    row, col = pos
    if grid[row+1][col+1] == "A":
        if grid[row+2][col+2] == "M":
            return True
    return False


def check_for_mas_diag_dl(grid: list, pos: tuple) -> bool:
    row, col = pos
    if grid[row+1][col-1] == "A":
        if grid[row+2][col-2] == "S":
            return True
    return False


def check_for_sam_diag_dl(grid: list, pos: tuple) -> bool:
    row, col = pos
    if grid[row+1][col-1] == "A":
        if grid[row+2][col-2] == "M":
            return True
    return False


def check_for_x(grid: list, pos: tuple) -> int:
    row, col = pos
    x_count = 0

    if grid[row][col] == "M":
        if check_for_mas_diag_dr(grid, pos):
            pos_2 = (row, col+2)
            if grid[row][col+2] == "M":
                if check_for_mas_diag_dl(grid, pos_2):
                    x_count += 1
            if grid[row][col+2] == "S":
                if check_for_sam_diag_dl(grid, pos_2):
                    x_count += 1
    if grid[row][col] == "S":
        if check_for_sam_diag_dr(grid, pos):
            pos_2 = (row, col+2)
            if grid[row][col+2] == "M":
                if check_for_mas_diag_dl(grid, pos_2):
                    x_count += 1
            if grid[row][col+2] == "S":
                if check_for_sam_diag_dl(grid, pos_2):
                    x_count += 1

    # if x_count > 0:
    #     print(f"Adding {x_count} at {pos}")

    return x_count


# calculate result

result_1 = 0

for row in range(len(puzzle_grid)):
    for col in range(len(puzzle_grid[0])):
        pos = (row, col)
        dirs = filter_directions(puzzle_grid, pos)
        result_1 += check_for_xmas(puzzle_grid, pos, dirs)

print("XMAS count:", result_1)

result_2 = 0

for row in range(len(puzzle_grid)-2):
    for col in range(len(puzzle_grid[0])-2):
        pos = (row, col)
        result_2 += check_for_x(puzzle_grid, pos)

print("X-MAS count:", result_2)
