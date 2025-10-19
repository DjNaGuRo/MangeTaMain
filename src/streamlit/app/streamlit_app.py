"""Application Streamlit principale."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go

# Configuration du thème personnalisé
def set_custom_theme(theme="Clair"):
    """Applique un thème personnalisé à l'application."""
    
    # Définir les couleurs selon le thème choisi
    if theme == "Sombre":
        colors = {
            "primary": "#ffffff",
            "secondary": "#f0f0f0",
            "background": "#1a1a1a",
            "text": "#e0e0e0",
            "card_bg": "#000000",  # ← Changé en noir pur
            "card_text": "#e0e0e0",
            "header_gradient": "linear-gradient(135deg, #ffffff 0%, #e0e0e0 100%)",
            "sidebar_gradient": "linear-gradient(180deg, #3a3a3a 0%, #2d2d2d 100%)",
            "border_color": "#3d3d3d",
            "info_bg": "#000000",  # ← Changé en noir
            "info_border": "#ffffff",
            "warning_bg": "#1a1a1a",  # ← Noir légèrement plus clair
            "warning_border": "#f39c12",
            "success_bg": "#000000",  # ← Changé en noir
            "success_border": "#ffffff",
            "button_text": "#1a1a1a"
        }
    elif theme == "Auto":
        colors = {
            "primary": "#667eea",
            "secondary": "#764ba2",
            "background": "#F0F2F6",
            "text": "#2C3E50",
            "card_bg": "white",
            "card_text": "#2C3E50",
            "header_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "sidebar_gradient": "linear-gradient(180deg, #667eea 0%, #764ba2 100%)",
            "border_color": "#e0e0e0",
            "info_bg": "#E8F4F8",
            "info_border": "#2196F3",
            "warning_bg": "#FFF3E0",
            "warning_border": "#FF9800",
            "success_bg": "#E8F5E9",
            "success_border": "#4CAF50",
            "button_text": "#ffffff"
        }
    else:  # Thème Clair
        colors = {
            "primary": "#667eea",
            "secondary": "#764ba2",
            "background": "#F0F2F6",
            "text": "#2C3E50",
            "card_bg": "white",
            "card_text": "#2C3E50",
            "header_gradient": "linear-gradient(135deg, #667eea 0%, #764ba2 100%)",
            "sidebar_gradient": "linear-gradient(180deg, #667eea 0%, #764ba2 100%)",
            "border_color": "#e0e0e0",
            "info_bg": "#E8F4F8",
            "info_border": "#2196F3",
            "warning_bg": "#FFF3E0",
            "warning_border": "#FF9800",
            "success_bg": "#E8F5E9",
            "success_border": "#CFDBD0",
            "button_text": "#ffffff"
        }
    
    st.markdown(f"""
        <style>
        /* Couleurs principales */
        :root {{
            --primary-color: {colors['primary']};
            --secondary-color: {colors['secondary']};
            --background-color: {colors['background']};
            --text-color: {colors['text']};
        }}
        
        /* Appliquer le background à toute l'application */
        .stApp {{
            background-color: {colors['background']};
            color: {colors['text']};
        }}
        
        /* Background de la zone principale */
        .main {{
            background-color: {colors['background']};
            color: {colors['text']};
        }}
        
        /* Background des blocs de contenu */
        .block-container {{
            background-color: {colors['background']};
            color: {colors['text']};
        }}
        
        /* Forcer la couleur du texte pour tous les éléments */
        .stMarkdown, p, span, div, label, h1, h2, h3, h4, h5, h6 {{
            color: {colors['text']} !important;
        }}
        
        /* Header stylisé */
        .main-header {{
            background: {colors['header_gradient']};
            padding: 2rem;
            border-radius: 10px;
            color: {colors['button_text']} !important;
            text-align: center;
            margin-bottom: 2rem;
            box-shadow: 0 4px 6px rgba(0,0,0,0.1);
        }}
        
        .main-header h1, .main-header p {{
            color: {colors['button_text']} !important;
        }}
        
        /* Cards stylisées - fond noir */
        .metric-card {{
            background: {colors['card_bg']};
            padding: 1.5rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(255,255,255,0.1);
            border-left: 4px solid {colors['primary']};
            margin: 1rem 0;
            color: {colors['card_text']};
        }}
        
        .metric-card h2, .metric-card h4, .metric-card p {{
            color: {colors['card_text']} !important;
        }}
        
        /* Sidebar personnalisée */
        [data-testid="stSidebar"] {{
            background: {colors['sidebar_gradient']};
        }}
        
        [data-testid="stSidebar"] * {{
            color: white !important;
        }}
        
        /* Boutons stylisés */
        .stButton>button {{
            background: {colors['header_gradient']};
            color: {colors['button_text']} !important;
            border: none;
            border-radius: 25px;
            padding: 0.5rem 2rem;
            font-weight: bold;
            transition: all 0.3s ease;
        }}
        
        .stButton>button:hover {{
            transform: translateY(-2px);
            box-shadow: 0 4px 8px rgba(255,255,255,0.2);
        }}
        
        /* Animations */
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .fade-in {{
            animation: fadeIn 0.5s ease-out;
        }}
        
        /* Tables stylisées - fond noir */
        .dataframe {{
            border-radius: 10px;
            overflow: hidden;
            background-color: {colors['card_bg']};
            color: {colors['card_text']};
            border: 1px solid {colors['border_color']};
        }}
        
        .dataframe th {{
            background-color: {colors['primary']} !important;
            color: {colors['button_text']} !important;
        }}
        
        .dataframe td {{
            color: {colors['card_text']} !important;
            background-color: {colors['card_bg']} !important;
        }}
        
        /* Expanders avec fond noir */
        [data-testid="stExpander"] {{
            background-color: {colors['card_bg']};
            border-radius: 10px;
            border: 1px solid {colors['border_color']};
        }}
        
        [data-testid="stExpander"] * {{
            color: {colors['card_text']} !important;
        }}
        
        /* Métriques avec fond noir */
        [data-testid="stMetric"] {{
            background-color: {colors['card_bg']};
            padding: 1rem;
            border-radius: 10px;
            box-shadow: 0 2px 4px rgba(255,255,255,0.05);
            border: 1px solid {colors['border_color']};
        }}
        
        [data-testid="stMetric"] * {{
            color: {colors['card_text']} !important;
        }}
        
        /* Input fields en mode sombre - fond noir */
        input, textarea, select {{
            background-color: {colors['card_bg']} !important;
            color: {colors['text']} !important;
            border: 1px solid {colors['border_color']} !important;
        }}
        
        /* Date picker */
        [data-testid="stDateInput"] {{
            background-color: {colors['card_bg']};
            color: {colors['text']};
        }}
        
        /* Slider */
        .stSlider {{
            color: {colors['text']};
        }}
        
        /* Selectbox - fond noir */
        [data-baseweb="select"] {{
            background-color: {colors['card_bg']} !important;
        }}
        
        /* Multiselect */
        [data-baseweb="tag"] {{
            background-color: {colors['primary']} !important;
            color: {colors['button_text']} !important;
        }}
        
        /* Tabs */
        .stTabs [data-baseweb="tab-list"] {{
            background-color: {colors['card_bg']};
        }}
        
        .stTabs [data-baseweb="tab"] {{
            color: {colors['text']} !important;
        }}
        
        /* Info boxes avec fond noir */
        .info-box {{
            background: {colors['info_bg']};
            border-left: 4px solid {colors['info_border']};
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
            color: {colors['text']};
            border: 1px solid {colors['border_color']};
        }}
        
        .info-box h3, .info-box h4, .info-box p, .info-box li {{
            color: {colors['text']} !important;
        }}
        
        .warning-box {{
            background: {colors['warning_bg']};
            border-left: 4px solid {colors['warning_border']};
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
            color: {colors['text']};
            border: 1px solid {colors['border_color']};
        }}
        
        .warning-box h3, .warning-box h4, .warning-box p, .warning-box li {{
            color: {colors['text']} !important;
        }}
        
        .success-box {{
            background: {colors['success_bg']};
            border-left: 4px solid {colors['success_border']};
            padding: 1rem;
            border-radius: 5px;
            margin: 1rem 0;
            color: {colors['text']};
            border: 1px solid {colors['border_color']};
        }}
        
        .success-box h3, .success-box h4, .success-box p, .success-box li {{
            color: {colors['text']} !important;
        }}
        
        /* Radio buttons et checkboxes */
        [data-testid="stRadio"] label {{
            color: {colors['text']} !important;
        }}
        
        /* Download buttons */
        .stDownloadButton button {{
            background: {colors['primary']} !important;
            color: {colors['button_text']} !important;
        }}
        
        /* Progress bar */
        .stProgress > div > div {{
            background-color: {colors['primary']} !important;
        }}
        </style>
    """, unsafe_allow_html=True)

def main():
    """Lance l'application Streamlit principale."""
    st.set_page_config(
        page_title="MangeTaMain - Analyse de recettes les moins bien notées",
        page_icon="🍽️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # Initialiser le thème dans session_state AVANT la sidebar
    if 'theme' not in st.session_state:
        st.session_state.theme = "Clair"
    
    # Appliquer le thème sélectionné AVANT tout le reste
    set_custom_theme(st.session_state.theme)
    
    # Sidebar avec icônes et design amélioré
    with st.sidebar:
        st.markdown("### 📋 Navigation")
        
        pages = {
            "🏠 Accueil": "Accueil",
            "📊 Analyse": "Analyse des données",
            "📈 Visualisations": "Visualisations",
            "🎯 Recommandations": "Recommandations"
        }
        
        page = st.radio("", list(pages.keys()), label_visibility="collapsed")
        selected_page = pages[page]
        
        st.markdown("---")
        st.markdown("### ⚙️ Paramètres")
        
        # Sélecteur de thème avec callback
        def change_theme():
            """Callback appelé quand le thème change."""
            st.session_state.theme = st.session_state.theme_selector
        
        theme = st.selectbox(
            "Thème", 
            ["Clair", "Sombre", "Auto"],
            index=["Clair", "Sombre", "Auto"].index(st.session_state.theme),
            key="theme_selector",
            on_change=change_theme
        )
        
        st.markdown("---")
        st.markdown("### 📞 Contact")
        st.markdown("📧 contact@mangetamain.fr")
        st.markdown("🌐 www.mangetamain.fr")
    
    # Header avec design moderne
    st.markdown("""
        <div class="main-header fade-in">
            <h1>🍽️ MangeTaMain</h1>
            <p>Analyse de recettes les moins bien notées</p>
        </div>
    """, unsafe_allow_html=True)
    
    if selected_page == "Accueil":
        show_home_page_modern()
    elif selected_page == "Analyse des données":
        show_data_analysis_modern()
    elif selected_page == "Visualisations":
        show_visualizations_modern()
    elif selected_page == "Recommandations":
        show_recommendations_modern()

# ...existing code... (gardez toutes les autres fonctions inchangées)

# ...existing code... (gardez toutes les autres fonctions inchangées)

def show_home_page_modern():
    """Page d'accueil avec design moderne."""
    
    # Section héro
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="fade-in">', unsafe_allow_html=True)
        st.markdown("## 👋 Bienvenue sur MangeTaMain!")
        
        st.markdown("""
        <div class="info-box">
            <h3>🎯 Notre Mission</h3>
            <p>Analyser de recettes de cuisine les moins bien notées et en proposant des solutions concrètes.</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Input personnalisé
        st.markdown("### 👤 Personnalisation")
        name = st.text_input("Entrez votre prénom :", placeholder="Ex: Marie")
        
        if name:
            st.markdown(f"""
            <div class="success-box fade-in">
                <h4>✨ Bonjour {name} !</h4>
                <p>Ravi de vous accueillir dans notre outil d'analyse culinaire 🍴</p>
            </div>
            """, unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with col2:
        st.markdown('<div class="fade-in">', unsafe_allow_html=True)
        
        # Statistiques en temps réel
        st.markdown("### 📊 Statistiques en direct")
        
        metrics_data = {
            "Recettes analysées": 1247,
            "Notes moyennes": 3.8,
            "Utilisateurs actifs": 523,
            "Améliorations suggérées": 89
        }
        
        for metric, value in metrics_data.items():
            st.metric(metric, value, delta=f"+{np.random.randint(5, 20)}%")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Section fonctionnalités avec cards
    st.markdown("---")
    st.markdown("## 🚀 Fonctionnalités principales")
    
    col1, col2, col3, col4 = st.columns(4)
    
    features = [
        ("📊", "Analyse", "Exploration approfondie des données"),
        ("📈", "Visualisations", "Graphiques interactifs"),
        ("🎯", "Recommandations", "Suggestions personnalisées"),
        ("📋", "Rapports", "Exports détaillés")
    ]
    
    for col, (icon, title, desc) in zip([col1, col2, col3, col4], features):
        with col:
            st.markdown(f"""
            <div class="metric-card fade-in">
                <h2 style="text-align: center;">{icon}</h2>
                <h4 style="text-align: center;">{title}</h4>
                <p style="text-align: center; color: #666;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

def show_data_analysis_modern():
    """Page d'analyse avec design moderne."""
    st.markdown("## 📊 Analyse des données")
    
    # Filtres avancés
    with st.expander("🔍 Filtres avancés", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            date_range = st.date_input("Période", [])
        with col2:
            category = st.multiselect("Catégories", ["Entrées", "Plats", "Desserts"])
        with col3:
            rating_range = st.slider("Notes", 1.0, 5.0, (1.0, 5.0))
    
    # Données d'exemple
    np.random.seed(42)
    sample_data = pd.DataFrame({
        'recette_id': range(1, 101),
        'nom_recette': [f"Recette {i}" for i in range(1, 101)],
        'note_moyenne': np.random.uniform(1, 5, 100),
        'nb_evaluations': np.random.randint(10, 1000, 100),
        'temps_preparation': np.random.randint(15, 180, 100),
        'difficulte': np.random.choice(['Facile', 'Moyen', 'Difficile'], 100)
    })
    
    # Métriques en cards
    col1, col2, col3, col4 = st.columns(4)
    
    metrics = [
        ("📋 Total recettes", len(sample_data), "green"),
        ("⭐ Note moyenne", f"{sample_data['note_moyenne'].mean():.2f}", "blue"),
        ("⚠️ Mal notées", len(sample_data[sample_data['note_moyenne'] < 3]), "red"),
        ("⏱️ Temps moyen", f"{sample_data['temps_preparation'].mean():.0f} min", "orange")
    ]
    
    for col, (label, value, color) in zip([col1, col2, col3, col4], metrics):
        with col:
            delta = f"+{np.random.randint(1, 15)}%" if color in ["green", "blue"] else f"-{np.random.randint(1, 10)}%"
            st.metric(label, value, delta)
    
    # Tableau interactif
    st.markdown("### 📋 Données détaillées")
    
    # Ajout d'une barre de recherche
    search = st.text_input("🔍 Rechercher une recette", "")
    if search:
        sample_data = sample_data[sample_data['nom_recette'].str.contains(search, case=False)]
    
    st.dataframe(
        sample_data,
        use_container_width=True,
        hide_index=True,
        column_config={
            "note_moyenne": st.column_config.ProgressColumn(
                "Note",
                format="%.2f ⭐",
                min_value=0,
                max_value=5,
            ),
            "nb_evaluations": st.column_config.NumberColumn(
                "Évaluations",
                format="%d 👥"
            ),
            "temps_preparation": st.column_config.NumberColumn(
                "Temps (min)",
                format="%d ⏱️"
            )
        }
    )
    
    # Bouton d'export
    col1, col2, col3 = st.columns([1, 1, 2])
    with col1:
        st.download_button(
            "📥 Exporter CSV",
            sample_data.to_csv(index=False).encode('utf-8'),
            "recettes_analyse.csv",
            "text/csv"
        )
    with col2:
        st.download_button(
            "📊 Exporter Excel",
            sample_data.to_csv(index=False).encode('utf-8'),
            "recettes_analyse.xlsx"
        )

def show_visualizations_modern():
    """Page de visualisations avec Plotly."""
    st.markdown("## 📈 Visualisations interactives")
    
    # Données d'exemple
    np.random.seed(42)
    notes = np.random.uniform(1, 5, 1000)
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Distribution", "🔥 Top/Flop", "⏱️ Corrélations", "🎯 Insights"])
    
    with tab1:
        # Histogramme avec Plotly
        fig = px.histogram(
            x=notes,
            nbins=20,
            title="Distribution des notes",
            labels={'x': 'Note', 'y': 'Fréquence'},
            color_discrete_sequence=['#667eea']
        )
        fig.update_layout(
            plot_bgcolor='rgba(0,0,0,0)',
            paper_bgcolor='rgba(0,0,0,0)',
            font=dict(size=12)
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        col1, col2 = st.columns(2)
        
        with col1:
            # Top recettes
            top_recipes = pd.DataFrame({
                'Recette': [f'Recette {i}' for i in range(1, 11)],
                'Note': np.random.uniform(4.5, 5.0, 10)
            }).sort_values('Note', ascending=False)
            
            fig = px.bar(
                top_recipes,
                x='Note',
                y='Recette',
                orientation='h',
                title='🏆 Top 10 Recettes',
                color='Note',
                color_continuous_scale='Greens'
            )
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            # Flop recettes
            flop_recipes = pd.DataFrame({
                'Recette': [f'Recette {i}' for i in range(1, 11)],
                'Note': np.random.uniform(1.0, 2.5, 10)
            }).sort_values('Note')
            
            fig = px.bar(
                flop_recipes,
                x='Note',
                y='Recette',
                orientation='h',
                title='📉 Flop 10 Recettes',
                color='Note',
                color_continuous_scale='Reds'
            )
            st.plotly_chart(fig, use_container_width=True)
    
    with tab3:
        # Scatter plot
        chart_data = pd.DataFrame({
            'temps': np.random.randint(15, 180, 100),
            'note': np.random.uniform(1, 5, 100),
            'difficulte': np.random.choice(['Facile', 'Moyen', 'Difficile'], 100)
        })
        
        fig = px.scatter(
            chart_data,
            x='temps',
            y='note',
            color='difficulte',
            title='Corrélation Temps / Note / Difficulté',
            labels={'temps': 'Temps de préparation (min)', 'note': 'Note moyenne'},
            trendline="ols"
        )
        st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("### 🎯 Insights clés")
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.markdown("""
            <div class="info-box">
                <h4>📊 Observations principales</h4>
                <ul>
                    <li>68% des recettes ont une note > 3.5</li>
                    <li>Les recettes rapides (<30min) sont mieux notées</li>
                    <li>Forte corrélation entre simplicité et satisfaction</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
        
        with col2:
            st.markdown("""
            <div class="warning-box">
                <h4>⚠️ Points d'attention</h4>
                <ul>
                    <li>32% des recettes sous la moyenne</li>
                    <li>Temps de préparation souvent sous-estimé</li>
                    <li>Manque d'images pour 15% des recettes</li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

def show_recommendations_modern():
    """Page de recommandations moderne."""
    st.markdown("## 🎯 Recommandations intelligentes")
    
    # Système de scoring
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💡 Suggestions d'amélioration")
        
        recommendations = [
            {
                "title": "Simplifier les recettes complexes",
                "impact": "Élevé",
                "effort": "Moyen",
                "priority": 1,
                "icon": "🎯"
            },
            {
                "title": "Optimiser le temps de préparation",
                "impact": "Moyen",
                "effort": "Faible",
                "priority": 2,
                "icon": "⏱️"
            },
            {
                "title": "Améliorer la présentation visuelle",
                "impact": "Élevé",
                "effort": "Élevé",
                "priority": 3,
                "icon": "📸"
            },
            {
                "title": "Clarifier les instructions",
                "impact": "Moyen",
                "effort": "Faible",
                "priority": 4,
                "icon": "📝"
            },
            {
                "title": "Ajouter des variantes",
                "impact": "Faible",
                "effort": "Moyen",
                "priority": 5,
                "icon": "🔄"
            }
        ]
        
        for rec in recommendations:
            impact_color = {"Élevé": "🔴", "Moyen": "🟡", "Faible": "🟢"}
            
            with st.expander(f"{rec['icon']} {rec['title']}", expanded=rec['priority'] <= 2):
                col_a, col_b, col_c = st.columns(3)
                col_a.metric("Impact", rec['impact'], impact_color[rec['impact']])
                col_b.metric("Effort", rec['effort'])
                col_c.metric("Priorité", f"#{rec['priority']}")
                
                st.progress(min(100, rec['priority'] * 20))
    
    with col2:
        st.markdown("### 🔧 Filtres personnalisés")
        
        note_min = st.slider("Note minimale ⭐", 1.0, 5.0, 2.0, 0.5)
        temps_max = st.slider("Temps max (min) ⏱️", 15, 180, 60, 15)
        
        st.markdown("---")
        
        categorie = st.multiselect(
            "Catégories 🍽️",
            ["Entrées", "Plats", "Desserts", "Boissons"],
            default=["Plats"]
        )
        
        difficulte = st.multiselect(
            "Difficulté 📊",
            ["Facile", "Moyen", "Difficile"],
            default=["Facile", "Moyen"]
        )
        
        st.markdown("---")
        
        if st.button("🔍 Appliquer les filtres", use_container_width=True):
            st.success("✅ Filtres appliqués avec succès!")
            
        if st.button("🔄 Réinitialiser", use_container_width=True):
            st.info("ℹ️ Filtres réinitialisés")

if __name__ == "__main__":
    main()