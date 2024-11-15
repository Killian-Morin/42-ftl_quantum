FROM python:3.9-bullseye

WORKDIR /usr/src/app/

RUN pip install --upgrade pip

# Copy the requirements for the build
COPY ./requirements.txt ./requirements.txt

# Install uv, a fast python package manager
RUN pip install --no-cache-dir uv

# Install the dependencies from the requirements.txt using uv
RUN uv pip install --no-cache-dir --system -r ./requirements.txt

# Copy relevant files into the container at /usr/src/app
COPY ./exercices ./exercices
COPY .env ./.env

# No CMD instruction to keep the container running
# the command that does that is specified in the docker-compose.yml
