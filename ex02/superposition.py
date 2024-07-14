from qiskit import QuantumCircuit, transpile, assemble
from qiskit_aer import AerSimulator, Aer
from qiskit.visualization import plot_histogram, plot_state_city, plot_bloch_vector

# * Create the quantum circuit and apply an Hadamard gate to the qubit to create the superposition state
qc = QuantumCircuit(1, 1)
qc.h(0)
qc.measure(0, 0)
# qc.measure_all()

# * Draw the circuit
print("ASCII representation of the circuit:")
print(qc, "\n")
qc.draw(output='mpl', filename="circuit_plus_state", interactive=True)

# * Get a statevector Aer simulator
sim = Aer.get_backend('statevector_simulator')

# * Get an Aer simulator and transpile ??
# * Just another way to instantiate a simulator
# sim = AerSimulator()
# qc = transpile(qc, sim)

# * Run the circuit on the selected simulator with a precise number of shots
shots=500
result = sim.run(qc, shots=shots).result()

# * Result processing
counts = result.get_counts()
print(f"Measurements results: \n\tfor the 0 state: {counts['0']}\n\tfor the 1 state: {counts['1']}\n")
counts['0'] = counts['0'] / 100
counts['1'] = counts['1'] / 100
print(f"Measurements results as percentage of 1: \n\tfor the 0 state: {counts['0']}\n\tfor the 1 state: {counts['1']}\n")

# * Draw the result in a histogram
plot_histogram(counts, title=f"Measurement result of the plus state with {shots} shots", filename="histogram_plus_state")

# ? OTHER VERSION with a qasm_simulator
# qc = QuantumCircuit(1, 1)
# qc.h(0)
# qc.measure(0, 0)

# print("ASCII representation of the circuit:")
# print(qc, "\n")
# qc.draw(output='mpl', filename="alt_circuit_plus_state", interactive=True)

# * Get a qasm_simulator Aer simulator and transpile ??
# sim = Aer.get_backend('qasm_simulator')
# qc_transpile = transpile(qc, sim)

# # * Assemble the circuit into a qobj
# qobj = assemble(qc_transpile, shots=shots)

# # * Execute the circuit on the qasm simulator
# # ! execute() is deprecated
# # result = execute(qc, backend=simulator, shots=500).result()
# result = sim.run(qc_transpile, shots=500).result()

# counts = result.get_counts()
# print(f"Measurements results: \n\tfor the 0 state: {counts['0']}\n\tfor the 1 state: {counts['1']}\n")
# counts['0'] = counts['0'] / 100
# counts['1'] = counts['1'] / 100
# print(f"Measurements results as percentage of 1: \n\tfor the 0 state: {counts['0']}\n\tfor the 1 state: {counts['1']}\n")

# # Draw the result in a histogram
# plot_histogram(counts, title=f"Measurement result of the plus state with {shots} shots", filename="alt_histogram_plus_state")
