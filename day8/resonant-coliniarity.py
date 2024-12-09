from collections import defaultdict
from pathlib import Path


def group_antennas(mat):
    res = defaultdict(set)

    for i in range(len(mat)):
        for j in range(len(mat[0])):
            freq = mat[i][j]
            if mat[i][j] != ".":
                res[freq].add((i, j))

    return res


def in_range(x, y, num_rows, num_columns):
    return 0 <= x < num_rows and 0 <= y < num_columns


def find_anodes(mat, groupped, with_expansion=False):
    anodes = set()
    num_rows, num_columns = len(mat), len(mat[0])
    for freq, positions in groupped.items():
        for current_x, current_y in positions:
            for x, y in positions:
                if current_x == x and current_y == y:
                    continue
                diff_x, diff_y = current_x - x, current_y - y
                anode_x, anode_y = x - diff_x, y - diff_y
                if not with_expansion:
                    if in_range(anode_x, anode_y, num_rows, num_columns):
                        anodes.add((anode_x, anode_y))
                else:
                    anodes.add((x, y))
                    while in_range(anode_x, anode_y, num_rows, num_columns):
                        anodes.add((anode_x, anode_y))
                        anode_x -= diff_x
                        anode_y -= diff_y
    return anodes


def main():
    input_path = Path("resonant-coliniarity-input.txt")
    input_data = input_path.read_text().strip()
    mat = input_data.split("\n")
    groupped = group_antennas(mat)
    print(
        len(find_anodes(mat, groupped)),
        len(find_anodes(mat, groupped, with_expansion=True)),
    )


if __name__ == "__main__":
    main()
