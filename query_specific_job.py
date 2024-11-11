import os
from dotenv import load_dotenv

from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.visualization import plot_histogram, plot_distribution


RED = '\033[31m'
GREEN = '\033[32m'
YELLOW = '\033[33m'
BLUE = '\033[34m'
PURPLE = '\033[35m'
RESET = '\033[0m'


def load_account():
    """ Load the account associated with the token found in the .env

    * Take environment variables from .env
    * Get the TOKEN var from the .env that was loaded

    * Save the account to disk for future use using the token,
    * 'overwrite' to 'True' so that the existing account is overwritten
    """

    load_dotenv()
    token = os.getenv("TOKEN")

    QiskitRuntimeService.save_account(channel="ibm_quantum", token=token, overwrite=True)
    print(f"{GREEN}Account loaded !\n\n{RESET}")


def query_job():
    """Query all jobs of the account and propose the choice to get more info on one"""

    # * Try to get a service instance, need to have the IBMQ account loaded
    # * If not loaded, call load_account()
    try:
        service = QiskitRuntimeService(instance="ibm-q/open/main")
        print(f"{GREEN}No exception, the account was already saved{RESET}\n\n")
    except Exception:
        print(f"{RED}Exception catched, the account was not saved and needs to be loaded{RESET}")
        load_account()
        service = QiskitRuntimeService(channel='ibm_quantum', instance="ibm-q/open/main")

    # * Get all jobs of this account and prints them
    all_jobs = service.jobs(limit=None)
    print("All jobs runned on this account:")
    for job in all_jobs:
        job_date = job.creation_date.strftime("%d %b %Y, %I:%M%p %Z")
        print(f"job runned on {YELLOW}{job.backend().name}{RESET}, id: {YELLOW}{job.job_id()}{RESET}, created at: {job_date}")

    # * Gives the choice of which job to get more data
    job_id = input(f"\n{BLUE}Prompt to get info for: {RESET}")

    # * Get the job saved under the job_id, it should be a RuntimeJobV2 object
    try:
        job = service.job(job_id)
    except Exception as e:
        print(f"{RED}{e}{RESET}")
        return

    # * If the job is valid, get the result of the first PUB of it
    job_result = job.result()[0]

    # * Get the name of the backend that runned this job
    bck_name = job.backend().name

    # * In the PubResult, get the data attribute, inside it there are the classical bits
        # * Those classical bits, depending on how the ClassicalRegister is instantiated have different names
        # * Here I try the two names that I came across my jobs: 'meas' and 'c' and store the result in
        # * 'meas' for ex04 and 'c' for deutsch-jozsa for the moment
    try:
        c_bits_data = job_result.data.meas
    except Exception:
        c_bits_data = job_result.data.c

    # * Get the number of shots used for this specific job
    shots = c_bits_data.num_shots

    # * Get the result stored in the classical bits
    pub_result = c_bits_data.get_counts()

    # * Sort the dict of the results by keys
    pub_result = dict(sorted(pub_result.items()))

    # * Print the occurences for all states with the number of shots runned with the name of the backend
    print(f"{BLUE}Measurement results info on a total of {shots} shots (runned on {bck_name}):{RESET}")
    for state, result in pub_result.items():
        print(f"\tfor the {state} state: {PURPLE}{result}{RESET}")

    # * Create a dict for the counts, for each states: number of occurences
    # * Create a dict for the percentage, for each states: number of occurences / number of shots
    result_counts = dict()
    result_percentage = dict()
    for state, result in pub_result.items():
        result_counts[state] = result
        result_percentage[state] = result / shots

    # * Print the result with a total of 1
    print(f"{BLUE}Measurement results as percentage of 1 (runned on {bck_name}):{RESET}")
    for state, result in result_percentage.items():
        print(f"\tfor the {state} state: {GREEN}{result}{RESET}")

    # * Plot the counts result in a histogram
    title = rf"Counts result of {job_id} with {shots} shots runned on {bck_name}"
    plot_histogram(result_counts, title=title, filename=f"histogram_counts_{job_id}_{bck_name}", figsize=(12, 8))

    # * Plot the percentage result in a histogram
    title = rf"Percentage result of {job_id} with {shots} shots runned on {bck_name}"
    plot_distribution(result_counts, title=title, filename=f"histogram_percentage_{job_id}_{bck_name}", figsize=(12, 8))


if __name__ == "__main__":
    query_job()
