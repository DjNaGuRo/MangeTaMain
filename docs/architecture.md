# Architecture du projet

## Structure des dossiers

MangeTaMain/
├── src/ # Code source principal
│ ├── __init__.py
│ ├── constants.py # Constantes globales
│ ├── data_loader.py # Chargement des données
│ ├── preprocessing.py # Nettoyage et préprocessing
│ ├── data_visualization.py # Fonctions de visualisation
│ └── streamlit/ # Application Streamlit
│ └── app/
│ ├── streamlit_app.py # Application principale
│ ├── layouts/ # Pages de l'interface
│ └── utils.py # Utilitaires Streamlit
├── notebooks/ # Notebooks Jupyter
│ ├── data_cleaning.ipynb
│ └── data_vizualisation.ipynb
├── tests/ # Tests unitaires
├── data/ # Données (non versionnées)
│ ├── raw/ # Données brutes
│ └── processed/ # Données nettoyées
├── docs/ # Documentation Sphinx
├── docker-compose.yml # Configuration Docker
├── Dockerfile # Image Docker
└── pyproject.toml # Configuration Poetry