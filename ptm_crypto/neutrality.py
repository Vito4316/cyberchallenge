from binascii import hexlify, unhexlify
from Crypto.Util.number import bytes_to_long, long_to_bytes

f = open("neutrality_file", "r")

l = []

for line in f.readlines():
    l += [hexlify(long_to_bytes(int(line)))]

for line in l:
    print(line.decode())