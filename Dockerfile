FROM python:3.9

WORKDIR /Anmelde_server

COPY ./src ./src
COPY ./template ./template
COPY settings.yml ./settings.yml
COPY ./logs ./logs
COPY requirements.txt ./requirements.txt

RUN pip install -r ./requirements.txt
WORKDIR /Anmelde_server/src

CMD ["python", "app.py","-v"]
