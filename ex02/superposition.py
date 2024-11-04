from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram


GREEN = '\033[32m'
ORANGE = '\033[33m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
RESET = '\033[0m'
SHOTS = 500


def process_result(counts, sim):
    """ Process the result from the simulation, print the results/values

    Params
    -----
        counts (dict): holds the result of the simulation for the case '0' and '1'
        sim (str): type of simulator used

    * Print the occurences for both states for the total shots
    * Divide the occurence of the states by the number of shots
    *   and print the result as a total of 1

    Return
    -----
        final_counts (dict): the result of each state as percentage of 1, to be used in the histogram
    """

    print(f"\n{ORANGE}============================={RESET}")

    print(f"{BLUE}Measurements results ({sim} simulator):{RESET}")
    print(f"\tfor the 0 state: {PURPLE}{counts['0']}{RESET}")
    print(f"\tfor the 1 state: {PURPLE}{counts['1']}{RESET}\n")

    final_counts = {
        '0': counts['0'] / SHOTS,
        '1': counts['1'] / SHOTS
    }
    print(f"{BLUE}Measurements results as percentage of 1 ({sim} simulator):{RESET}")
    print(f"\tfor the 0 state: {GREEN}{final_counts['0']}{RESET}")
    print(f"\tfor the 1 state: {GREEN}{final_counts['1']}{RESET}\n")

    return final_counts


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
    * Process the result
    * Plot the result in a histogram that will be saved in a .png file
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
    final_counts = process_result(counts, sim_type)

    title = f"Measurement result of the plus state $|+\\rangle$ with {SHOTS} shots ({sim_type})"
    plot_histogram(final_counts, title=title, filename="histogram_plus_state")


if __name__ == "__main__":
    superposition()
