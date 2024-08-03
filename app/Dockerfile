# syntax=docker/dockerfile:1

FROM public.ecr.aws/lambda/python:3.12 as base

RUN pip install poetry==1.8.3 && poetry self add poetry-plugin-export==1.8.0

RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=poetry.lock,target=poetry.lock \
    poetry export --without-hashes --format constraints.txt --without dev --output /opt/constraints.txt

RUN --mount=type=bind,target=. \
    poetry build --format wheel --output /opt

FROM public.ecr.aws/lambda/python:3.12 as final

RUN --mount=type=cache,target=/root/.cache/pip \
    --mount=type=bind,from=base,source=/opt/,target=/opt/ \
    pip install /opt/*.whl --constraint /opt/constraints.txt

CMD [ "app.handler" ]
