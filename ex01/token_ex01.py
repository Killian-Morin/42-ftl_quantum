import os
from dotenv import load_dotenv

from qiskit_ibm_runtime import QiskitRuntimeService

def load_account():
    load_dotenv()
    token = os.getenv("TOKEN")
    # Save the account to disk for future use.
    QiskitRuntimeService.save_account(channel="ibm_quantum", token=token, overwrite=True)

load_account()

# Initialize your account with the specified instance to be used
service = QiskitRuntimeService(instance="ibm-q/open/main")

backends = service.backends()

underline = '\033[04m'
blue = '\033[34m'
purple = '\033[35m'
reset = '\033[0m'

print(blue, "Backends accessible with this account:", reset)
for bck in backends:
    if bck.simulator:
        bck_type = "simulated"
    else:
        bck_type = "real"
    status = bck.status()
    date = bck.online_date.strftime("%d %b %Y, %I:%M%p")
    processor_type = bck.processor_type["family"]
    print(f"\t{purple}{bck.name}{reset} | " +
            f"{underline}{bck_type}{reset} quantum computer | " +
            f"pending jobs: {underline}{status.pending_jobs}{reset} | " +
            f"total number of qubits: {underline}{bck.num_qubits}{reset} | " +
            f"went online on {underline}{date}{reset} | " +
            f"type of processor: {underline}{processor_type}{reset}")
