from collections import defaultdict, deque
from pathlib import Path


def get_print_conditions(graph, start_node, update_nodes):
    visited = set()
    stack = [start_node]

    while stack:
        node = stack.pop()

        if node not in visited:
            visited.add(node)

            for neighbor in reversed(graph.get(node)):
                if neighbor not in visited and neighbor in update_nodes:
                    stack.append(neighbor)

    visited.remove(start_node)
    return visited


def check_ok_update(graph, update):
    update_set = set(update)
    already_printed = set()
    is_valid = True
    for num in update:
        needed_printed_numbers = get_print_conditions(graph, num, update_set)
        if not needed_printed_numbers.issubset(already_printed):
            return False
        already_printed.add(num)

    return True


def get_dependencies(graph, start_node, update_nodes):
    visited = set()
    result = []
    stack = [(start_node, False)]

    while stack:
        node, visited_flag = stack.pop()

        if visited_flag:
            result.append(node)
        elif node not in visited:
            visited.add(node)
            stack.append((node, True))

            for neighbor in reversed(graph.get(node)):
                if neighbor not in visited and neighbor in update_nodes:
                    stack.append((neighbor, False))

    return result


def part1(graph, updates):
    middle_sum = 0
    for update in updates:
        if check_ok_update(graph, update):
            middle_sum += update[len(update) // 2]

    return middle_sum


def part2(graph, updates):
    middle_sum = 0
    for update in updates:
        if not check_ok_update(graph, update):
            correct_order = []
            update_set = set(update)
            update_len = len(update)
            for num in update:
                precondition = get_dependencies(graph, num, update_set)
                correct_order += [i for i in precondition if i not in correct_order]
                if len(correct_order) == update_len:
                    break
            middle_sum += correct_order[len(update) // 2]

    return middle_sum


def main():
    input_path = Path("print-queue-input.txt")
    input_data = input_path.read_text().strip()

    rules_raw, updates_raw = input_data.split("\n\n")
    updates = [list(map(int, update.split(","))) for update in updates_raw.split("\n")]

    graph = defaultdict(list)

    for rule in rules_raw.split("\n"):
        node_dest, node_src = map(int, rule.split("|"))
        graph[node_src].append(node_dest)

    print(part1(graph, updates))
    print(part2(graph, updates))


if __name__ == "__main__":
    main()
