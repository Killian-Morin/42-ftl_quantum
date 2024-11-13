import os
import sys
from dotenv import load_dotenv

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.visualization import plot_histogram
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


NB_QUBITS = 4
SHOTS = 500

RESET = '\033[0m'
GREEN = '\033[32m'
RED = '\033[31m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
PINK = '\033[95m'
BOLD = '\033[01m'


def constant_oracle_subject():
    """ Create the constant oracle from the subject exemple

    * Create the QuantumCircuit with 4 qubits
    * Apply an X gate on the last qubit: q_3
    * Draw in the terminal and save as constant_oracle_subject.png the circuit

    Return
    -----
        qc (QuantumCircuit): representation of the constant oracle quantum circuit
    """

    qc = QuantumCircuit(NB_QUBITS)

    qc.x(NB_QUBITS - 1)

    qc.draw(output="mpl", filename="constant_oracle_subject")

    print(f"{GREEN}Created the constant oracle function from the subject{RESET}")

    return qc


def balanced_oracle_subject():
    """ Create the balanced oracle from the subject exemple

    * Create the QuantumCircuit with 4 qubits
    * Apply an X gate on the first 3 qubits: q_0, q_1 and q_2
    * Apply three CNOT control gate with q_3 as the target and q_0, q_1 and q_2 as the controller
    * Apply again an X gate on the first 3 qubits: q_0, q_1 and q_2
    * Draw in the terminal and save as balanced_oracle_subject.png the circuit

    Return
    -----
        qc (QuantumCircuit): representation of the balanced oracle quantum circuit
    """

    qc = QuantumCircuit(NB_QUBITS)

    qc.x([0, 1, 2])

    qc.cx(0, 3)
    qc.cx(1, 3)
    qc.cx(2, 3)

    qc.x([0, 1, 2])

    qc.draw(output="mpl", filename="balanced_oracle_subject")

    print(f"{GREEN}Created the balanced oracle function from the subject{RESET}")

    return qc


def oracle_eval():
    """ Placeholder to put the oracle given during the correction """


def compile_circuit(oracle_function):
    """ Compiles a circuit for use in the Deutsch-Jozsa algorithm

    Param
    -----
        oracle_function (QuantumCircuit): the circuit of the oracle function

    * n represent the number of input qubits
    * The oracle has n input qubits and 1 output qubits

    * Create a temporary circuit with 4 qubits (3 input and 1 output) and 3 classical bits (measurements)
    * Apply an X gate to the output qubit q_3, his state is ∣1⟩
    * Apply Hadamard gates to all qubits, each qubits are put in equal superposition state
    * Add a barrier for visualization to separate from the beginning of the oracle
    * Take the oracle function and apply it to the current circuit
        * This apply the instructions of the oracle onto the current circuit
    * Add a barrier for visualization to separate from the end of the oracle
    * Apply Hadamard gates to the input qubits
    * The state is transformed to an all-zero state (constant function) or a superposition state (balanced function)
    * Measure the input qubits and store the result in the classical bits
    * Draw the circuit obtained by the composition, saved as 'composed_circuit.png'
        * the part between the barriers is the oracle function

    Return
    -----
        qc (QuantumCircuit): representation of the composed oracle function
    """
    n = NB_QUBITS - 1

    qc = QuantumCircuit(n + 1, n)

    qc.x(n)

    qc.h(range(n + 1))

    qc.barrier()

    qc.compose(oracle_function, inplace=True)

    qc.barrier()

    qc.h(range(n))

    qc.measure(range(n), range(n))

    qc.draw(output="mpl", filename="composed_circuit")

    print(f"Composed the instructions of the oracle on a circuit to use it in the Deutsch-Jozsa algorithm")

    return qc


def sim_run_oracle(oracle_function):
    """ Run the Oracle on a simulator

    Param
    -----
        oracle_function (QuantumCircuit): the circuit of the oracle function

    * Get an AerSimulator, the method used is automatically selected based on the circuit and noise model
    * Run the composed circuit on a AerSimulator SHOTS times
        * with the memory parameter to true in order to have the outcome of the shot as a list
    * Get the type of AerSimulator that was used
    * Get the outcome of the shots
    * Deduce the type of the oracle function
    *   if one of the state is in ∣1⟩ then balanced or if they are none ∣0⟩ = constant)
    * Plot the counts result
    """

    print("\nThis will run the circuit on a Qiskit Aer simulator ...")

    sim = AerSimulator(method='automatic')

    result = sim.run(oracle_function, shots=SHOTS, memory=True).result()

    sim_type = result.results[0].metadata['method']
    print(f"The type of AerSimulator used was {PURPLE}{sim_type} {RESET}\n")

    measurements = result.get_memory()
    counts = result.get_counts()

    print(f"The measurements for the q_0, q_1 and q_2 are: {YELLOW}{measurements}{RESET}\n")

    if "1" in measurements[0]:
        print(f"{RED}RESULT - SIMULATOR{RESET}: The function is {YELLOW}balanced{RESET}, some qubits at 1 !\n")
    else:
        print(f"{RED}RESULT - SIMULATOR{RESET}: The function is {YELLOW}constant{RESET}, all qubits at 0 !\n")

    title = f"Counts measurement result for the simulation of type {sim_type}"
    plot_histogram(counts, title=title, filename="histogram_sim_counts", figsize=(12, 8))


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
        print(f"{GREEN}No exception, the account was already saved{RESET}\n")
    except Exception:
        print(f"{RED}Exception catched, the account was not saved and needs to be loaded{RESET}")
        load_dotenv()
        token = os.getenv("TOKEN")
        service = QiskitRuntimeService(channel='ibm_quantum', instance="ibm-q/open/main", token=token)
        QiskitRuntimeService.save_account(channel="ibm_quantum", token=token, overwrite=True)
        print(f"{GREEN}Account loaded{RESET}")

    print("Get the least busy and operational quantum computer ...")
    backend = service.least_busy(operational=True, simulator=False)
    backend_status = backend.status()
    print(f"It's {PURPLE}{backend.name}{RESET} ({backend_status.pending_jobs} pending jobs)\n")

    return backend


