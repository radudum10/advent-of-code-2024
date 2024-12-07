from copy import deepcopy
from collections import deque
from pathlib import Path


def concat_numbers(n1, n2):
    return int(str(n1) + str(n2))


def eval_ops(numbers, target, current, with_concat=False):
    if not numbers:
        return target == current

    if current > target:
        return False

    return (
        eval_ops(numbers[1:], target, current + numbers[0], with_concat)
        or eval_ops(numbers[1:], target, current * numbers[0], with_concat)
        or (
            with_concat
            and eval_ops(
                numbers[1:], target, concat_numbers(current, numbers[0]), with_concat
            )
        )
    )


def main():
    input_path = Path("bridge-repair-input.txt")
    input_data = input_path.read_text().strip()

    equations = {}

    res_p1, res_p2 = 0, 0
    for eq in input_data.split("\n"):
        target, numbers = eq.split(": ")
        target = int(target)
        numbers = list(map(int, numbers.split(" ")))

        if eval_ops(numbers[1:], target, numbers[0]):
            res_p1 += target
        if eval_ops(numbers[1:], target, numbers[0], with_concat=True):
            res_p2 += target

    print(res_p1)
    print(res_p2)


if __name__ == "__main__":
    main()
