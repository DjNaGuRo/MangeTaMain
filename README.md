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
