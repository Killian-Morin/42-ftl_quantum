import os
import numpy as np

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit.visualization import plot_histogram


NB_QUBITS = 4

reset = '\033[0m'
red = '\033[31m'
blue = '\033[34m'
purple = '\033[35m'


def constant_oracle_subject():
    """
    The constant oracle from the subject exemple

    Creation steps:
        - Create the QuantumCircuit with 4 qubits
        - Apply an X gate on the last qubit: q_3
        - Draw the circuit
        - Return this circuit
    """
    print("\nThis create the constant oracle function of the subject (view it in constant_oracle_subject.png)")

    qc = QuantumCircuit(NB_QUBITS)
    qc.x(NB_QUBITS - 1)

    qc.draw(output="mpl", filename="constant_oracle_subject")

    return qc


def balanced_oracle_subject():
    """
    The balanced oracle from the subject exemple

    Creation steps:
        - Create the QuantumCircuit with 4 qubits
        - Apply an X gate on the first 3 qubits: q_0, q_1 and q_2
        - Apply three CNOT control gate with q_3 as the control and q_0, q_1 and q_2 as the target
        - Apply again an X gate on the first 3 qubits: q_0, q_1 and q_2
        - Draw the circuit
        - Return this circuit
    """
    print("\nThis create the balanced oracle function of the subject (view it in balanced_oracle_subject.png)")

    qc = QuantumCircuit(NB_QUBITS)

    qc.x([0, 1, 2])

    qc.cx(0, 3)
    qc.cx(1, 3)
    qc.cx(2, 3)

    qc.x([0, 1, 2])

    qc.draw(output="mpl", filename="balanced_oracle_subject")

    return qc


def create_new_oracle_function():
    """
    Steps:
        - Create a quantum circuit with 4 qubits, 3 input qubits and 1 addditional output qubit
        - np.random.randint(0, 2) return 0 or 1,
                the first if has a 50% chance to apply an X gate to the output qubit (q_3), it flips to ∣1⟩
                the second if has a 50% chance of returning the circuit as this, thus making it a constant oracle
        - since we continue it will create a balanced oracle
                nb.random.choice() to select half of the possible input states (2^(3) = 8 states)
                range(2**nb_qubits) generates all possible states for the input qubits (from 0 to 2^(nb_qubits) - 1)
                2**nb_qubits // 2 calculates half of these states
                replace=false so that each state are only sampled once
        - helper function, add_cx that applies X gates to specific qubits based on a bit string
                take the circuit and a bit string as input
                the for loop iterates over the bit string and for each bit that is '1',
                    it applies an X gate to the corresponding qubit in the circuit
                the bit string is reversed to match the qubit numbering
        - in the for loop iterating over on_states
                for each state, a barrier is added for visualization
                call add_cx to prepare the qubits in the state specified by the binary representation of the state,
                    f"{state:0b}" to convert the state to a binary string
                apply a multi-controlled X gate (MCX) to flip the output qubit if all input qubits are in the specified state
                call add_cx again to uncompute the input state, this returns the input qubits to the ∣0⟩ state
        - add a barrier and return the quantum circuit
    """
    print("\nThis create a new oracle function with a 50%/50% chance of being constant or balanced ...")

    nb_qubits = 3
    qc = QuantumCircuit(nb_qubits + 1)

    if np.random.randint(0, 2):
        qc.x(nb_qubits)
    if np.random.randint(0, 2):
        print("\nA constant function was created (view it in constant_oracle_created.png)")
        qc.draw(output="mpl", filename="constant_oracle_created")
        return qc

    on_states = np.random.choice(
        range(2**nb_qubits),  # numbers to sample from (0 to 7)
        2**nb_qubits // 2,  # number of samples (8 / 2 = 4)
        replace=False,  # makes sure states are only sampled once
    )

    def add_cx(qc, bit_string):
        for qubit, bit in enumerate(reversed(bit_string)):
            if bit == "1":
                qc.x(qubit)
        return qc

    for state in on_states:
        qc.barrier()  # Barriers to help visualize how the functions are created
        qc = add_cx(qc, f"{state:0b}")
        qc.mcx(list(range(nb_qubits)), nb_qubits)
        qc = add_cx(qc, f"{state:0b}")

    qc.barrier()

    print("\nA balanced function was created (view it in balanced_oracle_created.png)")
    qc.draw(output="mpl", filename="balanced_oracle_created")
    return qc


