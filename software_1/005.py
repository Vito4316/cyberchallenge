from pwn import *
import Crypto.Util.number
from binascii import hexlify, unhexlify

def get_vals(r):
    s = r.recvline().decode()
    if "Good job!" in s:
        print(s)
        exit(0)
    if "line" in s:
        return "empty", 0, " ", 0
    s = s.strip().split(" ")
    return "number", int(s[5]), str(s[9]).split("-")[0], int(s[11][1:])

r = remote("piecewise.challs.cyberchallenge.it", 9110)

flag = b''

while True:
    t, n, e, b = get_vals(r)

    if t == "empty":
        r.sendline()
    elif t == "number":
        r.send(n.to_bytes(b, e))

    print(r.recvline())