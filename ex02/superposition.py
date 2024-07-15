from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_bloch_vector


def process_result(counts, sim):
    print(f"Measurements results ({sim} simulator):")
    print(f"\tfor the 0 state: {counts['0']}")
    print(f"\tfor the 1 state: {counts['1']}\n")

    final_counts = {'0': counts['0'] / 500, '1': counts['1'] / 500}
    print(f"Measurements results as percentage of 1 ({sim} simulator):")
    print(f"\tfor the 0 state: {final_counts['0']}")
    print(f"\tfor the 1 state: {final_counts['1']}\n")

    return final_counts

def superposition():
    # * Create the circuit with 1 qubit and 1 classical bit
    qc = QuantumCircuit(1, 1)

    # * Apply an Hadamard gate on the first qubit to create superposition
    qc.h(0)

    # * Apply the measurement tool to the circuit
    qc.measure(0, 0)

    # * Draw the circuit
    print("ASCII representation of the circuit:")
    print(qc, "\n")
    qc.draw(output='mpl', filename="circuit_plus_state", interactive=True)

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

    # * Draw the result in a histogram
    plot_histogram(final_counts, title=f"Measurement result of the plus state with {shots} shots ({sim_type})",
                    filename="histogram_plus_state")

superposition()
