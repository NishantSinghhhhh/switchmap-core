# I'm using a lightweight and compatible Python base image to keep the container small and efficient
FROM python:3.11-slim

# I'm setting up environment variables to optimize Python behavior and caching
ENV DEBIAN_FRONTEND=noninteractive \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PATH="/home/switchmap-core/core/venv/bin:$PATH" \
    PYTHONPATH="/home/switchmap-core/core"

# I'm creating a dedicated non-root user to improve container security
RUN groupadd -r switchmap && useradd --no-log-init -r -g switchmap switchmap

# I'm setting the working directory to ensure all operations are executed in a structured location
WORKDIR /home/switchmap-core/core

# I'm installing the essential system dependencies required for PostgreSQL interaction and compiling any required libraries
RUN apt-get update && apt-get install -y --no-install-recommends \
    libpq-dev \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# I'm creating a virtual environment to isolate Python dependencies and avoid polluting the global environment
RUN python3 -m venv venv

# I'm copying the dependency file separately so that Docker can cache this step efficiently
COPY requirements.txt .

# I'm installing Python dependencies inside the virtual environment, ensuring no unnecessary caching
RUN pip install --no-cache-dir -r requirements.txt

# I'm copying the entire Core source code into the container
COPY . .

# I'm making sure that logs and config directories exist with the correct permissions
RUN mkdir -p /etc/switchmap-core /var/log/switchmap-core && \
    chmod -R 755 /var/log/switchmap-core

# I'm copying the configuration file to its expected location inside the container
COPY examples/etc/config.yaml /etc/switchmap-core/config.yaml

# I'm copying the entrypoint script and making it executable to ensure the container starts correctly
COPY entrypoint.sh /home/switchmap-core/core/entrypoint.sh
RUN chmod +x /home/switchmap-core/core/entrypoint.sh

# I'm switching to the non-root user to prevent security vulnerabilities
USER switchmap


# I'm setting the entrypoint so the container starts with the correct command
ENTRYPOINT ["/home/switchmap-core/core/entrypoint.sh"]
