from pathlib import Path
import sys, inspect
import streamlit as st
import pandas as pd
import numpy as np
import yaml

# Initialize logging
try:
    from src.logging_config import get_logger
    logger = get_logger('streamlit.utils')
except Exception as e:
    print(f"Warning: Could not initialize logging in utils: {e}")
    logger = None


# ---------------------------------------------------------------------------
# Setup chemin src
# ---------------------------------------------------------------------------
def _ensure_src_on_path():
    root = Path(__file__).resolve()
    for p in [root, *root.parents]:
        if (p / "pyproject.toml").exists():
            project_root = p
            break
    else:
        project_root = Path.cwd()
    for add in (project_root, project_root / "src"):
        s = str(add)
        if s not in sys.path:
            sys.path.insert(0, s)
    return project_root


PROJECT_ROOT = _ensure_src_on_path()


# ---------------------------------------------------------------------------
# Chargement des données (cache)
# ---------------------------------------------------------------------------
@st.cache_data
def _read_csv(rel):
    p = PROJECT_ROOT / rel
    if not p.exists():
        return None
    try:
        return pd.read_csv(p)
    except Exception:
        return None


@st.cache_data(show_spinner=False)
def load_all_datasets():
    """Charge une seule fois toutes les données utiles et les retourne dans un dict."""
    if logger:
        logger.info("Loading all datasets for Streamlit application")
    
    try:
        merged_df = _read_csv("data/processed/merged_cleaned.csv")
        interactions = _read_csv("data/processed/interactions_cleaned.csv")
        clean_recipes = _read_csv("data/processed/recipes_cleaned.csv")
        raw_recipes = _read_csv("data/raw/RAW_recipes.csv")
        raw_interactions = _read_csv("data/raw/RAW_interactions.csv")
        
        # Log dataset information
        datasets_info = {}
        for name, df in [
            ("merged", merged_df),
            ("interactions", interactions),
            ("clean_recipes", clean_recipes),
            ("raw_recipes", raw_recipes),
            ("raw_interactions", raw_interactions)
        ]:
            if df is not None:
                datasets_info[name] = df.shape
                if logger:
                    logger.debug(f"Dataset '{name}': {df.shape}")
            else:
                if logger:
                    logger.warning(f"Dataset '{name}' could not be loaded")
        
        if logger:
            logger.info(f"Successfully loaded {len([d for d in datasets_info.values() if d is not None])} datasets")
        
        return {
            "merged": merged_df,
            "interactions": interactions,
            "clean_recipes": clean_recipes,
            "raw_recipes": raw_recipes,
            "raw_interactions": raw_interactions,
        }
    except Exception as e:
        if logger:
            logger.error(f"Error loading datasets: {str(e)}")
        raise


# --- Chargement commentaires externes (YAML) ---
@st.cache_data
def load_commentary_yaml():
    p = PROJECT_ROOT / "src" / "streamlit" / "app" / "comment.yaml"
    if not p.exists():
        return {}
    try:
        return yaml.safe_load(p.read_text(encoding="utf-8")) or {}
    except Exception:
        return {}


