from binascii import hexlify, unhexlify

#lol!
def lol(b, n):
    for i in range(n):
        x = (b << 1) & 0xfe
        y = (b & 0x80) >> 7
        b = x | y
    return bytes([b])  # Correctly convert single int to bytes

c = unhexlify('2a1aac0233b1c267105a6e0271b85c20a1d02945dbb96074af9cac4363b1b25fbadc2de63b7d967d05908a7501119e4e9315049472598a4e2a082bf4aa49404fab9304349265a054a748241250')

p = b''

for i in range(len(c)):
    p += lol(c[i], i+1)

print(p.decode(errors="ignore"))