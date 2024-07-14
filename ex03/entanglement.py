from qiskit import QuantumCircuit, transpile, assemble
from qiskit_aer import AerSimulator, Aer
from qiskit.visualization import plot_histogram, plot_state_city, plot_bloch_vector

# Create the circuit and apply to the first qubit to create superposition
qc = QuantumCircuit(2, 1)
# Apply an Hadamard gate on the first qubit to create superposition
qc.h(0)
# Apply an CNOT gate with the first qubit as control and second as target
qc.cx(0, 1)
qc.measure(0, 0)

# Draw the circuit
print("ASCII representation of the circuit:")
print(qc, "\n")
qc.draw(output='mpl', filename="circuit_psi_plus_bell_state", interactive=True)

# Get an Aer simulator
sim = Aer.get_backend('statevector_simulator')

# Run the circuit on the selected simulator with a precise number of shots
shots=500
result = sim.run(qc, shots=shots).result()

# Result processing
counts = result.get_counts()
print(f"Measurements results: \n\tfor the 00 state: {counts['0']}\n\tfor the 11 state: {counts['1']}\n")
counts['0'] = counts['0'] / 100
counts['1'] = counts['1'] / 100
print(f"Measurements results as percentage of 1: \n\tfor the 00 state: {counts['0']}\n\tfor the 11 state: {counts['1']}\n")

# Draw the result in a histogram
plot_histogram(counts, title=f"Measurement result of the psi plus Bell state with {shots} shots", filename="histogram_psi_plus_bell_state")

# ? OTHER VERSION with a qasm_simulator
# qc = QuantumCircuit(2)
# qc.h(0)
# qc.cx(0, 1)

# print("ASCII representation of the circuit:")
# print(qc, "\n")
# qc.draw(output='mpl', filename="alt_circuit_psi_plus_bell_state", interactive=True)

# * Get Aer's qasm_simulator
# simulator = Aer.get_backend('qasm_simulator')

# * Transpile the circuit for the simulator
# qc_transpile = transpile(qc, simulator)

# * Assemble the circuit into a qobj
# shots = 500
# qobj = assemble(qc_transpile, shots=shots)

# # * Execute the circuit on the qasm simulator
# # ! execute() is deprecated
# # result = execute(qc, backend=sim, shots=shots).result()
# result = sim.run(qc_transpile, shots=500).result()

# Get the counts (measurement results)
# counts = result.get_counts()

# print(f"Measurements results: \n\tfor the 00 state: {counts['0']}\n\tfor the 11 state: {counts['1']}\n")
# counts['0'] = counts['0'] / 100
# counts['1'] = counts['1'] / 100
# print(f"Measurements results as percentage of 1: \n\tfor the 00 state: {counts['0']}\n\tfor the 11 state: {counts['1']}\n")

# Plot a histogram of the results
# plot_histogram(counts, title=f"Measurement result of the psi plus Bell state with {shots} shots", filename="alt_histogram_psi_plus_bell_state")
