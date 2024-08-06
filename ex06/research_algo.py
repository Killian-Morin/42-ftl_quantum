import math, os
from dotenv import load_dotenv

from qiskit import QuantumCircuit
from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit.circuit.library import GroverOperator, MCMT, ZGate
from qiskit.visualization import plot_distribution, plot_histogram
from qiskit.transpiler.preset_passmanagers import generate_preset_pass_manager


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
    print(f"It's {PURPLE}{backend.name}{RESET}\n")

    return backend


def main():
    print("hello")

if __name__ == "__main__":
    main()
