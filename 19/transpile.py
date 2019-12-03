def try_int(x):
    try:
        return int(x)
    except:
        return x

def name(x):
    return "abcdef"[x]

def iden(x):
    return x

opcodes = {
    "addr": lambda a, b: f"{name(a)} + {name(b)}",
    "addi": lambda a, b: f"{name(a)} + {iden(b)}",
    "mulr": lambda a, b: f"{name(a)} * {name(b)}",
    "muli": lambda a, b: f"{name(a)} * {iden(b)}",
    "banr": lambda a, b: f"{name(a)} & {name(b)}",
    "bani": lambda a, b: f"{name(a)} & {iden(b)}",
    "borr": lambda a, b: f"{name(a)} | {name(b)}",
    "bori": lambda a, b: f"{name(a)} | {iden(b)}",
    "setr": lambda a, b: f"{name(a)}",
    "seti": lambda a, b: f"{iden(a)}",
    "gtir": lambda a, b: f"1 if {iden(a)} > {nsmr(b)} else 0",
    "gtri": lambda a, b: f"1 if {name(a)} > {iden(b)} else 0",
    "gtrr": lambda a, b: f"1 if {name(a)} > {name(b)} else 0",
    "eqir": lambda a, b: f"1 if {iden(a)} == {name(b)} else 0",
    "eqri": lambda a, b: f"1 if {name(a)} == {iden(b)} else 0",
    "eqrr": lambda a, b: f"1 if {name(a)} == {name(b)} else 0"
}

program = []
with open("input") as file:
    for line in file:
        if line.startswith("#"):
            continue
        program.append(list(map(try_int, line.split())))
for i, line in enumerate(program):
    op, a, b, c = line
    print(f"{i}: {name(c)} = {opcodes[op](a, b)}")