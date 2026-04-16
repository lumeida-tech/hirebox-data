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

**2. Configurer les variables d'environnement**
```bash
cp .env.example .env
```

**3. Installer les dépendances**
Crée un environnement virtuel et installe les dépendances définies dans `pyproject.toml`.
```bash
uv sync
```

**4. Télécharger le modèle**
Télécharge le modèle `google/gemma-4-E2B-it` dans le répertoire `models/`.
```bash
uvx hf download google/gemma-4-E2B-it --local-dir models/google/gemma-4-E2B-it
```

**5. Démarrer le serveur**
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