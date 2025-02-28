from pwn import *;
from string import printable;
from binascii import hexlify;

BLOCK = 16

def pad(s):
  return s + (BLOCK - len(s) % BLOCK) * chr(BLOCK - len(s) % BLOCK)

def send_enc(conn, s):
    conn.recvuntil("encrypt:")
    conn.sendline(s)
    txt = conn.recvline()
    enc = txt.decode()[39:]
    return enc

conn = remote("padding.challs.cyberchallenge.it", 9030)

s = ""
dec = ""

s += "a"
enc = send_enc(conn, s)


for x1 in range(16):
    enc_test = send_enc(conn, pad("}"))
    print(enc)
    print(enc[-33:])
    print(enc_test)
    print(enc_test[:32])
    if enc_test[:32] == enc[-33:]:
        print(f"New flag char found")



for _ in range(16):
    s += "a"
    enc = send_enc(conn, s)

    for c in printable:
        print(f"trying {c} ...")
        enc_test = send_enc(conn, pad(c))
        print(enc)
        print(enc[-33:])
        print(enc_test)
        print(enc_test[:32])
        if enc_test[:32] == enc[-33:]:
            print(f"New flag char found: {c}")
            break
