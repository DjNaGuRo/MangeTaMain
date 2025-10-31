import streamlit as st

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

from src.streamlit.app.utils import get_ds, render_viz, _safe_rerun

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

