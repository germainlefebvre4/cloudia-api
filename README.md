# Cloudia - API

This repository contains the API application for the Cloudia project.

---

Project overview: [https://github.com/germainlefebvre4/cloudia-project](https://github.com/germainlefebvre4/cloudia-project)

Documentation: [https://cloudia.readthedocs.io/](https://cloudia.readthedocs.io/)

---

## Getting started

Install required packages:

```bash
sudo apt update
sudo apt install python3-pip python3-dev
pip install poetry
```

Setup the database:

```bash
docker compose up -d db
```

Run the app:

```bash
poetry install
poetry run alembic upgrade head
poetry run python app/initial_data.py
poetry run uvicorn app.main:app --port=8080 --reload
```

### Troubleshooting

Some distributions might miss some packages. These are some hints if needed:

```bash
# cryptography/cffi
sudo apt install build-essential libssl-dev libffi-dev libpq-dev
```

## Development

### Setup workspace

```bash
sudo apt update
sudo apt install python3-pip python3-dev
pip install poetry
poetry install
```

### Run locally

This section use docker database called `cloudia`.

```bash
docker compose up -d db
poetry run alembic upgrade head
poetry run python app/initial_data.py
poetry run uvicorn app.main:app --port=8080 --reload
```

### Run tests

This section use docker database called `cloudia_test`.

```bash
docker compose up -d db_test
poetry run pytest -sv app/tests/
```
