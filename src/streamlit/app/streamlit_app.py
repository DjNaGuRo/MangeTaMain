"""Application Streamlit principale (plots + textes explicatifs)."""
import streamlit as st
import pandas as pd
import numpy as np
import sys, inspect
from pathlib import Path

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
# Imports visualisation
# ---------------------------------------------------------------------------
try:
    from src.data_visualization import (
        rating_distribution,
        recipe_mean_rating_distribution,
        top_users_by_activity,
        user_mean_rating_distribution,
        user_count_vs_mean_rating,
        activity_bucket_bar,
        analyze_contributors,
        statistique_descriptive,
        plot_prep_time_distribution,
        plot_ingredient,
        plot_n_steps_distribution,
        analyse_tags,
        plot_tags_distribution,
        plot_nutrition_distribution,
        analyze_ingredients_vectorized,
        minutes_group_negative_reviews_bar,
        spearman_correlation,
        plot_ingredients_vs_negative_score,
        analyze_tags_correlation,
        nutrition_correlation_analysis,
        get_most_negative_user,
    )
    DV_OK = True
    DV_ERR = None
except Exception as e:
    DV_OK = False
    DV_ERR = e

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

def load_recipes_data():
    return _read_csv("src/data/processed/merged_cleaned.csv")

def load_interactions_data():
    return _read_csv("src/data/processed/interactions_cleaned.csv")

def load_clean_recipes_data():
    return _read_csv("src/data/processed/recipes_cleaned.csv")


# ---------------------------------------------------------------------------
# Thème
# ---------------------------------------------------------------------------
def set_custom_theme(theme="Clair"):
    if theme == "Sombre":
        colors = {
            "primary": "#ffffff","secondary": "#f0f0f0","background": "#181a1b",
            "text": "#e0e0e0","header_gradient": "linear-gradient(135deg,#444,#111)",
            "sidebar_gradient": "linear-gradient(180deg,#333,#111)","button_text":"#ffffff"
        }
    else:
        colors = {
            "primary": "#667eea","secondary": "#764ba2","background": "#F0F2F6",
            "text": "#2C3E50","header_gradient": "linear-gradient(135deg,#667eea,#764ba2)",
            "sidebar_gradient": "linear-gradient(180deg,#667eea,#764ba2)","button_text":"#ffffff"
        }
    st.markdown(f"""
    <style>
    .stApp {{background:{colors['background']}; color:{colors['text']};}}
    .main-header {{background:{colors['header_gradient']}; padding:1.4rem; border-radius:14px;
                   color:{colors['button_text']} !important; text-align:center; margin-bottom:1.0rem;}}
    [data-testid="stSidebar"] {{background:{colors['sidebar_gradient']};}}
    [data-testid="stSidebar"] * {{color:#ffffff !important;}}
    .stButton>button {{
        background:{colors['header_gradient']}; color:{colors['button_text']} !important;
        border:none; border-radius:24px; padding:0.55rem 1.3rem; font-weight:600;
    }}
    </style>
    """, unsafe_allow_html=True)

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

# ---------------------------------------------------------------------------
# Wrapper rendu (affiche figure + docstring + texte explicatif)
# ---------------------------------------------------------------------------
def render_viz(label, func, df, show_doc=True, **kwargs):
    st.markdown(f"### {label}")
    if df is None:
        st.warning("Dataset manquant")
        return
    if not DV_OK:
        st.error(f"Module visualisation indisponible: {DV_ERR}")
        return
    try:
        fig = func(df, return_fig=True, **kwargs)
        if fig is None:
            st.info("Figure non retournée (return_fig manquant).")
            return
        st.pyplot(fig)
        if show_doc:
            doc = inspect.getdoc(func)
            if doc:
                st.caption(doc)
        extra = MD_MAP.get(func.__name__)
        if extra:
            st.markdown(extra)
    except Exception as e:
        st.error(f"Erreur: {e}")

# ---------------------------------------------------------------------------
# Page Accueil
# ---------------------------------------------------------------------------
def show_home_page():
    col1, col2 = st.columns([2,1])
    with col1:
        st.markdown("## Accueil")
        st.write("Application d’analyse des recettes et interactions.")
        name = st.text_input("Nom")
        if name:
            st.success(f"Bonjour {name}")
    with col2:
        df = load_recipes_data()
        if df is not None:
            st.metric("Recettes", len(df))
            st.metric("Colonnes", len(df.columns))
            st.metric("Manquants", int(df.isnull().sum().sum()))
        else:
            st.warning("Fichier merged_cleaned.csv absent.")

