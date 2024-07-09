import os
from dotenv import load_dotenv

from qiskit_ibm_runtime import QiskitRuntimeService

load_dotenv()

token = os.getenv("TOKEN")

QiskitRuntimeService.save_account(channel="ibm_quantum", token=token, overwrite=True)

# Initialize your account
service = QiskitRuntimeService(instance="ibm-q/open/main")

backends = service.backends()

print("Backends accessible with this account full detail: ")
for el in backends:
    if el.simulator:
        el_type = "simulated"
    else:
        el_type = "real"
    status = el.status()
    print(f"\t{el.name} is a {el_type} quantum computer, with {status.pending_jobs} pending jobs and a total of {el.num_qubits} qubits.")
