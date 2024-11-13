FROM python:3.9-bullseye

WORKDIR /usr/src/app/

RUN pip install --upgrade pip

RUN pip install python-dotenv

RUN pip install --no-cache-dir \
    qiskit \
    'qiskit[visualization]' \
    qiskit_aer \
    qiskit_ibm_runtime \
    matplotlib \
    ipython

# Copy relevant files into the container at /usr/src/app
COPY ./exercices ./exercices
COPY .env ./.env

# Command to keep the container running (not necessary with the docker-compose)
# CMD ["tail", "-f", "/dev/null"]