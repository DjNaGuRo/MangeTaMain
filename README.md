# MangeTaMain - Analyse Exploratoire de Données de Recettes

Ce projet contient une analyse exploratoire de données (EDA) sur un dataset de recettes et d'avis provenant de Food.com, développé par une équipe de 5 étudiants : Guy, Mohamed, Leonnel, Omar et Osman.

## 🎯 Objectif du Projet

L'objectif principal est d'identifier les caractéristiques communes aux **recettes les moins appréciées** par les utilisateurs d'une plateforme culinaire. En analysant les interactions des utilisateurs (notes, avis) et les informations descriptives des recettes, nous cherchons à :

- Comprendre quels facteurs influencent la satisfaction/insatisfaction des utilisateurs
- Dresser une carte statistique des recettes les moins appréciées
- Fournir des recommandations d'amélioration pour les concepteurs de contenu culinaire

## 📊 Datasets

Le projet exploite deux jeux de données principaux :

### Dataset Recipes
- Informations descriptives des recettes (nom, description, type de plat)
- Ingrédients et temps de préparation
- Données nutritionnelles (calories, lipides, glucides, protéines, etc.)
- Métadonnées (portions, difficulté, tags)

### Dataset Interactions
- Notes attribuées aux recettes (1-5)
- Commentaires et avis textuels
- Données d'activité utilisateurs
- Métadonnées temporelles

## 🏗️ Structure du Projet

```
MangeTaMain/
├── src/                          # Code source principal
│   ├── __init__.py
│   ├── data_loader.py           # Chargement des données
│   ├── preprocessing.py         # Nettoyage et préprocessing
│   ├── data_visualization.py    # Fonctions de visualisation
│   └── streamlit/               # Application Streamlit
│       └── app/
│           ├── streamlit_app.py # Application principale
│           ├── layouts/         # Pages de l'interface
│           └── utils.py         # Utilitaires Streamlit
├── notebooks/                   # Notebooks Jupyter
│   ├── data_cleaning.ipynb
│   └── data_vizualisation.ipynb
├── tests/                       # Tests unitaires
├── data/                        # Données (non versionnées)
│   ├── raw/                     # Données brutes
│   └── processed/               # Données nettoyées
├── docs/                        # Documentation Sphinx
├── docker-compose.yml           # Configuration Docker
├── Dockerfile                   # Image Docker
└── pyproject.toml              # Configuration Poetry
```

## ⚙️ Installation

### Prérequis
- Python 3.11 ou supérieur
- Poetry (gestionnaire de dépendances)
- Git

### Installation avec Poetry

1. **Clonez le repository :**
```bash
git clone <your-repo-url>
cd MangeTaMain
```

2. **Installez Poetry si nécessaire :**
```bash
curl -sSL https://install.python-poetry.org | python3 -
```

3. **Installez les dépendances :**
```bash
poetry install
```

4. **Activez l'environnement virtuel :**
```bash
poetry shell
# ou
eval $(poetry env activate)
```

## 🚀 Utilisation

### Préparation des données
Placez les données brutes dans le répertoire `data/raw` et les données nettoyées dans `data/processed` (ces dernières peuvent être obtenues en lançant le notebook `notebooks/data_cleaning.ipynb`).

### Lancement de l'application Streamlit

**Option 1: Via Docker Compose**
```bash
docker compose up
```

**Option 2: Via Streamlit directement**
```bash
poetry run streamlit run src/streamlit/app/streamlit_app.py
```

L'application sera disponible sur **http://localhost:8501**

### Navigation dans l'interface

L'application est organisée en plusieurs pages :

- 🏠 **Accueil** : Présentation du projet et aperçu des données
- 📊 **Données cleaning** : Détection des valeurs manquantes, traitement des doublons, suppression des valeurs aberrantes
- 📈 **Visualisations** : Distribution des ratings, analyse des contributeurs, corrélations nutritionnelles, analyse de sentiment
- 📝 **Conclusion** : Synthèse des résultats et perspectives

### Utilisation des notebooks

**Notebook de nettoyage des données :**
```bash
poetry run jupyter notebook notebooks/data_cleaning.ipynb
```

**Notebook de visualisation :**
```bash
poetry run jupyter notebook notebooks/data_vizualisation.ipynb
```

## 🧪 Tests et Développement

### Tests unitaires
```bash
poetry run pytest tests/ -v
```

### Linting et formatage
```bash
# Formatage avec Black
poetry run black src/

# Linting avec flake8
poetry run flake8 src/ --max-line-length=88
```

## 📚 Documentation

La documentation complète est générée avec Sphinx et disponible dans le dossier `docs/`. Pour consulter la documentation :

1. **Construire la documentation :**
```bash
# Option 1: Utilise le script de build automatique
./build_docs.sh

# Option 2: Commande manuelle
cd docs
poetry run sphinx-build -b html . _build/html
```

2. **Ouvrir la documentation :**
```bash
# Linux/WSL
xdg-open _build/html/index.html
# macOS
open _build/html/index.html
# Windows
start _build/html/index.html
```

### API Reference

La documentation automatique inclut :
- [`data_loader`](docs/api/data_loader.md) : Fonctions de chargement des données
- [`preprocessing`](docs/api/preprocessing.md) : Fonctions de nettoyage et préprocessing
- [`data_visualization`](docs/api/data_visualization.md) : Fonctions de visualisation
- [`streamlit_app`](docs/api/streamlit_app.md) : Application Streamlit

## 🔧 Dépendances Principales

- **numpy** : Calculs numériques
- **pandas** : Manipulation de données
- **matplotlib/seaborn** : Visualisations
- **streamlit** : Interface web interactive
- **plotly** : Visualisations interactives
- **scipy** : Calculs statistiques avancés

## 🛠️ Développement

Les outils de développement incluent :
- **pytest** : Tests unitaires
- **black** : Formatage du code
- **flake8** : Linting
- **sphinx** : Génération de documentation

## 📈 Méthodologie

Le projet suit une approche exploratoire structurée en trois phases :

1. **🔍 Exploration initiale** : Compréhension de la structure et qualité des données
2. **📊 Analyse statistique** : Analyse descriptive et identification des patterns
3. **🎯 Analyse ciblée** : Focus sur les recettes les moins appréciées et facteurs d'insatisfaction

## 👥 Équipe

- **ABDILLAHI OMAR DJAMA**
- **AMAR Mohamed**
- **Bagci Osman**
- **DJOUNANG NANA Guy Rostan**
- **SOP Leonnel Romuald**

## 📄 Licence

Ce projet est sous licence MIT - voir le fichier [LICENSE](LICENSE) pour plus de détails.

MIT License

Copyright (c) 2024 Guy, Mohamed, Leonnel, Omar, Osman

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

## 🤝 Contribution

Pour contribuer au projet :
1. Fork le repository
2. Créez une branche pour votre feature (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changements (`git commit -am 'Ajout nouvelle fonctionnalité'`)
4. Push vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Créez une Pull Request

## 📞 Support

Pour toute question ou support, consultez la [documentation complète](docs/) ou contactez l'équipe de développement.