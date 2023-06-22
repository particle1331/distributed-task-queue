FROM python:3.9.15-slim

WORKDIR /opt

COPY /api/* /tasks/* /opt/

RUN pip install -r requirements.txt

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:api"]
