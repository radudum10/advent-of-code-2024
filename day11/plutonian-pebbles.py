from typing import List, Tuple

from copy import deepcopy
from functools import cache
from itertools import chain
from pathlib import Path


@cache
def _blink(n: int) -> Tuple:
    if n == 0:
        return (1,)

    n_str = str(n)
    if len(n_str) % 2 == 0:
        half = len(n_str) // 2
        n1 = int(n_str[:half])
        n2 = int(n_str[half:])
        return (n1, n2)

    return (n * 2024,)


@cache
def _split_stone_once(num_tuple: Tuple) -> Tuple:
    return tuple(chain.from_iterable(map(_blink, num_tuple)))


@cache
def _split_stone(n: Tuple, n_blinks: int) -> int:
    if n_blinks == 0:
        return 1

    num_res = _split_stone_once(n)
    return sum(_split_stone((n,), n_blinks - 1) for n in num_res)


def split_all_stones(nums: List[int], n_blinks: int) -> int:
    res = 0
    for num in nums:
        res += _split_stone((num,), n_blinks)
    return res


def main():
    input_path = Path("plutonian-pebbles-input.txt").read_text().strip()
    nums = list(map(int, input_path.split(" ")))
    print(split_all_stones(nums, 25))
    print(split_all_stones(nums, 75))


if __name__ == "__main__":
    main()
