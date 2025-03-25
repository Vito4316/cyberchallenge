from pwn import *

def foo(r):
    print(r.recvuntil(b'Step'))
    step = r.recvline()
    nums = r.recvline()
    print(nums)
    nums = nums.strip()[1:-1].split(b',')
    nums = list(map(int, nums))
    print(r.recvuntil(b'Somma?'))
    r.sendline(str(sum(nums)))
    if b'10' in step:
        print(r.recvline())


r = remote("software-17.challs.olicyber.it", 13000)

r.recvuntil("... Invia un qualsiasi carattere per iniziare ...".encode())
r.sendline(b'0')


for _ in range(10):
    foo(r)