# import puzzle input
imported_data = list()

with open("01_input.txt") as input:
    for line in input.readlines():
        imported_data.append(line.strip("\n").split("  "))

# format data

left_list = sorted([int(lst[0]) for lst in imported_data])
right_list = sorted([int(lst[1]) for lst in imported_data])

# calculate result


def sum_differences(ll, rl):
    diff = 0
    for i in range(len(ll)):
        diff += (abs(ll[i]-rl[i]))
    return diff


def sum_similarities(ll, rl):
    similarity_code = 0
    for num in ll:
        similarity_code += (num * rl.count(num))
    return similarity_code


result_1 = sum_differences(left_list, right_list)
result_2 = sum_similarities(left_list, right_list)

print("Result 1:", result_1)
print("Result 2:", result_2)
