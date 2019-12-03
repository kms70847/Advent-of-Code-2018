import re

class ValDict:
    def __getitem__(self, value):
        return value
val = ValDict()
reg = {i:0 for i in range(5)}

opcodes = {
    "addr": lambda a, b: reg[a] + reg[b],
    "addi": lambda a, b: reg[a] + val[b],
    "mulr": lambda a, b: reg[a] * reg[b],
    "muli": lambda a, b: reg[a] * val[b],
    "banr": lambda a, b: reg[a] & reg[b],
    "bani": lambda a, b: reg[a] & val[b],
    "borr": lambda a, b: reg[a] | reg[b],
    "bori": lambda a, b: reg[a] | val[b],
    "setr": lambda a, b: reg[a],
    "seti": lambda a, b: val[a],
    "gtir": lambda a, b: 1 if val[a] > reg[b] else 0,
    "gtri": lambda a, b: 1 if reg[a] > val[b] else 0,
    "gtrr": lambda a, b: 1 if reg[a] > reg[b] else 0,
    "eqir": lambda a, b: 1 if val[a] == reg[b] else 0,
    "eqri": lambda a, b: 1 if reg[a] == val[b] else 0,
    "eqrr": lambda a, b: 1 if reg[a] == reg[b] else 0
}

def try_int(x):
    try:
        return int(x)
    except:
        return x

def get_nums(line):
    return [int(x) for x in re.findall(r"\d+", line)]

def chunk(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i:i+size]

with open("input") as file:
    directive = file.readline()
    ip_reg = int(re.match(r"#ip (\d)", directive).group(1))
    program = []
    for line in file:
        program.append(list(map(try_int, line.split())))

reg = {i:0 for i in range(5)}
while 0 <= reg[ip_reg] < len(program):
    name, a, b, c = program[reg[ip_reg]]
    reg[c] = opcodes[name](a,b)
    reg[ip_reg] += 1
print(reg[0])

#part 2:
"""
Disassembling the code by hand, it is apparent that the program is equivalent to "find the sum of the factors of B", where B is 911 for part 1, and 10551311 for part 2.

911 is prime, so its factors are 1 and 911, so the output of part 1 is 912.
The prime factors of 10551311 are [431, 24481], so the sum of its factors is...
"""
print(1+431+24481+10551311)