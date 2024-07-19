from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram


GREEN = '\033[32m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
RESET = '\033[0m'


def process_result(counts, sim, shots):
    # * Print the occurences for both states for the 500 shots
    print(f"{BLUE}Measurements results ({sim} simulator):{RESET}")
    print(f"\tfor the 0 state: {PURPLE}{counts['0']}{RESET}")
    print(f"\tfor the 1 state: {PURPLE}{counts['1']}{RESET}\n")

    # * Divide the occurence of the states by the number of shots
    # * Print the result with a total of 1
    final_counts = {
        '0': counts['0'] / shots,
        '1': counts['1'] / shots
    }
    print(f"{BLUE}Measurements results as percentage of 1 ({sim} simulator):{RESET}")
    print(f"\tfor the 0 state: {GREEN}{final_counts['0']}{RESET}")
    print(f"\tfor the 1 state: {GREEN}{final_counts['1']}{RESET}\n")

    # * Return the result as percentage of 1 to use it in the histogram
    return final_counts


def superposition():
    # * Create the circuit with 1 qubit and 1 classical bit
    qc = QuantumCircuit(1, 1)

    # * Apply an Hadamard gate on q_0 to create superposition
    qc.h(0)

    # * Apply the measurement tool to the circuit
    qc.measure(0, 0)

    # * Draw the circuit
    print("ASCII representation of the circuit:")
    print(qc, "\n")
    qc.draw(output='mpl', filename="circuit_plus_state", interactive=True)

    # * Get the Aer simulator, the method used is automatically selected based on the circuit and noise model
    sim = AerSimulator(method='automatic')

    # * Transpile the circuit for the simulator obtained
    qc_transpile = transpile(qc, backend=sim)

    # * Run the circuit on the simulator with a precise number of shots
    shots = 500
    result = sim.run(qc_transpile, shots=shots).result()

    # * Get the type of simulator that was used since the method was 'automatic'
    sim_type = result.results[0].metadata['method']

    # * Result processing
    counts = result.get_counts()
    final_counts = process_result(counts, sim_type, shots)

    # * Draw the result in a histogram
    plot_histogram(final_counts, title=f"Measurement result of the plus state with {shots} shots ({sim_type})",
                    filename="histogram_plus_state")


if __name__ == "__main__":
    superposition()
