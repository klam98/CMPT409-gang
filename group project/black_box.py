import time

class BlackBox:

    def __init__(self, b):
        self.b = b

    def box1(self, z):
        """Black box function.

        funtion = (b (dot) z) % 2.
        """
        accum = 0
        for i in range(len(self.b)):
            accum += int(self.b[i]) * int(z[i])
        accum %= 2
        print("%s (dot) %s = %d (mod 2)" % (self.b, z, accum))
        return accum

    def box2(self, z):
        """Black box function.

        funtion = ((b << n) | z).
        """
        res = self.b + z
        res = int(res)
        print("(%s << %d) | %s = %d" % (self.b, len(self.b), z, res))
        return res

    def run(self, inputs, function):
        """Determine if set is one-to-one."""
        print("--------------------------------")
        print("Running Test...")
        start = time.time()
        one_to_one = True
        outputs = []
        for bitstring in inputs:
            out = function(self, bitstring)
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
        
        run_time = end - start
        print("Time taken: %fs" % run_time)
        print("--------------------------------\n")
        return one_to_one, run_time