# ---------------------------------------------------------------------------
# Textes explicatifs (extraits / synthèses notebook)
# ---------------------------------------------------------------------------
MD_MAP = {
    "rating_distribution": (
        "Distribution des ratings: forte concentration sur 4 et 5 → biais positif important."
    ),
    "user_mean_rating_distribution": (
        "Moyenne par utilisateur: permet de voir le biais individuel et la dispersion des comportements de notation."
    ),
    "recipe_mean_rating_distribution": (
        "Moyenne par recette: repère les recettes systématiquement sur‑ ou sous‑notées."
    ),
    "top_users_by_activity": (
        "Top utilisateurs actifs: forte concentration de l’activité sur quelques comptes très prolifiques."
    ),
    "user_count_vs_mean_rating": (
        "Relation nombre d’avis vs note moyenne: beaucoup d’utilisateurs peu actifs; les plus actifs ont une moyenne élevée (~4.5–5)."
    ),
    "activity_bucket_bar": (
        "Segmentation de l’activité (buckets) pour comparer la note moyenne selon l’intensité de participation."
    ),
    "plot_prep_time_distribution": (
        "Catégorisation temps de préparation: la majorité ≤ 2h; valeurs extrêmes (0 ou très longues) peu influentes globalement."
    ),
    "plot_ingredient": (
        "Analyse ingrédients: quelques ingrédients dominants (sel, beurre, sucre); Pareto montre forte concentration."
    ),
    "plot_n_steps_distribution": (
        "Nombre d’étapes: distribution et complexité procédurale; extrêmes rares."
    ),
    "plot_tags_distribution": (
        "Distribution du nombre de tags par recette: mesure richesse descriptive et diversité catégorielle."
    ),
    "plot_nutrition_distribution": (
        "Caractéristiques nutritionnelles: dispersion des nutriments clés (calories, sucre, protéines, etc.)."
    ),
    "minutes_group_negative_reviews_bar": (
        "Test influence du temps sur insatisfaction: regroupements courte/moyenne/longue; pas de effet fort observé."
    ),
    "plot_ingredients_vs_negative_score": (
        "Nombre d’ingrédients vs insatisfaction: absence de corrélation notable → complexité n’augmente pas les critiques."
    ),
    "analyze_tags_correlation": (
        "Tags et insatisfaction: certaines catégories (equipment, meat, main-dish) associées à scores négatifs plus élevés."
    ),
    "nutrition_correlation_analysis": (
        "Nutrition vs insatisfaction: pas de corrélations significatives avec les avis négatifs ou score global."
    ),
}

EXTERNAL_COMMENTS = load_commentary_yaml()


def get_comment(func_name: str) -> str:
    # Priorité YAML puis MD_MAP
    return EXTERNAL_COMMENTS.get(func_name) or MD_MAP.get(func_name)


def get_ds():
    """Accès centralisé aux datasets (dans session_state)."""
    if "ds" not in st.session_state:
        st.session_state["ds"] = load_all_datasets()
    return st.session_state["ds"]


# ---------------------------------------------------------------------------
# Wrapper rendu (affiche figure + docstring + texte explicatif)
# ---------------------------------------------------------------------------
FAST_MODE = st.session_state.get("FAST_MODE", False)


def render_viz(
    label,
    func,
    df,
    show_doc=False,
    expander=True,
    sample_if_fast: int | None = None,
    **kwargs,
):
    if df is None:
        st.warning(f"{label}: dataset manquant")
        if logger:
            logger.warning(f"Visualization '{label}' skipped: dataset is None")
        return
    
    if logger:
        logger.debug(f"Rendering visualization: {label} with function {func.__name__}")
    
    block = st.expander(label, expanded=not expander) if expander else st.container()
    with block:
        if FAST_MODE and sample_if_fast and len(df) > sample_if_fast:
            if logger:
                logger.debug(f"Sampling dataset for {label}: {len(df)} -> {sample_if_fast} rows")
            df = df.sample(sample_if_fast, random_state=42)
        try:
            fig = func(df, return_fig=True, **kwargs)
            if fig is None:
                st.info("Figure non retournée.")
                if logger:
                    logger.warning(f"Function {func.__name__} returned None for visualization {label}")
                return
            st.pyplot(fig, use_container_width=True)
            if logger:
                logger.debug(f"Successfully rendered visualization: {label}")
            
            if show_doc:
                doc = inspect.getdoc(func)
                comment = get_comment(func.__name__)
                if doc or comment:
                    with st.container():
                        if doc:
                            st.caption(doc)
                        if comment:
                            st.markdown(comment)
            if FAST_MODE:
                st.caption("FAST_MODE actif (échantillonnage).")
        except Exception as e:
            error_msg = f"Erreur: {e}"
            st.error(error_msg)
            if logger:
                logger.error(f"Error rendering visualization '{label}' with function {func.__name__}: {str(e)}")


def _safe_rerun():
    """Compatibilité versions Streamlit."""
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()
