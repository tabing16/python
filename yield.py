def onetoten():
    value = 1
    while value <= 10:
        yield value
        value += 1

for i in onetoten():
    print(i)