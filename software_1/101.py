
#integers found in function print_safe_contents
arr = [0xabb6bcbc, 0x9d9b9884, 0xa0cf8ba0, 0xa0cc978b, 0x9cca9a8d, 0xff829a8a]

#interpret longs as bytes in little endian
arr = [num.to_bytes(4, byteorder='little') for num in arr]

# flatten nested list into single list
arr = [ char for b_arr in arr for char in b_arr]

# Apply transformation seen in print_safe_contents
chrs = [chr((~i) & 0xFF) for i in arr]
result = ''.join(chrs)
print(result)
