FROM python:3.12.1-alpine

WORKDIR /onyxdb-agent

COPY requirements.txt .

RUN pip install -r requirements.txt

COPY main.py .
COPY src/ ./src

EXPOSE 8080

ENTRYPOINT ["python3", "main.py"]
