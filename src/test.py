

def mapper(x):
    return x * 2


listy = [1, 2, 3, 4, 5, 6, 7, 8, 9]

listy = list(map(mapper, listy))

print(listy)