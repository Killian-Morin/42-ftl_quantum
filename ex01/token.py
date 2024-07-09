from qiskit import IBMQ

# Cannot import load_dotenv so hard code the token
token = ''

IBMQ.save_account(token, overwrite=True)

provider = IBMQ.get_provider(hub="h1", group="g1", project="p1")
