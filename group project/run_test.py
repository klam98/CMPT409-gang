import csv
import random
import classical_simon
import simon

MAX_N = 10
OUTPUT_FILE = "simon_time_data.csv"

print("Beginning simon test with n 2-%d" % MAX_N)

print("\n--------------------------------")
print("--------------------------------\n")

with open(OUTPUT_FILE, mode="w") as data_file:
    data_writer = csv.writer(data_file)
    data_writer.writerow([
        "number of bits in bitstring",
        "classical time for one-to-one black box (s)",
        "quantum time for one-to-one black box (s)",
        "classical time for two-to-one black box (s)",
        "quantum time for two-to-one black box (s)",
    ])
    for n in range(2, MAX_N + 1):
        bitstring = ("{0:0%db}"%n).format(random.getrandbits(n))
        classical_data = classical_simon.test_simon(bitstring)
        quantum_data = simon.test_simon(bitstring)

        classical_one_to_one_time = classical_data["bb1_time"] if classical_data["bb1_res"] else classical_data["bb2_time"]
        classical_two_to_one_time = classical_data["bb1_time"] if not classical_data["bb1_res"] else classical_data["bb2_time"]
        quantum_one_to_one_time = quantum_data["bb1_time"] if quantum_data["bb1_res"] else quantum_data["bb2_time"]
        quantum_two_to_one_time = quantum_data["bb1_time"] if not quantum_data["bb1_res"] else quantum_data["bb2_time"]

        data_writer.writerow([
            n,
            classical_one_to_one_time,
            quantum_one_to_one_time,
            classical_two_to_one_time,
            quantum_two_to_one_time,
        ])

print("--------------------------------")
print("--------------------------------\n")

print("Simon test done.")
print("Data saved to: %s" % OUTPUT_FILE)
