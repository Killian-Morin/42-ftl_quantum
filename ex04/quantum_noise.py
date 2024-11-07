import os
from dotenv import load_dotenv

from qiskit import QuantumCircuit
from qiskit.visualization import plot_histogram
from qiskit.quantum_info import Statevector
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
RESET = '\033[0m'
SHOTS = 500


def load_account():
    """ Load the account associated with the token found in the .env

    * Take environment variables from .env
    * Get the TOKEN var from the .env that was loaded

    * Save the account to disk for future use using the token,
    * 'overwrite' to 'True' so that the existing account is overwritten
    """

    load_dotenv()
    token = os.getenv("TOKEN")

    QiskitRuntimeService.save_account(channel="ibm_quantum", token=token, overwrite=True)
    print(f"{GREEN}Account loaded !\n\n{RESET}")


def create_circuit():
    """ Create the circuit for the Phi Bell state to be used on real quantum hardware

    * Create a circuit with 2 qubits
    * Apply an Hadamard gate on q_0
    * Apply a CNOT gate with q_0 as control and q_1 as target
    * Get the measurement probabilities of the vector representing the circuit
    * Plot those ideal probabilities in a histogram
    * Apply the measurement tool to the circuit
    * Draw in the terminal and save the circuit as 'circuit_Phi_plus.png'

    Return:
    -----
        qc (QuantumCircuit): representation of the quantum circuit
    """

    qc = QuantumCircuit(2)

    qc.h(0)

    qc.cx(0, 1)

    ideal_distribution = Statevector.from_instruction(qc).probabilities_dict()
    title = "Ideal distribution of this circuit"
    plot_histogram(ideal_distribution, title=title, filename="ideal_dist_Phi_plus", figsize=(12, 8))

    # qc.measure([0, 1], [0, 1])
    qc.measure_all()

    print("\nASCII representation of the circuit:")
    print(qc, "\n")
    qc.draw(output='mpl', filename="circuit_Phi_plus", interactive=True)

    return qc


def get_backend_computer():
    """ Get a Service Backend to run the circuit on

    * Try to get a service instance, need to have the IBMQ account loaded
    * If not loaded, call load_account()
    * Get the least busy and operational backend quantum computer

    Return
    -----
        backend (IBMBackend): instance of a backend representing an IBM Quantum Backend
    """

    try:
        service = QiskitRuntimeService(instance="ibm-q/open/main")
        print(f"{GREEN}No exception, the account was already saved{RESET}\n\n")
    except Exception:
        print(f"{RED}Exception catched, the account was not saved and needs to be loaded{RESET}")
        load_account()
        service = QiskitRuntimeService(instance="ibm-q/open/main")

    print("Get the least busy and operational quantum computer ...")
    backend = service.least_busy(operational=True, simulator=False)
    backend_status = backend.status()
    print(f"It's {PURPLE}{backend.name}{RESET} ({backend_status.pending_jobs} pending jobs)\n")

    return backend


def run_circuit(qc, bck):
    """ Run the circuit on the backend obtained

    Params
    -----
        qc (QuantumCircuit): representation of the Quantum Circuit
        bck (IBMBackend): backend instance of the hardware used to execute

    * Optimize the circuit created for the particular backend obtained
    * Convert to an Instruction Set Architecture (ISA) circuit
        * ISA = the set of instructions the device can understand and execute
    * Draw the circuit after being converted
    * Get a Primitive, here SamplerV2, for the particular backend obtained
        * https://docs.quantum.ibm.com/api/qiskit/primitives
    * Run the circuit using the Primitive instantiated with the backend SHOTS times
        * Here 'isa_circuit' is considered a Primitive Unified Bloc (PUB)

    Return
    -----
        job (RuntimeJobV2): representation of the runtime of the V2 Primitive execution
    """

    pm = generate_preset_pass_manager(backend=bck, optimization_level=1)
    isa_circuit = pm.run(qc)

    isa_circuit.draw('mpl', idle_wires=False, filename="circuit_optimized_Phi_plus")

    sampler = Sampler(bck)

    job = sampler.run([isa_circuit], shots=SHOTS)

    print(f"Job ID: {job.job_id()}\n")
    print(f"Job Status: {job.status()}\n")

    return job


