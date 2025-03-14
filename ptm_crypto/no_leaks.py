from pwn import *
import base64
from string import printable

def get_cipher(r):
    while True:
        r.sendline(b'{"msg": "request"}')  # Make sure it's bytes
        cipher = r.recvline()
        print(cipher)
        
        if b'"error"' in cipher:
            continue
            
        cipher = cipher[16:-3]
        print(cipher)
        return base64.b64decode(cipher)

r = connect("socket.cryptohack.org", 13370)
r.recvline()
cipher_number = 2000
ciphers = []
for i in range(cipher_number):
    ciphers.append(get_cipher(r))

print(ciphers)

printable_bytes = [ord(i) for i in printable[:-8]]  

for i in range(20):
    p = set()
    for j in range(cipher_number):
        c = ciphers[j][i]
        p.add(c)
    
    possible = set(printable_bytes) - p
    
    readable_chars = [chr(b) for b in possible]
    readable_string = ''.join(readable_chars)
    
    print(f"Candidates for position {i}: {readable_string}")
    
    # If you want to debug and see what values are in p:
    #p_values = sorted(p)
    #print(f"Values in ciphertexts at position {i}: {p_values}")