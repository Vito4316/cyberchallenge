from binascii import hexlify, unhexlify
from Crypto.Util.number import bytes_to_long, long_to_bytes

f = open("neutrality_file", "r")

ciphers = []

for line in f.readlines():
    ciphers += [long_to_bytes(int(line))]

occ = [ [0] * 256 for _ in range(len(ciphers[0]))]

for i in range(len(ciphers[0])):
    for b in ciphers[i]:
        occ[i][b]+=1
    
    print("------------------------")
    print(f"column {i}")
    print("------------------------")
    for o, idx in zip(occ[i], range(256)):
        if o > 1:
            print(f"byte {hexlify(long_to_bytes(idx))}, found {o} times")

start = b'SEETF{'

for c in ciphers:
    c1 = c[:6]

    key = [ a ^ b for a, b in zip(start, c1)]

    ones = 0
    zeros = 0

    for byte in key:
        binary = bin(byte)[2:].zfill(8)
        ones += binary.count('1')
        zeros += binary.count('0')

    print(f"diff {abs(ones-zeros)}")

