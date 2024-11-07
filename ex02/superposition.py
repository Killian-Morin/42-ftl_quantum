from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram


GREEN = '\033[32m'
ORANGE = '\033[33m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
RESET = '\033[0m'
SHOTS = 500


def process_result(counts, sim_type):
    """ Process the result from the simulation, print and plot the results

    Params
    -----
        counts (dict): holds the result of the simulation for the case '0' and '1'
        sim_type (str): type of simulator used

    * Print the occurences for both states for the total shots
    * Plot an histogram for the counts result of the simulation
    * Divide the occurence of the states by the number of shots
    *   and print the result as a total of 1
    * Plot an histogram for the percentage result of the simulation
    """

    print(f"\n{ORANGE}============================={RESET}")

    print(f"{BLUE}Measurements results ({sim_type} simulator):{RESET}")
    print(f"\tfor the 0 state: {PURPLE}{counts['0']}{RESET}")
    print(f"\tfor the 1 state: {PURPLE}{counts['1']}{RESET}\n")

    title = f"Counts measurement result obtained for the plus state $|+\\rangle$ with {SHOTS} shots on AerSimulator with method {sim_type}"
    plot_histogram(counts, title=title, filename="histogram_plus_state_counts", figsize=(12, 8))

    final_counts = {
        '0': counts['0'] / SHOTS,
        '1': counts['1'] / SHOTS
    }
    print(f"{BLUE}Measurements results as percentage of 1 ({sim_type} simulator):{RESET}")
    print(f"\tfor the 0 state: {GREEN}{final_counts['0']}{RESET}")
    print(f"\tfor the 1 state: {GREEN}{final_counts['1']}{RESET}\n")

    title = f"Percentage measurement result obtained for the plus state $|+\\rangle$ with {SHOTS} shots on AerSimulator with method {sim_type}"
    plot_histogram(final_counts, title=title, filename="histogram_plus_state_percentage", figsize=(12, 8))


def superposition():
    """ Create a circuit to illustrate the principle of superposition

    * Create the circuit with 1 qubit and 1 classical bit
    * Apply an Hadamard gate on q_0 to create superposition
    * Apply the measurement tool to the circuit
    * Draw in the terminal and create a .png with the circuit
    * Get the Aer simulator,
    *   the method used is automatically selected based on the circuit and noise model
    * Transpile (i.e. adapt) the circuit for the simulator obtained
    * Run the circuit on the simulator with a precise number of shots
    * Get the type of simulator that was used since the method was 'automatic'
    * Process (print and plot) the result
    """

    qc = QuantumCircuit(1, 1)

    qc.h(0)

    qc.measure(0, 0)

    print("ASCII representation of the circuit:")
    print(qc)
    qc.draw(output='mpl', filename="circuit_plus_state", interactive=True)

    sim = AerSimulator(method='automatic')

    qc_transpile = transpile(qc, backend=sim)

    result = sim.run(qc_transpile, shots=SHOTS).result()

    sim_type = result.results[0].metadata['method']

    counts = result.get_counts()

    process_result(counts, sim_type)


if __name__ == "__main__":
    superposition()
