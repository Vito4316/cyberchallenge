from string import printable

def condition(c):
    return ord(c) & 0b10 > 0

key_chars = list(filter(condition, printable[:-8]))

print(key_chars)
