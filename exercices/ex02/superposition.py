from print_color import print

from qiskit import QuantumCircuit, transpile
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import SamplerV2 as Sampler
from qiskit_ibm_runtime.fake_provider import FakeSherbrooke
from qiskit.visualization import plot_histogram, plot_distribution


SHOTS = 500


def circuit_creation():
    """ Create a circuit to illustrate the principle of superposition

    * Create the circuit with 1 qubit
    * Apply an Hadamard gate on q_0 to create superposition
    * Apply the measurement tool to the circuit
    * Draw in the terminal and create a .png of the circuit

    Return
    -----
        qc (QuantumCircuit): the circuit for the superposition
    """

    qc = QuantumCircuit(1)

    qc.h(0)

    qc.measure_all()

    print("ASCII representation of the circuit:")
    print(qc)
    qc.draw(output='mpl', filename="circuit_plus_state", interactive=True)

    return qc


def aer_simulation(qc):
    """ Run the plus state circuit with an AerSimulator

    Param
    -----
        qc (QuantumCircuit): the circuit to run

    * Get the Aer simulator,
    *   the method used is automatically selected based on the circuit and noise model
    * Transpile (i.e. adapt) the circuit for the simulator obtained
    * Run the circuit on the simulator with a precise number of shots
    * Get the type of simulator that was used since the method was 'automatic'
    * Sort the dict of the results by keys
    * Process (print and plot) the result
    """

    print("\n=============================\n", color='yellow')

    print("Running the circuit with an AerSimulator", color='green')

    sim = AerSimulator(method='automatic')

    qc_transpile = transpile(qc, backend=sim)

    result = sim.run(qc_transpile, shots=SHOTS).result()

    sim_type = result.results[0].metadata['method']

    counts = result.get_counts()

    counts = dict(sorted(counts.items()))

    print(f"Measurements results with AerSimulator (type: {sim_type}):", color='green')

    for state, result in counts.items():
        print(f"\tfor the {state} state:", end=' ')
        print(result, color='purple', end=' (')
        print(result / SHOTS, color='purple', end=')\n')

    title = f"Count result for the plus state $|+\\rangle$ with {SHOTS} shots on AerSimulator (method {sim_type})"
    plot_histogram(counts, title=title, filename="histogram_aer_plus_state", figsize=(12, 8))

    title = f"Percentage result for the plus state $|+\\rangle$ with {SHOTS} shots on AerSimulator (method {sim_type})"
    plot_distribution(counts, title=title, filename="distribution_aer_plus_state", figsize=(12, 8))


def fake_backend_simulation(qc):
    """ Run the plus state circuit with a FakeBackend simulator

    Param
    -----
        qc (QuantumCircuit): the circuit to run

    * Get the FakeBackend simulator, mimics behaviors of real systems
    * Transpile (i.e. adapt) the circuit for the simulator obtained
    * Get a Primitive, here SamplerV2, for the particular backend obtained
        * https://docs.quantum.ibm.com/api/qiskit/primitives
    * Run the circuit on the simulator with a precise number of shots
    * Get the name of the ClassicalRegister from the circuit
    * Sort the dict of the results by keys
    * Process (print and plot) the result
    """

    print("\n=============================\n", color='yellow')

    print("Running the circuit with a FakeBackend simulator", color='cyan')

    backend = FakeSherbrooke()

    qc_transpile = transpile(qc, backend)

    sampler = Sampler(backend)
    job = sampler.run([qc_transpile], shots=SHOTS)
    result = job.result()[0]
    bits_name = qc.cregs[0].name
    counts = getattr(result.data, bits_name).get_counts()

    counts = dict(sorted(counts.items()))

    print(f"Measurements results with FakeBackend:", color='cyan')

    for state, result in counts.items():
        print(f"\tfor the {state} state:", end=' ')
        print(result, color='purple', end=' (')
        print(result / SHOTS, color='purple', end=')\n')

    title = f"Count result for the plus state $|+\\rangle$ with the FakeBackend simulation and {SHOTS} shots"
    plot_histogram(counts, title=title, filename="histogram_fake_plus_state", figsize=(12, 8))

    title = f"Percentage result for the plus state $|+\\rangle$ with the FakeBackend simulation and {SHOTS} shots"
    plot_distribution(counts, title=title, filename="distribution_fake_plus_state", figsize=(12, 8))


def main():
    """ main function to create the circuit and do the simulation with different types """

    qc = circuit_creation()

    aer_simulation(qc)

    fake_backend_simulation(qc)


if __name__ == "__main__":
    main()
