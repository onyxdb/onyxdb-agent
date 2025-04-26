FROM python:3.12.1-alpine

WORKDIR /onyxdb-agent

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY src/ ./src
COPY main.py .
COPY config.yml .

EXPOSE 9004

ENTRYPOINT ["python3", "main.py"]
