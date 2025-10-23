import pandas as pd
from pathlib import Path

# Path des données brutes
# RAW_recipes.csv
RAW_DATA_PATH_R = Path(__file__).parent.parent / "data" / "raw" / "RAW_recipes.csv"

# RAW_interactions.csv
RAW_DATA_PATH_I = Path(__file__).parent.parent / "data" / "raw" / "RAW_interactions.csv"


def load_recipes_data():
    return pd.read_csv(RAW_DATA_PATH_R)


def load_interactions_data():
    return pd.read_csv(RAW_DATA_PATH_I)
