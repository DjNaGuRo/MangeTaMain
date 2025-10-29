"""Application Streamlit principale."""

import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from pathlib import Path

# ============================================================================
# CHARGER LES DONNÉES
# ============================================================================

@st.cache_data
def load_recipes_data():  # ← Changé de load_interactions_data
    """Charge les données du CSV merged_cleaned.csv."""
    csv_path = Path(__file__).parent.parent.parent / "data" / "processed" / "merged_cleaned.csv"
    
    print(f"📍 Chemin du CSV : {csv_path}")
    print(f"📍 Le fichier existe ? {csv_path.exists()}")
    
    if not csv_path.exists():
        st.error(f"❌ CSV non trouvé à : {csv_path}")
        return None
    
    try:
        df = pd.read_csv(csv_path)
        st.success(f"✅ {len(df)} recettes chargées avec succès!")
        return df
    except Exception as e:
        st.error(f"❌ Erreur lors du chargement du CSV : {e}")
        return None

# ============================================================================
# CONFIGURATION DU THÈME
# ============================================================================

def set_custom_theme(theme="Clair"):
    """Applique un thème personnalisé à l'application."""
    
    # Définir les couleurs selon le thème choisi
    if theme == "Sombre":
        colors = {
            "primary": "#ffffff",
            "secondary": "#f0f0f0",
            "background": "#1a1a1a",
            "text": "#e0e0e0",
            "card_bg": "#000000",
            "card_text": "#e0e0e0",
            "header_gradient": "linear-gradient(135deg, #ffffff 0%, #e0e0e0 100%)",
            "sidebar_gradient": "linear-gradient(180deg, #3a3a3a 0%, #2d2d2d 100%)",
            "border_color": "#3d3d3d",
            "info_bg": "#000000",
            "info_border": "#ffffff",
            "warning_bg": "#1a1a1a",
            "warning_border": "#f39c12",
            "success_bg": "#000000",
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
        
        .stApp {{
            background-color: {colors['background']};
            color: {colors['text']};
        }}
        
        .main {{
            background-color: {colors['background']};
            color: {colors['text']};
        }}
        
        .block-container {{
            background-color: {colors['background']};
            color: {colors['text']};
        }}
        
        .stMarkdown, p, span, div, label, h1, h2, h3, h4, h5, h6 {{
            color: {colors['text']} !important;
        }}
        
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
        
        [data-testid="stSidebar"] {{
            background: {colors['sidebar_gradient']};
        }}
        
        [data-testid="stSidebar"] * {{
            color: white !important;
        }}
        
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
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .fade-in {{
            animation: fadeIn 0.5s ease-out;
        }}
        
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
        
        [data-testid="stExpander"] {{
            background-color: {colors['card_bg']};
            border-radius: 10px;
            border: 1px solid {colors['border_color']};
        }}
        
        [data-testid="stExpander"] * {{
            color: {colors['card_text']} !important;
        }}
        
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
        
        input, textarea, select {{
            background-color: {colors['card_bg']} !important;
            color: {colors['text']} !important;
            border: 1px solid {colors['border_color']} !important;
        }}
        
        [data-testid="stDateInput"] {{
            background-color: {colors['card_bg']};
            color: {colors['text']};
        }}
        
        .stSlider {{
            color: {colors['text']};
        }}
        
        [data-baseweb="select"] {{
            background-color: {colors['card_bg']} !important;
        }}
        
        [data-baseweb="tag"] {{
            background-color: {colors['primary']} !important;
            color: {colors['button_text']} !important;
        }}
        
        .stTabs [data-baseweb="tab-list"] {{
            background-color: {colors['card_bg']};
        }}
        
        .stTabs [data-baseweb="tab"] {{
            color: {colors['text']} !important;
        }}
        
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
        
        [data-testid="stRadio"] label {{
            color: {colors['text']} !important;
        }}
        
        .stDownloadButton button {{
            background: {colors['primary']} !important;
            color: {colors['button_text']} !important;
        }}
        
        .stProgress > div > div {{
            background-color: {colors['primary']} !important;
        }}
        </style>
    """, unsafe_allow_html=True)

# ============================================================================
# FONCTION PRINCIPALE
# ============================================================================

def main():
    """Lance l'application Streamlit principale."""
    st.set_page_config(
        page_title="MangeTaMain - Analyse de recettes les moins bien notées",
        page_icon="🍽️",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    if 'theme' not in st.session_state:
        st.session_state.theme = "Clair"
    
    set_custom_theme(st.session_state.theme)
    
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
        
        def change_theme():
            st.session_state.theme = st.session_state.theme_selector
        
        theme = st.selectbox(
            "Thème", 
            ["Clair", "Sombre", "Auto"],
            index=["Clair", "Sombre", "Auto"].index(st.session_state.theme),
            key="theme_selector",
            on_change=change_theme
        )
        
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

# ============================================================================
# PAGE D'ACCUEIL
# ============================================================================

def show_home_page_modern():
    """Page d'accueil avec design moderne."""
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown('<div class="fade-in">', unsafe_allow_html=True)
        st.markdown("## 👋 Bienvenue sur MangeTaMain!")
        
        st.markdown("""
        <div class="info-box">
            <h3>🎯 Notre Mission</h3>
            <p>Analyser les recettes de cuisine les moins bien notées et proposer des solutions concrètes.</p>
        </div>
        """, unsafe_allow_html=True)
        
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
        st.markdown("### 📊 Statistiques en direct")
        
        # Charger les données pour les statistiques réelles
        df = load_recipes_data()
        
        if df is not None:
            # Adapter les noms de colonnes à votre CSV
            st.metric("📋 Total recettes", len(df))
            st.metric("📊 Colonnes", len(df.columns))
            st.metric("⚠️ Valeurs manquantes", df.isnull().sum().sum())
            
            # Si vous avez une colonne 'note', afficher la moyenne
            if 'note' in df.columns or 'rating' in df.columns:
                note_col = 'note' if 'note' in df.columns else 'rating'
                avg_note = df[note_col].mean()
                st.metric("⭐ Note moyenne", f"{avg_note:.2f}")
        else:
            st.metric("📋 Total recettes", "N/A")
            st.metric("📊 Colonnes", "N/A")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
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
                <p style="text-align: center; font-size: 0.9em;">{desc}</p>
            </div>
            """, unsafe_allow_html=True)

# ============================================================================
# PAGE D'ANALYSE DES DONNÉES
# ============================================================================

def show_data_analysis_modern():
    """Page d'analyse avec design moderne."""
    st.markdown("## 📊 Analyse des données")
    
    # Charger les données
    df = load_recipes_data()
    
    if df is None:
        st.error("❌ Impossible de charger les données")
        st.stop()
    
    with st.expander("🔍 Filtres avancés", expanded=True):
        col1, col2, col3 = st.columns(3)
        
        with col1:
            st.markdown("Période")
        with col2:
            st.markdown("Catégories")
        with col3:
            st.markdown("Notes")
    
    # Métriques en cards
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        st.metric("📋 Total recettes", len(df))
    with col2:
        st.metric("📊 Colonnes", len(df.columns))
    with col3:
        st.metric("⚠️ Valeurs manquantes", df.isnull().sum().sum())
    with col4:
        st.metric("📈 Lignes", len(df))
    
    st.markdown("### 📋 Données détaillées")
    
    search = st.text_input("🔍 Rechercher", "")
    if search:
        mask = df.astype(str).applymap(lambda x: search.lower() in str(x).lower()).any(axis=1)
        df_filtered = df[mask]
    else:
        df_filtered = df
    
    # Sélectionner colonnes
    col_select = st.multiselect(
        "Colonnes à afficher",
        df.columns.tolist(),
        default=df.columns.tolist()[:5]  # 5 colonnes par défaut
    )
    
    # Pagination
    rows_per_page = st.slider("Lignes par page", 10, 500, 50)
    page_num = st.number_input("Page", min_value=1, value=1)
    start_idx = (page_num - 1) * rows_per_page
    end_idx = start_idx + rows_per_page
    
    total_pages = (len(df_filtered) + rows_per_page - 1) // rows_per_page
    st.info(f"📊 Page {page_num}/{total_pages} | {len(df_filtered)} résultats")
    
    st.dataframe(df_filtered.iloc[start_idx:end_idx][col_select], use_container_width=True)
    
    col1, col2 = st.columns(2)
    with col1:
        st.download_button(
            "📥 Exporter CSV",
            df_filtered.to_csv(index=False).encode('utf-8'),
            "recettes_analyse.csv",
            "text/csv"
        )
    
    st.markdown("### 📈 Statistiques descriptives")
    st.dataframe(df.describe(), use_container_width=True)

# ============================================================================
# PAGE DE VISUALISATIONS
# ============================================================================

def show_visualizations_modern():
    """Page de visualisations avec Plotly."""
    st.markdown("## 📈 Visualisations interactives")
    
    df = load_recipes_data()
    
    if df is None:
        st.error("❌ Impossible de charger les données")
        st.stop()
    
    numeric_cols = df.select_dtypes(include=[np.number]).columns.tolist()
    
    if not numeric_cols:
        st.warning("⚠️ Aucune colonne numérique trouvée")
        return
    
    tab1, tab2, tab3, tab4 = st.tabs(["📊 Distribution", "🔥 Top/Flop", "⏱️ Corrélations", "🎯 Insights"])
    
    with tab1:
        if len(numeric_cols) > 0:
            col_selected = st.selectbox("Colonne", numeric_cols, key="viz_col")
            fig = px.histogram(df, x=col_selected, nbins=20, title=f"Distribution de {col_selected}")
            fig.update_layout(plot_bgcolor='rgba(0,0,0,0)', paper_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig, use_container_width=True)
    
    with tab2:
        if len(numeric_cols) > 0:
            col1, col2 = st.columns(2)
            with col1:
                st.info("📊 Top 10")
            with col2:
                st.info("📉 Flop 10")
    
    with tab3:
        if len(numeric_cols) >= 2:
            col_x = st.selectbox("Axe X", numeric_cols, key="x_axis")
            col_y = st.selectbox("Axe Y", numeric_cols, key="y_axis", index=1 if len(numeric_cols) > 1 else 0)
            fig = px.scatter(df, x=col_x, y=col_y, title=f"{col_x} vs {col_y}", trendline="ols")
            st.plotly_chart(fig, use_container_width=True)
    
    with tab4:
        st.markdown("""
        <div class="info-box">
            <h4>📊 Observations</h4>
            <ul>
                <li>Données chargées avec succès</li>
                <li>Visualisations interactives disponibles</li>
            </ul>
        </div>
        """, unsafe_allow_html=True)

# ============================================================================
# PAGE DE RECOMMANDATIONS
# ============================================================================

def show_recommendations_modern():
    """Page de recommandations moderne."""
    st.markdown("## 🎯 Recommandations intelligentes")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.markdown("### 💡 Suggestions d'amélioration")
        
        recommendations = [
            {"title": "Simplifier les recettes complexes", "impact": "Élevé", "priority": 1, "icon": "🎯"},
            {"title": "Optimiser le temps de préparation", "impact": "Moyen", "priority": 2, "icon": "⏱️"},
            {"title": "Améliorer la présentation visuelle", "impact": "Élevé", "priority": 3, "icon": "📸"},
        ]
        
        for rec in recommendations:
            with st.expander(f"{rec['icon']} {rec['title']}", expanded=rec['priority'] <= 2):
                col_a, col_b = st.columns(2)
                col_a.metric("Impact", rec['impact'])
                col_b.metric("Priorité", f"#{rec['priority']}")
    
    with col2:
        st.markdown("### 🔧 Filtres")
        
        note_min = st.slider("Note minimale ⭐", 1.0, 5.0, 2.0, 0.5)
        temps_max = st.slider("Temps max (min) ⏱️", 15, 180, 60, 15)
        
        categorie = st.multiselect("Catégories 🍽️", ["Entrées", "Plats", "Desserts"], default=["Plats"])
        
        if st.button("🔍 Appliquer les filtres", use_container_width=True):
            st.success("✅ Filtres appliqués!")
        
        if st.button("🔄 Réinitialiser", use_container_width=True):
            st.info("ℹ️ Filtres réinitialisés")

# ============================================================================
# LANCER L'APPLICATION
# ============================================================================

if __name__ == "__main__":
    main()