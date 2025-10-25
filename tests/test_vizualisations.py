import matplotlib
matplotlib.use("Agg")  # évite d’ouvrir des fenêtres pendant les tests/CI

from pathlib import Path

# importe tes fonctions depuis TON module
from data_visualization import (
    numeric_summary, categorical_summary, correlation_table, group_numeric_by_category,
    uni_numeric_continuous, uni_numeric_discrete, uni_categorical,
    bi_quant_quant, bi_quant_qual,
    uni_all_numeric_continuous, uni_all_numeric_discrete, uni_all_categorical,
    bi_all_quant_quant, bi_all_quant_qual,
)

def test_numeric_and_categorical_summaries():
    df = make_df_small()
    num_cols = ["kcal", "servings", "fat_g", "protein_g"]
    cat_cols = ["cuisine"]

    num = numeric_summary(df, num_cols)
    assert set(num.index) == set(num_cols)
    assert {"mean", "std", "min", "max"}.issubset(num.columns)

    cat = categorical_summary(df, cat_cols, top_k=3)
    assert "cuisine" in cat and 1 <= len(cat["cuisine"]) <= 3

    corr = correlation_table(df, num_cols, method="pearson")
    assert set(corr.index) == set(num_cols) == set(corr.columns)

def test_group_numeric_by_category():
    df = make_df_small()
    stats = group_numeric_by_category(df, num="kcal", cat="cuisine")
    assert {"count", "mean", "std", "median"}.issubset(stats.columns)
    assert len(stats) > 0

def test_univariate_plots(tmp_path):
    df = make_df_small()
    p1 = tmp_path / "uni_kcal.png"
    p2 = tmp_path / "uni_servings.png"
    p3 = tmp_path / "uni_cuisine.png"

    uni_numeric_continuous(df, "kcal", bins=20, save_path=p1)
    uni_numeric_discrete(df, "servings", save_path=p2)
    uni_categorical(df, "cuisine", top_k=4, save_path=p3)

    for p in (p1, p2, p3):
        assert p.exists() and p.stat().st_size > 0

def test_bivariate_plots_and_returns(tmp_path):
    df = make_df_small()

    pqq = tmp_path / "qq.png"
    r = bi_quant_quant(df, "kcal", "fat_g", save_path=pqq)
    assert isinstance(r, float)
    assert pqq.exists()

    pqc = tmp_path / "qc.png"
    stats = bi_quant_qual(df, num="kcal", cat="cuisine", save_path=pqc)
    assert {"count", "mean", "std", "median"}.issubset(stats.columns)
    assert pqc.exists()

def test_batch_generators(tmp_path):
    df = make_df_small()
    num_cont = ["kcal", "fat_g", "protein_g"]
    num_disc = ["servings"]
    cats = ["cuisine"]

    out1 = uni_all_numeric_continuous(df, num_cont, save_dir=tmp_path / "uni_cont")
    out2 = uni_all_numeric_discrete(df, num_disc, save_dir=tmp_path / "uni_disc")
    out3 = uni_all_categorical(df, cats, save_dir=tmp_path / "uni_cat")
    assert len(out1) == len(num_cont)
    assert len(out2) == len(num_disc)
    assert len(out3) == len(cats)

    corr_df = bi_all_quant_quant(df, num_cont + num_disc, save_dir=tmp_path / "bi_qq")
    assert {"x", "y", "pearson_r"}.issubset(corr_df.columns)
    assert len(corr_df) >= 1

    pair_stats = bi_all_quant_qual(df, num_cont, cats, save_dir=tmp_path / "bi_qc")
    assert len(pair_stats) == len(num_cont) * len(cats)
