from collections import defaultdict
from pathlib import Path
import re


def groups(data, func):
    grouping = defaultdict(list)

    for y in range(len(data)):
        for x in range(len(data[y])):
            grouping[func(x, y)].append(data[y][x])

    char_groups = list(map(grouping.get, sorted(grouping)))

    return list(map(lambda l: "".join(l), char_groups))


def check_3x3_for_mas(mat_3x3: list) -> bool:
    fdiag = "".join(mat_3x3[i][i] for i in range(3))
    bdiag = "".join(mat_3x3[i][2 - i] for i in range(3))

    return fdiag in ("MAS", "SAM") and bdiag in ("MAS", "SAM")


def sliding_window(rows: list) -> int:
    mat = [list(row) for row in rows]
    window_size = 3

    x_mas_counter = 0
    for i in range(len(mat[0]) - 2):
        for j in range(len(mat) - 2):
            window_data = [
                [mat[i + wi][j + wj] for wj in range(window_size)]
                for wi in range(window_size)
            ]
            x_mas_counter += check_3x3_for_mas(window_data)

    return x_mas_counter


def xmas_on_row_col_diags(rows: list) -> int:
    cols = groups(rows, lambda x, y: x)
    rows = groups(rows, lambda x, y: y)
    fdiag = groups(rows, lambda x, y: x + y)
    bdiag = groups(rows, lambda x, y: x - y)

    xmas_counter = 0
    xmas_pattern = r"XMAS"
    for word in [*cols, *rows, *fdiag, *bdiag]:
        matches = re.findall(xmas_pattern, word)
        reverse_matches = re.findall(xmas_pattern, word[::-1])
        xmas_counter += len(matches) + len(reverse_matches)

    return xmas_counter


def main():
    input_path = Path("ceres-search-input.txt")
    text = input_path.read_text().strip()
    rows = text.split("\n")

    print(xmas_on_row_col_diags(rows))
    print(sliding_window(rows))


if __name__ == "__main__":
    main()
