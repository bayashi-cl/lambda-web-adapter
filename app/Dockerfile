# syntax=docker/dockerfile:1

FROM public.ecr.aws/lambda/python:3.12 as base

# hadolint ignore=DL3042
RUN --mount=type=cache,target=/root/.cache/pip \
    pip install poetry==1.8.3 poetry-plugin-export==1.8.0

RUN --mount=type=bind,source=pyproject.toml,target=pyproject.toml \
    --mount=type=bind,source=poetry.lock,target=poetry.lock \
    poetry export --without dev --output /tmp/requirements.txt

RUN --mount=type=cache,target=/root/.cache/pip \
    pip wheel --requirement /tmp/requirements.txt --wheel-dir /tmp/wheelhouse

RUN --mount=type=bind,target=. \
    poetry build --format wheel --output /tmp/wheelhouse


FROM public.ecr.aws/lambda/python:3.12 as final

# hadolint ignore=DL3013
RUN --mount=type=bind,from=base,source=/tmp/wheelhouse,target=/tmp/wheelhouse \
    pip install app --find-links /tmp/wheelhouse --no-index --no-cache-dir

CMD [ "app.handler" ]