def compile_circuit(function: QuantumCircuit):
    """
    Compiles a circuit for use in the Deutsch-Jozsa algorithm.

    n represent the number of input qubits
    the oracle has n input qubits and 1 output qubits

    Compile steps:
        - Create a temporary circuit with 4 qubits (3 input and 1 output) and 3 classical bits (measurements)
        - Apply an X gate to the output qubit q_3, his state is ∣1⟩
        - Apply Hadamard gates to all qubits, each qubits are put in equal superposition state
        - Take the oracle function and apply it to the current circuit,
            apply the instructions of the oracle onto the circuit created
        - Apply Hadamard gates to the input qubits,
            the state is transformed to an all-zero state (constant function)
            or a superposition state (balanced function)
        - Measure the input qubits and store the result in the classical bits
    """
    print("\nThis will compose/apply the instructions of the oracle on a temporary circuit (view it in temp_circuit.png and the composed circuit in composed_circuit.png)")

    n = NB_QUBITS - 1

    qc = QuantumCircuit(n + 1, n)

    qc.x(n)

    qc.h(range(n + 1))

    qc.barrier()

    qc.draw(output="mpl", filename="temp_circuit")

    qc.compose(function, inplace=True)

    qc.h(range(n))

    qc.measure(range(n), range(n))

    qc.draw(output="mpl", filename="composed_circuit")

    return qc


def sim_run_algo(function: QuantumCircuit):
    """
    Steps:
        - Get an AerSimulator, the method used is automatically selected based on the circuit and noise model
        - Run the composed circuit on a AerSimulator with 1 shot
            and with the memory parameter to true in order to have the outcome of the shot as a list
        - Get the type of AerSimulator that was used
        - Get the outcome of the first and only shot
        - Deduce the type of the oracle function (the qubits are in state ∣1⟩ = balanced or in state ∣0⟩ = constant)
    """
    print("\nThis will run the circuit on a Qiskit Aer simulator ...")

    sim = AerSimulator(method='automatic')

    result = sim.run(function, shots=1, memory=True).result()

    sim_type = result.results[0].metadata['method']
    print(f"The type of AerSimulator used was {purple}{sim_type} {reset}\n")

    measurements = result.get_memory()

    counts = result.get_counts()

    if "1" in measurements[0]:
        print(f"The function is {purple}balanced{reset}!\n")
    else:
        print(f"The function is {purple}constant{reset}!\n")

    plot_histogram(counts, filename="histogram_result")


def real_run_algo(function: QuantumCircuit):
    """
    """
    print("\nThis will run the circuit on a real quantum computer ...")


# f = deutsch_jozsa_function(3)
# print(f.draw())
# print(deutsch_jozsa_algorithm(f))


def main():
    print(f"{blue}What oracle function do you want to use ? Options are:{reset}")
    print("\tconstant oracle from the subject (option 1)")
    print("\tbalanced oracle from the subject (option 2)")
    print("\tcreate a new oracle function that has a 50% percent chance of being constant or balanced (option 3)")
    print("\tthe function that will be provided from the correction (option 4)")

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
        print(f"{red}Please try again\n\n{reset}")
        main()

    circuit_compiled = compile_circuit(oracle_function)

    sim_run_algo(circuit_compiled)

    print(f"{blue}Do you want to run this circuit on a real quantum computer ? (y or n){reset}")
    real_run = input()

    if real_run == "y":
        real_run_algo(circuit_compiled)
    else:
        print("\nFine, this is the end of this run of the Deutsch-Jozsa algorithm\n")


if __name__ == "__main__":
    main()