def real_run_oracle(oracle_function):
    """ Run the oracle on a real quantum hardware

    Param
    -----
        oracle_function (QuantumCircuit): the circuit of the oracle function

    * Optimize the circuit created for the particular backend obtained
    * Convert to an Instruction Set Architecture (ISA) circuit
        * ISA = the set of instructions the device can understand and execute
    * Draw the circuit after being converted, saved as 'circuit_optimized'
    * Get a Primitive, here SamplerV2, for the particular backend obtained
        * https://docs.quantum.ibm.com/api/qiskit/primitives
    * Run the circuit using the Primitive instantiated with the backend shots times
        * Here 'isa_circuit' is considered a Primitive Unified Bloc (PUB)
    * Get the result of the first PUB, this gives a PubResult object
    * In the PubResult, get the data attribute, inside it there are the classical bits
        * The way I instantiate the QuantumCircuit, the ClassicalRegister get the name 'c'
        * we use this name to get their content
    * Plot the result in a histogram, saved as 'histogram_real_result_{job_id}'
    """

    print("\nThis will run the circuit on a real quantum computer ...")

    bck = get_backend_computer()

    pm = generate_preset_pass_manager(backend=bck, optimization_level=1)
    isa_circuit = pm.run(oracle_function)

    isa_circuit.draw('mpl', idle_wires=False, filename="circuit_optimized_for_back")

    sampler = Sampler(bck)

    job = sampler.run([isa_circuit], shots=SHOTS)

    job_id = job.job_id()

    print(f"Job ID: {job_id}\n")
    print(f"Job Status: {job.status()}\n")

    result = job.result()[0]

    classical_bits_name = oracle_function.cregs[0].name

    counts = getattr(result.data, classical_bits_name).get_counts()

    # try:
    #     counts = result.data.c.get_counts()
    #     print(f"The classical bits/result was in {BOLD}c{RESET}")
    # except Exception:
    #     counts = result.data.meas.get_counts()
    #     print(f"The classical bits/result was in {BOLD}meas{RESET}")

    print(f"{RED}RESULT - HARDWARE{RESET}: with {SHOTS} the qubits are at {counts}")

    title = f"Counts measurement result of {job_id} runned on {bck.name} real quantum computer"
    plot_histogram(counts, title=title, filename=f"histogram_real_counts_{job_id}", figsize=(12, 8))


def main():
    """ main function to build the circuit for the oracle

    * Assert the arguments, need 1: 'constant', 'balanced' or 'eval'
    * Get the oracle function depending on the choice
    * Compile the oracle function to use it in the algorithm
    * Run the circuit on a simulator
    * Gives the choice to run the circuit on a real computer
    """

    assert len(sys.argv) == 2, f"{RED}Expect one argument: 'constant', 'balanced' or 'eval' if it's implemented{RESET}"

    assert sys.argv[1] == "constant" or sys.argv[1] == "balanced" or sys.argv[1] == "eval", \
            f"{RED}Expect a valid argument: 'constant', 'balanced' or 'eval' if it's implemented{RESET}"

    choice = sys.argv[1]

    if choice == "constant":
        oracle_function = constant_oracle_subject()
    elif choice == "balanced":
        oracle_function = balanced_oracle_subject()
    # ? FOR THE ORACLE FUNCTION GIVEN IN THE CORRECTION
    elif choice == "eval":
        # oracle_function = oracle_eval()
        # print("\nThe oracle function of the correction (view it in correction_oracle_function.png)")
        # oracle_function.draw(output="mpl", filename="correction_oracle_function")
        return

    circuit_compiled = compile_circuit(oracle_function)

    sim_run_oracle(circuit_compiled)

    real_run = input(f"{BLUE}Do you want to run this circuit on a real quantum computer ? (y or n): {RESET}")

    if real_run == "y":
        real_run_oracle(circuit_compiled)
    else:
        print("\nFine, this is the end of this run of the Deutsch-Jozsa algorithm\n")


if __name__ == "__main__":
    main()
