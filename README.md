mangetamain/

Structure du projet : 

│
├── .git/                               # Dossier Git
├── .gitignore                          # Fichiers à ignorer (venv, data, etc.)
│
├── .github/
│   └── workflows/
│       └── ci.yml                      # Pipeline CI/CD (tests, lint, etc.)
│
├── README.md                           # Présentation du projet
├── pyproject.toml                      # Gestionnaire de dépendances (Poetry)
├── requirements.txt                    # (Optionnel) pour compatibilité CI
├── Dockerfile                          # Conteneurisation du projet
│
├── data/                               # Données utilisées dans l’analyse
│   ├── raw/                            # Données brutes Kaggle
│   ├── processed/                      # Données nettoyées / filtrées
│   └── external/                       # Données externes / API / open data
│
├── notebooks/                          # Notebooks exploratoires
│   ├── 01_exploration.ipynb
│   ├── 02_cleaning.ipynb
│   └── 03_visualization.ipynb
│
├── src/                                # Code source du projet (lib Python)
│   ├── __init__.py
│   │
│   ├── data/                           # Gestion des données
│   │   ├── __init__.py
│   │   └── loader.py                   # Chargement, nettoyage, cache
│   │
│   ├── eda/                            # Analyse exploratoire & visualisation
│   │   ├── __init__.py
│   │   ├── preprocessing.py            # Feature engineering / traitement texte
│   │   ├── analysis.py                 # Calculs statistiques, agrégations
│   │   └── visualization.py            # Graphiques Plotly / Matplotlib
│   │
│   ├── utils/                          # Outils génériques
│   │   ├── __init__.py
│   │   ├── logger.py                   # Configuration des logs (debug + error)
│   │   └── helpers.py                  # Fonctions utilitaires diverses
│   │
│   └── main.py                         # Point d’entrée (exécution locale)
│
├── streamlit_app/                      # Application Streamlit
│   ├── app.py                          # Fichier principal (page d’accueil)
│   └── pages/                          # Pages additionnelles
│       ├── 1_Overview.py               # Vue d’ensemble (stats globales)
│       ├── 2_Visualizations.py         # Visualisations interactives
│       └── 3_Modeling.py               # (Optionnel) analyses avancées
│
├── tests/                              # Tests unitaires
│   ├── __init__.py
│   ├── conftest.py                     # Fixtures de test
│   ├── test_data_loader.py
│   ├── test_analysis.py
│   ├── test_visualization.py
│   └── test_logger.py
│
├── scripts/                            # Scripts exécutables CLI
│   ├── run_eda.py                      # Exécuter l’analyse complète
│   ├── export_charts.py                # Export des visualisations
│   └── generate_report.py              # Rapport auto (Markdown / HTML)
│
├── docs/                               # Documentation technique
│   ├── conf.py                         # Config Sphinx
│   ├── index.rst                       # Page d’accueil de la doc
│   └── api/                            # Doc auto des modules
│
└── logs/                               # Journaux d’exécution
    ├── debug.log
    └── error.log

