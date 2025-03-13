import base64
from binascii import hexlify

#I just requested a few encs from the server, print them as hex then do mtp on them

enc1 = "gMt+HRmVD5uDnDefOYzUjfO7eg0="
enc2 = "+JJA5Jze7SiYlbiAlUDiFOM2Y5s="
enc3 = "jCGkXzGjJ1jJJ9U+n6pFBqQ9rrg="
enc4 = "hVISsbPTU2jd6rOD4SdGQdeEP78="
enc5 = "OjusZAqJ4diDsUkDnio5hhhLz/w="

dec1 = base64.b64decode(enc1)
dec2 = base64.b64decode(enc2)
dec3 = base64.b64decode(enc3)
dec4 = base64.b64decode(enc4)
dec5 = base64.b64decode(enc5)

print(hexlify(dec1))
print(hexlify(dec2))
print(hexlify(dec3))
print(hexlify(dec4))
print(hexlify(dec5))

''' 

80cb7e1d19950f9b839c379f398cd48df3bb7a0d
f89240e49cdeed289895b8809540e214e336639b
8c21a45f31a32758c927d53e9faa4506a43daeb8
855212b1b3d35368ddeab383e1274641d7843fbf
3a3bac640a89e1d883b149039e2a3986184bcffc

'''