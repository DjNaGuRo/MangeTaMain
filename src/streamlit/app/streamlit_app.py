"""Application Streamlit principale."""

import streamlit as st
import pandas as pd
import numpy as np

def main():
    """Lance l'application Streamlit principale."""
    st.set_page_config(
        page_title="MangeTaMain - Analyse de recettes",
        page_icon="🍽️",
        layout="wide"
    )
    
    st.title("🍽️ Projet MangeTaMain – Analyse de recettes les moins notées")
    
    # Sidebar pour la navigation
    st.sidebar.title("Navigation")
    page = st.sidebar.selectbox(
        "Choisissez une page:",
        ["Accueil", "Analyse des données", "Visualisations", "Recommandations"]
    )
    
    if page == "Accueil":
        show_home_page()
    elif page == "Analyse des données":
        show_data_analysis()
    elif page == "Visualisations":
        show_visualizations()
    elif page == "Recommandations":
        show_recommendations()

def show_home_page():
    """Affiche la page d'accueil."""
    st.header("Bienvenue sur MangeTaMain!")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("À propos du projet")
        st.write("""
        Ce projet analyse les recettes de cuisine et leurs évaluations 
        pour identifier les recettes les moins bien notées et comprendre 
        les raisons de ces mauvaises évaluations.
        """)
        
        name = st.text_input("Entrez votre prénom :")
        if name:
            st.success(f"Bonjour {name} ! Bienvenue dans l'analyse culinaire 🍴")
    
    with col2:
        st.subheader("Fonctionnalités")
        st.write("""
        - 📊 Analyse des données de recettes
        - 📈 Visualisations interactives
        - 🎯 Système de recommandations
        - 📋 Rapports détaillés
        """)

def show_data_analysis():
    """Affiche la page d'analyse des données."""
    st.header("📊 Analyse des données")
    
    # Exemple de données (à remplacer par vos vraies données)
    st.subheader("Aperçu des données")
    
    # Génération de données d'exemple
    np.random.seed(42)
    sample_data = pd.DataFrame({
        'recette_id': range(1, 101),
        'nom_recette': [f"Recette {i}" for i in range(1, 101)],
        'note_moyenne': np.random.uniform(1, 5, 100),
        'nb_evaluations': np.random.randint(10, 1000, 100),
        'temps_preparation': np.random.randint(15, 180, 100)
    })
    
    st.dataframe(sample_data.head(10))
    
    # Métriques
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("Total recettes", len(sample_data))
    with col2:
        st.metric("Note moyenne", f"{sample_data['note_moyenne'].mean():.2f}")
    with col3:
        st.metric("Recettes mal notées (<3)", len(sample_data[sample_data['note_moyenne'] < 3]))
    with col4:
        st.metric("Temps moyen (min)", f"{sample_data['temps_preparation'].mean():.0f}")

def show_visualizations():
    """Affiche la page de visualisations."""
    st.header("📈 Visualisations")
    
    st.subheader("Distribution des notes")
    
    # Données d'exemple pour le graphique
    np.random.seed(42)
    notes = np.random.uniform(1, 5, 1000)
    
    st.histogram(notes, bins=20)
    
    st.subheader("Corrélation temps/note")
    chart_data = pd.DataFrame({
        'temps': np.random.randint(15, 180, 100),
        'note': np.random.uniform(1, 5, 100)
    })
    
    st.scatter_chart(chart_data, x='temps', y='note')

def show_recommendations():
    """Affiche la page de recommandations."""
    st.header("🎯 Recommandations")
    
    st.subheader("Améliorations suggérées")
    
    recommendations = [
        "Simplifier les recettes trop complexes",
        "Réduire le temps de préparation des plats longs",
        "Améliorer la présentation des recettes",
        "Ajouter plus d'images explicatives",
        "Clarifier les instructions de cuisson"
    ]
    
    for i, rec in enumerate(recommendations, 1):
        st.write(f"{i}. {rec}")
    
    st.subheader("Filtres avancés")
    col1, col2 = st.columns(2)
    
    with col1:
        note_min = st.slider("Note minimale", 1.0, 5.0, 1.0)
        temps_max = st.slider("Temps maximum (min)", 15, 180, 60)
    
    with col2:
        categorie = st.selectbox("Catégorie", ["Toutes", "Entrées", "Plats", "Desserts"])
        difficulte = st.selectbox("Difficulté", ["Toutes", "Facile", "Moyen", "Difficile"])

if __name__ == "__main__":
    main()