# import puzzle input

imported_data = list()

with open("06_input.txt") as input:
    for line in input.readlines():
        imported_data.append([pos for pos in line.strip("\n")])


# helper functions


def print_grid(grid):
    for line in grid:
        for pos in line:
            print(pos, end="")
        print()


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
    obstacles_faced = list()

    if facing == "^":
        for step in range(row, -1, -1):
            if (step, col) not in visited:
                visited.append((step, col))
            if (step, col) in obstacles:
                obstacles_faced.append((step, col))
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

    return distance, visited, obstacles_faced


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


# --- Part 2 ---

# Add obstacle in all visited positions calculated before
# Do this be appending (and then again removing) the position to the obstacles' list
# one after the other except for the guards starting position
# After adding an obstacle check if guard walks now in a loop
# Do this by recording the obstacles the guard encounters on their tour
# Once he is at the same obstacle for a second time, he is stuck


def walks_in_loop(grid) -> bool:
    current_pos, facing, obstacles, max_row, max_col = evaluate_starting_grid(grid)
    obstacles_faced = list()
    is_loop = False

    dist_1, visited, obstacles_faced = count_distance_to_obstacle(current_pos, facing, obstacles, max_row, max_col)
    current_pos = teleport_guard(current_pos, dist_1, facing)

    while not is_leaving_grid(current_pos, facing, max_row, max_col):
        break_out_of_loop = False
        facing = turn_guard(facing)
        distance, newly_visited, newly_faced_obstacles = count_distance_to_obstacle(current_pos, facing, obstacles, max_row, max_col)


        for obstacle in newly_faced_obstacles:
            if obstacle in obstacles_faced:
                break_out_of_loop = True
                break

        if break_out_of_loop:
            is_loop = True
            break

        current_pos = teleport_guard(current_pos, distance, facing)
        visited += [pos for pos in newly_visited if pos not in visited]
        obstacles_faced += newly_faced_obstacles

    return is_loop


def toggle_obstacle_or_not_in_grid(grid, toggle_position):
    row, col = toggle_position

    if grid[row][col] == "#":
        grid[row][col] = "."
    elif grid[row][col] == ".":
        grid[row][col] = "#"

    return grid


# calculate result

print()
print_grid(imported_data)

start, dir, obstacles, max_row, max_col = evaluate_starting_grid(imported_data)
current_pos = start
facing = dir
visited = list()
obstacles_faced = list()

# first move

dist_1, visited, obstacles_faced = count_distance_to_obstacle(current_pos, facing, obstacles, max_row, max_col)
current_pos = teleport_guard(current_pos, dist_1, facing)
print("\nAfter first move guard at position:", current_pos)

# all further moves

while not is_leaving_grid(current_pos, facing, max_row, max_col):
    facing = turn_guard(facing)
    distance, newly_visited, newly_faced_obstacles = count_distance_to_obstacle(current_pos, facing, obstacles, max_row, max_col)
    current_pos = teleport_guard(current_pos, distance, facing)
    visited += [pos for pos in newly_visited if pos not in visited]
    obstacles_faced += newly_faced_obstacles

print("Guard left grid at pos:", current_pos)
print(f"Guard visited --- {len(visited)} --- distinct positions on grid.")

helper_grid = [[(i, j) for j in range(len(imported_data[0]))] for i in range(len(imported_data))]

temp_grid = imported_data[:]
obstacle_positions_for_loop = list()

# wrong solution with real data: 1750 - takes extremely long to compute
for pos in visited:
    if pos != start:
        grid_to_test = toggle_obstacle_or_not_in_grid(temp_grid[:], pos)

        if walks_in_loop(grid_to_test):
            obstacle_positions_for_loop.append(pos)

        temp_grid = toggle_obstacle_or_not_in_grid(grid_to_test, pos)

print()
print("Number of possible locations for creating a loop:", len(obstacle_positions_for_loop))