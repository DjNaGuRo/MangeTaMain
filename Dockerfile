# Utilisation d'une image Python légère
FROM python:3.11-slim

# Définir le répertoire de travail à l'intérieur du conteneur Docker
WORKDIR /app

# Installer les dépendances de construction
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

# Configurer Poetry pour ne pas créer d'environnement virtuel
RUN poetry config virtualenvs.create false

# Copier les fichiers de configuration Poetry ET le README
COPY pyproject.toml README.md ./

# Installer SEULEMENT les dépendances (pas le projet comme package)
RUN poetry install --only=main --no-root

# Copier le code source de l'application
COPY src/ ./src/

# Créer un utilisateur non-root pour la sécurité
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Exposer le port 8501 pour permettre l'interaction avec notre conteneur docker
EXPOSE 8501

# Vérification de santé pour surveiller l'état du conteneur
HEALTHCHECK --interval=30s --timeout=10s --start-period=40s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Commande pour lancer l'application Streamlit au démarrage du conteneur
CMD ["streamlit", "run", "src/main.py", "--server.port=8501", "--server.address=0.0.0.0"]