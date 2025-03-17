from pwn import *
from binascii import hexlify, unhexlify
from Crypto.Util.Padding import pad, unpad


def get_cookie(r, m):
    print(r.recvuntil("> ".encode()))
    r.sendline("1".encode())
    print(r.recvuntil("Insert your username:".encode(), drop=True))
    r.sendline(m)
    print(r.recvuntil("Your login token: ".encode()))
    c = r.recvline().strip().decode()
    print(f"received: {c}")
    return c

def login(r, cookie):
    print(r.recvuntil("> ".encode()))
    r.sendline("2".encode())
    print(r.recvuntil("Insert your token: ".encode()))
    print(f"sending {cookie}")
    r.sendline(cookie)
    
    for _ in range(2):
        print(r.recvline())


username = b'0' * 12
target   = b'00000;is_admin=1'
original = b'usr=000000000000'

r = remote("notadmin.challs.cyberchallenge.it", 9032)

enc = bytes.fromhex(get_cookie(r, username))

iv  = enc[:16]
B_1 = enc[16:32]
B_L = enc[32:]

iv_modified = bytes([ a ^ b ^ c for a, b, c in zip(iv, original, target) ])

new_cookie = iv_modified + B_1 + B_L

print(f"sending: {hexlify(new_cookie)}")

login(r, hexlify(new_cookie))

