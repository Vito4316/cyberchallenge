from pwn import *
import base64

def send_enc(conn, s):
    print(f'Sending {s}')
    conn.sendline(base64.b64encode(s))
    enc = (conn.recvline().strip())
    enc = base64.b64decode(enc[22:-1])
    print(f'Received {enc}')
    print(conn.recvline())
    return enc

r = remote("130.192.5.212", 1755) 

print(r.recvline())
print(r.recvline())

enc = send_enc(r, b'0' * 32)

enc1 = enc[0:16]
enc2 = enc[16:32]

zero_xor_a = [ (a ^ b) for a, b in zip(enc1, enc2) ]

flag = "".join([ chr(a ^ b) for a, b in zip(zero_xor_a, b'0' * 16) ] )

print( flag)