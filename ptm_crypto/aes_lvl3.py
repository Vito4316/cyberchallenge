from pwn import *
import base64 as b64

def send_encrypt_request(conn, message):
    conn.recvuntil(b"3. Exit\n")
    conn.sendline(b"1")
    conn.recvuntil(b"Give me a message encoded in base64:\n")
    encoded_message = b64.b64encode(message)
    conn.sendline(encoded_message)
    response = conn.recvline()
    
    ciphertext_start = response.find(b"b'") + 2
    ciphertext_end = response.rfind(b"'")
    raw_ciphertext = response[ciphertext_start:ciphertext_end].decode('unicode_escape').encode('latin1')
    
    return raw_ciphertext

def send_flag_request(conn, ciphertext):
    conn.recvuntil(b"3. Exit\n")
    conn.sendline(b"2")
    conn.recvuntil(b"Give me the right ciphertext encoded in base64:\n")
    encoded_ciphertext = b64.b64encode(ciphertext)
    conn.sendline(encoded_ciphertext)
    response = conn.recvline()
    
    plaintext_response = conn.recvline()
    
    return response.strip(), plaintext_response.strip()


# we need to obtain dec(k, C) ^ adm_IV = "Gimme damn flag" = P
# we can craft M = P ^ IV_adm ^ IV
# 
# then, when enc with personal IV, 
# C1 = enc(k, P ^ IV_adm ^ IV ^ IV) <- last IV is because of CBC encryption
#
# then, dec(k, C1) = 
# AES_dec(k, C1) ^ IV_adm = 
# P ^ IV_adm ^ IV ^ IV ^ IV_adm = P

adm_iv = b64.b64encode('admin'.encode())[:16]
adm_iv = adm_iv+b'='*(16-len(adm_iv))
my_iv = b64.b64encode("Admin".encode())[:16]
my_iv = my_iv+b'='*(16-len(my_iv))

conn = remote("130.192.5.212", 1756)

conn.recvuntil(b"Who are you?\n")
conn.sendline("Admin".encode())

message = "Gimme damn flag".encode()

message = bytes([ a ^ b ^ c  for a, b, c in zip(message, adm_iv, my_iv)])

ciphertext = send_encrypt_request(conn, message)
print(f"[+] Encrypted message: {ciphertext.hex()}")

response, plaintext = send_flag_request(conn, ciphertext)
print(f"[+] Response: {response.decode()}")

