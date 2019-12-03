import re

class ValDict:
    def __getitem__(self, value):
        return value
val = ValDict()
reg = {i:0 for i in range(4)}

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

def get_nums(line):
    return [int(x) for x in re.findall(r"\d+", line)]

def chunk(seq, size):
    for i in range(0, len(seq), size):
        yield seq[i:i+size]

def eval(before, opcode, a, b, c):
    for i, val in enumerate(before):
        reg[i] = val
    reg[c] = opcodes[opcode](a,b)
    return [reg[i] for i in range(4)]

def iter_matches(before, args, after):
    code, a, b, c = args
    for opcode in opcodes.keys():
        if eval(before, opcode, a, b, c) == after:
            yield opcode


count = 0
opcode_possibilities = {}
with open("input1") as file:
    for lines in chunk(list(file), 4):
        before, args, after, _ = [get_nums(line) for line in lines]
        cands = list(iter_matches(before, args, after))
        #print(before, args, after, cands)
        if len(cands) >= 3:
            count += 1

        code = args[0]
        if code not in opcode_possibilities:
            opcode_possibilities[code] = set(cands)
        else:
            opcode_possibilities[code] &= set(cands)
#part 1
print(count)

derived_opcodes = {}
while opcode_possibilities:
    to_remove = [k for k,v in opcode_possibilities.items() if len(v) == 1]
    if not to_remove: break
    for key in to_remove:
        value = list(opcode_possibilities[key])[0]
        derived_opcodes[key] = value
        for v in opcode_possibilities.values():
            if value in v: v.remove(value)
        del opcode_possibilities[key]

reg = {i:0 for i in range(4)}
with open("input2") as file:
    for line in file:
        if not line.strip(): continue
        code, a, b, c = get_nums(line)
        opcode = derived_opcodes[code]
        reg[c] = opcodes[opcode](a,b)
print(reg[0])