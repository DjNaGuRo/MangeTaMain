"""
Mes visualisations univariées / bivariées pour la table `interactions`.
- Je veux un code clair, PEP8, sans sauvegarde PNG.
- J’utilise seaborn pour les KDE et certains barplots.
- Pas de double rendu dans Jupyter: je contrôle show/close/return.
"""

from __future__ import annotations

import ast
from typing import Optional, Sequence, Tuple, List
from collections import Counter

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# Initialize logging for visualizations
try:
    from .logging_config import get_logger
    logger = get_logger('visualization')
except Exception as e:
    print(f"Warning: Could not initialize logging in data_visualization: {e}")
    logger = None

# Ma palette fixe (Jaune, Bleu, Rouge, Vert, Violet, Gris)
PALETTE: Tuple[str, ...] = (
    "#F2C94C",  # jaune
    "#2F80ED",  # bleu
    "#EB5757",  # rouge
    "#27AE60",  # vert
    "#9B51E0",  # violet
    "#4F4F4F",  # gris
)


# ---------------------------------------------------------------------
# Petits utilitaires
# ---------------------------------------------------------------------
def _need_cols(df: pd.DataFrame, required: Sequence[str]) -> None:
    """Je vérifie que les colonnes requises sont bien présentes."""
    missing = [c for c in required if c not in df.columns]
    if missing:
        raise KeyError(f"Colonnes manquantes : {missing}")


def _finalize(fig: plt.Figure, show: bool, return_fig: bool):
    """
    Ma règle anti-doublon :
    - si show=True : j’affiche puis je ferme, et je ne retourne rien.
    - si return_fig=True : je ne montre pas, je ne ferme pas, et je retourne la figure.
    - sinon : je ferme et je ne retourne rien.
    (Patch Streamlit: si return_fig=True on NE ferme PAS, pas de plt.show()).
    """
    if return_fig:
        return fig
    if show:
        plt.show()
    plt.close(fig)
    return None


# ---------------------------------------------------------------------
# 1) Distribution des notes 1..5 + KDE
# ---------------------------------------------------------------------
def rating_distribution(
    interactions: pd.DataFrame,
    show: bool = False,
    return_fig: bool = False,
    kde: bool = True,
):
    """Je trace la distribution des notes (1..5). Je peux ajouter un KDE."""
    try:
        if logger:
            logger.debug(f"Generating rating distribution visualization (kde={kde})")
        
        _need_cols(interactions, ["rating"])
        s = pd.to_numeric(interactions["rating"], errors="coerce").dropna()
        s = s[(s >= 1) & (s <= 5)]
        
        if logger:
            logger.debug(f"Rating data: {len(s)} valid ratings out of {len(interactions)} total")

        fig, ax = plt.subplots(figsize=(6, 4))
        ax.hist(s, bins=[0.5, 1.5, 2.5, 3.5, 4.5, 5.5], color=PALETTE[1], edgecolor="white")
        ax.set_title("Distribution des notes valides")
        ax.set_xlabel("Note")
        ax.set_ylabel("Nombre d'occurrences")
        ax.set_xticks([1, 2, 3, 4, 5])
        ax.grid(axis="y", alpha=0.25)

        if kde:
            sns.kdeplot(s, ax=ax, color=PALETTE[5], lw=2)
        
        if logger:
            logger.debug("Successfully generated rating distribution plot")

        return _finalize(fig, show, return_fig)
    except Exception as e:
        if logger:
            logger.error(f"Error generating rating distribution plot: {str(e)}")
        raise


# fonction d'affichage des boxplots minutes, n_ingredients, n_steps


def plot_minutes_ningredients_nsteps(
    data_recipes: pd.DataFrame, show: bool = False, return_fig: bool = False
):
    """Trace le boxplot des minutes, du nombre d'ingrédients et du nombre d'étapes.

    Args:
        raw_recipes (pd.DataFrame): DataFrame contenant les données brutes des recettes.
        show (bool, optional): Indique si le graphique doit être affiché. Par défaut False.
        return_fig (bool, optional): Indique si la figure doit être retournée. Par défaut False.

    Returns:
        Optional[plt.Figure]: La figure matplotlib si return_fig est True, sinon None.
    """
    fig = plt.figure(figsize=(12, 6))

    plt.subplot(1, 3, 1)
    plt.boxplot(data_recipes["n_ingredients"])
    plt.title("Boxplot du nombre d'ingrédients")

    plt.subplot(1, 3, 2)
    plt.boxplot(data_recipes["n_steps"])
    plt.title("Boxplot du nombre d'étapes")

    plt.subplot(1, 3, 3)
    plt.boxplot(data_recipes["minutes"])
    plt.title("Boxplot du temps de préparation (minutes)")

    plt.tight_layout()
    plt.show()
    return _finalize(fig, show, return_fig)


