from pwn import *

context.arch = 'amd64'

r = remote("130.192.5.212", 17384)

ex1 = b'\x48\x89\xf8\x48\x01\xf0\x48\x01\xd0\xc3'

ex2 = """
cmp     rsi, rdx
mov     rax, rdi
cmovb   rsi, rdx
cmp     rsi, rdi
cmovnb  rax, rsi
ret
"""

ex2 = asm(ex2)


ex3 = """
mov     rax, rdi
and     edi, 3
je      .L3
cmp     edi, 1
je      .L9
lea     rdx, [rax-2]
add     rax, 1
cmp     edi, 2
cmove   rax, rdx
.L3:
ret
.L9:
sub     rax, 1
ret

"""

ex3 = asm(ex3)

ex4 = """
movzx   eax, BYTE PTR [rdi]
xor     edx, edx
test    al, al
je      .L10
.L13:
cmp     sil, al
sete    al
add     rdi, 1
movzx   eax, al
add     rdx, rax
movzx   eax, BYTE PTR [rdi]
test    al, al
jne     .L13
.L10:
mov     rax, rdx
ret
"""

ex4 = asm(ex4)

ex5 = """
cmp     BYTE PTR [rsi], 0
je      .L13
lea     rax, [rsi+1]
xor     r8d, r8d
.L3:
add     rax, 1
mov     ecx, r8d
add     r8d, 1
cmp     BYTE PTR [rax-1], 0
jne     .L3
cmp     BYTE PTR [rdi], 0
je      .L14
xor     eax, eax
.L4:
mov     rdx, rax
add     rax, 1
cmp     BYTE PTR [rdi+rax], 0
jne     .L4
xor     eax, eax
cmp     ecx, edx
jg      .L1
mov     r10d, edx
xor     r9d, r9d
sub     r10d, ecx
add     ecx, 1
movsx   rcx, ecx
.L5:
xor     eax, eax
jmp     .L8
.L12:
mov     rax, rdx
.L8:
movzx   edx, BYTE PTR [rsi+rax]
cmp     BYTE PTR [rdi+rax], dl
jne     .L7
lea     rdx, [rax+1]
cmp     rcx, rdx
jne     .L12
add     eax, 1
.L7:
cmp     r8d, eax
je      .L13
add     r9d, 1
add     rdi, 1
cmp     r9d, r10d
jle     .L5
.L14:
xor     eax, eax
.L1:
ret
.L13:
mov     eax, 1
ret

"""

ex5 = asm(ex5)

################

for _ in range(8):
    print(r.recvline())

r.sendline(ex1)

for _ in range(3):
    print(r.recvline())

r.sendline(ex2)

for _ in range(3):
    print(r.recvline())

r.sendline(ex3)

for _ in range(3):
    print(r.recvline())

r.sendline(ex4)

for _ in range(3):
    print(r.recvline())

r.sendline(ex5)


print(r.recvline())
print(r.recvline())
