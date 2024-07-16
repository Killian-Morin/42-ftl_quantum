import os
from dotenv import load_dotenv

from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram, plot_state_city, plot_bloch_vector
from qiskit.quantum_info import DensityMatrix, Statevector
from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime import SamplerV2 as Sampler


purple = '\033[35m'
reset = '\033[0m'
SHOTS = 500


def load_account():
    load_dotenv()
    token = os.getenv("TOKEN")
    # Save the account to disk for future use.
    QiskitRuntimeService.save_account(channel="ibm_quantum", token=token, overwrite=True)


def create_circuit():
    # * Create the circuit with 2 qubits and 1 classical bit
    qc = QuantumCircuit(2)

    # * Apply an Hadamard gate on the first qubit
    qc.h(0)

    # * Apply a CNOT gate with the first qubit as control and second as target
    qc.cx(0, 1)

    ideal_distribution = Statevector.from_instruction(qc).probabilities_dict()

    plot_histogram(ideal_distribution, title="Ideal distribution of this circuit", filename="ideal_dist_Phi_plus")

    # * Apply the measurement tool to the circuit
    # qc.measure([0, 1], [0, 1])
    qc.measure_all()

    # * Draw the circuit
    print("\nASCII representation of the circuit:")
    print(qc, "\n")
    qc.draw(output='mpl', filename="circuit_Phi_plus", interactive=True)

    return qc


def get_backend_computer():
    load_account()
    service = QiskitRuntimeService(instance="ibm-q/open/main")

    print("Get the least busy and operational quantum computer ...")
    backend = service.least_busy(operational=True, simulator=False)
    print("It's ", purple, backend.name, reset, "\n")

    return backend


def run_circuit(qc, bck):
    # * Optimize the circuit created for this particular device
    # * Convert to an ISA circuit and layout-mapped observables.
    pm = generate_preset_pass_manager(backend=bck, optimization_level=1)
    isa_circuit = pm.run(qc)

    isa_circuit.draw('mpl', idle_wires=False, filename="circuit_optimized_Phi_plus")

    sampler = Sampler(bck)

    job = sampler.run([isa_circuit], shots=SHOTS)

    print(f"Job ID: {job.job_id()}\n")
    print(f"Job Status: {job.status()}\n")

    return job


def process_result(job, bck):
    result = job.result()[0]
    job_id = job.job_id()
    pub_result = result.data.meas.get_counts()

    result_percentage = {
        '00': pub_result['00'] / SHOTS,
        '01': pub_result['01'] / SHOTS,
        '10': pub_result['10'] / SHOTS,
        '11': pub_result['11'] / SHOTS
    }

    print(f"Measurement results info on a total of {SHOTS} shots (runned on {bck.name}, id = {job_id}): ")
    print(f"\tfor the 00 state: {pub_result['00']}")
    print(f"\tfor the 01 state: {pub_result['01']}")
    print(f"\tfor the 10 state: {pub_result['10']}")
    print(f"\tfor the 11 state: {pub_result['11']}")

    print(f"Measurement results as percentage of 1 (runned on {bck.name}, id = {job_id}):")
    print(f"\tfor the 00 state: {result_percentage['00']} / 1")
    print(f"\tfor the 01 state: {result_percentage['01']} / 1")
    print(f"\tfor the 10 state: {result_percentage['10']} / 1")
    print(f"\tfor the 11 state: {result_percentage['11']} / 1")

    return result_percentage


def render_result(counts, bck, job):
    # * Plot the result in a histogram
    job_id = job.job_id()
    plot_histogram(counts, title=rf"Measurement result of the $\Phi^+$ Bell state with {SHOTS} shots runned on {bck.name}",
                    filename=f"histogram_Phi_plus_{job_id}")


def entanglement_real():
    # * Load the IBMQ account
    load_account()

    # * Create the circuit that creates the Φ^+ Bell state
    qc = create_circuit()

    # * Get a real quantum computer
    bck = get_backend_computer()

    # * Run the circuit on the backend gotten
    job = run_circuit(qc, bck)

    # * Result processing
    final_counts = process_result(job, bck)
    render_result(final_counts, bck, job)

entanglement_real()
