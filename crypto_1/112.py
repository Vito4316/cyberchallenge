from pwn import *
from binascii import hexlify, unhexlify

r = remote("predictable.challs.cyberchallenge.it", 9034)

print(r.recvuntil(b"> ",drop=True))

r.sendline(b"1")

print(r.recvuntil(b"Insert your username: "))

r.sendline(b"ciaon")

cookie = r.recvline()[18:-1]

print(r.recvuntil(b"> ",drop=True))

r.sendline(b"2")

original = b"login_token:ciao"
target =   b"login_token:admi"
iv = unhexlify(cookie[:32])

iv = bytes([ a ^ b ^ c for a, b, c in zip(iv, original, target)])

iv = hexlify(iv)

cookie = iv + cookie[32:]

print(r.recvuntil(b"Please give me your login token "))

r.sendline(cookie)

print(r.recvline())

print(r.recvuntil(b"What command do you want to execute? "))

r.sendline(hexlify(b"get_flag"))

cookie = r.recvline()[20:-1]

print(cookie)

print(r.recvuntil(b"> ",drop=True))

r.sendline(b"3")

print(r.recvuntil(b"What do you want to do? "))

r.sendline(cookie)

print(r.recvline())

r.close()