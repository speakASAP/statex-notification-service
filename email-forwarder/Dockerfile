FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y \
    postfix \
    mailutils \
    && rm -rf /var/lib/apt/lists/*

# Copy Python script
COPY forwarder.py .

# Install Python dependencies
RUN pip install --no-cache-dir requests

# Run the forwarder
CMD ["python", "forwarder.py"]
