from __future__ import annotations
import os, io
from pathlib import Path
import pandas as pd
from .logging_config import get_logger

logger = get_logger('data_loader')

DATA_DIR = Path(__file__).parent.parent / "data"
RAW_DIR = DATA_DIR / "raw"
PROCESSED_DIR = DATA_DIR / "processed"

RAW_RECIPES = RAW_DIR / "RAW_recipes.csv"
RAW_INTERACTIONS = RAW_DIR / "RAW_interactions.csv"
CLEAN_RECIPES = PROCESSED_DIR / "recipes_cleaned.csv"
CLEAN_INTERACTIONS = PROCESSED_DIR / "interactions_cleaned.csv"
CLEAN_MERGED = PROCESSED_DIR / "merged_cleaned.csv"

def _get_secret(name: str) -> str | None:
    try:
        import streamlit as st
        return st.secrets.get(name)
    except Exception:
        return None

def _get_url(var_name: str) -> str | None:
    return _get_secret(var_name) or os.getenv(var_name)

def _read_any(path_or_buf):
    s = str(path_or_buf).lower()
    if s.endswith((".parquet", ".parq", ".pq")):
        return pd.read_parquet(path_or_buf)
    return pd.read_csv(path_or_buf)

def _read_remote(url: str) -> pd.DataFrame:
    import requests
    r = requests.get(url, timeout=60)
    r.raise_for_status()
    buf = io.BytesIO(r.content)
    return _read_any(url if url.lower().endswith((".parquet", ".parq", ".pq")) else buf)

def _load_local_or_url(local_path: Path, url_env_name: str, label: str) -> pd.DataFrame:
    if local_path.exists():
        df = _read_any(str(local_path))
        return df
    url = _get_url(url_env_name)
    if not url:
        raise FileNotFoundError(f"Missing local file {local_path} and env/secret {url_env_name}")
    return _read_remote(url)

def load_recipes_data():        return _load_local_or_url(RAW_RECIPES, "RECIPES_RAW_URL", "raw recipes")
def load_interactions_data():   return _load_local_or_url(RAW_INTERACTIONS, "INTERACTIONS_RAW_URL", "raw interactions")
def load_clean_recipes():       return _load_local_or_url(CLEAN_RECIPES, "RECIPES_CLEAN_URL", "clean recipes")
def load_clean_interactions():  return _load_local_or_url(CLEAN_INTERACTIONS, "INTERACTIONS_CLEAN_URL", "clean interactions")
def load_clean_merged():        return _load_local_or_url(CLEAN_MERGED, "MERGED_CLEAN_URL", "merged cleaned")
