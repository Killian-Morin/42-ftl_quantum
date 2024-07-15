from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_state_city, plot_bloch_vector, plot_bloch_multivector
from qiskit.quantum_info import DensityMatrix, Statevector


def process_result(counts, sim):
    print(f"Measurements results ({sim} simulator):")
    print(f"\tfor the 00 state: {counts['0']}")
    print(f"\tfor the 11 state: {counts['1']}\n")

    final_counts = {'00': counts['0'] / 500, '11': counts['1'] / 500}
    print(f"Measurements results as percentage of 1 ({sim} simulator):")
    print(f"\tfor the 00 state: {final_counts['00']}")
    print(f"\tfor the 11 state: {final_counts['11']}\n")

    return final_counts

def entanglement():
    # * Create the circuit with 2 qubits and 1 classical bit
    qc = QuantumCircuit(2, 1)

    # * Apply an Hadamard gate on the first qubit
    qc.h(0)

    # * Apply a CNOT gate with the first qubit as control and second as target
    qc.cx(0, 1)

    # * Save the state of the qubits that will be used to render their probabilities
    qc.save_statevector()
    # * Other way to get the state of the qubits to render their probabilities
    # statevector = DensityMatrix(qc)
    # statevector = Statevector(qc)

    # * Apply the measurement tool to the circuit
    qc.measure(0, 0)

    # * Draw the circuit
    print("\nASCII representation of the circuit:")
    print(qc, "\n")
    qc.draw(output='mpl', filename="circuit_Phi_plus", interactive=True)

    # * Get the Aer simulator
    sim = AerSimulator(method='automatic')

    # * Transpile the circuit for the simulator chosen
    qc_transpile = transpile(qc, backend=sim)

    # * Run the circuit on the selected simulator with a precise number of shots
    shots = 500
    result = sim.run(qc_transpile, shots=500).result()

    # * Get the type of simulator that was used since chose 'automatic'
    sim_type = result.results[0].metadata['method']

    # * Result processing
    counts = result.get_counts()
    final_counts = process_result(counts, sim_type)

    # * Plot the result in a histogram
    plot_histogram(final_counts, title=rf"Measurement result of the $\Phi^+$ Bell state with {shots} shots ({sim_type})",
                    filename="histogram_Phi_plus")

    # * Get the state of the qubits as they were before the measurement and render them in a cityscape format
    statevector = result.get_statevector(qc)
    plot_state_city(statevector, title=r"$\Phi^+$ Bell state", alpha=0.5, filename="cityscape_Phi_plus", color=['midnightblue', 'crimson'])

entanglement()
