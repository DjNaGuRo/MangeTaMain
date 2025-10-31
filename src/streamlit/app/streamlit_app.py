"""Application Streamlit principale (plots + textes explicatifs)."""

import streamlit as st
import pandas as pd
import numpy as np
import sys, inspect
from pathlib import Path

import yaml


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
        plot_minutes_ningredients_nsteps,
    )
    from src.preprocessing import (
        detect_missing_values,
        detect_duplicates,
        remove_outliers_nutrition,
        clean_review,
        is_negative_sentence,
        binary_sentiment,
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


@st.cache_data(show_spinner=False)
def load_all_datasets():
    """Charge une seule fois toutes les données utiles et les retourne dans un dict."""
    merged_df = _read_csv("data/processed/merged_cleaned.csv")
    interactions = _read_csv("data/processed/interactions_cleaned.csv")
    clean_recipes = _read_csv("data/processed/recipes_cleaned.csv")
    raw_recipes = _read_csv("data/raw/RAW_recipes.csv")
    raw_interactions = _read_csv("data/raw/RAW_interactions.csv")
    return {
        "merged": merged_df,
        "interactions": interactions,
        "clean_recipes": clean_recipes,
        "raw_recipes": raw_recipes,
        "raw_interactions": raw_interactions,
    }


def get_ds():
    """Accès centralisé aux datasets (dans session_state)."""
    if "ds" not in st.session_state:
        st.session_state["ds"] = load_all_datasets()
    return st.session_state["ds"]


# ---------------------------------------------------------------------------
# Thème
# ---------------------------------------------------------------------------
def set_custom_theme(theme="Clair"):
    if theme == "Sombre":
        colors = {
            "primary": "#ffffff",
            "secondary": "#f0f0f0",
            "background": "#181a1b",
            "text": "#e0e0e0",
            "header_gradient": "linear-gradient(135deg,#444,#111)",
            "sidebar_gradient": "linear-gradient(180deg,#333,#111)",
            "button_text": "#ffffff",
        }
    else:
        colors = {
            "primary": "#667eea",
            "secondary": "#764ba2",
            "background": "#F0F2F6",
            "text": "#2C3E50",
            "header_gradient": "linear-gradient(135deg,#667eea,#764ba2)",
            "sidebar_gradient": "linear-gradient(180deg,#667eea,#764ba2)",
            "button_text": "#ffffff",
        }
    st.markdown(
        f"""
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
    """,
        unsafe_allow_html=True,
    )


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


EXTERNAL_COMMENTS = load_commentary_yaml()


def get_comment(func_name: str) -> str:
    # Priorité YAML puis MD_MAP
    return EXTERNAL_COMMENTS.get(func_name) or MD_MAP.get(func_name)


PAGES_ORDER = [
    ("🏠 Accueil", "home", lambda: show_home_page()),
    ("📊 Données cleaning", "data", lambda: show_data_page()),
    ("📈 Visualisations", "viz", lambda: show_visualizations()),
]


def _init_page_state():
    if "current_page_idx" not in st.session_state:
        st.session_state.current_page_idx = 0


def _go_delta(delta: int):
    st.session_state.current_page_idx = (
        st.session_state.current_page_idx + delta
    ) % len(PAGES_ORDER)


def _set_page_by_key(page_key: str):
    for i, (_, key, _) in enumerate(PAGES_ORDER):
        if key == page_key:
            st.session_state.current_page_idx = i
            break


def _safe_rerun():
    """Compatibilité versions Streamlit."""
    if hasattr(st, "rerun"):
        st.rerun()
    elif hasattr(st, "experimental_rerun"):
        st.experimental_rerun()


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
        return
    block = st.expander(label, expanded=not expander) if expander else st.container()
    with block:
        if FAST_MODE and sample_if_fast and len(df) > sample_if_fast:
            df = df.sample(sample_if_fast, random_state=42)
        try:
            fig = func(df, return_fig=True, **kwargs)
            if fig is None:
                st.info("Figure non retournée.")
                return
            st.pyplot(fig, use_container_width=True)
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
            st.error(f"Erreur: {e}")


# ---------------------------------------------------------------------------
# Page Accueil
# ---------------------------------------------------------------------------
def show_home_page():
    recipes_df = get_ds()["clean_recipes"]
    raw_interactions = get_ds()["raw_interactions"]

    st.markdown("## INTRODUCTION")
    st.markdown(
        """Notre équipe composé de Guy, Mohamed, Leonnel, Omar et Osman avons décidé de travailler sur le projet MangeTaMain sur la problématique 
            du **taux d'insatisfaction des recettes** en nous basant sur 2 tables : les recettes et les interactions utilisateurs (notes, avis).
            Voici un aperçu de la table recette :
                """
    )

    st.dataframe(recipes_df.head(5), use_container_width=True)

    st.markdown("""et voici un aperçu de la table interactions :""")

    st.dataframe(raw_interactions.head(5), use_container_width=True)

    st.markdown(
        """Le travaille se décline en plusieurs étapes :  
                - **data_cleaning** : comprendre la structure, les types de données, les valeurs manquantes, les valeurs aberrantes, etc.  
                - **Analyse univariée** : analyse statistique descriptive et visualisations pour comprendre les tendances, les distributions, les corrélations, etc.  
                - **Analyse bivariée** : exploration des relations entre les variables, identification des facteurs influençant le taux d'insatisfaction.  
                - **Ouverture** : Conclusion et suggestions pour la poursuite de l'analyse  
                """
    )

    # Boutons navigation rapides
    st.markdown("### Navigation rapide")
    c1, c2 = st.columns(2)
    with c1:
        if st.button("📊 Aller à la page data cleaning"):
            _set_page_by_key("data")
            _safe_rerun()
    with c2:
        if st.button("📈 Aller aux Visualisations"):
            _set_page_by_key("viz")
            _safe_rerun()


# ---------------------------------------------------------------------------
# Page Data cleaning
# ---------------------------------------------------------------------------
def show_data_page():
    st.markdown("## Data cleaning pour la table interactions")
    df_raw_interactions = get_ds()["raw_interactions"]
    if df_raw_interactions is None:
        st.error("Données non disponibles.")
        return

    st.markdown(
        """Il est primordial de nettoyer les données avant de procéder à toute analyse. Intéressons nous aux valeurs manquantes :"""
    )

    missing_interactions = detect_missing_values(df_raw_interactions)
    missing_df = (
        missing_interactions[missing_interactions > 0]
        .sort_values(ascending=False)
        .to_frame(name="missing")
        .astype(int)
    )

    if missing_df.empty:
        st.success("Aucune valeur manquante détectée.")
    else:
        with st.expander("Nombre de valeurs manquantes", expanded=False):
            for col, val in missing_df["missing"].items():
                st.write(f"{col}: {val}")

    # imputation
    st.markdown(
        """Nous avons décidé d'imputer les valeurs manquantes de la colonne 'review' par :  
        - "Excellent recipe! Loved it!" si rating = 5  
        - "Great recipe, will make again." si rating = 4  
        - "Good recipe, but could be improved." si rating = 3  
        - "Not my favorite."" si rating = 2  
        - "Did not like this recipe at all." si rating = 1  
        
        La proportion de valeurs manquantes est de 0.01%, donc cette imputation n'affectera pas significativement l'analyse globale.  
    Nous avons également vérifié qu'il n'y avait pas de doublons dans le dataset."""
    )

    st.markdown("### Analyse de la colonne rating")

    st.markdown(
        """
    Les notes données par les utilisateurs sont comprises entre 1 et 5. Cependant, nous observons que plusieurs lignes du jeu de données présentent une note égale à 0 (rating = 0), tout en contenant un commentaire textuel (review) souvent positif ou négatif.
    Cette situation est incohérente : une note de 0 ne correspond pas à une appréciation valide sur une échelle de 1 à 5, et le contenu des commentaires indique que les utilisateurs ont bien exprimé une opinion sur la recette.

    Nous en déduisons que la valeur 0 ne traduit pas une mauvaise note, mais plutôt l’absence de note — autrement dit, une valeur manquante codée par 0.

    En conséquence, nous considérons toutes les notes égales à 0 comme valeurs manquantes et nous les remplaçons par NaN afin de ne pas biaiser les statistiques descriptives ni les calculs de moyennes.
    Cela revient à interpréter ces cas comme des utilisateurs ayant laissé un commentaire sans attribuer de note chiffrée.
                """
    )

    st.markdown("### Evaluation de la proportion d'avis négatifs")

    st.markdown(
        """
    Notre étude portant sur les caractéristiques des recettes générant des avis négatifs, nous cherchons dans un premier temps à identifier les avis négatis.

    **PROCEDURE :**

    Au vue de la proportion très importante d'avis positif dans le dataset, nous admettrons qu'une recette est moins appréciée au moins 1 avis sur cette recette présente des suggestions ou des axes d'améliorations. En se basant sur ce constat, 2 features pourraient nous des informations. Dans un premier temps, nous allons considérer les recettes qui ont des avis notés à 3 ou moins et dans un second temps nous allons nous concentrer sur commentaires portant au moins un aspect négatif pour les avis ayant une note de 0 (absencce de note) et 4. Nous nous interesserons pas aux commentaires des recettes ayant reçu uniquement des notes de 5.
                """
    )

    st.markdown(
        """Nous avons donc commencé par isoler les avis avec une note de 3 ou moins :"""
    )

    ### CREATION DE LA COLONNE BINARY SENTIMENT

    df_raw_interactions["binary_sentiment"] = df_raw_interactions["rating"].apply(
        lambda x: 1 if x in [1, 2, 3] else 0
    )

    # Seed échantillon dans session_state
    if "binary_sample_seed" not in st.session_state:
        st.session_state.binary_sample_seed = 0

    interactions_binary_sentiment = st.multiselect(
        "Colonnes à afficher",
        df_raw_interactions.columns.tolist(),
        default=df_raw_interactions.columns.tolist()[:8],
    )

    # Échantillon stable (tant que seed inchangé)
    sample_df = df_raw_interactions[interactions_binary_sentiment].sample(
        min(5, len(df_raw_interactions)),
        random_state=st.session_state.binary_sample_seed,
    )
    st.dataframe(sample_df, use_container_width=True)

    col_btn, col_info = st.columns([1, 3])
    with col_btn:
        if st.button("🔄 Rafraîchir échantillon"):
            st.session_state.binary_sample_seed += 1
            _safe_rerun()
    with col_info:
        st.caption(f"Seed échantillon: {st.session_state.binary_sample_seed}")

    st.markdown(
        """Nous pouvons observer que les avis avec un rating de 1 à 3 ont bien un binary_sentiment de 1."""
    )

    st.markdown(
        """Passons maintenant aux avis avec un rating de 0 ou 4 :
                Comme expliqué précédemment, les avis avec un rating de 0 sont considérés comme une absence de note, mais contiennent des commentaires textuels qui peuvent nous donner une information sur l'insatisfaction de l'utilisateur concernant la recette.  
                De plus les avis avec un rating de 4 peuvent également contenir des commentaires négatifs, car une note de 4 n'est pas parfaite et peut refléter certaines insatisfactions. Exemple : "it was an amazing dish, we appreciated it so much, [...], but it was too sweet", ceci est une proposition d'amélioration de la recette par l'utilisateur et compte donc comme un avis négatif. Nous allons donc analyser les commentaires textuels (review) des avis avec un rating de 0 ou 4 pour détecter la présence d'aspects négatifs.  
                Pour cela nous allons faire de la tokenization et de l'analyse de sentiment afin d'identifier les phrases négatives dans les commentaires.  
                Enfin après avoir identifié les commentaires négatifs, nous mettons à jour la colonne binary_sentiment dans le dataset original.
                """
    )

    # ---------------------------------------------------------------------------
    # Cleaning de la table recipes
    # ---------------------------------------------------------------------------

    st.markdown("### Data cleaning pour la table recettes")

    df_raw_recipes = get_ds()["raw_recipes"]
    if df_raw_recipes is None:
        st.error("Données non disponibles.")
        return

    missing_recipes = detect_missing_values(df_raw_recipes)
    missing_recipes_df = (
        missing_recipes[missing_recipes > 0]
        .sort_values(ascending=False)
        .to_frame(name="missing")
        .astype(int)
    )

    if missing_recipes_df.empty:
        st.success("Aucune valeur manquante détectée.")
    else:
        with st.expander("Nombre de valeurs manquantes", expanded=False):
            for col, val in missing_recipes_df["missing"].items():
                st.write(f"{col}: {val}")

    # imputation
    st.markdown(
        """Nous obervons que les données manquantes sont dans la colonne 'description' de la recette. Cette variable n'est pas utile dans notre étude, donc pour ne pas avoir de valeurs manquantes 
        nous avons décidé d'imputer les valeurs manquantes par "No_description". Nous avons également supprimé la ligne dont l'information dans "name" était manquante.
        Nous avons également vérifié qu'il n'y avait pas de doublons dans le dataset."""
    )

    st.markdown(""" **étude des valeurs extrêmes:**  """)

    render_viz(
        "boxplot des minutes, n_ingredients et n_steps",
        plot_minutes_ningredients_nsteps,
        df_raw_recipes,
    )

    st.markdown(
        """Nous pouvons remarquer la présence de valeurs extrêmes dans les 3 colonnes, en particulier dans la colonne temps de préparation
                """
    )

    st.markdown(
        """Pour la colonne *minutes* nous décidons de ne pas garder les recettes qui ont plus de 1 mois en temps
                de préparation, ces valeurs représentent 0.03% du dataset"""
    )

    st.markdown("""**colonne nutrition**""")

    st.markdown(
        """Pour la colonne nutrition nous faisons du feature engineering : nous allons split les valeurs nutritionelles respectivement par 'calories', 'total_fat', 'sugar', 'sodium', 'protein', 'saturated_fat', 'carbohydrates' """
    )

    st.markdown("""voici un aperçu de la table après le split""")

    df_raw_recipes[
        [
            "calories",
            "total_fat",
            "sugar",
            "sodium",
            "protein",
            "saturated_fat",
            "carbohydrates",
        ]
    ] = df_raw_recipes.nutrition.str.split(",", expand=True)

    splitted_recipes = st.multiselect(
        "Colonnes à afficher",
        df_raw_recipes.columns.tolist(),
        default=df_raw_recipes.columns.tolist()[:19],
    )
    st.dataframe(df_raw_recipes[splitted_recipes].head(5), use_container_width=True)

    st.markdown(
        """ Pour chacune des valeurs nutritionnelles, il également est possible de remarquer des valeurs très extrêmes ! Les valeurs max sont des valeurs abérrantes cependant d'autre valeurs tel que les recettes à plus de 3 000 calories sont potentiellement des recettes avec des scores nutritionnels calculés pour la totalité de la recette et non normalisé (par exemple par portion). les valeurs nutritionnels pour une portion sont d'environs 200~800 kcal. Comme nous n'avons pas d'information sur la quantité considéré (portion ou recette total), on décide donc de supprimer les recettes à plus de 3000 calories sachant qu'ils représentent qu'un très petit pourcentage de recette.  

        De même les valeurs nutrionnels pour :  
        - les glucides : 20 ~ 100 g > suppression des recettes à plus de 500g  
        - protéines : 10 ~ 100 g > suppression des recettes à plus de 500g  
        - Sodium : 200 ~ 1500 mg > suppression des recettes à plus de 5000mg  """
    )


# ---------------------------------------------------------------------------ra
# Page Visualisations
# ---------------------------------------------------------------------------
def show_visualizations():
    st.markdown("## Visualisations")

    df_merged = get_ds()["merged"]
    df_inter = get_ds()["interactions"]
    df_clean_recipes = get_ds()["clean_recipes"]

    tabs = st.tabs(
        ["Distribution", "Utilisateurs", "Recettes", "Corrélations", "Nutrition"]
    )

    with tabs[0]:
        render_viz("Distribution brute des notes", rating_distribution, df_inter)

        st.markdown(""" Distribution brute des notes """)

        render_viz(
            "Moyennes des notes par recette", recipe_mean_rating_distribution, df_inter
        )
        render_viz(
            "Moyennes des notes par utilisateur",
            user_mean_rating_distribution,
            df_inter,
        )
        
        render_viz(
            "Analyse des contributeurs des recettes",
            analyze_contributors,
            df_clean_recipes,
        )

    with tabs[1]:
        render_viz("Top utilisateurs actifs", top_users_by_activity, df_inter)
        render_viz("Activité (buckets) vs note moyenne", activity_bucket_bar, df_inter)
        render_viz(
            "Nombre d'avis vs moyenne (échantillon)",
            user_count_vs_mean_rating,
            df_inter,
            sample=2500,
        )

    with tabs[2]:
        render_viz(
            "Temps de préparation (catégories)", plot_prep_time_distribution, df_merged
        )
        render_viz(
            "Ingrédients + Pareto",
            plot_ingredient,
            df_clean_recipes if df_clean_recipes is not None else df_merged,
        )
        render_viz("Nombre d'étapes", plot_n_steps_distribution, df_merged)
        if df_merged is not None and "tags" in df_merged.columns:
            render_viz("Distribution des tags", plot_tags_distribution, df_merged)
            if st.checkbox("Afficher stats tags"):
                try:
                    st.dataframe(analyse_tags(df_merged))
                except Exception as e:
                    st.error(e)
        if df_clean_recipes is not None and st.checkbox("Stats ingrédients vectorisés"):
            st.dataframe(analyze_ingredients_vectorized(df_clean_recipes))

    with tabs[3]:
        if df_merged is not None:
            render_viz(
                "Minutes vs insatisfaction (groupes)",
                minutes_group_negative_reviews_bar,
                df_merged,
            )
            if {"n_ingredients", "negative_reviews"}.issubset(df_merged.columns):
                render_viz(
                    "Ingrédients vs insatisfaction",
                    plot_ingredients_vs_negative_score,
                    df_merged,
                )
            if "tags" in df_merged.columns and {
                "negative_reviews",
                "total_reviews",
            }.issubset(df_merged.columns):
                render_viz(
                    "Tags vs insatisfaction", analyze_tags_correlation, df_merged
                )

    with tabs[4]:
        needed = {
            "calories",
            "sugar",
            "protein",
            "sodium",
            "total_fat",
            "carbohydrates",
        }
        if df_merged is None or not needed.issubset(df_merged.columns):
            st.warning("Colonnes nutrition manquantes.")
        else:
            render_viz("Distribution nutrition", plot_nutrition_distribution, df_merged)
            render_viz(
                "Corrélations nutrition ↔ insatisfaction",
                nutrition_correlation_analysis,
                df_merged,
            )


# ---------------------------------------------------------------------------
# Main
# ---------------------------------------------------------------------------
def main():
    st.set_page_config(page_title="MangeTaMain", page_icon="🍽️", layout="wide")
    _init_page_state()
    if "theme" not in st.session_state:
        st.session_state.theme = "Clair"
    set_custom_theme(st.session_state.theme)

    ds = get_ds()

    # Barre supérieure avec chevrons
    top_left, top_center, top_right = st.columns([0.7, 5, 0.7])
    with top_left:
        if st.button("◀"):
            _go_delta(-1)
            _safe_rerun()
    with top_center:
        label, key, _ = PAGES_ORDER[st.session_state.current_page_idx]
        st.markdown(
            f"<h2 style='text-align:center'>{label}</h2>", unsafe_allow_html=True
        )
    with top_right:
        if st.button("▶"):
            _go_delta(1)
            _safe_rerun()

    with st.sidebar:
        st.markdown("### Pages")
        selected = st.radio(
            "Aller à",
            [lbl for (lbl, _, _) in PAGES_ORDER],
            index=st.session_state.current_page_idx,
        )
        if PAGES_ORDER[st.session_state.current_page_idx][0] != selected:
            for i, (lbl, key, _) in enumerate(PAGES_ORDER):
                if lbl == selected:
                    st.session_state.current_page_idx = i
                    _safe_rerun()
                    break
        st.selectbox(
            "Thème",
            ["Clair", "Sombre"],
            index=["Clair", "Sombre"].index(st.session_state.theme),
            key="theme_selector",
            on_change=lambda: st.session_state.update(
                theme=st.session_state.theme_selector
            ),
        )
        if not DV_OK:
            st.caption(f"⚠️ Module viz: KO ({DV_ERR})")

    st.markdown(
        """
    <div class="main-header">
      <h1>🍽️ MangeTaMain</h1>
      <p>Analyse des recettes et interactions (plots & explications)</p>
    </div>
    """,
        unsafe_allow_html=True,
    )

    _, _, render = PAGES_ORDER[st.session_state.current_page_idx]
    render()


if __name__ == "__main__":
    main()
