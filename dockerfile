FROM ubuntu:20.04

RUN apt-get update && \
    apt-get install -y apt-utils software-properties-common && \
    add-apt-repository ppa:deadsnakes/ppa && \
    apt-get update && \
    apt-get install -y python3.12 python3.12-venv 


WORKDIR /app

# Create venv and install playwright
RUN python3.12 -m venv /app/venv && \
    /app/venv/bin/pip install --upgrade pip && \
    /app/venv/bin/pip install playwright && \
    /app/venv/bin/python -m playwright install --with-deps

COPY dockerMain.py /app/

CMD ["bash"]