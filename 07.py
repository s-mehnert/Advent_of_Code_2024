from itertools import product

# import puzzle input

imported_data = list()

with open("07_input.txt") as input:
    for line in input.readlines():
        imported_data.append([int(num.strip(":")) for num in line.strip("\n").split()])

for line in imported_data:
    print("Result:", line[0], "--> numbers:", line[1:])


# helper functions


def equation_is_possible(equation: list) -> bool:
    test_value = equation[0]
    numbers = equation[1:]

    possible_operator_combinations = list(product(["+", "*", "||"], repeat=len(numbers)-1))

    for combo in possible_operator_combinations:
        nums = numbers[:]
        temp_result = 0

        while nums:
            temp_result = nums.pop(0)
            for i in range(len(combo)):
                if combo[i] == "+":
                    temp_result += nums.pop(0)                 
                elif combo[i] == "*":
                    temp_result *= nums.pop(0)
                elif combo[i] == "||":
                    temp_result = int(str(temp_result) + str(nums.pop(0)))

        if temp_result == test_value:
            return True

    return False


# calculate result

result_1 = 0

for line in imported_data:
    to_be_added = line[0]
    if equation_is_possible(line):
        result_1 += to_be_added


print("Total calibration result:", result_1)
