import os
from dotenv import load_dotenv

from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.visualization import plot_histogram


job_id = 'ctb7hnpdf6zg0080t7q0'

load_dotenv()
token = os.getenv("TOKEN")

service = QiskitRuntimeService(channel='ibm_quantum', instance="ibm-q/open/main", token=token)

job = service.job(job_id)
job_result = job.result()[0]

bck_name = job.backend().name

shots = job_result.data.meas.num_shots

pub_result = job_result.data.meas.get_counts()

result_percentage = {
    '00': pub_result['00'] / shots,
    '01': pub_result['01'] / shots,
    '10': pub_result['10'] / shots,
    '11': pub_result['11'] / shots
}

print(f"Measurement results info on a total of {shots} shots (runned on {bck_name}): ")
print(f"\tfor the 00 state: {pub_result['00']}")
print(f"\tfor the 01 state: {pub_result['01']}")
print(f"\tfor the 10 state: {pub_result['10']}")
print(f"\tfor the 11 state: {pub_result['11']}")

print(f"Measurement results as percentage of 1 (runned on {bck_name}):")
print(f"\tfor the 00 state: {result_percentage['00']} / 1")
print(f"\tfor the 01 state: {result_percentage['01']} / 1")
print(f"\tfor the 10 state: {result_percentage['10']} / 1")
print(f"\tfor the 11 state: {result_percentage['11']} / 1")

plot_histogram(result_percentage, title=rf"Measurement result of the $\Phi^+$ Bell state with {shots} shots runned on {bck_name})",
                filename=f"histogram_{job_id}_{bck_name}")
