import pandas as pd
from pathlib import Path
from .logging_config import get_logger

logger = get_logger('data_loader')

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
    try:
        logger.info(f"Loading raw recipes data from {RAW_RECIPES}")
        if not RAW_RECIPES.exists():
            logger.error(f"Raw recipes file not found: {RAW_RECIPES}")
            raise FileNotFoundError(f"File not found: {RAW_RECIPES}")
        
        data = pd.read_csv(RAW_RECIPES)
        logger.info(f"Successfully loaded recipes data: {data.shape[0]} rows, {data.shape[1]} columns")
        logger.debug(f"Recipes columns: {list(data.columns)}")
        return data
    except Exception as e:
        logger.error(f"Error loading recipes data: {str(e)}")
        raise


def load_interactions_data():
    """Charge les données brutes des interactions."""
    try:
        logger.info(f"Loading raw interactions data from {RAW_INTERACTIONS}")
        if not RAW_INTERACTIONS.exists():
            logger.error(f"Raw interactions file not found: {RAW_INTERACTIONS}")
            raise FileNotFoundError(f"File not found: {RAW_INTERACTIONS}")
        
        data = pd.read_csv(RAW_INTERACTIONS)
        logger.info(f"Successfully loaded interactions data: {data.shape[0]} rows, {data.shape[1]} columns")
        logger.debug(f"Interactions columns: {list(data.columns)}")
        return data
    except Exception as e:
        logger.error(f"Error loading interactions data: {str(e)}")
        raise


def load_clean_recipes():
    """Charge le fichier recipes_cleaned.csv"""
    try:
        logger.info(f"Loading cleaned recipes data from {CLEAN_RECIPES}")
        if not CLEAN_RECIPES.exists():
            logger.warning(f"Cleaned recipes file not found: {CLEAN_RECIPES}")
            logger.info("You may need to run data preprocessing first")
            raise FileNotFoundError(f"File not found: {CLEAN_RECIPES}")
        
        data = pd.read_csv(CLEAN_RECIPES)
        logger.info(f"Successfully loaded cleaned recipes: {data.shape[0]} rows, {data.shape[1]} columns")
        return data
    except Exception as e:
        logger.error(f"Error loading cleaned recipes data: {str(e)}")
        raise


def load_clean_interactions():
    """Charge le fichier interactions_cleaned.csv"""
    try:
        logger.info(f"Loading cleaned interactions data from {CLEAN_INTERACTIONS}")
        if not CLEAN_INTERACTIONS.exists():
            logger.warning(f"Cleaned interactions file not found: {CLEAN_INTERACTIONS}")
            logger.info("You may need to run data preprocessing first")
            raise FileNotFoundError(f"File not found: {CLEAN_INTERACTIONS}")
        
        data = pd.read_csv(CLEAN_INTERACTIONS)
        logger.info(f"Successfully loaded cleaned interactions: {data.shape[0]} rows, {data.shape[1]} columns")
        return data
    except Exception as e:
        logger.error(f"Error loading cleaned interactions data: {str(e)}")
        raise


def load_clean_merged():
    """Charge le fichier merged_cleaned.csv"""
    try:
        logger.info(f"Loading merged cleaned data from {CLEAN_MERGED}")
        if not CLEAN_MERGED.exists():
            logger.warning(f"Merged cleaned file not found: {CLEAN_MERGED}")
            logger.info("You may need to run data preprocessing first")
            raise FileNotFoundError(f"File not found: {CLEAN_MERGED}")
        
        data = pd.read_csv(CLEAN_MERGED)
        logger.info(f"Successfully loaded merged data: {data.shape[0]} rows, {data.shape[1]} columns")
        return data
    except Exception as e:
        logger.error(f"Error loading merged cleaned data: {str(e)}")
        raise
