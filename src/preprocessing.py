import pandas as pd
from pathlib import Path
import json
import re
import matplotlib.pyplot as plt
import seaborn as sns
from .logging_config import get_logger

# étude des avis négatifs
# Importation des constantes
from .constants import (
    NEGATION_WORDS,
    POSITIVE_WORDS,
    NEGATIVE_WORDS,
    CONTRACTIONS,
    SUBTLE_NEG_RE,
    NEGATED_POS_RE,
    CONTRACTIONS_RE,
    TOKEN_RE,
    SENTENCE_SPLIT_RE,
    CLAUSE_BREAKERS,
    DEFAULT_NEGATION_WINDOW,
    NUTRITION_THRESHOLDS,
)


logger = get_logger('preprocessing')

try:
    from src.data_visualization import _finalize
except Exception:

    def _finalize(fig, show=False, return_fig=False):
        if show:
            plt.show()
        return fig if return_fig else None


# Detection des valeurs manquantes
def detect_missing_values(df: pd.DataFrame) -> pd.Series:
    logger.info(f"Detecting missing values in dataframe with shape {df.shape}")
    missing_values = df.isnull().sum()
    missing_count = (missing_values > 0).sum()
    logger.info(f"Found missing values in {missing_count} columns")
    if missing_count > 0:
        logger.debug(f"Columns with missing values: {missing_values[missing_values > 0].to_dict()}")
    return missing_values[missing_values > 0]


# Detection des doublons
def detect_duplicates(df: pd.DataFrame) -> int:
    logger.info(f"Detecting duplicates in dataframe with shape {df.shape}")
    duplicates_count = df.duplicated().sum()
    logger.info(f"Found {duplicates_count} duplicate rows")
    if duplicates_count > 0:
        logger.warning(f"Dataset contains {duplicates_count} duplicate rows that may need removal")
    return duplicates_count


# suppression des valeurs abbérantes pour les colonnes nutritionnelles
# paramètres de la fonction : dataframe, colonne, limite haute
def remove_outliers_nutrition(
    df: pd.DataFrame, column: str, upper_limit: float
) -> pd.DataFrame:
    return df[df[column] <= upper_limit]


def save_cleaned_datasets(cleaned_df, file_name, output_dir="../data/processed"):
    """
    Sauvegarde les datasets nettoyés avec métadonnées

    Args:
        cleaned_df: DataFrame des données nettoyées
        output_dir: Répertoire de destination
    """
    try:
        logger.info(f"Starting to save cleaned dataset: {file_name}")
        logger.debug(f"Dataset shape: {cleaned_df.shape}")

        # Créer le répertoire
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
        logger.debug(f"Output directory created/verified: {output_path}")

        logger.info(f"=== SAUVEGARDE DANS {output_path} ===")

        # Sauvegarder les datasets
        cleaned_file = output_path / f"{file_name}.csv"

        cleaned_df.to_csv(cleaned_file, index=False)
        logger.info(f"✅ Successfully saved: {cleaned_file} ({cleaned_df.shape})")

        return {"interactions_file": cleaned_file}
    except Exception as e:
        logger.error(f"Error saving cleaned dataset {file_name}: {str(e)}")
        raise



def clean_review(text: str, window: int = 3) -> str:
    if not text:
        return ""
    s = CONTRACTIONS_RE.sub(
        lambda m: CONTRACTIONS[m.group(0).lower()], str(text).lower().strip()
    )
    tokens = TOKEN_RE.findall(s)
    out, neg = [], 0
    for t in tokens:
        if t in CLAUSE_BREAKERS:
            neg = 0
            continue
        if t in NEGATION_WORDS or t == "not":
            neg = window
            out.append("not")
            continue
        if neg > 0 and t in POSITIVE_WORDS:
            out.append(f"not_{t}")
            neg -= 1
            continue
        out.append(t)
        if neg > 0:
            neg -= 1
    return " ".join(out)


_SENT_SPLIT_RE = re.compile(r"[.!?;]+")


def is_negative_sentence(sent: str, clean_tokens: list) -> bool:
    if SUBTLE_NEG_RE.search(sent):
        return True
    toks = re.findall(r"[a-z]+", sent.lower())
    if any(t in NEGATIVE_WORDS for t in toks):
        return True
    if any(t in NEGATION_WORDS or t == "not" for t in toks) and any(
        t in POSITIVE_WORDS for t in toks
    ):
        return True
    if any(NEGATED_POS_RE.match(t) for t in clean_tokens):
        return True
    return False


def binary_sentiment(review: str, clean_review_str: str) -> int:
    clean_tokens = clean_review_str.split()
    for s in filter(None, _SENT_SPLIT_RE.split(str(review))):
        if is_negative_sentence(s, clean_tokens):
            return 1
    return 0


# merge des deux datasets pour analyse
def merge_datasets(interactions_df, recipes_df, on="recipe_id"):
    merged_df = interactions_df.merge(recipes_df, on=on, how="left")
    return merged_df
