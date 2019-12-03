a=0;b=0;c=0;d=0

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
        if 256 <= d:
            c = 0
            while True:
                b = c + 1
                b = b * 256
                if b > d:
                    break
                else:
                    c = c + 1
            d = c
        else:
            break
    if e == a: break
    print(e)
#9566170: correct