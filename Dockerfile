FROM python:3.11-slim-buster

RUN apt update -y && apt install -y awscli && apt upgrade -y && apt clean && rm -rf /var/lib/apt/lists/*
WORKDIR /app

COPY . /app
RUN pip install -r requirements.txt

CMD ["dvc", "repro"]