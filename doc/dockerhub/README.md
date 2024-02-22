# Cloudia - API

## Overview

This service is part of the Cloudia project. It is used to handle data.

## Getting started

```bash
poetry run uvicorn app.main:app --port=8080 --reload
```

## Environment variables

| Name | Description | Default |
| --- | --- | --- |
| `SERVER_NAME` | Name of the server | `localhost` |
| `SERVER_HOST` | Server Host | `http://localhost:8080` |
| `BACKEND_CORS_ORIGINS` | URL to allow on CORS policies | `["http://localhost", "http://localhost:3000", "http://localhost:8080"]` |
| `SECRET_KEY` | Secret Key to hash sensitive data inside the app | `secret123` |
| `USER_ADMIN_FULLNAME` | Fullname of the admin user | `Admin` |
| `USER_ADMIN_EMAIL` | Email of the admin user | `admin@cloudia.fr` |
| `USER_ADMIN_PASSWORD` | Password of the admin user | `admin` |
| `USER_TEST_FULLNAME` | Fullname of the test user | `Test` |
| `USER_TEST_EMAIL` | Email of the test user | `test@cloudia.fr` |
| `USER_TEST_PASSWORD` | Password of the test user | `test` |
| `POSTGRES_SERVER` | Postres host | `localhost` |
| `POSTGRES_PORT` | Postres port | `5432` |
| `POSTGRES_DB` | Postres database name | `cloudia` |
| `POSTGRES_USER` | Postres user | `cloudia` |
| `POSTGRES_PASSWORD` | Postres password | `cloudia` |
| `USERS_OPEN_REGISTRATION` | Open self registration | `False` |
| `API_KEY_SECRET` | API Key secret to contact technical endpoints | `test123` |
| `GCP_SERVICE_ACCOUNT_JSON_KEY_FILE` | Path to the GCP service account JSON key file | `./gcp_service_account.json` |
| `GCP_ORGANIZATION_ID` | GCP organization ID | `123456789` |
| `AWS_ACCESS_KEY_ID` | AWS access key ID | `AWS_ACCESS_KEY_ID` |
| `AWS_SECRET_ACCESS_KEY`| AWS secret access key | `AWS_SECRET_ACCESS_KEY` |
| `AWS_DEFAULT_REGION` | AWS default region | `eu-east-1` |

## Docker

```bash
poetry export -f requirements.txt --output requirements.txt --without-hashes
docker build -t cloudia-api:latest .
```
