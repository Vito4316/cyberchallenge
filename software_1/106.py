'''

Morph executes code that is contained inside a memory address at 0x100c78, which I will call ptr

This memory address contains chunks of 17 bytes that represent the initial part of an executable code, which will contain a cmp (to check if one char of flag is correct) and a jump to exit the program or to continue.

this information is extracted from FUN_001008d0, which will disassemble into a function which will address ptr + i * 17

let's call functions[i] = ptr[i * 17 : (i+1) * 17]

all elements functions, regardless of order of execution, will xor the next function with their index multiplied by 17

then, xored_function[i] = functions[i] ^ (i * 17)

the byte code then has always the same form, exception made for the fifth byte, which will contain a different value to compare (the correspondent byte of the flag)

for example:

00100c78 56              PUSH       param_2
00100c79 52              PUSH       param_3
00100c7a 8a 07           MOV        AL,byte ptr [string]
00100c7c 3c 43 <--       CMP        AL,0x43
00100c7e 0f 85 db        JNZ        LAB_00100f5f
         02 00 00
00100c84 e9 b8 02        JMP        LAB_00100f41
         00 00

which means that xored_function[i][5] will always contain the char to compare, the following code processes the memory area and then extracts the corresponding bytes 

N.B. function FUN_00100987 will swap entries, but this will have no effect on the program execution. 

'''

from binascii import hexlify

functions_number = 0x56528a073c430f85db020000e9b802000047439b162d521e94db131111f8b61311117470a8251e6b2da79b202222cbb42022226561b9340f673cb69b313333dab63133331216ce43783f4bc1d3464444ad304644440307df52693c5ad0d3575555bc365755553034ec615a1269e3136466668f346466662125fd704b0d78f2137577779e36757777deda028fb4d7870ddb8a888861b88a8888cfcb139ea5f4961cdb9b999970869b9999fcf820ad969aa52f9ba8aaaa43a4a8aaaaede931bc87c9b43e9bb9bbbb5246babbbb9a9e46cbf0bcc349c3cecccc2520cdcccc8b8f57dae1b5d25823dcdddd3406dcddddb8bc64e9d2b1e16b03efeeee0724efeeeea9ad75f8c3ccf07a23feffff1646feffff46429a172c241f95db111010f9b81110107773ab261d622ea49b202121c8b62021216460b8350e013db79b333232dbb43332321511c9447f624cc6db424343aa364243430206de5368755bd1d3555454bd305554543337ef6259446ae0136465658c366465652024fc714a0b79f3137776769f3477767690909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090909090585f41b8000000004983f811741c8a1f88c130cb881f49ffc048ffc7ebeab83c000000bf010000000f05c300

functions_bytes = functions_number.to_bytes((functions_number.bit_length() + 7) // 8, byteorder='big')

flag = "".join(chr(functions_bytes[17 * i + 5] ^ (17 * i & 0xff)) for i in range(24))

print(flag)
