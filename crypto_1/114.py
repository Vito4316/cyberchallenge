from binascii import hexlify, unhexlify

#request to encrypt empty string
cipher = unhexlify(b'efcdc86c7ddb86d7fbc40112c2763ff69fd1b05659eadd96cb9f517f9c3b5397')
#request to encrypt b'0' * len(cipher)
cipher1 = unhexlify(b'ac8e813806a9b5a288f7654dac465195ac8e813806a9b5a288f7654dac465195efcdc86c7ddb86d7fbc40112c2763ff69fd1b05659eadd96cb9f517f9c3b5397')

print("".join([ chr(x ^ y) for x, y in zip(cipher, cipher1)]))
