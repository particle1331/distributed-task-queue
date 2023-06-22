FROM python:3.9.15-slim

WORKDIR /opt

COPY /tasks/* /opt/

RUN pip install -r requirements.txt

ENTRYPOINT ["celery"]