# ---------------------------------------------------------------------
# 2) Distribution des moyennes par recette + KDE
# ---------------------------------------------------------------------
def recipe_mean_rating_distribution(
    interactions: pd.DataFrame,
    bins: int = 25,
    show: bool = False,
    return_fig: bool = False,
    kde: bool = True,
):
    """Je calcule la moyenne des notes par recette puis je trace un histo (+KDE)."""
    _need_cols(interactions, ["recipe_id", "rating"])
    tmp = interactions.copy()
    tmp["rating"] = pd.to_numeric(tmp["rating"], errors="coerce")
    g = (
        tmp.dropna(subset=["rating"])
        .groupby("recipe_id", observed=True)["rating"]
        .mean()
    )

    fig, ax = plt.subplots(figsize=(8, 5))
    ax.hist(g, bins=bins, color=PALETTE[0], alpha=0.9, edgecolor="white")
    ax.set_title("Distribution des notes moyennes par recette")
    ax.set_xlabel("Note moyenne")
    ax.set_ylabel("Nombre de recettes")
    ax.grid(axis="y", alpha=0.25)

    if kde:
        sns.kdeplot(g, ax=ax, color=PALETTE[5], lw=2)

    return _finalize(fig, show, return_fig)


# ---------------------------------------------------------------------
# 3) Top-10 utilisateurs par activité
# ---------------------------------------------------------------------
def top_users_by_activity(
    interactions: pd.DataFrame,
    top_k: int = 10,
    show: bool = False,
    return_fig: bool = False,
):
    """Je montre les utilisateurs qui ont le plus d’interactions (Top-k)."""
    _need_cols(interactions, ["user_id"])
    counts = interactions["user_id"].value_counts().head(top_k)

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.bar(counts.index.astype(str), counts.values, color=PALETTE[2])
    ax.set_title(f"Top {top_k} des utilisateurs avec le plus d'interactions")
    ax.set_xlabel("User ID")
    ax.set_ylabel("Nombre d'interactions")
    ax.tick_params(axis="x", labelrotation=45)
    for lab in ax.get_xticklabels():
        lab.set_horizontalalignment("right")
    ax.grid(axis="y", alpha=0.25)

    return _finalize(fig, show, return_fig)


# ---------------------------------------------------------------------
# 4) Distribution de la moyenne des notes par utilisateur + KDE
# ---------------------------------------------------------------------
def user_mean_rating_distribution(
    interactions: pd.DataFrame,
    bins: int = 40,
    show: bool = False,
    return_fig: bool = False,
    kde: bool = True,
):
    """Je trace la distribution de la moyenne des notes attribuées par utilisateur."""
    _need_cols(interactions, ["user_id", "rating"])
    tmp = interactions.copy()
    tmp["rating"] = pd.to_numeric(tmp["rating"], errors="coerce")
    g = tmp.dropna(subset=["rating"]).groupby("user_id", observed=True)["rating"].mean()

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(g, bins=bins, color=PALETTE[3], alpha=0.95, edgecolor="white")
    ax.set_title("Distribution de la moyenne des notes par utilisateur")
    ax.set_xlabel("Moyenne des notes attribuées")
    ax.set_ylabel("Nombre d'utilisateurs")
    ax.grid(axis="y", alpha=0.25)

    if kde:
        sns.kdeplot(g, ax=ax, color=PALETTE[5], lw=2)

    return _finalize(fig, show, return_fig)


# ---------------------------------------------------------------------
# 5) Scatter : nombre d’avis ↔ note moyenne
# ---------------------------------------------------------------------
def user_count_vs_mean_rating(
    interactions: pd.DataFrame,
    sample: Optional[int] = None,
    alpha: float = 0.6,
    show: bool = False,
    return_fig: bool = False,
):
    """Je relie le nombre d’avis d’un user à sa note moyenne (scatter)."""
    _need_cols(interactions, ["user_id", "rating"])
    tmp = interactions.copy()
    tmp["rating"] = pd.to_numeric(tmp["rating"], errors="coerce")
    tmp = tmp.dropna(subset=["rating"])

    agg = (
        tmp.groupby("user_id", observed=True)
        .agg(n_reviews=("rating", "size"), mean_rating=("rating", "mean"))
        .reset_index()
    )
    if sample and len(agg) > sample:
        agg = agg.sample(sample, random_state=42)

    fig, ax = plt.subplots(figsize=(9, 5))
    ax.scatter(
        agg["n_reviews"], agg["mean_rating"], s=18, alpha=alpha, color=PALETTE[4]
    )
    ax.set_title(
        "Relation entre le nombre d'avis laissés et la note moyenne par utilisateur"
    )
    ax.set_xlabel("Nombre d'avis laissés")
    ax.set_ylabel("Note moyenne attribuée")
    ax.grid(alpha=0.25)

    return _finalize(fig, show, return_fig)


