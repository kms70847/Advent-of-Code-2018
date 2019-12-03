x = 10551311
i = 2
factors = []
while i <= x:
    while x%i == 0:
        factors.append(i)
        x /= i
    i += 1
print(factors)