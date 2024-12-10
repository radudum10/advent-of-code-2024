from collections import deque
from copy import deepcopy
from itertools import groupby
from operator import itemgetter
from pathlib import Path


def parse_disk_map(disk_map_raw):
    id_number = 0
    disk_map = []
    for i, elem in enumerate(map(int, disk_map_raw)):
        if i % 2 == 0:
            disk_map += [id_number] * elem
            id_number += 1
        else:
            disk_map += ["."] * elem

    return disk_map


def get_free_positions(disk_map):
    free_positions = deque([i for i, x in enumerate(disk_map) if x == "."])

    spans = []
    for k, g in groupby(enumerate(free_positions), lambda x: x[0] - x[1]):
        spans.append(list(map(itemgetter(1), g)))

    return free_positions, spans


def compress_disk_map(disk_map, free_positions):
    disk_map_copy = [elem for elem in disk_map]
    len_disk_map_copy = len(disk_map_copy)
    for i, elem in enumerate(disk_map_copy[::-1]):
        if not free_positions:
            break
        if elem != ".":
            free_pos = free_positions.popleft()
            if (len_disk_map_copy - i - 1) < free_pos:
                break

            disk_map_copy[free_pos] = elem
            disk_map_copy[len_disk_map_copy - i - 1] = "."

    return disk_map_copy


def checksum(disk_map_compressed):
    checksum = 0
    for i, elem in enumerate(disk_map_compressed):
        if isinstance(elem, int):
            checksum += i * elem

    return checksum


def move_blocks(disk_map, spans):
    for_moving = []
    for k, g in groupby(enumerate(disk_map), lambda x: x[1]):
        if k == ".":
            continue
        for_moving.append(list(g))

    for group in reversed(for_moving):
        group_size = len(group)

        good_span, good_span_idx = None, 0
        for span in spans:
            if not span:
                good_span_idx += 1
                continue

            if span[-1] < group[-1][0] and group_size <= len(span):
                good_span = span
                break

            good_span_idx += 1

        if not good_span:
            continue

        elem = group[0][1]
        move_start = good_span[0]
        move_end = move_start + group_size

        disk_map[move_start:move_end] = [elem] * group_size

        block_start = group[0][0]
        block_end = block_start + group_size
        disk_map[block_start:block_end] = ["."] * group_size

        spans[good_span_idx] = good_span[group_size:]

    return disk_map


def main():
    input_path = Path("disk-fragmenter-input.txt")
    disk_map_raw = input_path.read_text().strip("\n")
    disk_map = parse_disk_map(disk_map_raw)
    free_positions, spans = get_free_positions(disk_map)
    compressed_disk_map = compress_disk_map(disk_map, deepcopy(free_positions))
    print(checksum(compressed_disk_map))

    compressed_disk_map = move_blocks(disk_map, spans)
    print(checksum(compressed_disk_map))


if __name__ == "__main__":
    main()
