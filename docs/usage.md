## Lancement de l'application

L'application peut être lancée via Docker Compose ou directement avec Streamlit.

**Préparation automatique des données :**
Au premier lancement, les données seront automatiquement téléchargées et extraites dans `data/raw` et `data/processed` si elles sont absentes, grâce à la fonction `ensure_data` (voir la variable d'environnement `DATA_REMOTE_URL`). Il n'est plus nécessaire de placer manuellement les fichiers ou d'exécuter les notebooks pour préparer les données.

1. Lancez l'application via Docker Compose :
```bash
docker compose up
```

2. Lancez l'application via Streamlit :
```bash
poetry run streamlit run src/streamlit/app/streamlit_app.py
```

L'application sera disponible sur http://localhost:8501

## Navigation dans l'interface

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


## Utilisation des notebooks (optionnel)

Les notebooks du dossier `notebooks/` servent à l'exploration, au nettoyage ou à la visualisation avancée des données. Leur utilisation est facultative, car l'application gère automatiquement le téléchargement et la préparation des données.

#### Notebook principal
```bash
poetry run jupyter notebook notebooks/data_cleaning.ipynb
```

#### Notebook de visualisation
```bash
poetry run jupyter notebook notebooks/data_vizualisation.ipynb
```

## Tests

#### Lancer les tests unitaires :

```bash
poetry run pytest tests/ -v
```

## Linting et formatage

```bash
# Formatage avec Black
poetry run black src/

# Linting avec flake8
poetry run flake8 src/ --max-line-length=88
```

