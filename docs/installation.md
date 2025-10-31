# Installation et Configuration

```markdown

## Prérequis# Installation et Configuration



- Python 3.11 ou supérieur## Prérequis

- Poetry (gestionnaire de dépendances)

- Git- Python 3.11 ou supérieur

- Poetry (gestionnaire de dépendances)

## Installation avec Poetry- Git



1. **Clonez le repository :**## Installation avec Poetry

```bash

git clone <your-repo-url>1. **Clonez le repository :**

cd MangeTaMain```bash

```git clone <your-repo-url>

cd MangeTaMain

2. **Installez Poetry si nécessaire :**```

```bash

curl -sSL https://install.python-poetry.org | python3 -2. **Installez Poetry si nécessaire :**

``````bash

curl -sSL https://install.python-poetry.org | python3 -

3. **Installez les dépendances :**```

```bash

poetry install3. **Installez les dépendances :**

``````bash

poetry install

4. **Activez l'environnement virtuel :**```

```bash

poetry shell4. **Activez l'environnement virtuel :**

# ou```bash

eval $(poetry env activate)poetry shell

```# ou

eval $(poetry env activate)

## Vérification de l'installation```



Pour vérifier que l'installation s'est bien déroulée :

```bash
poetry run python -c "import pandas as pd; import streamlit as st; print('Installation réussie!')"
```