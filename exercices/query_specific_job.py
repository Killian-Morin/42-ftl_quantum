import os
from dotenv import load_dotenv
from print_color import print

from qiskit_ibm_runtime import QiskitRuntimeService
from qiskit.visualization import plot_histogram, plot_distribution


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
    print("Account loaded !\n", tag='success', tag_color='green', color='white')


def query_job():
    """Query all jobs of the account and propose the choice to get more info on one"""

    # * Try to get a service instance, need to have the IBMQ account loaded
    # * If not loaded, call load_account()
    try:
        service = QiskitRuntimeService(instance="ibm-q/open/main")
        print("No exception, the account was already saved\n", tag='success', tag_color='green', color='white')
    except Exception:
        print("The account was not saved and needs to be loaded\n", tag='exception', tag_color='red', color='white')
        load_account()
        service = QiskitRuntimeService(channel='ibm_quantum', instance="ibm-q/open/main")

    # * Get all jobs of this account and prints them
    all_jobs = service.jobs(limit=None)
    print("All jobs runned on this account:")
    for job in all_jobs:
        job_date = job.creation_date.strftime("%d %b %Y, %I:%M%p %Z")
        print("job runned on ", end='')
        print(job.backend().name, format='underline', end='')
        print(", id: ", end='')
        print(job.job_id(), color='yellow', end='')
        print(", created at: ", end='')
        print(job_date)

    # * Gives the choice of which job to get more data
    print("Which job to get results from", color="cyan", tag='prompt', end=': ')
    job_id = input()

    # * Get the job saved under the job_id, it should be a RuntimeJobV2 object
    try:
        job = service.job(job_id)
    except Exception as e:
        print(e, tag='exception', tag_color='red')
        return

    # * If the job is valid, get the result of the first PUB of it
    job_result = job.result()[0]

    # * Get the name of the backend that runned this job
    bck_name = job.backend().name

    # * In the PubResult, get the data attribute, inside it there are the classical bits
        # * Those classical bits, depending on how the ClassicalRegister is instantiated have different names
        # * Here I try the two names that I came across my jobs: 'meas' and 'c'
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
    print(f"\nMeasurement results on a total of {shots} shots (runned on {bck_name})", color='blue')
    for state, result in pub_result.items():
        print(f"\tfor the state {state}", end=': ')
        print(result, color='purple', end=" (")
        print(result / shots, color='green', end=")\n")

    # * Plot the results with an histogram (count)
    title = rf"Count result of {job_id} with {shots} shots runned on {bck_name}"
    plot_histogram(pub_result, title=title, filename=f"histogram_{job_id}_{bck_name}", figsize=(12, 8))

    # * Plot the results with a distribution (percentage)
    title = rf"Percentage result of {job_id} with {shots} shots runned on {bck_name}"
    plot_distribution(pub_result, title=title, filename=f"distribution_{job_id}_{bck_name}", figsize=(12, 8))


if __name__ == "__main__":
    query_job()
