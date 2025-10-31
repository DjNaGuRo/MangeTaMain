# Notebooks Jupyter

## Notebooks d'analyse

### Data Cleaning (`notebooks/data_cleaning.ipynb`)
Ce notebook contient :
- Chargement et exploration des données brutes
- Détection des valeurs manquantes et doublons
- Nettoyage des colonnes nutritionnelles
- Imputation des valeurs manquantes pour les avis
- Sauvegarde des données nettoyées

### Data Visualization (`notebooks/data_vizualisation.ipynb`)
Ce notebook présente :
- Analyses univariées et bivariées
- Distributions des ratings et moyennes
- Analyse des contributeurs les plus actifs
- Corrélations entre variables nutritionnelles
- Analyse de sentiment des avis négatifs

## Structure des données

### Table Recettes
- **name** : Nom de la recette
- **minutes** : Temps de préparation
- **n_ingredients** : Nombre d'ingrédients
- **n_steps** : Nombre d'étapes
- **ingredients** : Liste des ingrédients
- **nutrition** : Valeurs nutritionnelles [calories, total_fat, sugar, sodium, protein, saturated_fat, carbohydrates]

### Table Interactions
- **user_id** : Identifiant utilisateur
- **recipe_id** : Identifiant recette
- **date** : Date de l'avis
- **rating** : Note (1-5)
- **review** : Texte de l'avis