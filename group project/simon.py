# Adapted from: https://qiskit.org/textbook/ch-algorithms/simon.html

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

from black_box import BlackBox


## SETUP
# implement Simon's algorithm for an example with 3-qubits and bitstring b = '110'
b = '110'
print("Setting bitstring as %s..." % b)
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
results = aer_sim.run(qobj).result()
counts = results.get_counts()

for key in counts.keys():
    counts[key] = str(counts[key] / 10) + "%"

print("Probability distribution of qubit states: %s\n" % counts)

# test each input to see if the black box is one-to-one or two-to-one
bb = BlackBox(b)
print("Black box 1:")
bb.run(counts, BlackBox.box1)
print("Black box 2:")
bb.run(counts, BlackBox.box2)
