FROM python:3.11-slim

# Install Docker CLI (docker-ce-cli via Docker official repo), ansible and tools
RUN apt-get update && apt-get install -y --no-install-recommends \
    ca-certificates curl gnupg lsb-release apt-transport-https \
    && mkdir -p /etc/apt/keyrings \
    && curl -fsSL https://download.docker.com/linux/debian/gpg | gpg --dearmor -o /etc/apt/keyrings/docker.gpg \
    && echo "deb [arch=$(dpkg --print-architecture) signed-by=/etc/apt/keyrings/docker.gpg] https://download.docker.com/linux/debian $(lsb_release -cs) stable" \
       > /etc/apt/sources.list.d/docker.list \
    && apt-get update && apt-get install -y --no-install-recommends \
       docker-ce-cli sshpass git build-essential python3-pip \
    && pip3 install --no-cache-dir ansible flask requests \
    && apt-get clean && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY webhook.py /app/webhook.py
COPY playbooks /app/playbooks

EXPOSE 5001
CMD ["python3", "/app/webhook.py"]

