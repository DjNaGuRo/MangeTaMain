FROM python:3.12-slim

WORKDIR /app

# Installer les dépendances système
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    && rm -rf /var/lib/apt/lists/*

# Variables d'environnement
ENV PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1 \
    STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Copier et intaller les dépendances depuis poetry
COPY pyproject.toml poetry.lock ./
RUN pip install --upgrade pip && \
    pip install --no-cache-dir poetry && \
    poetry config virtualenvs.create false && \
    poetry install --only=main --no-interaction --no-ansi
 



# Copier le code source et les fichiers de configuration
COPY src/ ./src/
COPY .env.template ./
COPY README.md ./


# Utilisateur non-root pour la sécurité
RUN useradd --create-home --shell /bin/bash appuser && \
    chown -R appuser:appuser /app
USER appuser


# Port Streamlit
EXPOSE 8501


# Vérification de santé
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Démarrage de l'application
CMD ["streamlit", "run", "src/streamlit/app/streamlit_app.py", "--server.address=0.0.0.0", "--server.port=8501"]