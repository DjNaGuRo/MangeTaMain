import numpy as np
import pandas as pd

def make_df_small() -> pd.DataFrame:
    rng = np.random.default_rng(42)
    n = 200
    return pd.DataFrame({
        "kcal": rng.normal(500, 120, n),         # numérique CONTINU
        "servings": rng.integers(1, 6, n),       # numérique DISCRET (entiers)
        "cuisine": rng.choice(["fr", "it", "jp", "us"], n),  # catégoriel
        "fat_g": rng.normal(20, 5, n),
        "protein_g": rng.normal(15, 4, n),
    })
