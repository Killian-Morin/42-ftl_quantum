import os
from dotenv import load_dotenv

from qiskit import QuantumCircuit, transpile
from qiskit.visualization import plot_histogram, plot_state_city, plot_bloch_vector
from qiskit.quantum_info import DensityMatrix, Statevector
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
RESET = '\033[0m'
SHOTS = 500


def load_account():
    # * Take environment variables from .env
    load_dotenv()

    # * Get the TOKEN var from the .env that was loaded
    token = os.getenv("TOKEN")

    # * Save the account to disk for future use using the token,
    # * 'overwrite' to 'True' so that the existing account is overwritten
    QiskitRuntimeService.save_account(channel="ibm_quantum", token=token, overwrite=True)
    print(f"{GREEN}Account loaded !\n\n{RESET}")


def create_circuit():
    # * Create the circuit with 2 qubits
    qc = QuantumCircuit(2)

    # * Apply an Hadamard gate on q_0
    qc.h(0)

    # * Apply a CNOT gate with q_0 as control and q_1 as target
    qc.cx(0, 1)

    # * Get the measurement probabilities of the vector representing the circuit
    # * Plot those ideal probabilities in a histogram
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
    # * Try to get an instance, need to have the IBMQ account loaded
    # * If not loaded, call load_account()
    try:
        service = QiskitRuntimeService(instance="ibm-q/open/main")
        print(f"{GREEN}No exception, the account was already saved{RESET}\n\n")
    except Exception:
        print(f"{RED}Exception catched, the account was not saved and needs to be loaded{RESET}")
        load_account()
        service = QiskitRuntimeService(instance="ibm-q/open/main")

    # * Get the least busy and operational backend quantum computer and print it
    print("Get the least busy and operational quantum computer ...")
    backend = service.least_busy(operational=True, simulator=False)
    print(f"It's {PURPLE}{backend.name}{RESET}\n")

    return backend


def run_circuit(qc, bck):
    # * Optimize the circuit created for the particular backend obtained
    # * Convert to an Instruction Set Architecture (ISA) circuit
    # * ISA = the set of instructions the device can understand and execute
    pm = generate_preset_pass_manager(backend=bck, optimization_level=1)
    isa_circuit = pm.run(qc)

    # * Draw the circuit after being converted
    isa_circuit.draw('mpl', idle_wires=False, filename="circuit_optimized_Phi_plus")

    # * Get a Primitive, here Sampler, for the particular backend obtained
    # * https://docs.quantum.ibm.com/api/qiskit/primitives
    sampler = Sampler(bck)

    # * Run the circuit using the Primitive instantiated with the backend shots times
    # * Here 'isa_circuit' is considered a Primitive Unified Bloc (PUB)
    job = sampler.run([isa_circuit], shots=SHOTS)

    # * Print basic information on the job
    print(f"Job ID: {job.job_id()}\n")
    print(f"Job Status: {job.status()}\n")

    return job


def process_result(job, bck):
    # * Get the result of the first PUB, this gives a PubResult object
    result = job.result()[0]

    # * Get the job_id of the execution
    job_id = job.job_id()

    # * In the PubResult, get the data attribute, inside it there are the classical bits
    # * Those classical bits are called 'meas' by default and we get their results
    pub_result = result.data.meas.get_counts()

    # * Print the occurences for the four states for the 500 shots with the name of the backend and the job_id
    print(f"{BLUE}Measurement results info on a total of {SHOTS} shots (runned on {bck.name}, id = {job_id}):{RESET}")
    print(f"\tfor the 00 state: {PURPLE}{pub_result['00']}{RESET}")
    print(f"\tfor the 01 state: {PURPLE}{pub_result['01']}{RESET}")
    print(f"\tfor the 10 state: {PURPLE}{pub_result['10']}{RESET}")
    print(f"\tfor the 11 state: {PURPLE}{pub_result['11']}{RESET}")

    # * Divide the occurence of the states by the number of shots
    result_percentage = {
        '00': pub_result['00'] / SHOTS,
        '01': pub_result['01'] / SHOTS,
        '10': pub_result['10'] / SHOTS,
        '11': pub_result['11'] / SHOTS
    }

    # * Print the result with a total of 1
    print(f"Measurement results as percentage of 1 (runned on {bck.name}, id = {job_id}):")
    print(f"\tfor the 00 state: {GREEN}{result_percentage['00']}{RESET}")
    print(f"\tfor the 01 state: {GREEN}{result_percentage['01']}{RESET}")
    print(f"\tfor the 10 state: {GREEN}{result_percentage['10']}{RESET}")
    print(f"\tfor the 11 state: {GREEN}{result_percentage['11']}{RESET}")

    # * Return the result as percentage of 1 to use it in the histogram
    return result_percentage


def render_result(counts, bck, job):
    # * Plot the result in a histogram
    job_id = job.job_id()
    plot_histogram(counts, title=rf"Measurement result of the $\Phi^+$ Bell state with {SHOTS} shots runned on {bck.name}",
                    filename=f"histogram_Phi_plus_{job_id}")


def entanglement_real():
    # * Create the circuit that creates the Φ^+ Bell state
    qc = create_circuit()

    # * Get a real quantum computer
    bck = get_backend_computer()

    # * Run the circuit on the backend obtained
    job = run_circuit(qc, bck)

    # * Result processing (print and render)
    final_counts = process_result(job, bck)
    render_result(final_counts, bck, job)


if __name__ == "__main__":
    entanglement_real()
