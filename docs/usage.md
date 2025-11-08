
# Lancement de l'application

L'application charge désormais toutes les données directement depuis une base PostgreSQL distante. Assurez-vous d'avoir configuré les variables d'environnement nécessaires (voir `database_config.md`).

Vous pouvez lancer l'application soit via Docker Compose, soit directement avec Streamlit :

1. Lancez l'application via docker compose:
```bash
docker compose up
```

2. Lancez l'application via Streamlit 
```bash
poetry run streamlit run src/streamlit/app/streamlit_app.py
```

L'application sera disponible sur http://localhost:8501


# Navigation dans l'interface

L'application est organisée en plusieurs pages :

🏠 Accueil

Présentation du projet et aperçu des données


📊 Données cleaning

- Détection des valeurs manquantes
- Traitement des doublons
- Suppression des valeurs aberrantes
- Imputation des données manquantes


📈 Visualisations

- Distribution des ratings
- Analyse des contributeurs
- Corrélations nutritionnelles
- Analyse de sentiment des avis


📝 Conclusion

Synthèse des résultats et perspectives



# Utilisation des notebooks


## Notebook principal

```bash
poetry run jupyter notebook notebooks/data_cleaning.ipynb
```


## Notebook de visualisation

```bash
poetry run jupyter notebook notebooks/data_vizualisation.ipynb
```


# Tests


## Lancer les tests unitaires

```bash
poetry run pytest tests/ -v
```


# Linting et formatage

```bash
# Formatage avec Black
poetry run black src/

# Linting avec flake8
poetry run flake8 src/ --max-line-length=88
```

