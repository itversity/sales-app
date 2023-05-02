FROM python:3.11

RUN apt update && apt upgrade -y
RUN apt install -y \
    telnet && \
    rm -rf /var/lib/apt/lists/*

# Deploy application
COPY requirements.txt /

# Install application dependencies
RUN pip install -r requirements.txt

WORKDIR /app
ENTRYPOINT ["gunicorn", "--chdir", "/app", "-w", "2", "--threads", "2", "-b", "0.0.0.0:5000", "app:app"]