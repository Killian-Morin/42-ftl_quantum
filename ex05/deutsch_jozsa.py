import os
import numpy as np
from dotenv import load_dotenv

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.visualization import plot_histogram
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


NB_QUBITS = 4

RESET = '\033[0m'
GREEN = '\033[32m'
RED = '\033[31m'
ORANGE = '\033[33m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
PINK = '\033[95m'


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
    * Apply three CNOT control gate with q_3 as the control and q_0, q_1 and q_2 as the target
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


def create_new_oracle_function():
    """ Create a new random oracle function

    * Create a quantum circuit with 4 qubits, 3 input qubits and 1 addditional output qubit
    * np.random.randint(0, 2) return 0 or 1, so 50% chance to enter in both if
    * 50% chance of applying an X gate to the output qubit (q_3), flips it to ∣1⟩
        * 50% chance of returning the circuit as this, making it a constant oracle
        * The constant oracle circuit is created and saved as constant_oracle_created.png
    * The next lines of code create a random balanced oracle,
        * explicative comments on each part (since pretty dense)

    * It finally prints, saves the balanced function under 'balanced_oracle_created.png'
        * and returns the created balanced circuit

    Return
    -----
        qc (QuantumCircuit): representation of the balanced or constant oracle quantum circuit
    """

    nb_qubits = 3

    qc = QuantumCircuit(nb_qubits + 1)

    if np.random.randint(0, 2):
        qc.x(nb_qubits)
    if np.random.randint(0, 2):
        print("Created a random constant oracle function")
        qc.draw(output="mpl", filename="constant_oracle_created")
        return qc

    # * nb.random.choice() to select half of the possible input states (2^(3) = 8 states)
    # * range(2**nb_qubits) -> generates all possible states for the input qubits (from 0 to 2^(nb_qubits) - 1 so 7)
    # * 2**nb_qubits // 2 -> calculates half of these states (8 / 2 = 4)
    # * replace=False -> so that each state are only sampled once
    on_states = np.random.choice(
        range(2**nb_qubits),
        2**nb_qubits // 2,
        replace=False,
    )

    # * Helper function that applies X gates to specific qubits based on a bit string
    # * take the circuit and a bit string as parameter
    # * iterates over the bit string and for each bit that is '1' apply an X gate to the corresponding qubit
    # * the bit string is reversed to match the qubit numbering
    def add_cx(qc, bit_string):
        for qubit, bit in enumerate(reversed(bit_string)):
            if bit == "1":
                qc.x(qubit)
        return qc

    # * For each state, a barrier is added for visualization (optional)
    # * Call add_cx to prepare the qubit in the state specified by the binary representation of the state,
    # *     f"{state:0b}" to convert the state to a binary string
    # * Apply a multi-controlled X gate (MCX) to flip the output qubit if all input qubits are in the specified state
    # * Call add_cx again to uncompute the input state, this returns the input qubits to the ∣0⟩ state
    for state in on_states:
        qc.barrier()
        qc = add_cx(qc, f"{state:0b}")
        qc.mcx(list(range(nb_qubits)), nb_qubits)
        qc = add_cx(qc, f"{state:0b}")

    # * Add a barrier for visualization (optional)
    qc.barrier()

    # * Draw and return the balanced circuit
    print(f"{GREEN}Created a random balanced oracle function{RESET}")
    qc.draw(output="mpl", filename="balanced_oracle_created")
    return qc


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
    * Add a barrier for visualization (optional)
    * Draw the temporary circuit before composing it with the oracle, saved as 'temp_circuit.png'
    * Take the oracle function and apply it to the current circuit
    * This apply the instructions of the oracle onto the current circuit
    * Apply Hadamard gates to the input qubits
    * The state is transformed to an all-zero state (constant function) or a superposition state (balanced function)
    * Measure the input qubits and store the result in the classical bits
    * Draw the circuit obtained by the composition, saved as 'composed_circuit.png'

    Return
    -----
        qc (QuantumCircuit): representation of the composed oracle function
    """
    n = NB_QUBITS - 1

    qc = QuantumCircuit(n + 1, n)

    qc.x(n)

    qc.h(range(n + 1))

    qc.barrier()

    qc.draw(output="mpl", filename="temp_circuit")

    qc.compose(oracle_function, inplace=True)

    qc.h(range(n))

    qc.measure(range(n), range(n))

    qc.draw(output="mpl", filename="composed_circuit")

    print(f"{GREEN}Composed the instructions of the oracle on a circuit to use it in the Deutsch-Jozsa algorithm{RESET}")

    return qc


def sim_run_algo(oracle_function):
    """ Run the Oracle on a simulator

    Param
    -----
        oracle_function (QuantumCircuit): the circuit of the oracle function

    * Get an AerSimulator, the method used is automatically selected based on the circuit and noise model
    * Run the composed circuit on a AerSimulator with 1 shot
        * with the memory parameter to true in order to have the outcome of the shot as a list
    * Get the type of AerSimulator that was used
    * Get the outcome of the first and only shot
    * Deduce the type of the oracle function (the qubits are in state ∣1⟩ = balanced or in state ∣0⟩ = constant)
    * Plot the counts result, saved as 'histogram_sim_result'
    """

    print("\nThis will run the circuit on a Qiskit Aer simulator ...")

    sim = AerSimulator(method='automatic')

    result = sim.run(oracle_function, shots=1, memory=True).result()

    sim_type = result.results[0].metadata['method']
    print(f"The type of AerSimulator used was {PURPLE}{sim_type} {RESET}\n")

    measurements = result.get_memory()
    counts = result.get_counts()

    if "1" in measurements[0]:
        print(f"RESULT - SIMULATOR: The function is {ORANGE}balanced{RESET}, qubits at 1 !\n")
    else:
        print(f"RESULT - SIMULATOR: The function is {ORANGE}constant{RESET}, qubits at 0 !\n")

    plot_histogram(counts, title=f"Result of the simulation of type {sim_type}", filename="histogram_sim_result")


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
        load_dotenv()
        token = os.getenv("TOKEN")
        service = QiskitRuntimeService(channel='ibm_quantum', instance="ibm-q/open/main", token=token)
        QiskitRuntimeService.save_account(channel="ibm_quantum", token=token, overwrite=True)

    print("Get the least busy and operational quantum computer ...")
    backend = service.least_busy(operational=True, simulator=False)
    print(f"It's {PURPLE}{backend.name}{RESET}\n")

    return backend


def real_run_algo(oracle_function):
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

    isa_circuit.draw('mpl', idle_wires=False, filename="circuit_optimized")

    sampler = Sampler(bck)

    job = sampler.run([isa_circuit], shots=1)

    job_id = job.job_id()

    print(f"Job ID: {job_id}\n")
    print(f"Job Status: {job.status()}\n")

    result = job.result()[0]

    pub_result = result.data.c.get_counts()

    print(f"{RED}{result.get_counts()}{RESET}")
    print(f"{RED}{pub_result}{RESET}")

    title = f"Result of {job_id} runned on {bck.name} real quantum computer"
    plot_histogram(pub_result, title=title, filename=f"histogram_real_result_{job_id}")


def main():
    """ main function to determine what oracle to use, then run the circuit

    * Gives the choice of using the constant, balanced oracle of the subject,
        * create a new oracle function or the function provided in the correction
    * Get the oracle function depending on the choice
    * Compile the oracle function to use it in the algorithm
    * Run the circuit on a simulator
    * Gives the choice to run the circuit on a real computer
    """

    print(f"{BLUE}What oracle function do you want to use ? Options are:{RESET}")
    print(f"\tconstant oracle from the subject ({PINK}option 1{RESET})")
    print(f"\tbalanced oracle from the subject ({PINK}option 2{RESET})")
    print(f"\tcreate a new oracle function that has a 50% percent chance of being constant or balanced ({PINK}option 3{RESET})")
    print(f"\tthe function that will be provided from the correction ({PINK}option 4{RESET})")

    choice = input()

    if choice == "1":
        oracle_function = constant_oracle_subject()
    elif choice == "2":
        oracle_function = balanced_oracle_subject()
    elif choice == "3":
        oracle_function = create_new_oracle_function()
    # ? FOR THE ORACLE FUNCTION GIVEN IN THE CORRECTION
    # elif choice == "4":
    #     oracle_function = FUNCTION CALL
    #     print("\nThe oracle function of the correction (view it in correction_oracle_function.png)")
    #     oracle_function.draw(output="mpl", filename="correction_oracle_function")
    else:
        os.system("clear")
        print(f"{RED}Please try again\n\n{RESET}")
        main()

    circuit_compiled = compile_circuit(oracle_function)

    sim_run_algo(circuit_compiled)

    real_run = input(f"{BLUE}Do you want to run this circuit on a real quantum computer ? (y or n): {RESET}")

    if real_run == "y":
        real_run_algo(circuit_compiled)
    else:
        print("\nFine, this is the end of this run of the Deutsch-Jozsa algorithm\n")


if __name__ == "__main__":
    main()