# ---------------------------------------------------------------------------
# Page Données
# ---------------------------------------------------------------------------
def show_data_page():
    st.markdown("## Aperçu données recettes")
    df = load_recipes_data()
    if df is None:
        st.error("Données non disponibles.")
        return
    cols = st.multiselect("Colonnes à afficher", df.columns.tolist(), default=df.columns.tolist()[:8])
    st.dataframe(df[cols].head(300), use_container_width=True)
    st.markdown("### Statistiques descriptives")
    st.dataframe(df.describe(include='all').transpose(), use_container_width=True)

# ---------------------------------------------------------------------------
# Page Visualisations
# ---------------------------------------------------------------------------
def show_visualizations():
    st.markdown("## Visualisations")
    df_recipes = load_recipes_data()
    df_inter = load_interactions_data()
    df_clean = load_clean_recipes_data()

    tabs = st.tabs(["Distribution", "Utilisateurs", "Recettes", "Corrélations", "Nutrition"])

    with tabs[0]:
        render_viz("Distribution brute des notes", rating_distribution, df_inter)
        render_viz("Moyennes des notes par recette", recipe_mean_rating_distribution, df_inter)
        render_viz("Moyennes des notes par utilisateur", user_mean_rating_distribution, df_inter)

    with tabs[1]:
        render_viz("Top utilisateurs actifs", top_users_by_activity, df_inter)
        render_viz("Activité (buckets) vs note moyenne", activity_bucket_bar, df_inter)
        render_viz("Nombre d'avis vs moyenne (échantillon)", user_count_vs_mean_rating, df_inter, sample=2500)

    with tabs[2]:
        render_viz("Temps de préparation (catégories)", plot_prep_time_distribution, df_recipes)
        render_viz("Ingrédients + Pareto", plot_ingredient, df_clean if df_clean is not None else df_recipes)
        render_viz("Nombre d'étapes", plot_n_steps_distribution, df_recipes)
        if df_recipes is not None and "tags" in df_recipes.columns:
            render_viz("Distribution des tags", plot_tags_distribution, df_recipes)
            if st.checkbox("Afficher stats tags"):
                try:
                    st.dataframe(analyse_tags(df_recipes))
                except Exception as e:
                    st.error(e)
        if df_clean is not None and st.checkbox("Stats ingrédients vectorisés"):
            st.dataframe(analyze_ingredients_vectorized(df_clean))

    with tabs[3]:
        if df_recipes is not None:
            render_viz("Minutes vs insatisfaction (groupes)", minutes_group_negative_reviews_bar, df_recipes)
            if {"n_ingredients","negative_reviews"}.issubset(df_recipes.columns):
                render_viz("Ingrédients vs insatisfaction", plot_ingredients_vs_negative_score, df_recipes)
            if "tags" in df_recipes.columns and {"negative_reviews","total_reviews"}.issubset(df_recipes.columns):
                render_viz("Tags vs insatisfaction", analyze_tags_correlation, df_recipes)

    with tabs[4]:
        needed = {"calories","sugar","protein","sodium","total_fat","carbohydrates"}
        if df_recipes is None or not needed.issubset(df_recipes.columns):
            st.warning("Colonnes nutrition manquantes.")
        else:
            render_viz("Distribution nutrition", plot_nutrition_distribution, df_recipes)
            render_viz("Corrélations nutrition ↔ insatisfaction", nutrition_correlation_analysis, df_recipes)

# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    st.set_page_config(page_title="MangeTaMain", page_icon="🍽️", layout="wide")
    if "theme" not in st.session_state:
        st.session_state.theme = "Clair"
    set_custom_theme(st.session_state.theme)

    with st.sidebar:
        st.markdown("### Navigation")
        pages = {
            "🏠 Accueil": show_home_page,
            "📊 Données": show_data_page,
            "📈 Visualisations": show_visualizations,
        }
        choice = st.radio("Page", list(pages.keys()))
        st.selectbox(
            "Thème",
            ["Clair","Sombre"],
            index=["Clair","Sombre"].index(st.session_state.theme),
            key="theme_selector",
            on_change=lambda: st.session_state.update(theme=st.session_state.theme_selector),
        )
        st.caption("Module viz: " + ("OK" if DV_OK else f"KO ({DV_ERR})"))

    st.markdown("""
    <div class="main-header">
      <h1>🍽️ MangeTaMain</h1>
      <p>Analyse des recettes et interactions (plots + explications)</p>
    </div>
    """, unsafe_allow_html=True)

    pages[choice]()

if __name__ == "__main__":
    main()