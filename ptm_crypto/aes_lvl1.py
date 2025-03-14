from pwn import *
from string import printable
from binascii import hexlify, unhexlify

BLOCK = 16

def send_enc(conn, s):
    print(f'Sending {s}')
    conn.sendline( b'0' * 12 + s)
    enc = conn.recvline().strip()
    print(f'Received {enc}')
    return enc[64:]

conn = remote("130.192.5.212", 1750)

print(conn.recvline())
# n of chars to uncover
n = 48

flag = b''

for i in range(n):
    s = b'00' * (n - i)
    enc = send_enc(conn, s)

    for c in range(256):
        plain = s + flag + hex(c)[2:].encode()
        enc_test = send_enc(conn, plain)
        if enc_test[: n * 2] == enc[: n * 2]:
            print(f"New flag char found: {c}, flag={hex(c)[2:].encode() + flag}")
            flag += hex(c)[2:].encode()
            break

print(unhexlify(flag))

