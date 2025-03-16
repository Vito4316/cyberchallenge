import json
from pwn import *
from binascii import unhexlify

def req_flag(r):
    reqflag = json.dumps({"option": "get_flag"})
    r.sendline(reqflag.encode())
    enc = (r.recvline().strip())
    enc = json.loads(enc)
    return enc['encrypted_flag']

def req_enc(r, s):
    reqenc = json.dumps({"option": "encrypt_data", "input_data": s})
    r.sendline(reqenc.encode())
    enc = (r.recvline().strip())
    enc = json.loads(enc)
    return enc['encrypted_data']

line = "00000000000000000000000000000000000000000000000000000000"


r = remote("socket.cryptohack.org", 13372) 

r.recvline()



flag = unhexlify(req_flag(r))
enc = unhexlify(req_enc(r, line))
line = unhexlify(line)

flag = "".join([ chr(a ^ b ^ c) for a, b, c in zip(flag, enc, line)])

print(flag)

