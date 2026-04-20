## Prerequis
- **Python** 3.14+
- **uv** - gestionnaire de paquets

---

## Installation
**1. Cloner le depot**
```bash
git clone --branch=chore/retire-gemma-ai https://github.com/lumeida-tech/hirebox-data.git hirebox-ai
cd hirebox-ai
```

**2. Configurer les variables d'environnement**
```bash
cp .env.example .env
```

Ajoute ensuite les cles et IP autorisees dans `.env`.
```env
HIREBOX_ENABLE_API_SECURITY="false"
HIREBOX_BACKEND_API_KEY="HB_"
HIREBOX_ALLOW_API_KEYS="token-dev-1,token-dev-2"
HIREBOX_ALLOW_ORIGINS="127.0.0.1,::1"
```

En local, mets `HIREBOX_ENABLE_API_SECURITY="false"` pour manipuler facilement les routes.
En integration ou en production, passe cette valeur a `true`.

Le header attendu pour les routes protegees est :
```http
API_KEY: HB_token-dev-1
```

La verification `API_KEY + IP` s'applique uniquement aux routes que vous protegeez explicitement dans FastAPI.

**3. Installer les dependances**
Cree un environnement virtuel et installe les dependances definies dans `pyproject.toml`.
```bash
uv sync
```

**4. Telecharger le modele**
Telecharge le modele `google/gemma-4-E2B-it` dans le repertoire `models/`.
```bash
uvx hf download google/gemma-4-E2B-it --local-dir models/google/gemma-4-E2B-it
```

**5. Demarrer le serveur**
Lance FastAPI en mode developpement sur le port 8005.
```bash
uv run fastapi dev main.py # port 8000 pour le local et 8005 sur docker
```

---

## References
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
## Teste avec le Curl 
```bash
curl.exe -X POST "http://127.0.0.1:8000/generate-question-from-cv" -H "Content-Type: application/json" -H "API_KEY: HB_MPW_3YnwaiG0_peYMxa4MNBD5Ygg-sWrCtCnppsXPGw" -d "{\"cv_content\":\"Developpeur backend Python avec 5 ans d'experience\"}"
```


# uv run uvicorn main:app --host 0.0.0.0 --port 8005
