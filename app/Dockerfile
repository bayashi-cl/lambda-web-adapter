# syntax=docker/dockerfile:1

ARG PYTHON_VERSION=3.12
FROM python:${PYTHON_VERSION}-slim as base

WORKDIR /var/task

RUN pip install poetry
RUN poetry self add poetry-plugin-bundle


COPY . .
RUN poetry bundle venv --without dev .venv



FROM python:${PYTHON_VERSION}-slim as final

WORKDIR /var/task

COPY --from=public.ecr.aws/awsguru/aws-lambda-adapter:0.8.4 /lambda-adapter /opt/extensions/lambda-adapter

ENV PYTHONDONTWRITEBYTECODE=1
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

COPY --from=base /var/task/.venv /var/task/.venv
COPY --from=base /var/task/main.py /var/task/

ENV PATH=/var/task/.venv/bin:${PATH}

# CMD sleep infinity
CMD fastapi run
