# import puzzle input
imported_data = list()

with open("03_input.txt") as input:
    imported_data = input.read()
    # for line in input.readlines():
    #     imported_data.append(line.strip("\n").split(" "))


# format data

def extract_mul_1(input):
    extraction = list()
    start = 0
    end = 0
    for i in range(len(input)):
        if input[i] == "m":
            start = i
        if input[i] == ")" and start != 0:
            end = i
            extraction.append((start, end+1))
            start = 0
            end = 0
    return [input[ext[0]:ext[1]] for ext in extraction]


def extract_mul_2(input):
    extraction = list()
    start = 0
    end = 0
    is_enabled = True
    start_enable = 0
    end_enable = 0    
    for i in range(len(input)):
        if input[i] == "d":
            start_enable = i
        if input[i] == ")" and start_enable != 0:
            end_enable = i+1
            if input[start_enable: end_enable] == "do()":
                is_enabled = True
            elif input[start_enable: end_enable] == "don't()":
                is_enabled = False
        if input[i] == "m" and is_enabled:
            start = i
        if input[i] == ")" and start != 0:
            end = i
            extraction.append((start, end+1))
            start = 0
            end = 0
    return [input[ext[0]:ext[1]] for ext in extraction]


extracted_muls_1 = extract_mul_1(imported_data)
extracted_muls_2 = extract_mul_2(imported_data)

# calculate result


def calc(mul):
    nums = []
    if mul[:4] == "mul(":
        rest = mul[4:-1]
        if "," not in rest:
            nums = ["0", "0"]
        else:
            nums = rest.split(",")
    if len(nums) != 2:
        nums = ["0", "0"]
    num1, num2 = nums
    try:
        num1 = int(num1)
    except:
        num1 = 0
    try:
        num2 = int(num2)
    except:
        num2 = 0
    return num1 * num2


result_1 = 0
result_2 = 0

for mul in extracted_muls_1:
    result_1 += calc(mul)


for mul in extracted_muls_2:
    result_2 += calc(mul)

print("Result 1:", result_1)
print("Result 2:", result_2)