def process_result(job, bck, qc):
    """ Print, plot and process the result of the execution (job)

    Params
    -----
        job (RuntimeJobV2): representation of the runtime execution
        bck (IBMBackend): backend instance where the execution was run
        qc (QuantumCircuit): the QuantumCircuit for the classical bits name

    * Get the result of the first PUB (Primitive Unified Bloc), this gives a PubResult object
    * Get the job_id of the execution
    * Get the name of the classical bits register
    * Dynamically use the obtained name to get back the results stored inside it
        * getattr() take the object 'result.data' and his attribute 'classical_bits_name'
            * and returns the value of the attribute
        * this allow to not hardcode the name of the ClassicalRegister, by default 'meas'
        * in the PubResult, get the data attribute, inside it there are the classical bits
    * Print the occurences of each states for the total shots with the name of the backend and the job_id
    * Plot an histogram for the counts results of the job
    * Divide the occurence of the states by the number of shots
    * Print the results as percentage of 1
    * Plot an histogram for the percentage results of the job
    """

    result = job.result()[0]

    job_id = job.job_id()

    classical_bits_name = qc.cregs[0].name

    pub_result = getattr(result.data, classical_bits_name).get_counts()

    print(f"{BLUE}Measurement results info on a total of {SHOTS} shots (runned on {bck.name}, id = {job_id}):{RESET}")
    print(f"\tfor the 00 state: {PURPLE}{pub_result['00']}{RESET}")
    print(f"\tfor the 01 state: {PURPLE}{pub_result['01']}{RESET}")
    print(f"\tfor the 10 state: {PURPLE}{pub_result['10']}{RESET}")
    print(f"\tfor the 11 state: {PURPLE}{pub_result['11']}{RESET}")

    title = rf"Counts measurement result obtained for the $\Phi^+$ Bell state with {SHOTS} shots runned on {bck.name}"
    plot_histogram(pub_result, title=title, filename=f"histogram_Phi_plus_counts_{job_id}", figsize=(12, 8))

    result_percentage = {
        '00': pub_result['00'] / SHOTS,
        '01': pub_result['01'] / SHOTS,
        '10': pub_result['10'] / SHOTS,
        '11': pub_result['11'] / SHOTS
    }

    print(f"{BLUE}Measurement results as percentage of 1 (runned on {bck.name}, id = {job_id}):{RESET}")
    print(f"\tfor the 00 state: {GREEN}{result_percentage['00']}{RESET}")
    print(f"\tfor the 01 state: {GREEN}{result_percentage['01']}{RESET}")
    print(f"\tfor the 10 state: {GREEN}{result_percentage['10']}{RESET}")
    print(f"\tfor the 11 state: {GREEN}{result_percentage['11']}{RESET}")

    title = rf"Percentage measurement result obtained for the $\Phi^+$ Bell state with {SHOTS} shots runned on {bck.name}"
    plot_histogram(result_percentage, title=title, filename=f"histogram_Phi_plus_percentage_{job_id}", figsize=(12, 8))


def entanglement_real():
    """ Call the functions to set up, run and process the entanglement circuit

    * Create the circuit that creates the Φ^+ Bell state
    * Get a real quantum computer
    * Run the circuit on the backend obtained
    * Result processing (print and render)

    qc: the quantum circuit representing the Φ^+ Bell state
    bck: the backend instance that will be used to run the circuit
    job: the job instance, i.e. result/data of the execution on the quantum hardware
    """

    qc = create_circuit()

    bck = get_backend_computer()

    job = run_circuit(qc, bck)

    process_result(job, bck, qc)


if __name__ == "__main__":
    entanglement_real()
