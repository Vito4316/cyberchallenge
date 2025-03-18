from pwn import *
from binascii import hexlify, unhexlify


def is_padded_correctly(r, m):
    r.recvuntil(b"What do you want to decrypt (in hex)? ", drop=False)
    r.sendline(hexlify(m))
    resp = r.recvline()

    if b"Wow you are so strong at decrypting!" in resp:
        print(resp)    
        return True
    return False


def get_block(r, cipher):
    # cipher must be 32 bytes long
    block_size = 16

    if len(cipher) != 2 * block_size:
        raise ValueError("cipher must be exactly 32 bytes long (2 blocks of 16 bytes)")

    c0 = bytearray(cipher[:block_size])
    c1 = cipher[block_size:]
    recovered = bytearray(block_size)
    for i in range(block_size - 1, -1, -1):
        pad_val = block_size - i
        found = False

        for guess in range(256):
            c0_modified = bytearray(c0)

            for j in range(i + 1, block_size):
                c0_modified[j] = c0[j] ^ recovered[j] ^ pad_val

            c0_modified[i] = c0[i] ^ guess ^ pad_val

            test_cipher = bytes(c0_modified) + c1

            if is_padded_correctly(r, test_cipher):
                if pad_val == 1:    
                    test_cipher1 = bytearray(test_cipher)
                    test_cipher1[i-1] = (test_cipher1[i-1] + 1) % 256
                    if not is_padded_correctly(r, test_cipher1):
                        continue

                recovered[i] = guess

                print(f"test message {c0_modified} + guess {guess} + {c0_modified[i]}")
                print(f"flag {recovered.decode(errors="ignore")}")
                found = True
                break

        if not found:
            print("ERROR: No valid guess found for byte index", i)
            exit(-1)

    return bytes(recovered)

r = remote("padding.challs.cyberchallenge.it", 9033)
r.recvline()

flag_enc = unhexlify(r.recvline().strip())

flag = get_block(r, flag_enc[0:32]) + get_block(r, flag_enc[16:48]) + get_block(r, flag_enc[32:64])
