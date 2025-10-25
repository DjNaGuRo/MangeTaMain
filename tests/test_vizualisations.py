import pandas as pd
import numpy as np
from src import data_visualization as vis


def make_fake_data(n=1000):
    """Je crée un DataFrame factice pour les tests."""
    np.random.seed(42)
    return pd.DataFrame({
        "user_id": np.random.randint(1, 50, n),
        "recipe_id": np.random.randint(100, 200, n),
        "rating": np.random.randint(1, 6, n).astype(float),
        "review": ["ok"] * n,
        "binary_sentiment": np.random.choice([0, 1], n)
    })


def test_rating_distribution_runs_without_error():
    df = make_fake_data()
    # Je vérifie que la fonction ne plante pas et retourne None
    result = vis.rating_distribution(df)
    assert result is None


def test_rating_distribution_with_show(monkeypatch):
    df = make_fake_data()
    # j’empêche plt.show() d’ouvrir une fenêtre
    import matplotlib.pyplot as plt
    monkeypatch.setattr(plt, "show", lambda: None)
    vis.rating_distribution(df, show=True)


def test_recipe_mean_rating_distribution_has_data():
    df = make_fake_data()
    result = vis.recipe_mean_rating_distribution(df)
    assert result is None


def test_user_mean_rating_distribution_kde():
    df = make_fake_data()
    # Je m’assure que le KDE ne casse pas
    vis.user_mean_rating_distribution(df, kde=True)


def test_top_users_by_activity_topk():
    df = make_fake_data()
    # Je teste top_k = 5
    vis.top_users_by_activity(df, top_k=5)


def test_user_count_vs_mean_rating():
    df = make_fake_data()
    vis.user_count_vs_mean_rating(df, sample=20)


def test_activity_bucket_bar_levels():
    df = make_fake_data()
    vis.activity_bucket_bar(df, show=False)
