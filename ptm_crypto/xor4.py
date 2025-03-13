import os
from binascii import hexlify


def xor(a,b):
    return bytes([a[i]^b[i%len(b)] for i in range(len(a))])

out1 = b'R\xfb\xa2\x19\x8d4\x94 \x90xS\xf3\x1e\x9b\x8e\xa4\nKC\x9e\xe4\xf4\x98\xa0'
out2 = b'k\xfc\xef\x16\x8a/\xb8i\x90ci\xb9\x19\x8d\x9b\x97LFD\x8c\xe0\xb8\xde\xe2'

print(hexlify(out1))
print(hexlify(out2))


#then throw the two hexlify to any mtp cracker. 