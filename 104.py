from pwn import *;
from string import printable;
from binascii import hexlify;

BLOCK = 16

def pad(s):
  return s + (BLOCK - len(s) % BLOCK) * chr(BLOCK - len(s) % BLOCK)

def send_enc(conn, s):
    print(conn.recvuntil("encrypt:"))
    conn.sendline(s)
    txt = conn.recvline().strip()
    print(txt.decode())
    enc = txt.decode()[39:]
    return enc

conn = remote("padding.challs.cyberchallenge.it", 9030)

s = ""
flag = ""

for i in range(16):
    s = "a" * (15 - i)
    enc = send_enc(conn, (s + flag).encode())

    for c in printable:
        plain = s + flag + c
        print(f"trying {plain} ...")
        enc_test = send_enc(conn, plain.encode())
        print(enc)
        print(enc_test)
        if enc_test[:32] == enc[:32]:
            print(f"New flag char found: {c}, flag={c + flag}")
            flag = c + flag
            break