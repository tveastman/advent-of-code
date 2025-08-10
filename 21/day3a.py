from rich import print, inspect

print("START")

# read
with open("day3a-input.txt") as f:
    input = f.read().strip().split("\n")
print(f"{input=}")

# transpose
transposed = [list() for i in range(len(input[0]))]
for number in input:
    for d, digit in enumerate(number):
        transposed[d].append(int(digit))
print("transposed:", transposed)


# count
def count(digits):
    # return (gamma_bit, epsilon_bit)
    print(sum(digits))
    if sum(digits) > (len(digits) // 2):
        return 1, 0
    else:
        return 0, 1


gamma, epsilon = "", ""
for column in transposed:
    gb, eb = count(column)
    gamma += str(gb)
    epsilon += str(eb)
print(gamma, epsilon)
gamma, epsilon = int(gamma, base=2), int(epsilon, base=2)
print(f"{gamma * epsilon = }")


print("END")
