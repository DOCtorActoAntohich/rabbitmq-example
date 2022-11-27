FROM python:3.10
WORKDIR /app

COPY ./docker/requirements.txt ./requirements.txt
RUN python -m venv .venv && \
    .venv/bin/python -m pip install --no-cache-dir --upgrade pip setuptools wheel && \
    .venv/bin/python -m pip install --no-cache-dir -r ./requirements.txt && \
    rm ./requirements.txt

COPY ./gusamon ./gusamon

ENTRYPOINT [".venv/bin/python", "-m", "gusamon"]
