# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Flask web app for browsing, uploading, downloading, and deleting files from OpenShift PersistentVolumeClaims (PVCs). Primary use case: viewing `compliance-operator` scan results from OCP4 in HTML format via `oscap xccdf generate report`. Also usable as a general PVC file browser.

## Development Commands

```bash
# Install dependencies
pip install -r requirements.txt

# Run locally (port 5123)
SAVEPASS=yourpassword python app.py

# Run with gunicorn (production-like)
SAVEPASS=yourpassword gunicorn -b 0.0.0.0:5123 --log-level debug app:app

# Build container image
docker build -f dockerfile -t py-upload-download .
```

No test suite exists. No linter configured.

## Architecture

Single-file Flask app (`app.py`) — all routes, auth, and file operations in one module.

- **Auth**: password-only login via `SAVEPASS` env var, bcrypt-hashed comparison, Flask session-based
- **File storage**: serves from `UPLOAD_FOLDER` env var (default: `./data`), supports nested directory browsing
- **XCCDF conversion**: `.bzip2` files get a "Convert" button that shells out to `oscap xccdf generate report` (requires `openscap-scanner` installed — handled in Dockerfile via `yum`)
- **Templates**: `templates/index.html` (file browser) and `templates/login.html` (login form), plain HTML with Jinja2

## Environment Variables

| Variable | Purpose | Default |
|----------|---------|---------|
| `SAVEPASS` | Login password (required) | None |
| `UPLOAD_FOLDER` | Root directory to browse/upload | `data` |

## CI/CD

GitHub Actions (`.github/workflows/ci.yaml`): builds Docker image, pushes to Quay.io, signs with Cosign. Triggers on push to `main` and `feature/**` branches. Feature branches get `-feature` tag suffix.

## Deployment

Example OpenShift manifests in `example_deployment/`:
- `deployment_compliance_get_result_example.yaml` — mounts compliance PVCs (ocp4-cis, worker, master)
- `deployment_other_purpose.yaml` — generic PVC browsing (replace `replac-me-pvc-name`)
- `service.yaml` and `route.yaml` — OpenShift Service/Route

Container runs as non-root (UID 1001) on UBI9 Python 3.12 base image.
