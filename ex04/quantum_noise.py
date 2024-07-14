from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram, plot_state_city, plot_bloch_vector

# * Create the circuit and apply to the first qubit to create superposition
qc = QuantumCircuit(2, 1)
# * Apply an Hadamard gate on the first qubit to create superposition
qc.h(0)
# * Apply a CNOT gate with the first qubit as control and second as target
qc.cx(0, 1)
qc.measure(0, 0)

# * Draw the circuit
print("ASCII representation of the circuit:")
print(qc, "\n")
qc.draw(output='mpl', filename="circuit_psi_plus_bell_state", interactive=True)

# TODO: get a real quantum computer

shots=500
# TODO: run the program on a real quantum computer

# * Result processing
# counts = result.get_counts()
# print(f"Measurements results: \n\tfor the 00 state (real quantum computer): {counts['0']}\n\tfor the 11 state: {counts['1']}\n")
# counts['0'] = counts['0'] / 100
# counts['1'] = counts['1'] / 100
# print(f"Measurements results as percentage of 1 (real quantum computer): \n\tfor the 00 state: {counts['0']}\n\tfor the 11 state: {counts['1']}\n")

# * Draw the result in a histogram
# plot_histogram(counts, title=f"Measurement result of the psi plus Bell state with {shots} shots on a real quantum computer", filename="histogram_psi_plus_bell_state")
