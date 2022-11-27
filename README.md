# RabbitMQ example

This repository presents an example Producer and Consumer that communicate using RabbitMQ.

Intended for getting familiar with the tech. Intentionally oversimplified.

## How to run.

In root directory of the repository, copy `sample.env` to `.env`, and adjust values in it as you see fit.

After that, run `docker compose up --build`.

## Components

### `gusamon` module

In this module you can find:

- `pydantic.BaseSettings` that get settings from environment variables ([`settings.py`](gusamon/settings.py)).
- Example usage of `pika` library.
- `Producer` and `Consumer` classes that interact with RabbitMQ ([`queue_workers.py`](gusamon/queue_workers.py)).
- Example usage of `ArgumentParser` that decides to start up `Producer` or `Consumer` ([`__main__.py`](gusamon/__main__.py)).

### `Dockerfile`

- Argument for `ENTRYPOINT` is a list because that way you can append arguments using `docker compose`.
- Assumes build contest is root directory of this repository. That's how it finds `requirements.txt`.

### `sample.env` and `.env`

Used for passing "sensitive data" to containers, and basically copy settings between them.

Example: username and password to RabbitMQ are needed for both `gusamon` and `rabbitqm` containers.

`.env` is already `.gitignore`d.

### `docker-compose.yaml`

- Unites all containers in a single network `gaming_net`.
- Creates `rabbitmq` container with data from `.env` file, namely username and password.
- Does healthchecks to `rabbitmq` because it's a good practive, and it helps to avoid error spam.
- Solved error spam: `gusamon` containers depend on `rabbitmq` but without `condition: service_healthy` they start up before `rabbitmq` and spam errors like "unknown host" just because `rabbitmq` takes a while to start up.
- `command: ["--produce"]` just appends to `ENTRYPOINT` in `Dockerfile` but for each container there's own command even though image is the same. This allows to customize behavior of containers.
- `env_file` automagically populates each container's enviromnent with values from that file. This way you can give `rabbitmq` credentials to dependent apps.
- This is where Build Context for `Dockerfile` is set. It's relative to `pwd` though, so you're kind of _forced_ to run `docker compose` from root folder of this repository.

## Results

Producer will produce one message per second, then restart because it terminates successfully.

Consumer will not restart because it's forever blocked by listening for updates.
However, it does not print all messages right when they come.
Instead, it prints them in batches, and they look like this:

```txt
message.is_epic=True, message.payload='Gordon Freeman is Sus'
```

This is a proof that at least this monstrosity works :trollface:
