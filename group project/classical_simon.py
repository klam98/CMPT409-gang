import random
from black_box import BlackBox

# bitsting to test
b = '110'
print("Setting bitstring as %s..." % b)
n = len(b)

# generate 2^(n-1) + 1 unique inputs to test
print("Generating inputs...\n")
inputs = []
for i in range(2 ** (n-1) + 1):
    while True:
        bitstring = ("{0:0%db}"%n).format(random.getrandbits(n))
        if bitstring not in inputs:
            inputs.append(bitstring)
            break

# test each input to see if the black box is one-to-one or two-to-one
bb = BlackBox(b)

print("Black box 1:")
bb.run(inputs, BlackBox.box1)
print("Black box 2:")
bb.run(inputs, BlackBox.box2)
