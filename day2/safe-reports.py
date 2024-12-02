from pathlib import Path


def is_diff_ok(x: int, y: int) -> bool:
    return 1 <= abs(x - y) <= 3


def is_safe_array(arr: list) -> bool:
    prev = arr[0]
    is_ascending = arr[0] < arr[1]
    for i, next_elem in enumerate(arr[1:], 1):
        if (
            not is_diff_ok(prev, next_elem)
            or (is_ascending and prev > next_elem)
            or (not is_ascending and prev < next_elem)
        ):
            return False

        prev = next_elem

    return True


def safe_arrays(input_path: Path, with_damper: bool = False) -> int:
    safe_arrays_counter = 0
    for line in input_path.read_text().strip().split("\n"):
        arr = list(map(int, line.split()))
        is_safe = is_safe_array(arr)
        if not with_damper:
            safe_arrays_counter += bool(is_safe)
        else:
            for i in range(len(arr)):
                is_safe = is_safe_array(arr[:i] + arr[(i + 1) :])
                if is_safe:
                    safe_arrays_counter += 1
                    break

    return safe_arrays_counter


def main():
    input_path = Path("safe-reports-input.txt")
    print(safe_arrays(input_path))
    print(safe_arrays(input_path, True))


if __name__ == "__main__":
    main()
