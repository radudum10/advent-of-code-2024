from pathlib import Path
import re


def sum_mul_with_regex(input_pth: Path) -> int:
    input_data = input_pth.read_text()
    pattern = r"mul\(\d+,\d+\)"
    matches = re.findall(pattern, input_data)
    res = 0
    for match in matches:
        clean_match = list(map(int, match[len('mul('):-1].split(",")))
        res += clean_match[0] * clean_match[1]
    
    return res

def should_do(do_idxs: list, dont_idxs: list, match_idx: int) -> bool:
    nearest_do_idx = 0

    filtered_do_idxs = list(filter(lambda i: i <= match_idx, do_idxs))
    filtered_dont_idxs = list(filter(lambda i: i <= match_idx, dont_idxs))

    nearest_do_statement_idx = filtered_do_idxs[-1] if filtered_do_idxs else None
    nearest_dont_statement_idx = filtered_dont_idxs[-1] if filtered_dont_idxs else None
    
    if nearest_dont_statement_idx is None:
        return True

    if nearest_do_statement_idx is None:
        return False
    
    return nearest_do_statement_idx > nearest_dont_statement_idx


def sum_mul_with_do_and_dont(input_pth: Path) -> int:
    input_data = input_pth.read_text()
    do_pattern = r"do\(\)"
    dont_pattern = r"don't\(\)"
    do_idxs = [m.end() for m in re.finditer(do_pattern, input_data)]
    dont_idxs = [m.end() for m in re.finditer(dont_pattern, input_data)]
    mul_pattern = r"mul\(\d+,\d+\)"
    res = 0
    for match in re.finditer(mul_pattern, input_data):
        if should_do(do_idxs, dont_idxs, match.start()):
            clean_match = list(map(int, match.group()[len('mul('):-1].split(",")))
            res += clean_match[0] * clean_match[1]

    return res


def main():
    input_pth = Path('mul-it-over-input.txt')
    print(sum_mul_with_regex(input_pth))
    print(sum_mul_with_do_and_dont(input_pth))


if __name__ == '__main__':
    main()

