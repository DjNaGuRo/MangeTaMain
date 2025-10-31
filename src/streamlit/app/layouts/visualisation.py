import streamlit as st
from pathlib import Path
import sys

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

from src.streamlit.app.utils  import get_ds, render_viz, _safe_rerun

# ---------------------------------------------------------------------------
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

