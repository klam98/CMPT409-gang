import random
from black_box import BlackBox


def test_simon(bitstring):
    """Run experiment on bitstring."""
    print("Setting bitstring as %s..." % bitstring)
    n = len(bitstring)

    # generate 2^(n-1) + 1 unique inputs to test
    print("Generating inputs...\n")
    inputs = []
    for _ in range(2 ** (n-1) + 1):
        while True:
            bitstring = ("{0:0%db}"%n).format(random.getrandbits(n))
            if bitstring not in inputs:
                inputs.append(bitstring)
                break

    # test each input to see if the black box is one-to-one or two-to-one
    bb = BlackBox(bitstring)

    print("Black box 1:")
    bb1_res, bb1_time = bb.run(inputs, BlackBox.box1)
    print("Black box 2:")
    bb2_res, bb2_time = bb.run(inputs, BlackBox.box2)
    return {
        "bb1_res": bb1_res,
        "bb1_time": bb1_time,
        "bb2_res": bb2_res,
        "bb2_time": bb2_time,
    }


if __name__ == "__main__":
    bitstring = '110'
    test_simon(bitstring)
