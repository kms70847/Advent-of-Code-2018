with open("input") as file:
    data = [int(line) for line in file]

#part 1
print(sum(data))

#part 2
seen = {0}
x = 0
while True:
    for item in data:
        x += item
        if x in seen:
            print(x)
            exit(0)
        seen.add(x)