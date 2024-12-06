# import puzzle input

imported_data = list()

with open("06_input.txt") as input:
    for line in input.readlines():
        imported_data.append(line.strip("\n"))

for line in imported_data:
    print(line)
print()


# format data

formatted_data = list()

helper_grid = [[(i, j) for j in range(len(imported_data[0]))] for i in range(len(imported_data))]


# helper functions


def evaluate_starting_grid(grid: list) -> tuple:
    max_row = len(grid)-1
    max_col = len(grid[0])-1
    guard_pos = None
    facing = None
    obstacles = list()

    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j] == "#":
                obstacles.append((i, j))
            elif grid[i][j] != ".":
                guard_pos = (i, j)
                facing = grid[i][j]

    return guard_pos, facing, obstacles, max_row, max_col


def count_distance_to_obstacle(guard_pos: tuple, facing: str, obstacles: list, max_row, max_col) -> int:
    row, col = guard_pos
    distance = None
    visited = list()

    if facing == "^":
        for step in range(row, -1, -1):
            if (step, col) not in visited:
                visited.append((step, col))
            if (step, col) in obstacles:
                distance = row-step-1
                visited.pop()
                break
            distance = row-step
    elif facing == "v":
        for step in range(row, max_row+1):
            if (step, col) not in visited:
                visited.append((step, col))
            if (step, col) in obstacles:
                distance = step-row-1
                visited.pop()
                break
            distance = step-row
    elif facing == "<":
        for step in range(col, -1, -1):
            if (row, step) not in visited:
                visited.append((row, step))
            if (row, step) in obstacles:
                distance = col-step-1
                visited.pop()
                break
            distance = col-step
    elif facing == ">":
        for step in range(col, max_col+1):
            if (row, step) not in visited:
                visited.append((row, step))
            if (row, step) in obstacles:
                distance = step-col-1
                visited.pop()
                break
            distance = step-col

    return distance, visited


def teleport_guard(guard_pos: tuple, distance: int, facing: str) -> tuple:
    row, col = guard_pos

    if facing == "^":
        row -= distance
    elif facing == "v":
        row += distance
    elif facing == "<":
        col -= distance
    elif facing == ">":
        col += distance

    return (row, col)


def is_leaving_grid(guard_pos: tuple, facing: str, max_row, max_col) -> bool:
    row, col = guard_pos

    if facing == "^" and row == 0:
        return True
    if facing == "<" and col == 0:
        return True
    if facing == "v" and row == max_row:
        return True
    if facing == ">" and col == max_col:
        return True

    return False


def turn_guard(facing: str) -> str:
    turning_rules = {
        "^": ">",
        ">": "v",
        "v": "<",
        "<": "^"
    }
    return turning_rules[facing]


# calculate result

start, dir, obstacles, max_row, max_col = evaluate_starting_grid(imported_data)
current_pos = start
facing = dir
visited = list()

# first move

dist_1, visited = count_distance_to_obstacle(current_pos, facing, obstacles, max_row, max_col)
current_pos = teleport_guard(current_pos, dist_1, facing)
print("After first move guard at position:", current_pos)

# all further moves

while not is_leaving_grid(current_pos, facing, max_row, max_col):
    facing = turn_guard(facing)
    distance, newly_visited = count_distance_to_obstacle(current_pos, facing, obstacles, max_row, max_col)
    current_pos = teleport_guard(current_pos, distance, facing)
    visited += [pos for pos in newly_visited if pos not in visited]

print("Guard left grid at pos:", current_pos)
print(f"Guard visited --- {len(visited)} --- distinct positions on grid.")
