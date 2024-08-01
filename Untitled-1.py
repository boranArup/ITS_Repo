def chartoidx(c):
    c = c.upper()
    if len(c) == 1:
        num = ord(c)
        if  num > 64:
            return num - 65
    return int(c)

x = ""
while x != "x":
    x = input("num or letter: ")
    print(chartoidx(x))