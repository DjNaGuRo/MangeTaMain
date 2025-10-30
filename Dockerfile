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

# Installer directement les dépendances principales
RUN pip install --upgrade pip && \
    pip install --no-cache-dir \
    streamlit \
    pandas \
    numpy \
    plotly \
    scikit-learn \
    matplotlib \
    seaborn

# Copier tout le code source
COPY src/ ./src/
COPY streamlit_app/ ./streamlit_app/

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