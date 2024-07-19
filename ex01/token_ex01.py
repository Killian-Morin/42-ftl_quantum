import os
from dotenv import load_dotenv

from qiskit_ibm_runtime import QiskitRuntimeService


UNDERLINE = '\033[04m'
RED = '\033[31m'
GREEN = '\033[32m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
RESET = '\033[0m'


def load_account():
    # * Take environment variables from .env
    load_dotenv()

    # * Get the TOKEN var from the .env that was loaded
    token = os.getenv("TOKEN")

    # * Save the account to disk for future use using the token,
    # * 'overwrite' to 'True' so that the existing account is overwritten
    QiskitRuntimeService.save_account(channel="ibm_quantum", token=token, overwrite=True)
    print(f"{GREEN}Account loaded !\n\n{RESET}")


def process_data(service):
    # * Get all backends accessible via this account
    backends = service.backends()

    # * Print relevent information for each backend obtained
    print(f"{BLUE}Backends accessible with this account:{RESET}")
    for bck in backends:
        if bck.simulator:
            bck_type = "simulated"
        else:
            bck_type = "real"
        status = bck.status()
        date = bck.online_date.strftime("%d %b %Y, %I:%M%p %Z")
        processor_type = bck.processor_type["family"]
        print(f"\t{PURPLE}{bck.name}{RESET} | " +
                f"{UNDERLINE}{bck_type}{RESET} quantum computer | " +
                f"pending jobs: {UNDERLINE}{status.pending_jobs}{RESET} | " +
                f"total number of qubits: {UNDERLINE}{bck.num_qubits}{RESET} | " +
                f"went online on {UNDERLINE}{date}{RESET} | " +
                f"type of processor: {UNDERLINE}{processor_type}{RESET}")


def main():
    # * Try to get an instance, need to have the IBMQ account loaded
    # * If not loaded, call load_account()
    try:
        service = QiskitRuntimeService(instance="ibm-q/open/main")
        print(f"{GREEN}No exception, the account was already saved{RESET}\n\n")
    except Exception:
        print(f"{RED}Exception catched, the account was not saved and needs to be loaded{RESET}\n\n")
        load_account()
        service = QiskitRuntimeService(instance="ibm-q/open/main")

    process_data(service)


if __name__ == "__main__":
    main()
