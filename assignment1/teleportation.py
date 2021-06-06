# https://qiskit.org/textbook/ch-algorithms/teleportation.html
import logging
from unicodedata import normalize
import warnings
logging.captureWarnings(True)
warnings.filterwarnings("ignore", category=DeprecationWarning)
import numpy as np
from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit import IBMQ, Aer, transpile, assemble
from qiskit.visualization import plot_histogram, plot_bloch_multivector
from qiskit.extensions import Initialize
from qiskit_textbook.tools import random_state, array_to_latex

def create_bell_pair(qc, a, b):
    """Creates a bell pair in qc using qubits a & b"""
    qc.h(a) # Put qubit a into state |+>
    qc.cx(a,b) # CNOT with a as control and b as target

def alice_gates(qc, psi, a):
    qc.cx(psi, a)
    qc.h(psi)

def measure_and_send(qc, a, b):
    """Measures qubits a & b and 'sends' the results to Bob"""
    qc.barrier()
    qc.measure(a,0)
    qc.measure(b,1)

# This function takes a QuantumCircuit (qc), integer (qubit)
# and ClassicalRegisters (crz & crx) to decide which gates to apply
def bob_gates(qc, qubit, crz, crx):
    # Here we use c_if to control our gates with a classical
    # bit instead of a qubit
    qc.x(qubit).c_if(crx, 1) # Apply gates if the registers 
    qc.z(qubit).c_if(crz, 1) # are in the state '1'

# Create random 1-qubit state
print("Generating random state for psi...")
psi = random_state(1)
print("\tpsi: %s" % psi)
print("DONE.\n")

print("Initializing gates...")
init_gate = Initialize(psi)
init_gate.label = "init"
inverse_init_gate = init_gate.gates_to_uncompute()
print("DONE.\n")

## SETUP
print("Creating quantum register...")
qr = QuantumRegister(3, name="q")   # Protocol uses 3 qubits
print("Creating classical registers...")
crz = ClassicalRegister(1, name="crz") # and 2 classical registers
crx = ClassicalRegister(1, name="crx")
print("Creating quantum circuit...")
qc = QuantumCircuit(qr, crz, crx)
print("DONE.\n")

print("STEP 0: Initialize q0")
qc.append(init_gate, [0])
qc.barrier()
print(qc)
print("DONE.\n")

print("STEP 1: Create bell pair")
create_bell_pair(qc, 1, 2)
qc.barrier()
print(qc)
print("DONE.\n")

print("STEP 2: Send q1 to Alice and q2 to Bob")
alice_gates(qc, 0, 1)
print(qc)
print("DONE.\n")

print("STEP 3: Alice measuring and sending classical bits to Bob...")
measure_and_send(qc, 0, 1)
print(qc)
print("DONE.\n")

print("STEP 4: Bob decoding qubits...")
bob_gates(qc, 2, crz, crx)
print(qc)
print("DONE.\n")

print("STEP 5: Reversing intitialization process...")
qc.append(inverse_init_gate, [2])
print(qc)
print("DONE.\n")

print("STEP 6: Generating result...")
cr_result = ClassicalRegister(1)
qc.add_register(cr_result)
qc.measure(2,2)
print(qc)
# print("\tResults: %s" % cr_result)
print("DONE.\n")

print("STEP 7: Confirming results...")
qasm_sim = Aer.get_backend('qasm_simulator')
t_qc = transpile(qc, qasm_sim)
qobj = assemble(t_qc)
counts = qasm_sim.run(qobj).result().get_counts()

for key in counts.keys():
    counts[key] = str(counts[key] / 10) + "%"

print("\tProbability distribution of qubit states: %s" % counts)
print("DONE.\n")
print("We can see we have a 100% chance of measuring q_2 (the leftmost bit in the string) in the state |0>. This is the expected result, and indicates the teleportation protocol has worked properly.")