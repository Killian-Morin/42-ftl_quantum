from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram, plot_distribution
from qiskit.quantum_info import DensityMatrix, Statevector


GREEN = '\033[32m'
YELLOW = '\033[33m'
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

    * Print the occurences and percentages for both states for the total shots
    * Plot an histogram for the counts result of the simulation
    * Plot a distribution for the percentage result of the simulation
    """

    print(f"\n{YELLOW}============================={RESET}")

    print(f"{BLUE}Measurements results ({sim_type} simulator):{RESET}")
    print(f"\tfor the 00 state: {PURPLE}{counts['0']}{RESET} ({GREEN}{counts['0'] / SHOTS}{RESET})")
    print(f"\tfor the 11 state: {PURPLE}{counts['1']}{RESET} ({GREEN}{counts['1'] / SHOTS}{RESET})")

    title = f"Counts measurement result obtained for the $\Phi^+$ Bell state with {SHOTS} shots on AerSimulator with method {sim_type}"
    plot_histogram(counts, title=title, filename="histogram_Phi_plus", figsize=(12, 8))

    title = f"Percentage measurement result obtained for the $\Phi^+$ Bell state with {SHOTS} shots on AerSimulator with method {sim_type}"
    plot_distribution(counts, title=title, filename="distribution_Phi_plus", figsize=(12, 8))


def entanglement():
    """ Create a circuit that implement the principle of entanglement

    * Create a circuit with 2 qubits and 1 classical bit
    * Apply an Hadamard gate on q_0
    * Apply a CNOT gate with q_0 as control and q_1 as target

    If you want to see the probabilities of the state of the qubits (not really relevant)
    * Save the state of the qubits that will be used to render their probabilities
        * needed with statevector = result.get_statevector(qc) to plot the city
    * Other way to get the state of the qubits to render their probabilities

    * Apply the measurement tool to the circuit
    * Draw in the terminal and create a .png with the circuit
    * Get the Aer simulator,
    *   the method used is automatically selected based on the circuit and noise model
    * Transpile (i.e. adapt) the circuit for the simulator obtained
    * Run the circuit on the simulator with a precise number of shots
    * Get the type of simulator that was used since the method was 'automatic'
    * Process (print and plot) the result

    For the probabilities state of the qubits after the run
    * Get the state of the qubits as they were before the measurement,
        * DensityMatrix or StateVector must not be used
    * Render the probabilities in a cityscape format
    """

    qc = QuantumCircuit(2, 1)

    qc.h(0)

    qc.cx(0, 1)

    # qc.save_statevector()

    # statevector = DensityMatrix(qc)
    # statevector = Statevector(qc)

    qc.measure(0, 0)

    print("\nASCII representation of the circuit:")
    print(qc)
    qc.draw(output='mpl', filename="circuit_Phi_plus", interactive=True)

    sim = AerSimulator(method='automatic')

    qc_transpile = transpile(qc, backend=sim)

    result = sim.run(qc_transpile, shots=SHOTS).result()

    sim_type = result.results[0].metadata['method']

    counts = result.get_counts()

    process_result(counts, sim_type)

    # statevector = result.get_statevector(qc)
    # plot_state_city(statevector, title=r"$\Phi^+$ Bell state", alpha=0.5, filename="cityscape_Phi_plus", color=['midnightblue', 'crimson'])


if __name__ == "__main__":
    entanglement()
