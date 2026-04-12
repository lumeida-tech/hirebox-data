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
uv run fastapi dev main.py --port 8005
```

---

## Références

- [Documentation uv](https://docs.astral.sh/uv/getting-started/installation/#standalone-installer)
- [Documentation FastAPI](https://fastapi.tiangolo.com/)


uvx mypy .




add API_KEY