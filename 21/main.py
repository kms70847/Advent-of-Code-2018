def is_round(x):
    return x < 10 or x%10 == 0 and is_round(x//10)

a=0;b=0;c=0;d=0

seen = set()
prev_e = None

e = 0
while True:
    d = e | 65536
    e = 4332021
    while True:
        c = d & 255
        e = e + c
        e = e & 16777215
        e = e * 65899
        e = e & 16777215
        if d >= 256:
            d = d // 256
        else:
            break
    if not seen: print(e) #part 1
    if e in seen: print(prev_e); break #part 2
    seen.add(e)
    prev_e = e
    
#9566170: correct