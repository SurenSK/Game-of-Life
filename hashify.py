import hashlib
import math
import sys

# 8SUbSJCGCNDr should be FTEoBjeEveZpBJzk6YL3PzLDpwEt9yWTzzjVNEwvaov

# 62 Valid Chars, append with 'z' just to make it simply 6 bits per
# 0-10 digits, 11-36 lowers, 37-62 uppers, 63:0
hash_vals_LUT = ['0', '1', '2', '3', '4', '5', '6', '7',
                 '8', '9', 'A', 'B', 'C', 'D', 'E', 'F',
                 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N',
                 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V',
                 'W', 'X', 'Y', 'Z', 'a', 'b', 'c', 'd',
                 'e', 'f', 'g', 'h', 'i', 'j', 'k', 'l',
                 'm', 'n', 'o', 'p', 'q', 'r', 's', 't',
                 'u', 'v', 'w', 'x', 'y', 'z', 'z', 'y']
out_c_bits = int(math.log(hash_vals_LUT.__len__(), 2))


def hashing_func(_inp_str):
    input_str_hex = (hashlib.sha256(_inp_str.encode('UTF-8')).hexdigest())
    input_str_bin = (bin(int(input_str_hex, 16))[2:])
    padded_bin = str.zfill(input_str_bin, math.ceil(len(input_str_bin) / out_c_bits) * out_c_bits)

    output_string = ""
    for i in range(0, len(padded_bin), out_c_bits):
        bin_6 = (padded_bin[i + 0] + padded_bin[i + 1] + padded_bin[i + 2] +
                 padded_bin[i + 3] + padded_bin[i + 4] + padded_bin[i + 5])
        int_6 = int(bin_6, 2)
        output_string += (hash_vals_LUT[int_6])
    return output_string


if len(sys.argv) == 2:
    print("1 arg passed; entered string to be hashed:", sys.argv[1])
    inp_str = sys.argv[1]
elif len(sys.argv) == 1:
    print("No args passed; enter string to be hashed: ", end='')
    user_inp = input()
    inp_str = user_inp
    if user_inp == "":
        print("No value given; hashing default '8SUbSJCGCNDr'")
        inp_str = "8SUbSJCGCNDr"
else:
    print(len(sys.argv)-1, "args passed; entered string to be hashed:", sys.argv[1])
    inp_str = sys.argv[1]

assert inp_str != ""

print("\nHashing String:", inp_str)
assert hashing_func("8SUbSJCGCNDr") == "FTEoBjeEveZpBJzk6YL3PzLDpwEt9yWTzzjVNEwvaov"
print("Hashed  String:", hashing_func(inp_str))
