from collections import Counter
from pathlib import Path
import heapq


def read_lists(input_path: Path) -> (list, list):
    data = input_path.read_text().strip().split("\n")
    mapped_data = map(lambda x: list(map(int, x.split(" " * 3))), data)
    lst1, lst2 = map(list, zip(*mapped_data))

    return lst1, lst2


def list_distance(l1: list, l2: list) -> int:
    heapq.heapify(l1)
    heapq.heapify(l2)
    
    distance = 0
    for _ in range(len(l1)):
        min_lhs, min_rhs = heapq.heappop(l1), heapq.heappop(l2)
        distance += abs(min_lhs - min_rhs)
    
    return distance


def list_similarity(l1: list, l2: list) -> int:
    counter = Counter(l2)

    similarity = 0
    for elem in l1:
        similarity += elem * counter[elem]

    return similarity


def main():
    l1, l2 = read_lists(Path("list_distance_input.txt"))
    print(list_distance(l1, l2))
    
    l1, l2 = read_lists(Path("list_similarity_input.txt"))
    print(list_similarity(l1, l2))


if __name__ == "__main__":
    main()

