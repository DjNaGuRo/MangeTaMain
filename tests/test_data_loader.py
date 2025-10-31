import pandas as pd
import numpy as np
import matplotlib

from src.preprocessing import plot_minutes_ningredients_nsteps

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from src import preprocessing as pre


def make_df_small() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    n = 200
    return pd.DataFrame(
        {
            "recipe_id": np.arange(n),
            "minutes": rng.normal(60, 15, n),  # numérique CONTINU
            "n_ingredients": rng.integers(3, 15, n),  # numérique DISCRET (entiers)
            "n_steps": rng.integers(1, 10, n),  # numérique DISCRET (entiers)
            "description": rng.choice(
                ["Facile", "Moyen", "Difficile"], n
            ),  # catégoriel
            "ingredients": ["ingrédient " + str(i) for i in rng.integers(1, 50, n)],
            "steps": ["étape " + str(i) for i in rng.integers(1, 10, n)],
            "kcal": rng.normal(500, 120, n),  # numérique CONTINU
            "servings": rng.integers(1, 6, n),  # numérique DISCRET (entiers)
            "cuisine": rng.choice(["fr", "it", "jp", "us"], n),  # catégoriel
            "fat_g": rng.normal(20, 5, n),
            "protein_g": rng.normal(15, 4, n),
        }
    )


def make_interactions_small() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    n = 500
    return pd.DataFrame(
        {
            "interaction_id": np.arange(n),
            "user_id": rng.integers(1, 100, n),
            "recipe_id": rng.integers(0, 200, n),
            "rating": rng.integers(1, 5, n),
            "review": rng.choice(
                [
                    "Great recipe!",
                    "Not what I expected.",
                    "Would not recommend.",
                    "Absolutely loved it!",
                    "It was okay, nothing special.",
                ],
                n,
            ),
        }
    )


def make_merged_small() -> pd.DataFrame:
    interactions_df = make_interactions_small()
    recipes_df = make_df_small()
    merged_df = interactions_df.merge(recipes_df, on="recipe_id", how="left")
    return merged_df


#### Tests ####
def test_merge_datasets():
    merged_df = make_merged_small()
    assert not merged_df.empty


def test_plot_minutes_ningredients_nsteps(monkeypatch):
    recipes_df = make_df_small()
    monkeypatch.setattr(plt, "show", lambda: None)
    fig = pre.plot_minutes_ningredients_nsteps(recipes_df, show=False, return_fig=True)
    assert fig is not None
