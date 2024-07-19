from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_state_city
from qiskit.quantum_info import DensityMatrix, Statevector


GREEN = '\033[32m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
RESET = '\033[0m'


def process_result(counts, sim, shots):
    # * Print the occurences for both states for the 500 shots
    print(f"{BLUE}Measurements results ({sim} simulator):{RESET}")
    print(f"\tfor the 00 state: {PURPLE}{counts['0']}{RESET}")
    print(f"\tfor the 11 state: {PURPLE}{counts['1']}{RESET}\n")

    # * Divide the occurence of the states by the number of shots
    # * Print the result with a total of 1
    final_counts = {
        '00': counts['0'] / shots,
        '11': counts['1'] / shots
    }
    print(f"{BLUE}Measurements results as percentage of 1 ({sim} simulator):{RESET}")
    print(f"\tfor the 00 state: {GREEN}{final_counts['00']}{RESET}")
    print(f"\tfor the 11 state: {GREEN}{final_counts['11']}{RESET}\n")

    # * Return the result as percentage of 1 to use it in the histogram
    return final_counts


def entanglement():
    # * Create the circuit with 2 qubits and 1 classical bit
    qc = QuantumCircuit(2, 1)

    # * Apply an Hadamard gate on q_0
    qc.h(0)

    # * Apply a CNOT gate with q_0 as control and q_1 as target
    qc.cx(0, 1)

    # * Save the state of the qubits that will be used to render their probabilities
    # qc.save_statevector()
    # * Other way to get the state of the qubits to render their probabilities
    # statevector = DensityMatrix(qc)
    # statevector = Statevector(qc)

    # * Apply the measurement tool to the circuit
    qc.measure(0, 0)

    # * Draw the circuit
    print("\nASCII representation of the circuit:")
    print(qc, "\n")
    qc.draw(output='mpl', filename="circuit_Phi_plus", interactive=True)

    # * Get the Aer simulator, the method used is automatically selected based on the circuit and noise model
    sim = AerSimulator(method='automatic')

    # * Transpile the circuit for the simulator obtained
    qc_transpile = transpile(qc, backend=sim)

    # * Run the circuit on the selected simulator with a precise number of shots
    shots = 500
    result = sim.run(qc_transpile, shots=shots).result()

    # * Get the type of simulator that was used since chose 'automatic'
    sim_type = result.results[0].metadata['method']

    # * Result processing
    counts = result.get_counts()
    final_counts = process_result(counts, sim_type, shots)

    # * Plot the result in a histogram
    plot_histogram(final_counts, title=rf"Measurement result of the $\Phi^+$ Bell state with {shots} shots ({sim_type})",
                    filename="histogram_Phi_plus")

    # * Get the state of the qubits as they were before the measurement if DensityMatrix or StateVector was not used
    # * Render them in a cityscape format
    # statevector = result.get_statevector(qc)
    # plot_state_city(statevector, title=r"$\Phi^+$ Bell state", alpha=0.5, filename="cityscape_Phi_plus", color=['midnightblue', 'crimson'])


if __name__ == "__main__":
    entanglement()
