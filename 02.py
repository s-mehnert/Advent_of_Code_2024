# import puzzle input
imported_data = list()

with open("02_input.txt") as input:
    for line in input.readlines():
        imported_data.append(line.strip("\n").split(" "))


# format data

reports_list = list()
for report in imported_data:
    reports_list.append([int(level) for level in report])


# calculate result


def is_ascending(report):
    if report[0] < report[1]:
        return True
    return False


def is_descending(report):
    if report[0] > report[1]:
        return True
    return False


def is_safe(report):
    if is_ascending(report):
        for i in range(len(report)-1):
            if report[i] >= report[i+1] or abs(report[i] - report[i+1]) > 3:
                return False
        return True
    if is_descending(report):
        for i in range(len(report)-1):
            if report[i] <= report[i+1] or abs(report[i] - report[i+1]) > 3:
                return False
        return True
    return False


def is_safe_2(report, removed_single_bad_level=False):
    if is_ascending(report):
        for i in range(len(report)-1):
            if report[i] >= report[i+1] or abs(report[i] - report[i+1]) > 3:
                if removed_single_bad_level:
                    return False
                removed_single_bad_level = True
                reports_one_bad_removed = [report[:i] + report[i+1:] for i in range(len(report))]
                for rep in reports_one_bad_removed:
                    if is_safe_2(rep, True):
                        return True
                return False
        return True
    if is_descending(report):
        for i in range(len(report)-1):
            if report[i] <= report[i+1] or abs(report[i] - report[i+1]) > 3:
                if removed_single_bad_level:
                    return False
                removed_single_bad_level = True
                reports_one_bad_removed = [report[:i] + report[i+1:] for i in range(len(report))]
                for rep in reports_one_bad_removed:
                    if is_safe_2(rep, True):
                        return True
                return False
        return True
    if removed_single_bad_level:
        return False
    removed_single_bad_level = True
    reports_one_bad_removed = [report[:i] + report[i+1:] for i in range(len(report))]
    for rep in reports_one_bad_removed:
        if is_safe_2(rep, True):
            return True
    return False


result_1 = 0
for report in reports_list:
    if is_safe(report):
        result_1 += 1

result_2 = 0
for report in reports_list:
    if is_safe_2(report):
        result_2 += 1


print("Result 1:", result_1)
print("Result 2:", result_2)
