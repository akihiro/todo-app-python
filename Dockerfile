FROM debian:12-slim AS build
RUN apt-get update && \
    apt-get install --no-install-suggests --no-install-recommends --yes python3-venv gcc libpython3-dev && \
    python3 -m venv /venv && \
    /venv/bin/pip install --upgrade pip setuptools wheel

FROM build AS build-venv
COPY ./requirements.lock /
RUN sed -i '/-e/d' /requirements.lock
RUN /venv/bin/pip install -r ./requirements.lock
WORKDIR /app
COPY ./src ./
RUN python3 -m compileall .

FROM gcr.io/distroless/python3-debian12:nonroot
COPY --from=build-venv --link /venv/ /venv/
COPY --from=build-venv --link /app /app
WORKDIR /app
ENTRYPOINT []
CMD ["/venv/bin/gunicorn", "todo_app_python:app", "--workers", "4", "--worker-class" ,"uvicorn.workers.UvicornWorker", "--bind", "[::]:8000"]
