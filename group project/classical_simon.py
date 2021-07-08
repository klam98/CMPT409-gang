import random
import time


def black_box(b1, b2):
    """Black box function.

    In this case we will be using the mod 2 of dot product to stay aligned with the quantum implementation.
    """
    dot = 0
    for i in range(len(b1)):
        bit1 = int(b1[i]) - int('0')
        bit2 = int(b2[i]) - int('0')
        dot += bit1 * bit2
    dot_mod = dot  % 2
    print("%s (dot) %s = %d (mod 2)" % (b1, b2, dot_mod))
    return dot_mod


# bitsting to test
print("Setting bitstring as 110...")
b = '110'
n = len(b)

# generate 2^(n-1) + 1 unique inputs to test
print("Generating inputs...")
inputs = []
for i in range(2 ** (n-1) + 1):
    while True:
        bitstring = ("{0:0%db}"%n).format(random.getrandbits(n))
        if bitstring not in inputs:
            inputs.append(bitstring)
            break

# test each input to see if the black box is one-to-one or two-to-one
print("Running Test...")
start = time.time()
one_to_one = True
outputs = []
for bitstring in inputs:
    out = black_box(b, bitstring)
    if out in outputs:
        one_to_one = False
        break
    outputs.append(out)
end = time.time()
print("DONE.\n")

if one_to_one:
    print("The black box function is one-to-one.")
else:
    print("The black box function is two-to-one.")

print("Time taken: %fs" % (end - start))
