import pandas as pd
from pathlib import Path

# --- Définition des chemins ---
DATA_DIR = Path(__file__).parent.parent / "data"

# Dossiers
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

# Fichiers bruts
RAW_RECIPES = RAW_DIR / "RAW_recipes.csv"
RAW_INTERACTIONS = RAW_DIR / "RAW_interactions.csv"

# Fichiers nettoyés
CLEAN_RECIPES = PROCESSED_DIR / "recipes_cleaned.csv"
CLEAN_INTERACTIONS = PROCESSED_DIR / "interactions_cleaned.csv"
CLEAN_MERGED = PROCESSED_DIR / "merged_cleaned.csv"


# --- Fonctions de chargement ---
def load_recipes_data():
    """Charge les données brutes des recettes."""
    return pd.read_csv(RAW_RECIPES)


def load_interactions_data():
    """Charge les données brutes des interactions."""
    return pd.read_csv(RAW_INTERACTIONS)


def load_clean_recipes():
    """Charge le fichier recipes_cleaned.csv"""
    return pd.read_csv(CLEAN_RECIPES)


def load_clean_interactions():
    """Charge le fichier interactions_cleaned.csv"""
    return pd.read_csv(CLEAN_INTERACTIONS)


def load_clean_merged():
    """Charge le fichier merged_cleaned.csv"""
    return pd.read_csv(CLEAN_MERGED)
