# Portfolio & Gallery Website in Django

A personal portfolio and image gallery built with Django. This site showcases your work, photography, and personal projects with a clean, responsive design and admin-managed media uploads.

---

## Features

- Personal portfolio homepage
- Categorized image gallery (professional & personal)
- Hobbies page with a browser-based QuickDraw demo backed by the ML platform
- Admin interface for uploading and managing photos
- Static assets organized with vendor libraries
- Pre-commit hooks for code quality
- Docker-ready for deployment
- GitHub Actions for CI/CD

---

## Tech Stack

- Backend: Django 4.x
- Frontend: HTML, SCSS, JS (vanilla)
- Database: SQLite (default, can be swapped)
- CI/CD: GitHub Actions
- Containerization: Docker

---

## Setup

### 1. Clone the repo

```bash
git clone https://github.com/nanderdev/portfolio-gallery.git
cd portfolio-gallery
```

### 2. Create virtual environment

```bash
python -m venv venv
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements-dev.txt
```

### 4. Run migrations

```bash
python manage.py migrate
```

### 5. Start development server

```bash
python manage.py runserver
```

---

## Code Quality

This project uses Pre-Commit with:

- black for formatting
- ruff and flake8 for linting
- detect-secrets for secret scanning
- djlint for Django template hygiene

To run hooks manually:

```bash
pre-commit run --all-files
```

---

## Docker

Build and run the app with Docker:

```bash
docker build -t portfolio .
docker run -p 8000:8000 portfolio
```

---

## Secrets & Environment

Create a `.env` file based on `.env.example`:

```env
DEBUG=True
SECRET_KEY=your-secret-key
ALLOWED_HOSTS=localhost,127.0.0.1
ANALYTICS_DB_NAME=ml_platform
ANALYTICS_DB_USER=portfolio
ANALYTICS_DB_PASSWORD=your-dedicated-portfolio-reader-password
ANALYTICS_DB_HOST=postgres.postgresql.svc.cluster.local
ANALYTICS_DB_PORT=5432
QUICKDRAW_PREDICT_URL=http://quickdraw-serving.ml-serving.svc.cluster.local:8000/predict
```

For Kubernetes deployments, the `portfolio-secret` Secret should provide at least:

```env
SECRET_KEY=your-secret-key
ANALYTICS_DB_PASSWORD=your-dedicated-portfolio-reader-password
```

When the app runs inside Kubernetes, it defaults to the in-cluster service endpoint `http://quickdraw-serving.ml-serving.svc.cluster.local:8000/predict`.

When the app runs outside Kubernetes, it defaults to the local MicroK8s NodePort endpoint `http://127.0.0.1:31548/predict`.

If the portfolio app runs outside the cluster and that NodePort is not available, point `QUICKDRAW_PREDICT_URL` at a reachable QuickDraw serving endpoint.

---

## Media & Static Files

- Uploaded images are stored in `/media/` (excluded from Git)
- Static assets are in `/static/`, including vendor libraries

---

## Deployment

### CI/CD

Automated via GitHub Actions:

- CI: Pre-commit and Django tests on PRs
- CD: Docker image pushed on release
- Release PRs managed with Release Please

### Deployment with MicroK8s

To deploy the application to your MicroK8s cluster, use the provided `deploy.sh` script. This script applies all necessary Kubernetes manifests, including:

- Namespace
- PersistentVolumeClaim for media storage
- Deployment (using the `latest` Docker image tag)
- Service
- Ingress

#### Prerequisites

- MicroK8s is installed and running
- You’ve built and pushed your Docker image to DockerHub with the `latest` tag
- Your Kubernetes manifests are located in the project root:
  - `namespace.yaml`
  - `media-pvc.yaml`
  - `deployment.yaml`
  - `service.yaml`
  - `ingress.yaml`

#### Usage

Make the script executable and run it:

```bash
chmod +x deploy.sh
./deploy.sh


---

## License

This project is licensed under the MIT License.

---

## Author

Made by Nander
Portfolio: https://nanderspeerstra.com
GitHub: https://github.com/nanderspeerstra
