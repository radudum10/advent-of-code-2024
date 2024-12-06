from copy import deepcopy
from pathlib import Path


def count_guard_steps(guard_map, start_x, start_y):
    dir_row, dir_col = -1, 0
    i, j = start_x, start_y

    while (i >= 0 and i < len(guard_map)) and (j >= 0 and j < len(guard_map[0])):
        if guard_map[i][j] == "#":
            if dir_row != 0:
                i += -dir_row
                dir_col = -dir_row
                dir_row = 0
            elif dir_col != 0:
                j += -dir_col
                dir_row = dir_col
                dir_col = 0
        else:
            guard_map[i][j] = "X"

        i += dir_row
        j += dir_col

    x_counter = 0
    for i in range(len(guard_map)):
        for j in range(len(guard_map[i])):
            if guard_map[i][j] == "X":
                x_counter += 1

    return x_counter


def check_map_loop(guard_map, start_x, start_y):
    dir_row, dir_col = -1, 0
    i, j = start_x, start_y
    visited = set()
    while (i >= 0 and i < len(guard_map)) and (j >= 0 and j < len(guard_map[0])):
        pos_with_dir = (i, j, dir_row, dir_col)
        if pos_with_dir in visited:
            return True
        if guard_map[i][j] == "#":
            if dir_row != 0:
                i += -dir_row
                dir_col = -dir_row
                dir_row = 0
            elif dir_col != 0:
                j += -dir_col
                dir_row = dir_col
                dir_col = 0
        else:
            visited.add(pos_with_dir)

        i += dir_row
        j += dir_col

    return False


def count_obstacles(guard_map, start_x, start_y):
    good_obstacles_count = 0
    for i in range(len(guard_map)):
        for j in range(len(guard_map)):
            if guard_map[i][j] == ".":
                alternative_guard_map = deepcopy(guard_map)
                alternative_guard_map[i][j] = "#"
                good_obstacles_count += bool(
                    check_map_loop(alternative_guard_map, start_x, start_y)
                )

    return good_obstacles_count


def main():
    input_path = Path("guard-map-input.txt")
    input_map = input_path.read_text().strip()
    guard_map = [list(r) for r in input_map.split("\n")]

    start_x, start_y = None, None

    for i in range(len(guard_map)):
        for j in range(len(guard_map[i])):
            if guard_map[i][j] == "^":
                start_x, start_y = i, j
                break

    print(count_guard_steps(deepcopy(guard_map), start_x, start_y))
    print(count_obstacles(guard_map, start_x, start_y))


if __name__ == "__main__":
    main()
