import numpy as np

from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit, ClassicalRegister, QuantumRegister
from qiskit.visualization import plot_histogram

# IBMQ.load_account()

n = 3 # the length of the first register for querying the oracle

# Choose a type of oracle at random. With probability half it is constant,
# and with the same probability it is balanced
oracleType, oracleValue = np.random.randint(2), np.random.randint(2)

if oracleType == 0:
    print("The oracle returns a constant value ", oracleValue)
else:
    print("The oracle returns a balanced function")
    a = np.random.randint(1,2**n) # this is a hidden parameter for balanced oracle.

# Creating registers
# n qubits for querying the oracle and one qubit for storing the answer
qr = QuantumRegister(n+1) #all qubits are initialized to zero
# for recording the measurement on the first register
cr = ClassicalRegister(n)

circuitName = "DeutschJozsa"
djCircuit = QuantumCircuit(qr, cr)

# Create the superposition of all input queries in the first register by applying the Hadamard gate to each qubit.
for i in range(n):
    djCircuit.h(qr[i])

# Flip the second register and apply the Hadamard gate.
djCircuit.x(qr[n])
djCircuit.h(qr[n])

# Apply barrier to mark the beginning of the oracle
djCircuit.barrier()

if oracleType == 0:#If the oracleType is "0", the oracle returns oracleValue for all input.
    if oracleValue == 1:
        djCircuit.x(qr[n])
    else:
        djCircuit.id(qr[n])
else: # Otherwise, it returns the inner product of the input with a (non-zero bitstring)
    for i in range(n):
        if (a & (1 << i)):
            djCircuit.cx(qr[i], qr[n])

# Apply barrier to mark the end of the oracle
djCircuit.barrier()

# Apply Hadamard gates after querying the oracle
for i in range(n):
    djCircuit.h(qr[i])

# Measurement
djCircuit.barrier()
for i in range(n):
    djCircuit.measure(qr[i], cr[i])

djCircuit.draw(output='mpl', scale=0.5, filename="circuit_test")

backend = AerSimulator(method='automatic')
shots = 1000
job = backend.run(djCircuit, shots=shots)
results = job.result()
answer = results.get_counts()

plot_histogram(answer, filename="histogram")

import os
from dotenv import load_dotenv

from qiskit import transpile
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler


load_dotenv()
token = os.getenv("TOKEN")
QiskitRuntimeService.save_account(channel="ibm_quantum", token=token, overwrite=True)

service = QiskitRuntimeService(instance="ibm-q/open/main")
backend = service.least_busy(operational=True, simulator=False)

pm = generate_preset_pass_manager(backend=backend, optimization_level=1)
isa_circuit = pm.run(djCircuit)

sampler = Sampler(backend)

job = sampler.run([isa_circuit], shots=1024)

# * autre méthode avec transpile pour remplacer generate_preset_pass_manager()
# * djCompiled = transpile(djCircuit, backend=backend, optimization_level=1)

results = job.result()
counts = results.get_counts()

threshold = int(0.01 * shots) # the threshold of plotting significant measurements
filteredAnswer = {k: v for k,v in counts.items() if v >= threshold} # filter the counts for better view of plots

removedCounts = np.sum([ v for k,v in counts.items() if v < threshold ]) # number of counts removed
filteredAnswer['other_bitstrings'] = removedCounts  # the removed counts are assigned to a new index

plot_histogram(filteredAnswer, filename="test_histogram_real")
print(filteredAnswer)
