FROM python:3.9.15-slim

WORKDIR /opt

COPY ./api/requirements.txt .
RUN pip install -r requirements.txt
RUN pip install -U git+https://github.com/particle1331/distributed-task-queue.git@main 

COPY ./api ./api

EXPOSE 8000

ENTRYPOINT ["uvicorn", "main:app"]
