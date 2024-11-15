import os
from dotenv import load_dotenv
from print_color import print

from qiskit_ibm_runtime import QiskitRuntimeService


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


def process_data(service):
    """ Print data from the service available

    * Get all backends accessible via this account

    * Print relevent information for each backend obtained
    """

    backends = service.backends()

    print("Backends accessible with this account:", color='blue')
    for bck in backends:
        if bck.simulator:
            bck_type = "simulated"
        else:
            bck_type = "real"
        status = bck.status()
        date = bck.online_date.strftime("%d %b %Y, %I:%M%p %Z")
        processor_type = bck.processor_type["family"]

        print(f"\t{bck.name}", color='purple', end=' | ')
        print(bck_type, format='underline', end=' ')
        print("quantum computer | pending jobs: ", end=' ')
        print(status.pending_jobs, color='cyan', end=' | ')
        print("total number of qubits: ", end=' ')
        print(bck.num_qubits, color='cyan', end=' | ')
        print(f"went online on {date} | type of processor: {processor_type}")


def main():
    """
    * Try to get a service instance, need to have the IBMQ account loaded
    * If not loaded, call load_account()

    * process_data(service) will print the information about the services available
    """

    try:
        service = QiskitRuntimeService(instance="ibm-q/open/main")
        print("No exception, the account was already saved\n", tag='success', tag_color='green', color='white')
    except Exception:
        print("The account was not saved and needs to be loaded\n", tag='exception', tag_color='red', color='white')
        load_account()
        service = QiskitRuntimeService(instance="ibm-q/open/main")

    process_data(service)


if __name__ == "__main__":
    main()
