from collections import defaultdict
from pathlib import Path


def find_plant_group(garden, start_pos, num_rows, num_cols):
    stack = [start_pos]
    plant = garden[start_pos[0]][start_pos[1]]
    visited, sides = set(), set()
    while stack:
        i, j = stack.pop()

        if (i, j) in visited:
            continue

        visited.add((i, j))

        for di, dj in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            ni, nj = i + di, j + dj

            if (
                not (0 <= ni < num_rows)
                or not (0 <= nj < num_cols)
                or garden[ni][nj] != plant
            ):
                sides.add(((ni, nj), (di, dj)))
                continue

            if (ni, nj) not in visited:
                stack.append((ni, nj))

    return visited, sides


def is_consecutive(p1, p2):
    if p1[0] == p2[0] and abs(p1[1] - p2[1]) == 1:
        return True
    if p1[1] == p2[1] and abs(p1[0] - p2[0]) == 1:
        return True

    return False


def points_graph(points):
    graph = defaultdict(list)
    for cp in points:
        for op in points:
            if cp == op:
                continue
            if is_consecutive(cp, op):
                graph[cp].append(op)

    for k in points - graph.keys():
        graph[k] = []
    return graph


def get_cc(graph):
    visited = set()
    components = []

    def dfs(node, component):
        stack = [node]
        while stack:
            pnt = stack.pop()
            if pnt in visited:
                continue
            visited.add(pnt)
            component.append(pnt)
            for nei in graph[pnt]:
                if nei not in visited:
                    stack.append(nei)

    for node in graph:
        if node not in visited:
            component = []
            dfs(node, component)
            components.append(component)

    return components


def calculate_cost(garden, num_rows, num_cols, with_bulk_discount=False):
    visited = set()
    cost = 0
    for i in range(num_rows):
        for j in range(num_cols):
            if (i, j) in visited:
                continue

            new_visited, sides = find_plant_group(garden, (i, j), num_rows, num_cols)
            visited |= new_visited
            if with_bulk_discount:
                grouped_sides = defaultdict(list)
                for side in sides:
                    grouped_sides[side[1]].append(side[0])

                n_sides = 0
                for side_group in grouped_sides.values():
                    graph = points_graph(side_group)
                    cc = get_cc(graph)
                    n_sides += len(cc)
                cost += len(new_visited) * n_sides
            else:
                cost += len(new_visited) * len(sides)
    return cost


def main():
    input_path = Path("garden-groups-input.txt")
    data = input_path.read_text().strip()
    garden = data.split("\n")
    num_rows, num_cols = len(garden), len(garden[0])
    print(calculate_cost(garden, num_rows, num_cols))
    print(calculate_cost(garden, num_rows, num_cols, with_bulk_discount=True))


if __name__ == "__main__":
    main()
