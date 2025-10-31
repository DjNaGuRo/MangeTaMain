FROM python:3.11-slim

WORKDIR /app

# Installer les dépendances
RUN apt-get update && apt-get install -y \
    build-essential \
    curl \
    git \
    && rm -rf /var/lib/apt/lists/*

# Variables d'environnement
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false \
    PYTHONUNBUFFERED=1 \
    PYTHONDONTWRITEBYTECODE=1

# Installer Poetry
RUN pip install poetry

# Configurer Poetry
RUN poetry config virtualenvs.create false

# Copier les fichiers Poetry
COPY pyproject.toml poetry.lock README.md ./

# Installer les dépendances
RUN poetry install --only=main --no-root

# Copier le code source
COPY src/ ./src/


# Créer un utilisateur non-root
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Exposer le port
EXPOSE 8501

# Healthcheck
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# ✅ CHEMIN CORRIGÉ
CMD ["streamlit", "run", "src/streamlit/app/streamlit_app.py", "--server.port=8501", "--server.address=0.0.0.0"]