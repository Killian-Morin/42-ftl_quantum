from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
import numpy as np


NB_QUBITS = 4


def constant_oracle_subject():
    """
    The constant oracle from the subject exemple

    Creation steps:
        - Create the QuantumCircuit with 4 qubits
        - Apply an X gate on the last qubit: q_3
        - Draw the circuit
        - Return this circuit
    """
    qc = QuantumCircuit(NB_QUBITS)
    qc.x(NB_QUBITS - 1)

    qc.draw(output='mpl', filename="constant_oracle_subject")

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
    qc = QuantumCircuit(NB_QUBITS)

    qc.x([0, 1, 2])

    qc.cx(0, 3)
    qc.cx(1, 3)
    qc.cx(2, 3)

    qc.x([0, 1, 2])

    qc.draw(output='mpl', filename="balanced_oracle_subject")

    return qc


def deutsch_jozsa_oracle_function():
    """
    Create a random Deutsch-Jozsa function.

    Creation steps:
        - Create the circuit with 4 qubits
        - On a 50% chance, apply an X gate on q_3, this create a constant function
        - On a 50% chance return this circuit, making the constant oracle
    """
    num_qubits = 4  # 3 input qubits + 1 output qubit
    qc = QuantumCircuit(num_qubits)

    # Randomly decide if the oracle will be constant
    if np.random.randint(0, 2):
        # Flip output qubit with 50% chance
        qc.x(num_qubits - 1)
    if np.random.randint(0, 2):
        # Return constant circuit with 50% chance
        return qc

    # If not constant, create a balanced function
    # Choose half of the possible input states (2^(3) = 8 states)
    on_states = np.random.choice(
        range(2**(num_qubits - 1)),  # numbers to sample from (0 to 7)
        2**(num_qubits - 1) // 2,    # number of samples (8 / 2 = 4)
        replace=False                # ensures states are sampled only once
    )

    def add_cx(qc, bit_string):
        for qubit, bit in enumerate(reversed(bit_string)):
            if bit == "1":
                qc.x(qubit)
        return qc

    for state in on_states:
        qc.barrier()  # Barriers help visualize the function creation, optional
        bit_string = f"{state:03b}"  # Convert state to a 3-bit binary string
        qc = add_cx(qc, bit_string)  # Prepare the qubits in the input state
        qc.mcx(list(range(num_qubits - 1)), num_qubits - 1)  # Apply the controlled-NOT
        qc = add_cx(qc, bit_string)  # Uncompute the input state

    qc.barrier()
    return qc


def deutsch_jozsa_oracle_algo(function: QuantumCircuit):
    oracle = deutsch_jozsa_oracle_function()
    n = oracle.num_qubits - 1
    qc = QuantumCircuit(n + 1, n)

    # Initialize the circuit
    qc.x(n)
    qc.h(range(n + 1))

    # Apply the oracle
    qc.compose(oracle, inplace=True)

    # Apply Hadamard gates to input qubits
    qc.h(range(n))

    # Measure the input qubits
    qc.measure(range(n), range(n))

    return qc


def compile_circuit(function: QuantumCircuit):
    """
    Compiles a circuit for use in the Deutsch-Jozsa algorithm.

    n represent the number of input qubits
    the oracle has n input qubits and 1 output qubits

    Compile steps:
        - Create a temporary circuit with 5 qubits (4 input and 1 output) and 3 classical bits
        - Apply an X gate on q_3, his state is ∣1⟩
        - Apply Hadamard gates to all qubits, each qubits are put in equal superposition state
        - Take the oracle function and apply it to the current circuit
        - Apply Hadamard gates to the input qubits,
            the state is transformed to an all-zero state (constant function)
            or a superposition state (balanced function)
        - Measure the input qubits and store the result in the classical bits
    """
    n = function.num_qubits - 1
    qc = QuantumCircuit(n + 1, n)
    qc.x(n)
    qc.h(range(n + 1))
    qc.compose(function, inplace=True)
    qc.h(range(n))
    qc.measure(range(n), range(n))
    return qc


def deutsch_jozsa_algorithm(function: QuantumCircuit):
    """
    Determine if a Deutsch-Jozsa function is constant or balanced.
    """
    qc = compile_circuit(function)

    result = AerSimulator().run(qc, shots=1, memory=True).result()
    measurements = result.get_memory()
    if "1" in measurements[0]:
        return "balanced"
    return "constant"

# f = deutsch_jozsa_function(3)
# print(f.draw())
# print(deutsch_jozsa_algorithm(f))

f = deutsch_jozsa_oracle_function()
# print(deutsch_jozsa_oracle_algo(f))
print(f.draw())
print(deutsch_jozsa_algorithm(f))

# constant_oracle_subject()
# print("\n")
# balanced_oracle_subject()
