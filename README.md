## Prérequis

- **Python** 3.14+
- **uv** — gestionnaire de paquets

---

## Installation

**1. Cloner le dépôt**

```bash
git clone https://github.com/lumeida-tech/hirebox-data.git hirebox-ai
cd hirebox-ai
```

**2. Installer les dépendances**

Crée un environnement virtuel et installe les dépendances définies dans `pyproject.toml`.

```bash
uv sync
```

**3. Démarrer le serveur**

Lance FastAPI en mode développement sur le port 8005.

```bash
uv run fastapi dev  # port 8000 pour le local et 8005 sur docker
```

---

## Références

- [Documentation uv](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)
- [Documentation FastAPI](https://fastapi.tiangolo.com/)

## Linting local
```bash
uv run ruff check .
uv run ruff format --check .
uv run mypy
docker build -f dockerfile -t hirebox-ai:test .
```

## Docker
```bash
docker build -f dockerfile -t hirebox-ai .
docker compose up -d
```

## GitHub Actions

La pipeline GitHub Actions est definie dans `.github/workflows/ci.yml` avec 4 etapes:

- lint et verification de formatage avec `ruff`
- verification de typage statique avec `mypy`
- build de l'image Docker via le `dockerfile`
- deploiement sur FastAPI Cloud uniquement sur la branche `main`

Secrets GitHub a configurer pour le deploiement:

- `FASTAPI_CLOUD_TOKEN` (nom officiel recommande)
- `FASTAPI_CLOUD_APP_ID`

Compatibilite ajoutee si tu as deja cree les anciens noms:

- `FASTAPICLOUD_TOKEN`
- `FASTAPICLOUD_APP_ID`

Le deploiement CI utilise `uv run fastapi deploy`, avec l'entree FastAPI configuree sur `main:app`.
