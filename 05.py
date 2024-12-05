# import puzzle input

rules = list()
updates = list()

with open("05_input.txt") as input:
    rules, updates = input.read().split("\n\n")
    rules = rules.split("\n")
    updates = updates.split("\n")


# format data

formatted_rules = [[int(num) for num in rule.split("|")] for rule in rules]
formatted_updates = [[int(num) for num in update.split(",")] for update in updates]


# helper functions


def has_correct_order(update: list, rules: list) -> bool:

    for i in range(len(update)):
        for rule in rules:
            if update[i] in rule:
                first, last = rule
                if update[i] == last:
                    if first in update[i+1:]:
                        return False

    return True


def calculate_sum_of_middle_page_nums(correct_updates: list) -> int:
    sum_mps = 0

    for update in correct_updates:
        middle_page = update[len(update)//2]
        sum_mps += middle_page

    return sum_mps


# --- Part 2 ---


def swap_places(update, idx1, idx2):
    update[idx1], update[idx2] = update[idx2], update[idx1]
    return update


def reorder_update(update: list, rules: list) -> list:

    for i in range(len(update)):
        for rule in rules:
            if update[i] in rule:
                first, last = rule
                if update[i] == last:
                    if first in update[i+1:]:
                        swapped = swap_places(update, i, update.index(first))
                        return swapped


# calculate result

correct_updates = list()
for update in formatted_updates:
    if has_correct_order(update, formatted_rules):
        correct_updates.append(update)

result_1 = calculate_sum_of_middle_page_nums(correct_updates)

print("Sum of correct updates' middle pages:", result_1)

wrong_updates = [update for update in formatted_updates if update not in correct_updates]

for update in wrong_updates:
    while not has_correct_order(update, formatted_rules):
        reorder_update(update, formatted_rules)

result_2 = calculate_sum_of_middle_page_nums(wrong_updates)

print("Sum of reordered updates' middle pages:", result_2)
