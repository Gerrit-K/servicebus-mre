FROM python:3.9-slim

COPY requirements.txt ./
RUN pip install -r requirements.txt

RUN useradd python
USER python

WORKDIR /app
COPY src/* .
ENTRYPOINT [ "python", "./main.py" ]
