from pwn import *
import base64
from string import printable

def get_cipher(r):
    r.sendline("{\"msg\": \"request\"}")
    cipher = r.recvline()
    cipher = cipher[16:-2]
    return cipher

r = connect("socket.cryptohack.org", 13370)

r.recvline()

cipher_number = 100
ciphers = []

for i in range(cipher_number):
    ciphers.append(get_cipher(r))
    
ciphers = [ base64.b64decode(i) for i in ciphers ]

printable_bytes = [ord(i) for i in printable[:-8]]  # Just the integer values


for i in range(20):
    p = set()
    for j in range(cipher_number):
        c = ciphers[j][i]
        p.add(c)
    
    possible = set(printable_bytes) - p
    
    readable_chars = [chr(b) for b in p]
    
    readable_string = ''.join(readable_chars)
    
    print(f"Candidates for position {i}: {readable_string}")
    

