# src/visuals/interactions_univariate.py
"""
Mes visualisations univariées / bivariées pour la table `interactions`.
- Je veux un code clair, PEP8, sans sauvegarde PNG.
- J’utilise seaborn pour les KDE et certains barplots.
- Pas de double rendu dans Jupyter: je contrôle show/close/return.
"""

from __future__ import annotations

from typing import Optional, Sequence, Tuple

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns  # j’assume que seaborn est installé

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
    _need_cols(interactions, ["rating"])
    s = pd.to_numeric(interactions["rating"], errors="coerce").dropna()
    s = s[(s >= 1) & (s <= 5)]

    fig, ax = plt.subplots(figsize=(6, 4))
    ax.hist(s, bins=[0.5, 1.5, 2.5, 3.5, 4.5, 5.5], color=PALETTE[1], edgecolor="white")
    ax.set_title("Distribution des notes valides")
    ax.set_xlabel("Note")
    ax.set_ylabel("Nombre d'occurrences")
    ax.set_xticks([1, 2, 3, 4, 5])
    ax.grid(axis="y", alpha=0.25)

    if kde:
        sns.kdeplot(s, ax=ax, color=PALETTE[5], lw=2)

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
    g = tmp.dropna(subset=["rating"]).groupby("recipe_id", observed=True)["rating"].mean()

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
    ax.scatter(agg["n_reviews"], agg["mean_rating"], s=18, alpha=alpha, color=PALETTE[4])
    ax.set_title("Relation entre le nombre d'avis laissés et la note moyenne par utilisateur")
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

    # Nombre d’interactions par utilisateur (value_counts mappé)
    counts = df["user_id"].value_counts()
    df["n_interactions_user"] = df["user_id"].map(counts)

    # Catégorisation selon [0, 1, 10, 60, +∞[
    full_bins = [*bins, float("inf")]
    df["interaction_level"] = pd.cut(
        df["n_interactions_user"],
        bins=full_bins,
        labels=labels,
        include_lowest=True,
        ordered=True,
    )

    # Moyenne des notes par utilisateur + catégorie
    user_stats = (
        df.groupby("user_id", observed=True)
        .agg(note_moyenne=("rating", "mean"), interaction_level=("interaction_level", "first"))
        .reset_index()
    )

    fig, ax = plt.subplots(figsize=(6, 4))
    sns.barplot(
        data=user_stats,
        x="interaction_level",
        y="note_moyenne",
        order=list(labels),
        color=PALETTE[1],  # bleu
        ax=ax,
        estimator=np.mean,
    )
    ax.set_title("Relation entre l'activité et la moyenne des notes attribuées")
    ax.set_xlabel("Catégorie d'activité de l'utilisateur")
    ax.set_ylabel("Moyenne des notes")
    ax.set_ylim(0, 5.2)
    ax.grid(axis="y", alpha=0.25)

    return _finalize(fig, show, return_fig)
