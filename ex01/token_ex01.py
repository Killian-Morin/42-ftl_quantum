import os
from dotenv import load_dotenv

from qiskit_ibm_runtime import QiskitRuntimeService

load_dotenv()

token = os.getenv("TOKEN")

# Save the account to disk for future use.
QiskitRuntimeService.save_account(channel="ibm_quantum", token=token, overwrite=True)

# Initialize your account with the specified instance to be used
service = QiskitRuntimeService(instance="ibm-q/open/main")

backends = service.backends()

print("Backends accessible with this account: ")
for el in backends:
    if el.simulator:
        el_type = "simulated"
    else:
        el_type = "real"
    status = el.status()
    date = el.online_date.strftime("%d %b %Y, %I:%M%p")
    processor_type = el.processor_type["family"]
    print(f"\t{el.name} | {el_type} quantum computer | pending jobs: {status.pending_jobs} | total number of qubits: {el.num_qubits} | went online on {date} | type of processor: {processor_type}")
