# MangeTaMain - Analyse Exploratoire de Données de Recettes

Ce projet contient une analyse exploratoire de données (EDA) sur un dataset de recettes et d'avis provenant de Food.com.

## Structure du Projet

```
MangeTaMain/
├── src/
│   ├── data/
│   └── streamlit/
├── notebooks/
├── tests/
├── pyproject.toml
└── README.md
```

## Installation avec Poetry

1. Assurez-vous d'avoir Poetry installé. Si ce n'est pas le cas :
   ```bash
   curl -sSL https://install.python-poetry.org | python3 -
   ```

2. Installez les dépendances :
   ```bash
   poetry install
   ```

3. Activez l'environnement virtuel :
   ```bash
   poetry shell
   ```

## Utilisation

### Lancer Jupyter Notebook
```bash
poetry run jupyter notebook
```

### Lancer le notebook principal
```bash
poetry run jupyter notebook notebooks/lab-recipe-student.ipynb
```

## Dépendances Principales

- **numpy** : Calculs numériques
- **pandas** : Manipulation de données
- **matplotlib** : Visualisations de base
- **seaborn** : Visualisations statistiques avancées
- **jupyter** : Environnement de notebooks

## Développement

Les outils de développement incluent :
- **pytest** : Tests unitaires
- **black** : Formatage du code
- **flake8** : Linting
- **mypy** : Vérification de types
## **\* Projet EDA – Analyse des Recettes les Moins Appréciées**

Objectif général

L’objectif principal de ce projet est d’identifier les caractéristiques communes aux recettes les moins appréciées par les utilisateurs d’une plateforme culinaire.
En analysant à la fois les interactions des utilisateurs (notes, avis, likes) et les informations descriptives des recettes, le projet vise à :

Comprendre quels facteurs influencent la satisfaction ou l’insatisfaction des utilisateurs (temps de préparation, difficulté, ingrédients, etc.).

Dresser une carte statistique des recettes les moins appréciées afin d’en tirer des recommandations d’amélioration pour les concepteurs de contenu culinaire.

Jeux de données

Deux jeux de données distincts sont exploités :

Dataset Recipes

Contient les informations descriptives des recettes publiées sur la plateforme :

Nom, description et type de plat (entrée, plat principal, dessert…)

Ingrédients et temps de préparation

Données nutritionnelles (énergie, lipides, glucides, protéines, etc.)

Informations complémentaires : nombre de portions, difficulté, etc.

Dataset Interactions

Contient les données d’activité des utilisateurs vis-à-vis des recettes :

Notes attribuées aux recettes

Commentaires et avis

Nombre de vues, likes, favoris

Ces deux jeux de données sont corrélés par un identifiant commun de recette, permettant une analyse croisée complète.

Démarche analytique

Le projet suit une approche exploratoire structurée en trois grandes parties :

1️ Exploration initiale

Objectif : comprendre la structure et la qualité des données.
Cette phase comprend :

Aperçu général des datasets (dimensions, types de variables, premières observations)

Détection des valeurs manquantes

Identification des doublons et des valeurs extrêmes

Correction / Nettoyage des anomalies détectées

L’objectif est d’obtenir un jeu de données propre et fiable pour la suite de l’analyse.

2️ Analyse statistique

## Commande pour lancer Streamlit
poetry run streamlit run src/streamlit/app/streamlit_app.py

## Interface graphique
 Local URL: http://localhost:8501
  Network URL: http://192.168.1.189:8501