with open("input") as file:
    target = int(file.read())

seq = [3,7]
a = 0
b = 1
while(len(seq) < target+10):
    x = seq[a] + seq[b]
    if x < 10:
        seq.append(x)
    else:
        seq.extend([x//10, x%10])
    a = (a + seq[a] + 1) % len(seq)
    b = (b + seq[b] + 1) % len(seq)

print("".join(str(x) for x in seq[target:target+10]))


#part 2
seq = [3,7]
a = 0
b = 1
target = [int(x) for x in str(target)]
w = len(target)
while not(seq[-w:] == target or seq[-w-1:-1] == target):
    x = seq[a] + seq[b]
    if x < 10:
        seq.append(x)
    else:
        seq.extend([x//10, x%10])
    a = (a + seq[a] + 1) % len(seq)
    b = (b + seq[b] + 1) % len(seq)

print(len(seq) - w - (0 if seq[-w:] == target else 1))