import math
import os
import sys
from dotenv import load_dotenv

from qiskit import QuantumCircuit
from qiskit_aer import AerSimulator
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.circuit.library import GroverOperator, MCMT, ZGate
from qiskit.visualization import plot_distribution, plot_histogram
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager
from qiskit_ibm_runtime.fake_provider import FakeManilaV2
from qiskit import transpile


RESET = '\033[0m'
GREEN = '\033[32m'
RED = '\033[31m'
ORANGE = '\033[33m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
PINK = '\033[95m'


def get_backend_computer():
    """  Get a backend quantum computer """

    # * Try to get an instance, need to have the IBMQ account loaded
    # * If not loaded, load the token and save the account
    try:
        service = QiskitRuntimeService(instance="ibm-q/open/main")
        print(f"{GREEN}No exception, the account was already saved{RESET}\n\n")
    except Exception:
        print(f"{RED}Exception catched, the account was not saved and needs to be loaded{RESET}")
        load_dotenv()
        token = os.getenv("TOKEN")
        service = QiskitRuntimeService(channel='ibm_quantum', instance="ibm-q/open/main", token=token)
        QiskitRuntimeService.save_account(channel="ibm_quantum", token=token, overwrite=True)

    # * Get the least busy and operational backend quantum computer and print it
    print("Get the least busy and operational quantum computer ...")
    backend = service.least_busy(operational=True, simulator=False)
    backend_status = backend.status()
    print(f"It's {PURPLE}{backend.name}{RESET} ({backend_status.pending_jobs} pending jobs)\n")

    return backend


def state_initialisation(n):
    """

    Param
    -----
        n (int): the number of qubits in the circuit

    * Create a circuit with the number of qubits passed as arguments
    * Apply on all qubits an Hadamard Gate
    * Add a barrier for visualization
    * Draw the circuit that corresponds to the initiation step

    Return
    -----
        qc (QuantumCircuit): the circuit with n qubits set to ∣0⟩
    """

    qc = QuantumCircuit(n)

    for qubit in range(n):
        qc.h(qubit)

    qc.barrier()

    qc.draw(output="mpl", filename=f"state_initialisation_circuit_{n}")

    return qc


def oracle_exemple():
    """ The oracle example from the subject (for 3 qubits)

    * Create a circuit with 3 qubits
    * Apply an Hadamard gate on q_2
    * Apply a multi-controled X gate with q_0 as the first control,
        * q_1 as the second control and q_2 as the target
    * Apply an Hadamard gate on q_2
    * Draw the oracle circuit

    Return
    -----
        qc (QuantumCircuit): the circuit of the oracle
    """

    qc = QuantumCircuit(3)

    qc.h(2)

    qc.ccx(0, 1, 2)

    qc.h(2)

    qc.draw(output="mpl", filename="oracle_circuit_subject")

    return qc


def oracle_creation():
    """ Oracle function furnished by the correction
    """
    return 0


def diffuser(qc, oracle):
    """

    Params
    -----
        qc (QuantumCircuit): the circuit with all qubits set to superposition
        oracle (QuantumCircuit): the circuit of the oracle
    """

    qc.compose(oracle, inplace=True)
    # circuit_initialized.compose(oracle.power(1), inplace=True)

    qc.measure_all()
    qc.draw(output="mpl", filename="circuit_composed")

    return qc


def sim_run_search(circuit):
    """ Run the search algorithm on a simulator

    Param
    -----
        circuit (QuantumCircuit): the circuit of the oracle function

    * Get an AerSimulator, the method used is automatically selected based on the circuit and noise model
    * Run the composed circuit on a AerSimulator with 1 shot
        * with the memory parameter to true in order to have the outcome of the shot as a list
    * Get the type of AerSimulator that was used
    * Get the outcome of the shots
    * Deduce the type of the oracle function
    *   if one of the state is in ∣1⟩ then balanced or if they are none ∣0⟩ = constant)
    * Plot the counts result
    """

    print("\nThis will run the circuit on a Qiskit Aer simulator ...")

    backend = FakeManilaV2()

    transpiled_circuit = transpile(circuit, backend)
    transpiled_circuit.draw('mpl', style="iqp")

    # Run the transpiled circuit using the simulated fake backend
    sampler = Sampler(backend)
    job = sampler.run([transpiled_circuit], shots=500)
    result = job.result()[0]
    bits_name = circuit.cregs[0].name
    counts = getattr(result.data, bits_name).get_counts()

    # sim = AerSimulator(method='automatic')

    # result = sim.run(circuit, memory=True).result()

    # sim_type = result.results[0].metadata['method']
    # print(f"The type of AerSimulator used was {PURPLE}{sim_type} {RESET}\n")

    # counts = result.get_counts()

    # title=f"Counts measurement result for the simulation of type {sim_type}"
    plot_histogram(counts, title="test", filename="histogram_sim_counts", figsize=(12, 8))


def real_run_search(circuit):
    """ Run the search algorithm on real quantum hardware

    Param
    -----
        circuit (QuantumCircuit): the circuit for the search

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
    isa_circuit = pm.run(circuit)

    isa_circuit.draw('mpl', idle_wires=False, filename="circuit_optimized_for_back")

    sampler = Sampler(bck)

    job = sampler.run([isa_circuit])

    job_id = job.job_id()

    print(f"Job ID: {job_id}\n")
    print(f"Job Status: {job.status()}\n")

    result = job.result()[0]

    classical_bits_name = circuit.cregs[0].name

    counts = getattr(result.data, classical_bits_name).get_counts()

    title = f"Counts measurement result of {job_id} runned on {bck.name} real quantum computer"
    plot_histogram(counts, title=title, filename=f"histogram_real_counts_{job_id}", figsize=(12, 8))


def main():
    """ main function to do the search

    * Assert the arguments, need one for the number of qubits
    * Get the number of qubits passed as arguments, if < 2 (the minimum) take 2 by default
    * Get the circuit based on the number of qubits passed as arguments
    """

    assert len(sys.argv) == 2, f"{RED}Expect arguments: an int for the number of qubits{RESET}"

    qubits_nb = int(sys.argv[1]) if int(sys.argv[1]) >= 2 else 2

    print(f"{GREEN}Will create a circuit with {qubits_nb} qubits !{RESET}\n")

    qc = state_initialisation(qubits_nb)

    print(f"{BLUE}Created the circuit and initialized the qubits. Here's what it looks like:{RESET}")
    print(qc, "\n")

    oracle = oracle_creation()

    if oracle == 0 and qubits_nb == 3:
        oracle = oracle_exemple()
    else:
        print(f"{RED}No oracle function available and not compatible with the oracle from the exmeple{RESET}")
        return

    print(f"{PURPLE}The oracle was created. Here it is:{RESET}")
    print(oracle, "\n")

    grover_op = GroverOperator(oracle, insert_barriers=True)
    grover_op.draw(output="mpl", filename="grover_circuit")
    grover_op.decompose().draw(output="mpl", filename="grover_circuit_decompose")

    circuit = diffuser(qc, grover_op)

    sim_run_search(circuit)


if __name__ == "__main__":
    main()
