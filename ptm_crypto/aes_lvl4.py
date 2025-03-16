from pwn import *
import base64 as b64
from binascii import hexlify

#{"param1":"flag??", "userdata":" first two blocks, 32 bytes
#                                       <- our input blocks (aligned to 16)
#b'", "param2":"random_parameter"}' <- last two blocks

#we want to send two blocks as a message, then modify them through bit flipping
#first block will be gibberish, second one will contain b'", "admin" : "true"             '

def encrypt(r, m):
    print(r.recvuntil("> ".encode()))
    r.sendline("1".encode())
    print(r.recvuntil("> ".encode()))
    r.sendline(b64.b64encode(m.encode()))
    print(r.recvuntil("Your encrypted cookie is: b'".encode()))
    c = r.recvline().strip()
    print(f"received: {b64.b64decode(c)}")
    return b64.b64decode(c)

def login(r, cookie):
    print(r.recvuntil("> ".encode()))
    r.sendline("2".encode())
    print(r.recvuntil("> ".encode()))
    r.sendline(cookie)
    
    for _ in range(2):
        print(r.recvline())

r = remote("130.192.5.212", 1754)

bitflip = "00000000000000000000000000000000"

target = b'", "admin":"true'

enc = encrypt(r, bitflip)

bf = enc[:32]
b1 = enc[32:48]
b2 = enc[48:64]
bl = enc[64:]

# naming Ti the output of AES_dec(k, Ci)
# Ti = Pi ^ Ci-1
# then if Si-1 = Ci-1 ^ P^i ^ Target and we copy Si-1 into Ci-1
# the resulting block would be Target only, as all other variables would be eliminated

bn = bytes([a ^ b ^ c for a, b, c in zip(b1, bitflip[:16].encode(), target)])

enc = bf + bn + b2 + bl

login(r, b64.b64encode(enc))
