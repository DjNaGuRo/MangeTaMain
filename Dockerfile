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

# Désactiver la collecte de statistiques d'utilisation de Streamlit
ENV STREAMLIT_BROWSER_GATHER_USAGE_STATS=false

# Copier les fichiers de dépendances en premier (pour optimiser le cache Docker)
COPY requirements.txt ./
COPY pyproject.toml ./

# Mettre à jour pip et installer les dépendances Python
RUN pip3 install --no-cache-dir --upgrade pip && \
    pip3 install --no-cache-dir -r requirements.txt

# Copier le code source de l'application
COPY src/ ./src/

# Créer un utilisateur non-root pour la sécurité
RUN useradd --create-home --shell /bin/bash app && \
    chown -R app:app /app
USER app

# Exposer le port 8501 pour permettre l'interaction avec notre conteneur docker
EXPOSE 8501

# Vérification de santé pour surveiller l'état du conteneur
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl --fail http://localhost:8501/_stcore/health || exit 1

# Commande pour lancer l'application Streamlit au démarrage du conteneur
ENTRYPOINT ["streamlit", "run", "src/main.py", "--server.port=8501", "--server.address=0.0.0.0"]