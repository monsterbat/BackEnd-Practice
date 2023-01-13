FROM python:3.10-slim-buster
WORKDIR /app
COPY requirements.txt requirements.txt
COPY . .
RUN apt-get update -y && apt-get install -y gcc
RUN pip3 install -r requirements.txt
CMD ["nohup","python3","app.py","&"]