# ---------------------------------------------------------------------
# 6) Activité (mes bornes) ↔ moyenne des notes (barplot seaborn)
# ---------------------------------------------------------------------
def activity_bucket_bar(
    interactions: pd.DataFrame,
    bins: Tuple[int, int, int, int] = (0, 1, 10, 60),  # => [0,1,10,60,inf]
    labels: Tuple[str, str, str, str] = ("Faible", "Modérée", "Haute", "Extrême"),
    show: bool = False,
    return_fig: bool = False,
):
    """
    Je catégorise l’activité utilisateur avec mes bornes
    puis je trace la moyenne des notes par catégorie.
    """
    _need_cols(interactions, ["user_id", "rating"])

    df = interactions.copy()
    df["rating"] = pd.to_numeric(df["rating"], errors="coerce")
    df = df.dropna(subset=["rating"])

    counts = df["user_id"].value_counts()
    df["n_interactions_user"] = df["user_id"].map(counts)

    full_bins = [*bins, float("inf")]
    df["interaction_level"] = pd.cut(
        df["n_interactions_user"],
        bins=full_bins,
        labels=labels,
        include_lowest=True,
        ordered=True,
    )

    user_stats = (
        df.groupby("user_id", observed=True)
        .agg(
            note_moyenne=("rating", "mean"),
            interaction_level=("interaction_level", "first"),
        )
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(
        data=user_stats,
        x="interaction_level",
        y="note_moyenne",
        order=list(labels),
        color=PALETTE[1],
        ax=ax,
        estimator=np.mean,
    )
    ax.set_title("Relation entre l'activité et la moyenne des notes attribuées")
    ax.set_xlabel("Catégorie d'activité de l'utilisateur")
    ax.set_ylabel("Moyenne des notes")
    ax.set_ylim(0, 5.2)
    ax.grid(axis="y", alpha=0.25)

    return _finalize(fig, show, return_fig)


# fonction permettant de récupérer l'utilisateur avec le plus d'avis dont le rating est entre 1 et 3 et affiche ses notes
def get_most_negative_user(interactions: pd.DataFrame) -> int:
    """Récupère l'utilisateur avec le plus d'avis négatifs (notes 1 à 3) et affiche ses statistiques.
    Args:
        interactions (pd.DataFrame): DataFrame des interactions utilisateurs.
    Returns:
        dict :  Dictionnaire avec l'ID utilisateur et le décompte des notes 1 à 5.
    """

    most_negative_user_id = (
        interactions.groupby("user_id")["rating"]
        .apply(lambda x: (x <= 3).sum())
        .idxmax()
    )

    most_negative_user_reviews = interactions[
        interactions["user_id"] == most_negative_user_id
    ]
    rating_counts = (
        most_negative_user_reviews["rating"]
        .value_counts()
        .reindex([1, 2, 3, 4, 5], fill_value=0)
    )

    review_counts = {
        "user_id": most_negative_user_id,
        "rating_counts": rating_counts.to_dict(),
    }

    return review_counts


## Anlyse des contributeurs
def analyze_contributors(
    df_pp_raw_recipes: pd.DataFrame,
    show: bool = False,
    return_fig: bool = False,
) -> Optional[plt.Figure]:
    """Analyse des contributeurs dans le dataset des recettes nettoyées.

    Args:
        df_pp_raw_recipes (pd.DataFrame): DataFrame des recettes nettoyées.
        show (bool): Afficher directement (Jupyter).
        return_fig (bool): Retourner la figure (Streamlit).

    Returns:
        Optional[plt.Figure]: Figure si return_fig=True.
    """
    _need_cols(df_pp_raw_recipes, ["contributor_id"])
    total_recipes = len(df_pp_raw_recipes)
    unique_contributors = df_pp_raw_recipes["contributor_id"].nunique()

    contributor_counts = df_pp_raw_recipes["contributor_id"].value_counts()

    fig, axs = plt.subplots(2, 2, figsize=(12, 8))

    contributor_counts_limited = contributor_counts[contributor_counts <= 20]
    axs[0, 0].hist(contributor_counts_limited, bins=20, alpha=0.7)
    axs[0, 0].set_xlabel("Nombre de recettes par contributeur")
    axs[0, 0].set_ylabel("Nombre de contributeurs")
    axs[0, 0].set_title("Distribution des contributions (≤20 recettes)")

    axs[0, 1].boxplot(contributor_counts)
    axs[0, 1].set_ylabel("Nombre de recettes")
    axs[0, 1].set_title("Boxplot des contributions")

    top_20 = contributor_counts.head(20)
    axs[1, 0].bar(range(1, len(top_20) + 1), top_20.values)
    axs[1, 0].set_xlabel("Rang du contributeur")
    axs[1, 0].set_ylabel("Nombre de recettes")
    axs[1, 0].set_title("Top 20 contributeurs")
    axs[1, 0].set_xticks(range(1, len(top_20) + 2, 2))

    cumsum_recipes = contributor_counts.sort_values(ascending=False).cumsum()
    axs[1, 1].plot(
        range(1, len(cumsum_recipes) + 1), cumsum_recipes.values / total_recipes * 100
    )
    axs[1, 1].set_xlabel("Nombre de contributeurs")
    axs[1, 1].set_ylabel("% cumulé des recettes")
    axs[1, 1].set_title("Concentration des contributions")
    axs[1, 1].grid(True)

    fig.tight_layout()

    # (Ancien code calcul concentration conservé si besoin futur)
    _ = unique_contributors  # placeholders pour éviter avertissements

    return _finalize(fig, show, return_fig)


# statistique descriptive pour les variables non catégorielles
def statistique_descriptive(df: pd.DataFrame, column: str) -> pd.DataFrame:
    """Calcule des statistiques descriptives sur une colonne donnée.

    Args:
        df (pd.DataFrame): DataFrame des recettes nettoyées.
        column (str): Nom de la colonne à analyser.

    Returns:
        pd.DataFrame: DataFrame contenant les statistiques descriptives.
    """
    column_data = df[column]

    stats = {
        "Moyenne": column_data.mean(),
        "Médiane": column_data.median(),
        "Écart-type": column_data.std(),
        "Variance": column_data.var(),
        "Minimum": column_data.min(),
        "Maximum": column_data.max(),
        "quantile_025": column_data.quantile(0.25),
        "quantile_075": column_data.quantile(0.75),
        "skewness": column_data.skew(),
        "kurtosis": column_data.kurtosis(),
    }

    stats_df = pd.DataFrame.from_dict(stats, orient="index", columns=["Valeur"])
    return stats_df


# visualisation graphique du temps de préparation des recettes


# catégorisation des temps de préparation
def categorize_cooking_time(minutes):
    if minutes <= 15:
        return "Très rapide (≤15 min)"
    elif minutes <= 30:
        return "Rapide (16-30 min)"
    elif minutes <= 60:
        return "Moyen (31-60 min)"
    elif minutes <= 120:
        return "Long (1-2h)"
    elif minutes <= 240:
        return "Très long (2-4h)"
    else:
        return "Extrême (>4h)"


def plot_prep_time_distribution(
    df: pd.DataFrame, show: bool = False, return_fig: bool = False
) -> Optional[plt.Figure]:
    """Trace la distribution du temps de préparation des recettes.

    Args:
        df (pd.DataFrame): DataFrame des recettes nettoyées.
        show (bool, optional): Indique si le graphique doit être affiché. Par défaut False.
        return_fig (bool, optional): Indique si la figure doit être retournée. Par défaut False.

    Returns:
        Optional[plt.Figure]: La figure matplotlib si return_fig est True, sinon None.
    """

    df_temp = df.copy()
    df_temp["time_category"] = df_temp["minutes"].apply(categorize_cooking_time)
    time_distribution = df_temp["time_category"].value_counts()

    fig, ax = plt.subplots(figsize=(14, 10))
    ax.bar(
        time_distribution.index, time_distribution.values, color=PALETTE[0], alpha=0.9
    )
    ax.set_title("Distribution des temps de préparation des recettes")
    ax.set_xlabel("Catégorie de temps de préparation")
    ax.set_ylabel("Nombre de recettes")
    ax.grid(axis="y", alpha=0.25)

    return _finalize(fig, show, return_fig)


# Version encore plus rapide avec vectorisation
def analyze_ingredients_vectorized(df: pd.DataFrame) -> pd.DataFrame:
    """Version vectorisée ultra-rapide.

    Args:
        df (pd.DataFrame): DataFrame des recettes nettoyées.

    Returns:
        pd.DataFrame: DataFrame contenant les statistiques sur les ingrédients.
    """

    def parse_and_count(x):
        try:
            parsed = ast.literal_eval(x) if isinstance(x, str) else x
            return len(parsed), parsed
        except:
            return 0, []

    results = df["ingredients"].apply(parse_and_count)

    lengths = pd.Series([r[0] for r in results])
    ingredients_lists = [r[1] for r in results]

    all_ingredients = [item for sublist in ingredients_lists for item in sublist]

    ingredient_counts = Counter(all_ingredients)

    stats = {
        "Nb_uniques_ingredients": len(ingredient_counts),
        "Nb_total_ingredients": len(all_ingredients),
        "Nb_ingredients_les_plus_utilises": ingredient_counts.most_common(3),
        "Moyenne": lengths.mean(),
        "Médiane": lengths.median(),
        "Écart-type": lengths.std(),
        "Minimum": lengths.min(),
        "Maximum": lengths.max(),
    }

    return pd.DataFrame.from_dict(stats, orient="index", columns=["Valeur"])


# fonction de visualisation pour les ingrédients
def plot_ingredient(
    df: pd.DataFrame, show: bool = False, return_fig: bool = False
) -> Optional[plt.Figure]:
    """Trace la distribution du nombre d'ingrédients par recette et la courbe de pareto

    Args:
        df (pd.DataFrame): DataFrame des recettes nettoyées.
        show (bool, optional): Indique si le graphique doit être affiché. Par défaut False.
        return_fig (bool, optional): Indique si la figure doit être retournée. Par défaut False.

    Returns:
        Optional[plt.Figure]: La figure matplotlib si return_fig est True, sinon None.
    """
    ingredients_per_recipe = df["ingredients"].apply(lambda x: len(ast.literal_eval(x)))

    def list_ingredients(df: pd.DataFrame) -> List[str]:
        all_ingredients = []
        for ingredients in df["ingredients"]:
            try:
                parsed_ingredients = ast.literal_eval(ingredients)
                all_ingredients.extend(parsed_ingredients)
            except (ValueError, SyntaxError):
                continue
        return all_ingredients

    list_ingredient = list_ingredients(df)
    ingredient_counts = Counter(list_ingredient)

    total_uses = sum(ingredient_counts.values())
    cumulative_uses = 0
    sorted_ingredients = ingredient_counts.most_common()
    rank_80_percent = 0

    for rank, (_, count) in enumerate(sorted_ingredients, start=1):
        cumulative_uses += count
        if cumulative_uses / total_uses >= 0.8:
            rank_80_percent = rank
            break

    fig, axes = plt.subplots(1, 2, figsize=(18, 10))
    axes[0].hist(
        ingredients_per_recipe, bins=30, alpha=0.7, color="lightblue", edgecolor="black"
    )
    axes[0].set_title("Distribution du nombre d'ingrédients par recette")
    axes[0].set_xlabel("Nombre d'ingrédients")
    axes[0].set_ylabel("Fréquence")
    axes[0].axvline(
        ingredients_per_recipe.mean(),
        color="red",
        linestyle="--",
        label=f"Moyenne: {ingredients_per_recipe.mean():.1f}",
    )
    axes[0].legend()

    frequencies_all = list(ingredient_counts.values())
    sorted_frequencies = sorted(frequencies_all, reverse=True)
    cumulative_percent = np.cumsum(sorted_frequencies) / sum(sorted_frequencies) * 100
    axes[1].plot(range(1, len(cumulative_percent) + 1), cumulative_percent)
    axes[1].set_title("Courbe de Pareto - Concentration des ingrédients")
    axes[1].set_xlabel("Rang de l'ingrédient")
    axes[1].set_ylabel("% cumulé des utilisations")
    axes[1].axvline(
        rank_80_percent,
        color="green",
        linestyle="--",
        alpha=0.7,
        label=f"{rank_80_percent}ème ingrédient le plus utilisé",
    )
    axes[1].grid(True, alpha=0.3)
    axes[1].axhline(80, color="red", linestyle="--", alpha=0.7, label="80%")
    axes[1].legend()

    fig.tight_layout()
    return _finalize(fig, show, return_fig)


# fonction de catégorisation du nombre d'étapes
def categorize_steps(n_steps):
    if n_steps <= 3:
        return "Très simple (≤3 étapes)"
    elif n_steps <= 6:
        return "Simple (4-6 étapes)"
    elif n_steps <= 10:
        return "Modéré (7-10 étapes)"
    elif n_steps <= 15:
        return "Complexe (11-15 étapes)"
    elif n_steps <= 20:
        return "Très complexe (16-20 étapes)"
    else:
        return "Extrême (>20 étapes)"


# visualisation graphique sur le nombre d'étapes des recettes
def plot_n_steps_distribution(
    df: pd.DataFrame, show: bool = False, return_fig: bool = False
) -> Optional[plt.Figure]:
    """Trace la distribution du nombre d'étapes des recettes.

    Args:
        df (pd.DataFrame): DataFrame des recettes nettoyées.
        show (bool, optional): Indique si le graphique doit être affiché. Par défaut False.
        return_fig (bool, optional): Indique si la figure doit être retournée. Par défaut False.

    Returns:
        Optional[plt.Figure]: La figure matplotlib si return_fig est True, sinon None.
    """

    df_temp = df.copy()
    df_temp["complexity_category"] = df_temp["n_steps"].apply(categorize_steps)
    complexity_distribution = df_temp["complexity_category"].value_counts()

    fig, axes = plt.subplots(2, 2, figsize=(18, 12))

    axes[0, 0].hist(
        df["n_steps"], bins=30, alpha=0.7, color="skyblue", edgecolor="black"
    )
    axes[0, 0].axvline(
        df["n_steps"].mean(),
        color="red",
        linestyle="--",
        label=f'Moyenne: {df["n_steps"].mean():.1f}',
    )
    axes[0, 0].axvline(
        df["n_steps"].median(),
        color="orange",
        linestyle="--",
        label=f'Médiane: {df["n_steps"].median():.1f}',
    )
    axes[0, 0].set_title("Distribution du nombre d'étapes")
    axes[0, 0].set_xlabel("Nombre d'étapes")
    axes[0, 0].set_ylabel("Fréquence")
    axes[0, 0].legend()
    axes[0, 0].grid(True, alpha=0.3)

    complexity_order = [
        "Très simple (≤3 étapes)",
        "Simple (4-6 étapes)",
        "Modéré (7-10 étapes)",
        "Complexe (11-15 étapes)",
        "Très complexe (16-20 étapes)",
        "Extrême (>20 étapes)",
    ]
    complexity_ordered = complexity_distribution.reindex(complexity_order, fill_value=0)
    complexity_ordered.plot(kind="bar", ax=axes[1, 0], color="lightcoral", alpha=0.8)
    axes[1, 0].set_title("Distribution par catégories de complexité")
    axes[1, 0].set_xlabel("Catégories de complexité")
    axes[1, 0].set_ylabel("Nombre de recettes")
    axes[1, 0].tick_params(axis="x", rotation=45)

    sorted_steps = np.sort(df["n_steps"])
    cumulative_prob = np.arange(1, len(sorted_steps) + 1) / len(sorted_steps)
    axes[0, 1].plot(sorted_steps, cumulative_prob, linewidth=2)
    axes[0, 1].set_title("Distribution cumulative")
    axes[0, 1].set_xlabel("Nombre d'étapes")
    axes[0, 1].set_ylabel("Probabilité cumulative")
    axes[0, 1].grid(True, alpha=0.3)

    colors = ["#ff9999", "#66b3ff", "#99ff99", "#ffcc99", "#ff99cc", "#c2c2f0"]
    axes[1, 1].pie(
        complexity_ordered.values,
        labels=complexity_ordered.index,
        autopct="%1.1f%%",
        colors=colors,
        startangle=90,
    )
    axes[1, 1].set_title("Répartition par complexité")

    fig.tight_layout()
    return _finalize(fig, show, return_fig)


# étude de la variable tags
def analyse_tags(df: pd.DataFrame) -> pd.DataFrame:
    """Analyse de la variable 'tags' dans le dataset des recettes nettoyées.

    Args:
        df (pd.DataFrame): DataFrame des recettes nettoyées.

    Returns:
        pd.DataFrame: DataFrame contenant les statistiques sur les tags.
    """
    l_tags = list(df.tags)
    list_tags = []
    for item in l_tags:
        item = ast.literal_eval(item)
        for i in item:
            list_tags.append(i)

    tag_counts = Counter(list_tags)
    most_common_tags = tag_counts.most_common(3)

    frequency_distribution = {}
    for tag, count in tag_counts.items():
        if count == 1:
            frequency_distribution["Unique (1)"] = (
                frequency_distribution.get("Unique (1)", 0) + 1
            )
        elif count <= 5:
            frequency_distribution["Très rare (2-5)"] = (
                frequency_distribution.get("Très rare (2-5)", 0) + 1
            )
        elif count <= 20:
            frequency_distribution["Rare (6-20)"] = (
                frequency_distribution.get("Rare (6-20)", 0) + 1
            )
        elif count <= 100:
            frequency_distribution["Peu commun (21-100)"] = (
                frequency_distribution.get("Peu commun (21-100)", 0) + 1
            )
        elif count <= 1000:
            frequency_distribution["Commun (101-1000)"] = (
                frequency_distribution.get("Commun (101-1000)", 0) + 1
            )
        else:
            frequency_distribution["Très commun (>1000)"] = (
                frequency_distribution.get("Très commun (>1000)", 0) + 1
            )

    percent_frequency = {
        k: v / len(tag_counts.values()) * 100 for k, v in frequency_distribution.items()
    }
    stats = {
        "Nb_uniques_tags": len(set(list_tags)),
        "Nb_tags_les_plus_utilises": most_common_tags,
        "Taux_tags_Uniques (1)": percent_frequency.get("Unique (1)", 0),
        "Taux_tags_Tres_rares (2-5)": percent_frequency.get("Très rare (2-5)", 0),
        "Taux_tags_Rares (6-20)": percent_frequency.get("Rare (6-20)", 0),
        "Taux_tags_Peu_communs (21-100)": percent_frequency.get(
            "Peu commun (21-100)", 0
        ),
        "Taux_tags_Communs (101-1000)": percent_frequency.get("Commun (101-1000)", 0),
        "Taux_tags_Tres_communs (>1000)": percent_frequency.get(
            "Très commun (>1000)", 0
        ),
    }

    stats_df = pd.DataFrame.from_dict(stats, orient="index", columns=["Valeur"])
    return stats_df


# fonction de visualisation distribution du nombre de tags par recette
def plot_tags_distribution(
    df: pd.DataFrame, show: bool = False, return_fig: bool = False
) -> Optional[plt.Figure]:
    """Trace la distribution du nombre de tags par recette.

    Args:
        df (pd.DataFrame): DataFrame des recettes nettoyées.
        show (bool, optional): Indique si le graphique doit être affiché. Par défaut False.
        return_fig (bool, optional): Indique si la figure doit être retournée. Par défaut False.

    Returns:
        Optional[plt.Figure]: La figure matplotlib si return_fig est True, sinon None.
    """

    tags_per_recipe = df["tags"].apply(lambda x: len(ast.literal_eval(x)))

    fig, ax = plt.subplots(figsize=(10, 6))
    ax.hist(tags_per_recipe, bins=30, alpha=0.7, color="lightgreen", edgecolor="black")
    ax.set_title("Distribution du nombre de tags par recette")
    ax.set_xlabel("Nombre de tags")
    ax.set_ylabel("Fréquence")
    ax.axvline(
        tags_per_recipe.mean(),
        color="red",
        linestyle="--",
        label=f"Moyenne: {tags_per_recipe.mean():.1f}",
    )
    ax.axvline(
        tags_per_recipe.median(),
        color="orange",
        linestyle="--",
        label=f"Médiane: {tags_per_recipe.median():.1f}",
    )
    ax.legend()
    ax.grid(True, alpha=0.3)

    return _finalize(fig, show, return_fig)


### fonction permettant d'afficher la distribution des calories, du sucre et des protéines, saturated fat, total fat, carbohydrates et sodium
def plot_nutrition_distribution(
    df: pd.DataFrame, show: bool = False, return_fig: bool = False
) -> Optional[plt.Figure]:
    """Trace la distribution d'une variable nutritionnelle donnée.

    Args:
        df (pd.DataFrame): DataFrame des recettes nettoyées.
        column (str): Nom de la colonne nutritionnelle à analyser.
        show (bool, optional): Indique si le graphique doit être affiché. Par défaut False.
        return_fig (bool, optional): Indique si la figure doit être retournée. Par défaut False.

    Returns:
        Optional[plt.Figure]: La figure matplotlib si return_fig est True, sinon None.
    """

    fig, axes = plt.subplots(2, 3, figsize=(18, 12))
    sns.histplot(df["calories"], bins=20, kde=False, ax=axes[0, 0], color="skyblue")
    axes[0, 0].set_title("Distribution des calories")
    axes[0, 0].set_xlabel("Calories (kcal)")
    sns.histplot(df["sugar"], bins=20, kde=False, ax=axes[0, 1], color="lightgreen")
    axes[0, 1].set_title("Distribution du sucre")
    axes[0, 1].set_xlabel("Sucre (g)")
    sns.histplot(df["protein"], bins=20, kde=False, ax=axes[0, 2], color="salmon")
    axes[0, 2].set_title("Distribution des protéines")
    axes[0, 2].set_xlabel("Protéines (g)")
    sns.histplot(df["sodium"], bins=20, kde=False, ax=axes[1, 0], color="orange")
    axes[1, 0].set_title("Distribution du sodium")
    axes[1, 0].set_xlabel("Sodium (mg)")
    sns.histplot(df["total_fat"], bins=20, kde=False, ax=axes[1, 1], color="purple")
    axes[1, 1].set_title("Distribution des graisses totales")
    axes[1, 1].set_xlabel("Graisses totales (g)")
    sns.histplot(df["carbohydrates"], bins=20, kde=False, ax=axes[1, 2], color="brown")
    axes[1, 2].set_title("Distribution des carbohydrates")
    axes[1, 2].set_xlabel("Carbohydrates (g)")
    fig.tight_layout()

    return _finalize(fig, show, return_fig)


# ---------------------------------------------------------------------
# BIVARIÉ — Durée (minutes) → groupes → insatisfaction
# ---------------------------------------------------------------------
def minutes_group_negative_reviews_bar(
    merged_df: pd.DataFrame,
    minutes_col: str = "minutes",
    y_col: str = "negative_reviews",
    show: bool = False,
    return_fig: bool = False,
):
    """Trace le score moyen d’insatisfaction selon la durée de préparation.

    Cette fonction regroupe les recettes selon la durée de préparation :
        - Invalide si minutes = 0 ou manquant
        - Courte ≤ 30 min
        - Moyenne 31–180 min
        - Longue > 180 min
    Après le filtrage, j’affiche un barplot clair et lisible avec seaborn.
    """

    _need_cols(merged_df, [minutes_col, y_col])

    def _regroup_time(m):
        if pd.isna(m):
            return "Invalide"
        m = float(m)
        if m == 0:
            return "Invalide"
        elif m <= 30:
            return "Courte (≤30 min)"
        elif m <= 180:
            return "Moyenne (31–180 min)"
        else:
            return "Longue (>180 min)"

    df = merged_df[[minutes_col, y_col]].copy()
    df[minutes_col] = pd.to_numeric(df[minutes_col], errors="coerce")
    df[y_col] = pd.to_numeric(df[y_col], errors="coerce")

    df["time_group"] = df[minutes_col].apply(_regroup_time)
    df = df[(df["time_group"] != "Invalide") & df[y_col].notna()]

    order = ["Courte (≤30 min)", "Moyenne (31–180 min)", "Longue (>180 min)"]

    fig, ax = plt.subplots(1, 2, figsize=(14, 8))
    sns.barplot(
        data=df,
        x="time_group",
        y=y_col,
        order=order,
        errorbar=None,
        edgecolor="black",
        hue="time_group",
        palette="crest",
        ax=ax[0],
    )
    ax[0].set_title(
        "Score moyen d’insatisfaction selon la durée de préparation", fontsize=13
    )
    ax[0].set_xlabel("Catégorie de durée")
    ax[0].set_ylabel("Score moyen d’insatisfaction")
    ax[0].grid(axis="y", alpha=0.25)

    sns.regplot(
        data=df[df["minutes"] < 1000],
        x="minutes",
        y=y_col,
        scatter_kws={"alpha": 0.3, "s": 10},
        line_kws={"color": "red"},
        ax=ax[1],
    )
    ax[1].set_xscale("log")
    ax[1].set_title(
        "Relation entre le temps de préparation et le score d’insatisfaction"
    )
    ax[1].set_xlabel("Durée de préparation (minutes, échelle log)")
    ax[1].set_ylabel("Score d’insatisfaction")

    return _finalize(fig, show, return_fig)


# fonction de corrélation de Spearman
def spearman_correlation(df: pd.DataFrame, col1: str, col2: str) -> float:
    """Calcule le coefficient de corrélation de Spearman entre deux colonnes.

    Args:
        df (pd.DataFrame): DataFrame contenant les données.
        col1 (str): Nom de la première colonne.
        col2 (str): Nom de la deuxième colonne.

    Returns:
        corr (float): Coefficient de corrélation.
    """
    corr = df[col1].corr(df[col2], method="spearman")
    return corr


###visualison de la distribution du nombre d'ingrédients par recette en fonction du score d'insatisfaction
def plot_ingredients_vs_negative_score(
    merged_df: pd.DataFrame, show: bool = False, return_fig: bool = False
):
    """Trace la relation entre le nombre d’ingrédients et le score d’insatisfaction.

    Args:
        merged_df (pd.DataFrame): DataFrame fusionné contenant les données.
        show (bool, optional): Indique si le graphique doit être affiché. Par défaut False.
        return_fig (bool, optional): Indique si la figure doit être retournée. Par défaut False.
    Returns:
        Optional[plt.Figure]: La figure matplotlib si return_fig est True, sinon None.
    """
    fig = plt.figure(figsize=(7, 5))
    sns.scatterplot(
        data=merged_df, x="n_ingredients", y="negative_reviews", alpha=0.3, s=10
    )
    plt.title("Relation entre le nombre d’ingrédients et le score d’insatisfaction")
    plt.xlabel("Nombre d’ingrédients")
    plt.ylabel("Score d’insatisfaction")
    return _finalize(fig, show, return_fig)


### analyse de la corrélation entre les tags et le score d'insatisfaction
def analyze_tags_correlation(
    merged_df: pd.DataFrame, show: bool = False, return_fig: bool = False
):
    """Analyse la corrélation entre les tags et le score d’insatisfaction.

    Args:
        merged_df (pd.DataFrame): DataFrame fusionné contenant les données.
        show (bool, optional): Indique si le graphique doit être affiché. Par défaut False.
        return_fig (bool, optional): Indique si la figure doit être retournée. Par défaut False.
    Returns:
        Optional[plt.Figure]: La figure matplotlib si return_fig est True, sinon None.
    """

    def safe_eval(x):
        if isinstance(x, list):
            return x
        if isinstance(x, str):
            try:
                return ast.literal_eval(x)
            except:
                return []
        return []

    merged_df = merged_df.copy()
    merged_df["tags"] = merged_df["tags"].apply(safe_eval)

    tag_counts = Counter(
        tag for tags in merged_df["tags"] if isinstance(tags, list) for tag in tags
    )

    top_tags = [t for t, _ in tag_counts.most_common(15)]
    tag_sentiment = []

    merged_df["negative_score"] = merged_df["negative_reviews"] * np.log1p(
        merged_df["total_reviews"]
    )

    for tag in top_tags:
        subset = merged_df[
            merged_df["tags"].apply(lambda tags: isinstance(tags, list) and tag in tags)
        ]
        mean_score = subset["negative_score"].mean()
        count = len(subset)
        tag_sentiment.append((tag, mean_score, count))

    tag_df = pd.DataFrame(
        tag_sentiment, columns=["tag", "mean_negative_score", "count"]
    ).sort_values("mean_negative_score", ascending=False)
    tag_df["popularity"] = tag_df["count"]
    combined = tag_df.copy()

    fig, ax = plt.subplots(2, 1, figsize=(12, 12))

    sns.barplot(
        data=tag_df.head(10),
        x="mean_negative_score",
        y="tag",
        palette="rocket",
        hue="mean_negative_score",
        ax=ax[0],
    )
    ax[0].set_title("Top 10 des tags de recettes les plus critiqués")
    ax[0].set_xlabel("Score moyen d’insatisfaction")
    ax[0].set_ylabel("Tag (type de recette)")
    ax[0].grid(axis="x", alpha=0.25)
    ax[0].legend([], [], frameon=False)

    sns.scatterplot(
        data=combined,
        x="popularity",
        y="mean_negative_score",
        hue="mean_negative_score",
        palette="coolwarm",
        size="mean_negative_score",
        sizes=(50, 200),
        alpha=0.7,
        ax=ax[1],
    )
    ax[1].set_title(
        "Relation entre la popularité des tags et leur score d’insatisfaction"
    )
    ax[1].set_xlabel("Fréquence du tag (nombre de recettes)")
    ax[1].set_ylabel("Score moyen d’insatisfaction")
    ax[1].set_xscale("log")
    ax[1].legend([], [], frameon=False)

    fig.tight_layout()
    return _finalize(fig, show, return_fig)


# correlation entre les caractéristiques nutritionnelles et le score d'insatisfaction
def nutrition_correlation_analysis(
    merged_df: pd.DataFrame, show: bool = False, return_fig: bool = False
):
    """Analyse la corrélation entre les caractéristiques nutritionnelles et le score d’insatisfaction.

    Args:
        merged_df (pd.DataFrame): DataFrame fusionné contenant les données.
        show (bool, optional): Indique si le graphique doit être affiché. Par défaut False.
        return_fig (bool, optional): Indique si la figure doit être retournée. Par défaut False.
    Returns:
        Optional[plt.Figure]: La figure matplotlib si return_fig est True, sinon None.
    """

    nutrition_cols = [
        "calories",
        "sugar",
        "protein",
        "sodium",
        "total_fat",
        "carbohydrates",
    ]

    merged_df = merged_df.copy()
    merged_df["negative_score"] = merged_df["negative_reviews"] * np.log1p(
        merged_df["total_reviews"]
    )

    fig = plt.figure(figsize=(8, 5))
    sns.heatmap(
        merged_df[nutrition_cols + ["negative_score"]].corr(method="spearman"),
        annot=True,
        cmap="coolwarm",
        center=0,
    )
    plt.title(
        "Corrélation entre les variables nutritionnelles et le score d’insatisfaction"
    )
    fig.tight_layout()

    return _finalize(fig, show, return_fig)
