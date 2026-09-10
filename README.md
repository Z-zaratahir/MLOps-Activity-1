# MLOps Continuous Delivery Demo

This repository implements the continuous delivery exercise from
`MLOps_Continuous_Delivery_Tutorial.pdf`.

The application is a small Flask inference API. A semantic version tag runs
tests, builds one immutable Docker image, publishes it to GHCR, deploys that
same version to staging, and waits for production environment approval before
promoting it to production.

## API

Run locally:

```powershell
python -m pip install -r requirements.txt
python app.py
```

Endpoints:

- `GET /` returns the service status.
- `GET /health` returns application, model, Git commit, and health metadata.
- `POST /predict` accepts `{"value": 5}` and returns a teaching prediction of
  `10`.

Run tests with `python -m pytest`.

## Docker

The local Compose deployment uses the same image contract as CI/CD:

```powershell
docker compose up --build
Invoke-RestMethod http://localhost:5000/health
```

`APPLICATION_VERSION`, `MODEL_VERSION`, and `GIT_COMMIT` can be supplied as
environment variables or Docker build arguments. Production should use an
explicit version tag, not only `latest`.

## GitHub setup

Create two GitHub Environments:

1. `staging`: no required reviewer.
2. `production`: add the authorized required reviewer to create the approval
   gate.

Configure these environment secrets:

| Environment | Secrets |
| --- | --- |
| `staging` | `STAGING_HOST`, `STAGING_USER`, `STAGING_SSH_KEY`, `GHCR_USERNAME`, `GHCR_TOKEN` |
| `production` | `PRODUCTION_HOST`, `PRODUCTION_USER`, `PRODUCTION_SSH_KEY`, `GHCR_USERNAME`, `GHCR_TOKEN` |

`GHCR_TOKEN` must be able to read the published package on the target server.
Each target must have Docker installed and allow SSH access. The servers must
also expose port `5000` to the GitHub Actions runner for the staging smoke
test.

The optional environment variable `MODEL_VERSION` defaults to `model-7`.

## Release

Update `VERSION`, commit the change, and push a matching semantic version tag:

```powershell
git add .
git commit -m "feat: release application 1.0.0"
git push origin main
git tag v1.0.0
git push origin v1.0.0
```

The CD workflow only starts for tags matching `vMAJOR.MINOR.PATCH`, and it
fails if the tag does not match `VERSION`.

## Rollback

Use **Actions -> Rollback Production -> Run workflow**, then enter the known
good immutable version, such as `1.0.0`. The workflow pulls that exact image
and redeploys it to the production environment. The production approval gate
also applies to rollback.

## Workflow map

- `ci.yml`: tests pull requests and pushes to `main`.
- `cd.yml`: tests, builds, publishes, stages, smoke-tests, and promotes a
  tagged release.
- `rollback.yml`: manually redeploys a previously published version.