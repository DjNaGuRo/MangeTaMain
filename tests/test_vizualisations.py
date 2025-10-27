import pandas as pd
import numpy as np
import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from src import data_visualization as vis


def make_fake_data(n=1000):
    """Je crée un DataFrame factice pour les tests."""
    np.random.seed(42)
    return pd.DataFrame(
        {
            "user_id": np.random.randint(1, 50, n),
            "recipe_id": np.random.randint(100, 200, n),
            "rating": np.random.randint(1, 6, n).astype(float),
            "review": ["ok"] * n,
            "binary_sentiment": np.random.choice([0, 1], n),
        }
    )


# dataframe factice pour les tests de recipes
def make_fake_recipes_data(n=500):
    np.random.seed(42)
    ingredients_list = [
        str(["sugar", "flour", "eggs"]),
        str(["salt", "pepper", "chicken"]),
        str(["tomato", "basil", "mozzarella"]),
        str(["rice", "beans", "corn"]),
    ]

    tag_list = [
        str(["vegan"]),
        str(["gluten-free"]),
        str(["quick"]),
        str(["dessert"]),
    ]
    return pd.DataFrame(
        {
            "recipe_id": np.random.randint(100, 200, n),
            "contributor_id": np.random.randint(1, 20, n),
            "ingredients": np.random.choice(ingredients_list, n),
            "minutes": np.random.randint(10, 120, n),
            "n_steps": np.random.randint(1, 20, n),
            "tags": np.random.choice(tag_list, n),
            "calories": np.random.randint(100, 1000, n),
            "protein": np.random.randint(1, 50, n),
            "total_fat": np.random.randint(1, 50, n),
            "sodium": np.random.randint(50, 5000, n),
            "sugar": np.random.randint(1, 100, n),
            "carbohydrates": np.random.randint(1, 200, n),
        }
    )


def test_rating_distribution_runs_without_error():
    df = make_fake_data()
    # Je vérifie que la fonction ne plante pas et retourne None
    result = vis.rating_distribution(df)
    assert result is None


def test_rating_distribution_with_show(monkeypatch):
    df = make_fake_data()
    # j’empêche plt.show() d’ouvrir une fenêtre

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


def test_analyze_contributors_output(monkeypatch):
    df = make_fake_recipes_data()
    monkeypatch.setattr(plt, "show", lambda: None)
    result = vis.analyze_contributors(df)
    assert result is None


def test_statistique_descriptive():
    df = make_fake_recipes_data()
    # Je teste la fonction avec la colonne "minutes"
    result = vis.statistique_descriptive(df, column="minutes")
    assert result is not None


def test_plot_prep_time_distribution_runs_without_error(monkeypatch):
    df = make_fake_recipes_data()
    monkeypatch.setattr(plt, "show", lambda: None)
    result = vis.plot_prep_time_distribution(df, show=False)
    assert result is None


def test_plot_nutrition_distribution_runs_without_error(monkeypatch):
    df = make_fake_recipes_data()
    monkeypatch.setattr(plt, "show", lambda: None)
    result = vis.plot_nutrition_distribution(df, show=False)
    assert result is None


def test_analyse_tags_runs_without_error():
    df = make_fake_recipes_data()
    result = vis.analyse_tags(df)
    assert result is not None


def test_plot_tags_distribution_runs_without_error(monkeypatch):
    df = make_fake_recipes_data()
    monkeypatch.setattr(plt, "show", lambda: None)
    result = vis.plot_tags_distribution(df, show=False)
    assert result is None


def test_plot_ingredient_runs_without_error(monkeypatch):
    df = make_fake_recipes_data()
    monkeypatch.setattr(plt, "show", lambda: None)
    result = vis.plot_ingredient(df, show=False)
    assert result is None


def test_analyze_ingredients_runs_without_error():
    df = make_fake_recipes_data()
    result = vis.analyze_ingredients_vectorized(df)
    assert result is not None


def test_plot_n_steps_distribution_runs_without_error(monkeypatch):
    df = make_fake_recipes_data()
    monkeypatch.setattr(plt, "show", lambda: None)
    result = vis.plot_n_steps_distribution(df, show=False)
    assert result is None
