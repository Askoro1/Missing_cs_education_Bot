FROM python:3.9-slim-buster

COPY requirements.txt requirements.txt
RUN pip install -r requirements.txt

COPY . .

ENV TG_TOKEN ${TG_TOKEN}

CMD ["python", "src/startup_asb.py"]
