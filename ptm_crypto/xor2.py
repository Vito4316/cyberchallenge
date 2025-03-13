import random

def xor(a, b):
    return bytes([a[i]^b[i%len(b)] for i in range(len(a))])

def gen_stream(key, a, b):
    while True:
        key = (key*a+b)%256
        yield chr(key).encode()

# Original ciphertext
out = b'\xb2\xc6=7\xb3\xf6\xa7\xd0\xab\xf7 \xa2\xf6\xaf\xf1\x9c\xec\xac\xe6\x9c\xfd\xb0\xcb\xb0\xe0\xaa\xf8\xaf\xcb\xa1\xf5\xa7\xe9'

#in a few minutes this will return at least one correct string
for key in range(256):
    for a in range(256):
        for b in range(256):
            g = gen_stream(key, a, b)
            keystream = b""
            for _ in range(33):
                keystream += next(g)
            
            plain = xor(out, keystream)
            
            if all(32 < c < 127 for c in plain):
                print(f"Key: {key}, a: {a}, b: {b}")
                print(f"Flag: {plain.decode('ascii')}")