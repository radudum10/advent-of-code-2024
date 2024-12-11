from pathlib import Path


def count_trails(mat, start_pos, n_rows, n_cols, unique=True):
    stack = [(start_pos, int(mat[start_pos[0]][start_pos[1]]))]
    reached_peaks_counter = 0
    visited = set()
    while stack:
        pos, value = stack.pop()
        if pos in visited:
            continue
        
        if unique:
            visited.add(pos)
        if value == 9:
            reached_peaks_counter += 1
            continue
        
        for (di, dj) in [(0, -1), (0, 1), (1, 0), (-1, 0)]:
            ni, nj = pos[0] + di, pos[1] + dj
            if not (0 <= ni < n_rows) or not (0 <= nj < n_cols):
                continue

            if mat[ni][nj] == value + 1:
                stack.append(((ni, nj), value + 1))

    return reached_peaks_counter



def main():
    input_path = Path('trailheads-input.txt')
    raw_data = input_path.read_text().strip()

    mat = [list(map(int, l)) for l in raw_data.split('\n')]

    n_rows, n_cols = len(mat), len(mat[0])
    p1_sum, p2_sum = 0, 0
    for i in range(n_rows):
        for j in range(n_cols):
            if mat[i][j] == 0:
                p1_sum += count_trails(mat, (i, j), n_rows, n_cols)
                p2_sum += count_trails(mat, (i, j), n_rows, n_cols, False)
    
    print(p1_sum)
    print(p2_sum)
if __name__ == '__main__':
    main()

