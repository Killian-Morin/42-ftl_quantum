FROM python:3.9-bullseye

WORKDIR /usr/src/app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir \
    qiskit==0.39.5 \
    'qiskit[visualization]' \
    qiskit_aer \
    qiskit_ibmq_provider \
    qiskit_terra \
    matplotlib \
    python-dotenv

# Copy '.' into the container at /usr/src/app
COPY . .

# Add a command to keep the container running. This can be a simple command like tail -f /dev/null
CMD ["tail", "-f", "/dev/null"]