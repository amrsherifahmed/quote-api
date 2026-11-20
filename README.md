# Quote API

A tiny Flask API used to practise CI/CD with **Jenkins** and **GitHub Actions**.

## Endpoints

| Method | Path       | Response                                   |
|--------|------------|--------------------------------------------|
| GET    | `/health`  | `{"status": "ok"}`                         |
| GET    | `/quote`   | A random quote `{"text": "...", "author": "..."}` |
| GET    | `/version` | `{"version": "<APP_VERSION or dev>"}`      |

`APP_VERSION` is meant to be set by the pipeline (e.g. the git commit SHA).

## Run locally (Python)

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install -r requirements-dev.txt
python -m app.main                # http://localhost:5000/health
```

## Lint & test (what the pipelines will run)

```bash
flake8
pytest --cov=app --cov-report=term-missing --cov-fail-under=80
# JUnit report for Jenkins/Actions:
pytest --junitxml=test-results/junit.xml --cov=app --cov-report=xml
```

## Run with Docker

```bash
docker compose up --build         # http://localhost:5000
# or
docker build -t quote-api:local .
docker run -d -p 5000:5000 -e APP_VERSION=$(git rev-parse --short HEAD) quote-api:local
curl localhost:5000/version
```

The image runs **gunicorn** as a **non-root user** and has a Docker `HEALTHCHECK` on `/health`.

## Project layout

```
quote-api/
├── app/
│   ├── __init__.py
│   └── main.py              # Flask app (create_app factory)
├── tests/
│   └── test_main.py         # 5 tests, ~96% coverage
├── requirements.txt         # runtime deps (used in the image)
├── requirements-dev.txt     # + pytest, pytest-cov, flake8
├── Dockerfile
├── docker-compose.yml
├── .flake8 / pytest.ini
└── .dockerignore / .gitignore
```

## Next (your part)

- `.github/workflows/ci.yml`
- `Jenkinsfile`

Stages: Checkout → Lint → Test → Build → Scan (Trivy) → Push → Deploy.
