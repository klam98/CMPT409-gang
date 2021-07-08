# ignore deprecation warnings
import logging
import warnings
logging.captureWarnings(True)
warnings.filterwarnings("ignore", category=DeprecationWarning) 

# importing Qiskit
from qiskit import IBMQ, Aer
from qiskit.providers.ibmq import least_busy
from qiskit import QuantumCircuit, transpile, assemble

# import basic plot tools
from qiskit.visualization import plot_histogram
from qiskit_textbook.tools import simon_oracle

import time


## SETUP
# implement Simon's algorithm for an example with 3-qubits and bitstring b = '110'
print("Setting bitstring as 110...")
b = '110'
n = len(b)

print("Generating Simon circuit using 3 qubits...")
simon_circuit = QuantumCircuit(n*2, n)

# Apply Hadamard gates before querying the oracle
simon_circuit.h(range(n))    
    
# Apply barrier for visual separation
simon_circuit.barrier()

# creates a Simon oracle for the bitstring b
simon_circuit += simon_oracle(b)

# Apply barrier for visual separation
simon_circuit.barrier()

print("Applying Hadamard gates...\n")
# Apply Hadamard gates to the input register
simon_circuit.h(range(n))

# Measure qubits
simon_circuit.measure(range(n), range(n))
print(simon_circuit)
print("DONE.\n")


## Experiment using local simulator
print("Generating a random distribution of qubit states using the previously generated Simon circuit...")
aer_sim = Aer.get_backend('aer_simulator')
shots = 1024
qobj = assemble(simon_circuit, shots=shots)
start = time.time()
results = aer_sim.run(qobj).result()
end = time.time()
counts = results.get_counts()

for key in counts.keys():
    counts[key] = str(counts[key] / 10) + "%"

print("Probability distribution of qubit states: %s\n" % counts)

# Calculate the dot product of the results
def bdotz(b, z):
    accum = 0
    for i in range(len(b)):
        accum += int(b[i]) * int(z[i])
    return (accum % 2)

print("Compute dot product of bitstring b and the qubits from the Simon circuit:")
for z in counts:
    print('{} (dot) {} = {} (mod 2)'.format(b, z, bdotz(b,z)))

print("Since the result of each dot product is equal to 0 (mod 2), this implies that each qubit has a two-to-one mapping.\n")

print("Using these results, we can then use Gaussian elimination which has a run time of O(n^3) to determine exactly which inputs are one-to-one and which are two-to-one.")

print("Time taken: %fs" % (end - start))
