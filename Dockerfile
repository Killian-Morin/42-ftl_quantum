FROM python:3.9-bullseye

WORKDIR /usr/src/app

# Install system dependencies | not necessary
# RUN apt-get update \
#     && apt-get install -y build-essential \
#     && rm -rf /var/lib/apt/lists/*

RUN pip install --upgrade pip

RUN pip install python-dotenv

RUN pip install --no-cache-dir \
    qiskit \
    'qiskit[visualization]' \
    qiskit_aer \
    qiskit_ibm_runtime \
    matplotlib \
    ipython

# Copy '.' into the container at /usr/src/app
COPY . .

# Add a command to keep the container running. This can be a simple command like tail -f /dev/null
CMD ["tail", "-f", "/dev/null"]