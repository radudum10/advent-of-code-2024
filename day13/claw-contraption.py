from math import isclose
from pathlib import Path
import re

ERR = 10000000000000
TOL = 1e-3


def extract_digits(input_str):
    return list(map(int, re.findall(r"\d+", input_str)))


def solver(a, b, p, with_err=False):
    if not with_err:
        coef_a = (p[0] * b[1] - p[1] * b[0]) / (a[0] * b[1] - b[0] * a[1])
        coef_b = p[0] / b[0] - coef_a * a[0] / b[0]
    else:
        num = a[0] * b[1] - a[1] * b[0]
        coef_a = (
            (p[0] * b[1] - b[0] * p[1]) / num + (ERR / num) * b[1] - (ERR / num) * b[0]
        )
        coef_b = (ERR / b[0]) + ((p[0] - coef_a * a[0]) / b[0])

    if abs(coef_a - round(coef_a)) < TOL and abs(coef_b - round(coef_b)) < TOL:
        return coef_a * 3 + coef_b

    return 0


def main():
    input_path = Path("claw-contraption-input.txt")
    input_data = input_path.read_text().strip()

    cost_p1, cost_p2 = 0, 0
    for block in input_data.split("\n\n"):
        a, b, p = block.split("\n")
        a_coords, b_coords, prize = (
            extract_digits(a),
            extract_digits(b),
            extract_digits(p),
        )
        cost_p1 += solver(a_coords, b_coords, prize)
        cost_p2 += solver(a_coords, b_coords, prize, with_err=True)
    print(cost_p1)
    print(cost_p2)


if __name__ == "__main__":
    main()
