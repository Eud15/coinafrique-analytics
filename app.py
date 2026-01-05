"""
Application Streamlit - Projet CoinAfrique
Master AI - DIT
Auteur: Eudoxie
Date: Janvier 2026
"""

import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime
import os
import re
import sys

# Configuration de la page
st.set_page_config(
    page_title="CoinAfrique Analytics",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# CSS Orange & Bleu (Sans Dégradés)
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;500;600;700&display=swap');
    
    * {
        font-family: 'Poppins', sans-serif;
    }
    
    /* Couleurs Orange & Bleu */
    :root {
        --primary-blue: #2563eb;
        --primary-blue-dark: #1e40af;
        --primary-blue-light: #3b82f6;
        --primary-orange: #f97316;
        --primary-orange-dark: #ea580c;
        --primary-orange-light: #fb923c;
        --success: #10b981;
        --warning: #f59e0b;
        --danger: #ef4444;
        --light: #f8fafc;
        --dark: #1e293b;
        --gray: #64748b;
        --border: #e2e8f0;
        --shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -1px rgba(0, 0, 0, 0.06);
        --shadow-lg: 0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 10px 10px -5px rgba(0, 0, 0, 0.04);
    }
    
    /* Background */
    .main {
        background: #f1f5f9;
    }
    
    .block-container {
        padding: 2rem;
        background: white;
        border-radius: 16px;
        margin: 2rem auto;
        box-shadow: var(--shadow-lg);
    }
    
    /* Header */
    .app-header {
        background: var(--primary-blue);
        padding: 3rem 2rem;
        border-radius: 12px;
        margin-bottom: 2rem;
        box-shadow: var(--shadow-lg);
        text-align: center;
    }
    
    .app-header h1 {
        color: white;
        font-size: 2.5rem;
        font-weight: 700;
        margin: 0 0 0.5rem 0;
        letter-spacing: -0.5px;
    }
    
    .app-header p {
        color: rgba(255, 255, 255, 0.95);
        font-size: 1.1rem;
        margin: 0;
        font-weight: 300;
    }
    
    /* Section Headers */
    .section-title {
        font-size: 1.75rem;
        font-weight: 600;
        color: var(--dark);
        margin: 2.5rem 0 1.5rem 0;
        position: relative;
        padding-bottom: 0.75rem;
    }
    
    .section-title::after {
        content: '';
        position: absolute;
        bottom: 0;
        left: 0;
        width: 60px;
        height: 4px;
        background: var(--primary-orange);
        border-radius: 2px;
    }
    
    /* Cards */
    .custom-card {
        background: white;
        border-radius: 12px;
        padding: 1.5rem;
        box-shadow: var(--shadow);
        border: 2px solid var(--border);
        transition: all 0.3s ease;
        height: 100%;
    }
    
    .custom-card:hover {
        transform: translateY(-4px);
        box-shadow: var(--shadow-lg);
        border-color: var(--primary-blue);
    }
    
    /* Info Boxes */
    .info-box {
        background: var(--primary-blue);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        box-shadow: var(--shadow);
        border-left: 4px solid var(--primary-blue-dark);
    }
    
    .success-box {
        background: var(--success);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        box-shadow: var(--shadow);
        border-left: 4px solid #059669;
    }
    
    .warning-box {
        background: var(--warning);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        box-shadow: var(--shadow);
        border-left: 4px solid #d97706;
    }
    
    .error-box {
        background: var(--danger);
        color: white;
        padding: 1.5rem;
        border-radius: 12px;
        margin: 1.5rem 0;
        box-shadow: var(--shadow);
        border-left: 4px solid #dc2626;
    }
    
    /* Buttons */
    .stButton > button {
        background: var(--primary-orange);
        color: white;
        border: none;
        border-radius: 10px;
        padding: 0.75rem 2rem;
        font-weight: 500;
        font-size: 1rem;
        transition: all 0.3s ease;
        box-shadow: var(--shadow);
        width: 100%;
    }
    
    .stButton > button:hover {
        background: var(--primary-orange-dark);
        transform: translateY(-2px);
        box-shadow: var(--shadow-lg);
    }
    
    .stButton > button:active {
        transform: translateY(0);
    }
    
    /* Download Buttons */
    .stDownloadButton > button {
        background: white;
        color: var(--primary-blue);
        border: 2px solid var(--primary-blue);
        border-radius: 10px;
        padding: 0.6rem 1.5rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stDownloadButton > button:hover {
        background: var(--primary-blue);
        color: white;
    }
    
    /* Form Elements */
    .stTextInput > div > div > input,
    .stTextArea > div > div > textarea,
    .stSelectbox > div > div > select,
    .stMultiSelect > div > div {
        border: 2px solid var(--border);
        border-radius: 10px;
        padding: 0.75rem;
        transition: all 0.3s ease;
        font-size: 0.95rem;
    }
    
    .stTextInput > div > div > input:focus,
    .stTextArea > div > div > textarea:focus,
    .stSelectbox > div > div > select:focus,
    .stMultiSelect > div > div:focus-within {
        border-color: var(--primary-blue);
        box-shadow: 0 0 0 3px rgba(37, 99, 235, 0.1);
    }
    
    /* Metrics */
    [data-testid="stMetricValue"] {
        font-size: 2rem;
        font-weight: 700;
        color: var(--primary-blue);
    }
    
    [data-testid="stMetricLabel"] {
        font-size: 0.9rem;
        color: var(--gray);
        font-weight: 500;
        text-transform: uppercase;
        letter-spacing: 0.5px;
    }
    
    [data-testid="stMetricDelta"] {
        font-size: 0.85rem;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        background: var(--light);
        padding: 0.5rem;
        border-radius: 12px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 0.75rem 1.5rem;
        font-weight: 500;
        color: var(--gray);
        transition: all 0.3s ease;
        border: 2px solid transparent;
    }
    
    .stTabs [data-baseweb="tab"]:hover {
        background: white;
        color: var(--primary-blue);
    }
    
    .stTabs [aria-selected="true"] {
        background: var(--primary-blue);
        color: white;
        border-color: var(--primary-blue);
    }
    
    /* Dataframes */
    .stDataFrame {
        border-radius: 12px;
        overflow: hidden;
        box-shadow: var(--shadow);
        border: 1px solid var(--border);
    }
    
    /* Expander */
    .streamlit-expanderHeader {
        background: white;
        border: 2px solid var(--border);
        border-radius: 10px;
        font-weight: 500;
        color: var(--dark);
        transition: all 0.3s ease;
    }
    
    .streamlit-expanderHeader:hover {
        border-color: var(--primary-blue);
        background: rgba(37, 99, 235, 0.05);
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background: var(--dark);
    }
    
    [data-testid="stSidebar"] * {
        color: white !important;
    }
    
    [data-testid="stSidebar"] .stRadio > div {
        background: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 0.5rem;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label {
        padding: 0.75rem 1rem;
        border-radius: 8px;
        transition: all 0.3s ease;
        cursor: pointer;
    }
    
    [data-testid="stSidebar"] .stRadio > div > label:hover {
        background: rgba(249, 115, 22, 0.2);
    }
    
    [data-testid="stSidebar"] .stRadio input:checked + div {
        background: var(--primary-orange) !important;
    }
    
    /* Progress Bar */
    .stProgress > div > div > div {
        background: var(--primary-orange);
    }
    
    /* File Uploader */
    [data-testid="stFileUploader"] {
        background: white;
        border: 2px dashed var(--border);
        border-radius: 12px;
        padding: 2rem;
        transition: all 0.3s ease;
    }
    
    [data-testid="stFileUploader"]:hover {
        border-color: var(--primary-orange);
        background: rgba(249, 115, 22, 0.02);
    }
    
    /* Slider */
    .stSlider > div > div > div > div {
        background: var(--primary-blue);
    }
    
    /* Checkbox */
    .stCheckbox {
        background: white;
        padding: 1rem;
        border-radius: 10px;
        border: 2px solid var(--border);
        margin: 0.5rem 0;
        transition: all 0.3s ease;
    }
    
    .stCheckbox:hover {
        border-color: var(--primary-orange);
        background: rgba(249, 115, 22, 0.02);
    }
    
    /* Divider */
    hr {
        border: none;
        height: 2px;
        background: var(--border);
        margin: 2rem 0;
    }
    
    /* Scrollbar */
    ::-webkit-scrollbar {
        width: 10px;
        height: 10px;
    }
    
    ::-webkit-scrollbar-track {
        background: var(--light);
    }
    
    ::-webkit-scrollbar-thumb {
        background: var(--primary-blue);
        border-radius: 5px;
    }
    
    ::-webkit-scrollbar-thumb:hover {
        background: var(--primary-blue-dark);
    }
    
    /* Hide Streamlit elements */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    header {visibility: hidden;}
    
    /* MultiSelect custom styling */
    .stMultiSelect [data-baseweb="tag"] {
        background: var(--primary-orange);
        color: white;
    }
</style>
""", unsafe_allow_html=True)

# Créer les dossiers nécessaires
for dossier in ['data/brut', 'data/nettoye']:
    os.makedirs(dossier, exist_ok=True)

# ============================================================================
# COMPOSANTS
# ============================================================================

def render_header(title, subtitle=None):
    """Affiche un header stylisé"""
    html = f'<div class="app-header"><h1>{title}</h1>'
    if subtitle:
        html += f'<p>{subtitle}</p>'
    html += '</div>'
    st.markdown(html, unsafe_allow_html=True)

def render_section(title):
    """Affiche un titre de section"""
    st.markdown(f'<h2 class="section-title">{title}</h2>', unsafe_allow_html=True)

def render_info(content):
    """Affiche une info box"""
    st.markdown(f'<div class="info-box">{content}</div>', unsafe_allow_html=True)

def render_success(content):
    """Affiche une success box"""
    st.markdown(f'<div class="success-box">{content}</div>', unsafe_allow_html=True)

def render_warning(content):
    """Affiche une warning box"""
    st.markdown(f'<div class="warning-box">{content}</div>', unsafe_allow_html=True)

def render_error(content):
    """Affiche une error box"""
    st.markdown(f'<div class="error-box">{content}</div>', unsafe_allow_html=True)

# ============================================================================
# PAGE 1: ACCUEIL
# ============================================================================

def page_accueil():
    """Page d'accueil"""
    
    render_header(
        "CoinAfrique Analytics",
        "Plateforme d'analyse du marketplace sénégalais"
    )
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        render_section("À propos")
        st.markdown("""
        Cette application a été développée dans le cadre du **Master en Intelligence Artificielle** 
        au Dakar Institute of Technology. Elle permet de collecter, nettoyer et analyser 
        des données du marketplace CoinAfrique.
        
        **Fonctionnalités principales:**
        - Extraction automatisée de données web avec BeautifulSoup
        - Nettoyage et standardisation des données
        - Visualisation interactive avec Plotly
        - Export de données structurées en CSV
        """)
    
    with col2:
        render_info("""
        <strong>Auteur:</strong> Eudoxie<br>
        <strong>Programme:</strong> Master AI<br>
        <strong>Institution:</strong> DIT<br>
        <strong>Date:</strong> Janvier 2026<br>
        <strong>Technologies:</strong> Python, Streamlit, BeautifulSoup
        """)
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    render_section("Données disponibles")
    
    categories_info = {
        'Vêtements Homme': 'vetements_homme',
        'Chaussures Homme': 'chaussures_homme',
        'Vêtements Enfants': 'vetements_enfants',
        'Chaussures Enfants': 'chaussures_enfants'
    }
    
    cols = st.columns(4)
    
    for idx, (nom, fichier_base) in enumerate(categories_info.items()):
        with cols[idx]:
            fichier = f"data/nettoye/{fichier_base}_nettoye.csv"
            
            if os.path.exists(fichier):
                try:
                    df = pd.read_csv(fichier)
                    st.metric(nom, f"{len(df)}", "Disponible")
                except:
                    st.metric(nom, "0", "Erreur")
            else:
                st.metric(nom, "0", "Pas de données")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    render_section("Comment utiliser")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Option 1: Scraping automatique**
        
        1. Accéder à "Scraping"
        2. Sélectionner les catégories
        3. Configurer les paramètres
        4. Lancer le scraping
        5. Consulter les résultats
        """)
    
    with col2:
        st.markdown("""
        **Option 2: Import de données**
        
        1. Utiliser Web Scraper (Chrome)
        2. Exporter en CSV
        3. Importer dans "Import"
        4. Nettoyer les données
        5. Visualiser dans "Dashboard"
        """)

# ============================================================================
# PAGE 2: SCRAPER
# ============================================================================

def page_scraper():
    """Page de scraping"""
    
    render_header("Scraping automatique", "Extraction de données avec BeautifulSoup")
    
    render_info(
        "Ce module utilise BeautifulSoup pour extraire automatiquement les données depuis CoinAfrique. "
        "Les données sont nettoyées en temps réel pendant la collecte."
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    render_section("Configuration")
    
    col1, col2 = st.columns(2)
    
    with col1:
        categories_disponibles = {
            'Vêtements Homme': ('vetements_homme', 'https://sn.coinafrique.com/categorie/vetements-homme'),
            'Chaussures Homme': ('chaussures_homme', 'https://sn.coinafrique.com/categorie/chaussures-homme'),
            'Vêtements Enfants': ('vetements_enfants', 'https://sn.coinafrique.com/categorie/vetements-enfants'),
            'Chaussures Enfants': ('chaussures_enfants', 'https://sn.coinafrique.com/categorie/chaussures-enfants')
        }
        
        categories_selectionnees = st.multiselect(
            "Sélectionner les catégories à scraper",
            options=list(categories_disponibles.keys()),
            default=list(categories_disponibles.keys()),
            help="Maintenez Ctrl/Cmd pour sélectionner plusieurs catégories"
        )
    
        with col2:
            max_pages = st.slider(
                "Nombre de pages par catégorie",
                min_value=1,
                max_value=100,
                value=5,
                step=1
            )

    # Et modifier le calcul des métriques:
    col1, col2, col3 = st.columns(3)
    col1.metric("Catégories sélectionnées", len(categories_selectionnees))
    col2.metric("Pages par catégorie", max_pages)
    col3.metric("Estimation", f"~{len(categories_selectionnees) * max_pages * 50} annonces")


    
    st.markdown("<br>", unsafe_allow_html=True)
    
    col1, col2, col3 = st.columns([1, 1, 1])
    with col2:
        lancer = st.button("Lancer le scraping", type="primary", use_container_width=True)
    
    if lancer:
        if not categories_selectionnees:
            render_error("Veuillez sélectionner au moins une catégorie.")
            return
        
        progress_bar = st.progress(0)
        status_text = st.empty()
        
        try:
            sys.path.append(os.path.dirname(__file__))
            from scraper_coinafrique import CoinAfriqueScraper
            
            scraper = CoinAfriqueScraper()
            total = len(categories_selectionnees)
            resultats = {}
            
            # Dans la boucle de scraping:
            for idx, nom_cat in enumerate(categories_selectionnees):
                nom_fichier, url = categories_disponibles[nom_cat]
                
                status_text.info(f"Scraping: {nom_cat} - {max_pages} pages...")
                progress_bar.progress((idx + 0.5) / total)
                
                annonces = scraper.scraper_page(url, max_pages)  # max_pages au lieu de max_annonces
                            
                if annonces:
                    df = pd.DataFrame(annonces)
                    
                    if 'vetements' in nom_fichier:
                        df.rename(columns={'type': 'type_habits'}, inplace=True)
                        colonnes = ['type_habits', 'prix', 'adresse', 'image_lien']
                    else:
                        df.rename(columns={'type': 'type_chaussures'}, inplace=True)
                        colonnes = ['type_chaussures', 'prix', 'adresse', 'image_lien']
                    
                    df = df[colonnes]
                    
                    fichier = f"data/nettoye/{nom_fichier}_nettoye.csv"
                    df.to_csv(fichier, index=False, encoding='utf-8-sig')
                    
                    resultats[nom_cat] = df
                
                progress_bar.progress((idx + 1) / total)
            
            status_text.empty()
            progress_bar.empty()
            
            render_success("Scraping terminé avec succès!")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            if resultats:
                render_section("Résultats")
                
                total_annonces = sum(len(df) for df in resultats.values())
                
                col1, col2, col3 = st.columns(3)
                col1.metric("Catégories traitées", len(resultats))
                col2.metric("Total annonces", total_annonces)
                col3.metric("Taux de succès", f"{(len(resultats)/total)*100:.0f}%")
                
                st.markdown("<br>", unsafe_allow_html=True)
                
                for nom_cat, df in resultats.items():
                    with st.expander(f"{nom_cat} - {len(df)} annonces", expanded=False):
                        
                        col1, col2, col3, col4 = st.columns(4)
                        col1.metric("Annonces", len(df))
                        
                        df['prix_num'] = df['prix'].apply(lambda x: 
                            float(re.sub(r'[^\d]', '', str(x))) if 'demande' not in str(x).lower() and re.sub(r'[^\d]', '', str(x)) else None
                        )
                        prix_valides = df['prix_num'].dropna()
                        
                        if len(prix_valides) > 0:
                            col2.metric("Prix moyen", f"{prix_valides.mean():,.0f} CFA")
                            col3.metric("Prix min", f"{prix_valides.min():,.0f} CFA")
                            col4.metric("Prix max", f"{prix_valides.max():,.0f} CFA")
                        
                        st.dataframe(
                            df.drop(columns=['prix_num'], errors='ignore').head(10),
                            use_container_width=True
                        )
                        
                        csv = df.drop(columns=['prix_num'], errors='ignore').to_csv(index=False, encoding='utf-8-sig')
                        st.download_button(
                            f"Télécharger {nom_cat}",
                            csv,
                            f"{categories_disponibles[nom_cat][0]}_nettoye.csv",
                            "text/csv",
                            key=f"download_{nom_cat}"
                        )
            else:
                render_warning("Aucune donnée collectée. Vérifiez votre connexion.")
        
        except Exception as e:
            render_error(f"Erreur: {str(e)}")

# ============================================================================
# PAGE 3: IMPORT
# ============================================================================

def page_importer():
    """Page d'import"""
    
    render_header("Import et nettoyage", "Importez vos données Web Scraper")
    
    render_info(
        "Importez les fichiers CSV bruts exportés depuis l'extension Web Scraper. "
        "Le système détectera automatiquement les colonnes et appliquera les transformations nécessaires."
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    render_section("Configuration")
    
    categories_map = {
        'Vêtements Homme': ('vetements', 'vetements_homme'),
        'Chaussures Homme': ('chaussures', 'chaussures_homme'),
        'Vêtements Enfants': ('vetements', 'vetements_enfants'),
        'Chaussures Enfants': ('chaussures', 'chaussures_enfants')
    }
    
    categorie_selectionnee = st.selectbox(
        "Type de données",
        list(categories_map.keys())
    )
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    uploaded_file = st.file_uploader(
        "Importer le fichier CSV",
        type=['csv'],
        help="Fichier exporté depuis Web Scraper"
    )
    
    if uploaded_file:
        try:
            df_brut = pd.read_csv(uploaded_file)
            
            render_success(f"Fichier chargé: {uploaded_file.name}")
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            render_section("Données brutes")
            
            col1, col2, col3, col4 = st.columns(4)
            col1.metric("Lignes", len(df_brut))
            col2.metric("Colonnes", len(df_brut.columns))
            col3.metric("Doublons", df_brut.duplicated().sum())
            col4.metric("Valeurs manquantes", df_brut.isnull().sum().sum())
            
            with st.expander("Aperçu", expanded=True):
                st.dataframe(df_brut.head(15), use_container_width=True)
            
            st.markdown("<br>", unsafe_allow_html=True)
            
            col1, col2, col3 = st.columns([1, 1, 1])
            with col2:
                nettoyer_btn = st.button("Nettoyer les données", type="primary", use_container_width=True)
            
            if nettoyer_btn:
                try:
                    sys.path.append(os.path.dirname(__file__))
                    from nettoyage_donnees import NettoyeurDonnees
                    
                    nettoyeur = NettoyeurDonnees()
                    type_cat, nom_fichier = categories_map[categorie_selectionnee]
                    
                    with st.spinner("Nettoyage en cours..."):
                        df_nettoye = nettoyeur.nettoyer_dataframe(df_brut, type_cat)
                        stats = nettoyeur.get_stats()
                    
                    render_success("Nettoyage terminé!")
                    
                    st.markdown("<br>", unsafe_allow_html=True)
                    
                    render_section("Résultats")
                    
                    col1, col2, col3, col4 = st.columns(4)
                    col1.metric("Lignes initiales", stats['lignes_initiales'])
                    col2.metric("Doublons supprimés", stats['doublons_supprimes'])
                    col3.metric("Lignes invalides", stats['lignes_invalides'])
                    col4.metric("Lignes finales", stats['lignes_finales'])
                    
                    fig = go.Figure(data=[
                        go.Bar(name='Avant', x=['Données'], y=[stats['lignes_initiales']], marker_color='#ef4444'),
                        go.Bar(name='Après', x=['Données'], y=[stats['lignes_finales']], marker_color='#10b981')
                    ])
                    
                    fig.update_layout(
                        title="Comparaison",
                        barmode='group',
                        height=300,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
                    
                    with st.expander("Données nettoyées", expanded=True):
                        st.dataframe(df_nettoye.head(20), use_container_width=True)
                    
                    fichier_sortie = f"data/nettoye/{nom_fichier}_nettoye.csv"
                    df_nettoye.to_csv(fichier_sortie, index=False, encoding='utf-8-sig')
                    
                    csv_nettoye = df_nettoye.to_csv(index=False, encoding='utf-8-sig')
                    
                    col1, col2, col3 = st.columns([1, 1, 1])
                    with col2:
                        st.download_button(
                            "Télécharger les données nettoyées",
                            csv_nettoye,
                            f"{nom_fichier}_nettoye.csv",
                            "text/csv",
                            use_container_width=True
                        )
                
                except Exception as e:
                    render_error(f"Erreur: {str(e)}")
        
        except Exception as e:
            render_error(f"Erreur de lecture: {str(e)}")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    render_section("Télécharger les données")
    
    categories = {
        'vetements_homme': 'Vêtements Homme',
        'chaussures_homme': 'Chaussures Homme',
        'vetements_enfants': 'Vêtements Enfants',
        'chaussures_enfants': 'Chaussures Enfants'
    }
    
    cols = st.columns(2)
    
    for idx, (fichier_base, nom_affichage) in enumerate(categories.items()):
        fichier = f"data/nettoye/{fichier_base}_nettoye.csv"
        
        with cols[idx % 2]:
            if os.path.exists(fichier):
                try:
                    df = pd.read_csv(fichier)
                    csv_data = df.to_csv(index=False, encoding='utf-8-sig')
                    
                    st.download_button(
                        f"{nom_affichage} ({len(df)} annonces)",
                        csv_data,
                        f"{fichier_base}_nettoye.csv",
                        "text/csv",
                        key=f"download_existing_{fichier_base}",
                        use_container_width=True
                    )
                except:
                    st.button(f"{nom_affichage} (Erreur)", disabled=True, use_container_width=True)
            else:
                st.button(f"{nom_affichage} (Indisponible)", disabled=True, use_container_width=True)

# ============================================================================
# PAGE 4: DASHBOARD (GRAPHIQUES ENRICHIS)
# ============================================================================

def page_dashboard():
    """Page dashboard avec graphiques variés"""
    
    render_header("Tableau de bord", "Visualisez et analysez vos données")
    
    categories = {
        'Vêtements Homme': 'vetements_homme',
        'Chaussures Homme': 'chaussures_homme',
        'Vêtements Enfants': 'vetements_enfants',
        'Chaussures Enfants': 'chaussures_enfants'
    }
    
    cat_select = st.selectbox("Catégorie", list(categories.keys()))
    
    fichier = f"data/nettoye/{categories[cat_select]}_nettoye.csv"
    
    if not os.path.exists(fichier):
        render_warning("Aucune donnée disponible pour cette catégorie.")
        render_info("Utilisez la page 'Scraping' ou 'Import' pour collecter des données.")
        return
    
    try:
        df = pd.read_csv(fichier)
        
        if len(df) == 0:
            render_warning("Le fichier est vide.")
            return
        
        # Préparation des données
        df['prix_num'] = df['prix'].apply(lambda x: 
            float(re.sub(r'[^\d]', '', str(x))) if 'demande' not in str(x).lower() and re.sub(r'[^\d]', '', str(x)) else None
        )
        
        if 'adresse' in df.columns:
            df['ville'] = df['adresse'].apply(lambda x: 
                x.split(',')[0].strip() if isinstance(x, str) and ',' in x else 'Non spécifié'
            )
        
        col_type = 'type_habits' if 'type_habits' in df.columns else 'type_chaussures'
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ========== STATISTIQUES CLÉS ==========
        render_section("Vue d'ensemble")
        
        col1, col2, col3, col4 = st.columns(4)
        
        col1.metric("Total annonces", f"{len(df):,}")
        
        prix_valides = df['prix_num'].dropna()
        
        if len(prix_valides) > 0:
            col2.metric("Prix moyen", f"{prix_valides.mean():,.0f} CFA")
            col3.metric("Prix min", f"{prix_valides.min():,.0f} CFA")
            col4.metric("Prix max", f"{prix_valides.max():,.0f} CFA")
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        # ========== GRAPHIQUES VARIÉS ==========
        render_section("Analyses détaillées")
        
        tab1, tab2, tab3, tab4, tab5 = st.tabs([
            "Répartition géographique",
            "Analyse des prix",
            "Produits populaires",
            "Statistiques avancées",
            "Données brutes"
        ])
        
        # TAB 1: Géographie (Pie + Bar)
        with tab1:
            if 'ville' in df.columns:
                villes = df['ville'].value_counts().head(10)
                
                col1, col2 = st.columns(2)
                
                with col1:
                    # Graphique circulaire (Pie)
                    fig_pie = px.pie(
                        values=villes.values,
                        names=villes.index,
                        title="Répartition par ville (Top 10)",
                        color_discrete_sequence=px.colors.sequential.Blues_r
                    )
                    fig_pie.update_traces(textposition='inside', textinfo='percent+label')
                    fig_pie.update_layout(height=400)
                    st.plotly_chart(fig_pie, use_container_width=True)
                
                with col2:
                    # Graphique en barre
                    fig_bar = px.bar(
                        x=villes.values,
                        y=villes.index,
                        orientation='h',
                        title="Nombre d'annonces par ville",
                        labels={'x': 'Annonces', 'y': 'Ville'}
                    )
                    fig_bar.update_traces(marker_color='#f97316')
                    fig_bar.update_layout(
                        height=400,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig_bar, use_container_width=True)
                
                # Tableau des statistiques
                st.markdown("**Statistiques par ville**")
                ville_stats = pd.DataFrame({
                    'Ville': villes.index,
                    'Nombre': villes.values,
                    'Pourcentage': (villes.values / len(df) * 100).round(2)
                })
                st.dataframe(ville_stats, use_container_width=True, hide_index=True)
        
        # TAB 2: Prix (Histogram + Box + Donut)
        with tab2:
            if len(prix_valides) > 0:
                col1, col2 = st.columns(2)
                
                with col1:
                    # Histogramme
                    fig_hist = px.histogram(
                        df.dropna(subset=['prix_num']),
                        x='prix_num',
                        nbins=30,
                        title='Distribution des prix',
                        labels={'prix_num': 'Prix (CFA)'}
                    )
                    fig_hist.update_traces(marker_color='#2563eb')
                    fig_hist.update_layout(
                        height=350,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig_hist, use_container_width=True)
                
                with col2:
                    # Box plot
                    fig_box = px.box(
                        df.dropna(subset=['prix_num']),
                        y='prix_num',
                        title='Boîte à moustaches',
                        labels={'prix_num': 'Prix (CFA)'}
                    )
                    fig_box.update_traces(marker_color='#f97316')
                    fig_box.update_layout(
                        height=350,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig_box, use_container_width=True)
                
                # Tranches de prix (Donut)
                st.markdown("**Répartition par tranche de prix**")
                
                # Créer des tranches de prix
                bins = [0, 5000, 10000, 20000, 50000, float('inf')]
                labels = ['0-5K', '5K-10K', '10K-20K', '20K-50K', '50K+']
                df_prix = df.dropna(subset=['prix_num']).copy()
                df_prix['tranche'] = pd.cut(df_prix['prix_num'], bins=bins, labels=labels)
                
                tranche_counts = df_prix['tranche'].value_counts()
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Donut chart
                    fig_donut = go.Figure(data=[go.Pie(
                        labels=tranche_counts.index,
                        values=tranche_counts.values,
                        hole=0.4,
                        marker=dict(colors=['#2563eb', '#3b82f6', '#60a5fa', '#93c5fd', '#dbeafe'])
                    )])
                    fig_donut.update_layout(
                        title="Distribution par tranche de prix",
                        height=350
                    )
                    st.plotly_chart(fig_donut, use_container_width=True)
                
                with col2:
                    st.markdown("**Statistiques**")
                    quartiles = prix_valides.quantile([0.25, 0.5, 0.75])
                    st.metric("Médiane", f"{quartiles[0.5]:,.0f} CFA")
                    st.metric("Q1 (25%)", f"{quartiles[0.25]:,.0f} CFA")
                    st.metric("Q3 (75%)", f"{quartiles[0.75]:,.0f} CFA")
                    st.metric("Écart-type", f"{prix_valides.std():,.0f} CFA")
        
        # TAB 3: Produits (Bar horizontal + Donut des catégories)
        with tab3:
            if col_type in df.columns:
                top_produits = df[col_type].value_counts().head(15)
                
                col1, col2 = st.columns([2, 1])
                
                with col1:
                    # Bar horizontal
                    fig_prod = px.bar(
                        x=top_produits.values,
                        y=top_produits.index,
                        orientation='h',
                        title='Top 15 produits',
                        labels={'x': 'Nombre', 'y': 'Produit'}
                    )
                    fig_prod.update_traces(marker_color='#f97316')
                    fig_prod.update_layout(
                        height=500,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig_prod, use_container_width=True)
                
                with col2:
                    st.markdown("**Top 10 produits**")
                    for idx, (produit, count) in enumerate(top_produits.head(10).items(), 1):
                        pourcentage = (count / len(df)) * 100
                        st.write(f"**{idx}. {produit}**")
                        st.progress(pourcentage / 100)
                        st.caption(f"{count} annonces ({pourcentage:.1f}%)")
                        if idx < 10:
                            st.markdown("<br>", unsafe_allow_html=True)
                
                # Graphique de concentration (Donut)
                st.markdown("**Concentration du marché**")
                
                top_5 = df[col_type].value_counts().head(5).sum()
                autres = len(df) - top_5
                
                fig_concentration = go.Figure(data=[go.Pie(
                    labels=['Top 5 produits', 'Autres produits'],
                    values=[top_5, autres],
                    hole=0.5,
                    marker=dict(colors=['#2563eb', '#f97316'])
                )])
                fig_concentration.update_layout(
                    title="Concentration : Top 5 vs Reste",
                    height=300
                )
                st.plotly_chart(fig_concentration, use_container_width=True)
        
        # TAB 4: Statistiques avancées
        with tab4:
            col1, col2 = st.columns(2)
            
            with col1:
                st.markdown("**Analyse des prix par ville**")
                
                if 'ville' in df.columns and len(prix_valides) > 0:
                    # Prix moyen par ville (top 10)
                    df_ville_prix = df.dropna(subset=['prix_num']).groupby('ville')['prix_num'].agg(['mean', 'count']).reset_index()
                    df_ville_prix = df_ville_prix[df_ville_prix['count'] >= 3].nlargest(10, 'mean')
                    
                    fig_ville_prix = px.bar(
                        df_ville_prix,
                        x='mean',
                        y='ville',
                        orientation='h',
                        title='Prix moyen par ville (min 3 annonces)',
                        labels={'mean': 'Prix moyen (CFA)', 'ville': 'Ville'}
                    )
                    fig_ville_prix.update_traces(marker_color='#2563eb')
                    fig_ville_prix.update_layout(
                        height=400,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    st.plotly_chart(fig_ville_prix, use_container_width=True)
            
            with col2:
                st.markdown("**Distribution des disponibilités**")
                
                # Annonces avec/sans prix
                prix_dispo = len(df[df['prix'] != 'Prix non disponible'])
                prix_non_dispo = len(df) - prix_dispo
                
                fig_dispo = go.Figure(data=[go.Pie(
                    labels=['Prix disponible', 'Prix sur demande'],
                    values=[prix_dispo, prix_non_dispo],
                    hole=0.4,
                    marker=dict(colors=['#10b981', '#f59e0b'])
                )])
                fig_dispo.update_layout(
                    title="Disponibilité des prix",
                    height=300
                )
                st.plotly_chart(fig_dispo, use_container_width=True)
                
                # Annonces avec/sans adresse
                adresse_dispo = len(df[df['adresse'] != 'Adresse non disponible'])
                adresse_non_dispo = len(df) - adresse_dispo
                
                fig_adresse = go.Figure(data=[go.Pie(
                    labels=['Adresse disponible', 'Adresse non disponible'],
                    values=[adresse_dispo, adresse_non_dispo],
                    hole=0.4,
                    marker=dict(colors=['#10b981', '#ef4444'])
                )])
                fig_adresse.update_layout(
                    title="Disponibilité des adresses",
                    height=300
                )
                st.plotly_chart(fig_adresse, use_container_width=True)
            
            # Tableau récapitulatif
            st.markdown("**Tableau récapitulatif**")
            
            recap = pd.DataFrame({
                'Métrique': [
                    'Total annonces',
                    'Prix moyen',
                    'Prix médian',
                    'Écart-type prix',
                    'Villes uniques',
                    'Produits uniques',
                    'Taux prix disponible',
                    'Taux adresse disponible'
                ],
                'Valeur': [
                    f"{len(df):,}",
                    f"{prix_valides.mean():,.0f} CFA" if len(prix_valides) > 0 else "N/A",
                    f"{prix_valides.median():,.0f} CFA" if len(prix_valides) > 0 else "N/A",
                    f"{prix_valides.std():,.0f} CFA" if len(prix_valides) > 0 else "N/A",
                    f"{df['ville'].nunique()}" if 'ville' in df.columns else "N/A",
                    f"{df[col_type].nunique()}",
                    f"{(prix_dispo/len(df)*100):.1f}%",
                    f"{(adresse_dispo/len(df)*100):.1f}%"
                ]
            })
            st.dataframe(recap, use_container_width=True, hide_index=True)
        
        # TAB 5: Données brutes
        with tab5:
            col1, col2 = st.columns([3, 1])
            
            with col1:
                recherche = st.text_input("Rechercher", placeholder="Nike, Adidas, Dakar...")
            
            with col2:
                tri_col = st.selectbox("Trier", ['Aucun'] + list(df.columns))
            
            df_affiche = df.copy()
            
            if recherche:
                df_affiche = df_affiche[
                    df_affiche.astype(str).apply(
                        lambda row: row.str.contains(recherche, case=False, na=False).any(),
                        axis=1
                    )
                ]
                render_info(f"{len(df_affiche)} résultats trouvés pour '{recherche}'")
            
            if tri_col != 'Aucun':
                try:
                    df_affiche = df_affiche.sort_values(tri_col)
                except:
                    pass
            
            st.dataframe(
                df_affiche.drop(columns=['prix_num', 'ville'], errors='ignore'),
                use_container_width=True,
                height=400
            )
            
            col1, col2, col3 = st.columns(3)
            col1.metric("Affichées", len(df_affiche))
            col2.metric("Total", len(df))
            col3.metric("Pourcentage", f"{(len(df_affiche)/len(df)*100):.1f}%")
            
            csv = df_affiche.drop(columns=['prix_num', 'ville'], errors='ignore').to_csv(
                index=False, encoding='utf-8-sig'
            )
            
            st.download_button(
                "Télécharger les données filtrées",
                csv,
                f"{categories[cat_select]}_filtre.csv",
                "text/csv",
                use_container_width=True
            )
    
    except Exception as e:
        render_error(f"Erreur: {str(e)}")

# ============================================================================
# PAGE 5: ÉVALUATION
# ============================================================================

def page_evaluation():
    """Page évaluation"""
    
    render_header("Évaluation", "Votre avis compte")
    
    render_info("Cette évaluation est anonyme et nous aide à améliorer l'application.")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    with st.form("formulaire_evaluation", clear_on_submit=True):
        
        render_section("Informations")
        
        col1, col2 = st.columns(2)
        
        with col1:
            nom = st.text_input("Nom complet", placeholder="Jean Dupont")
            email = st.text_input("Email", placeholder="jean@example.com")
        
        with col2:
            organisation = st.text_input("Organisation", placeholder="DIT, Université...")
            role = st.selectbox("Rôle", ["-- Sélectionner --", "Étudiant", "Enseignant", "Chercheur", "Professionnel", "Autre"])
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        render_section("Notes")
        
        st.caption("De 1 (Mauvais) à 5 (Excellent)")
        
        col1, col2 = st.columns(2)
        
        with col1:
            note_interface = st.slider("Interface", 1, 5, 3)
            note_fonctions = st.slider("Fonctionnalités", 1, 5, 3)
        
        with col2:
            note_perf = st.slider("Performance", 1, 5, 3)
            note_global = st.slider("Note globale", 1, 5, 3)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        render_section("Commentaires")
        
        col1, col2 = st.columns(2)
        
        with col1:
            points_forts = st.text_area("Points forts", height=150)
        
        with col2:
            ameliorations = st.text_area("Améliorations", height=150)
        
        commentaires = st.text_area("Autres commentaires", height=100)
        
        st.markdown("<br>", unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 1, 1])
        
        with col2:
            submitted = st.form_submit_button("Soumettre", type="primary", use_container_width=True)
        
        if submitted:
            erreurs = []
            
            if not nom or len(nom) < 2:
                erreurs.append("Nom requis")
            if not email or '@' not in email:
                erreurs.append("Email invalide")
            if role == "-- Sélectionner --":
                erreurs.append("Rôle requis")
            
            if erreurs:
                for erreur in erreurs:
                    render_error(erreur)
            else:
                eval_data = {
                    'date': datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                    'nom': nom,
                    'email': email,
                    'organisation': organisation,
                    'role': role,
                    'note_interface': note_interface,
                    'note_fonctions': note_fonctions,
                    'note_perf': note_perf,
                    'note_global': note_global,
                    'points_forts': points_forts,
                    'ameliorations': ameliorations,
                    'commentaires': commentaires
                }
                
                fichier_eval = "data/evaluations.csv"
                
                try:
                    if os.path.exists(fichier_eval):
                        df_eval = pd.read_csv(fichier_eval)
                        df_eval = pd.concat([df_eval, pd.DataFrame([eval_data])], ignore_index=True)
                    else:
                        df_eval = pd.DataFrame([eval_data])
                    
                    df_eval.to_csv(fichier_eval, index=False, encoding='utf-8-sig')
                    
                    render_success("Merci pour votre évaluation!")
                    st.balloons()
                    
                except Exception as e:
                    render_error(f"Erreur: {str(e)}")
    
    st.markdown("<br><br>", unsafe_allow_html=True)
    
    # Statistiques
    fichier_eval = "data/evaluations.csv"
    
    if os.path.exists(fichier_eval):
        try:
            df_eval = pd.read_csv(fichier_eval)
            
            if len(df_eval) > 0:
                with st.expander("Statistiques des évaluations", expanded=False):
                    
                    col1, col2, col3, col4 = st.columns(4)
                    
                    col1.metric("Total", len(df_eval))
                    col2.metric("Note moyenne", f"{df_eval['note_global'].mean():.1f}/5")
                    col3.metric("Interface", f"{df_eval['note_interface'].mean():.1f}/5")
                    col4.metric("Fonctionnalités", f"{df_eval['note_fonctions'].mean():.1f}/5")
                    
                    notes_moyennes = {
                        'Interface': df_eval['note_interface'].mean(),
                        'Fonctionnalités': df_eval['note_fonctions'].mean(),
                        'Performance': df_eval['note_perf'].mean(),
                        'Global': df_eval['note_global'].mean()
                    }
                    
                    fig = go.Figure(data=[
                        go.Bar(
                            x=list(notes_moyennes.keys()),
                            y=list(notes_moyennes.values()),
                            marker_color=['#2563eb', '#f97316', '#10b981', '#f59e0b']
                        )
                    ])
                    
                    fig.update_layout(
                        title="Notes moyennes",
                        yaxis_title="Note (/5)",
                        yaxis_range=[0, 5],
                        height=300,
                        plot_bgcolor='rgba(0,0,0,0)',
                        paper_bgcolor='rgba(0,0,0,0)'
                    )
                    
                    st.plotly_chart(fig, use_container_width=True)
        
        except:
            pass

# ============================================================================
# NAVIGATION
# ============================================================================

def main():
    """Fonction principale"""
    
    with st.sidebar:
        st.markdown("<h2 style='color: white; margin-bottom: 2rem; text-align: center;'>Navigation</h2>", unsafe_allow_html=True)
        
        page = st.radio(
            "",
            ["Accueil", "Scraping", "Import", "Dashboard", "Évaluation"]
        )
        
        st.markdown("<br><br>", unsafe_allow_html=True)
        
        st.markdown("<h3 style='color: white;'>Informations</h3>", unsafe_allow_html=True)
        st.markdown("""
        <p style='color: rgba(255,255,255,0.8); font-size: 0.9rem;'>
        <strong>Projet:</strong> CoinAfrique Analytics<br>
        <strong>Programme:</strong> Master AI<br>
        <strong>Institution:</strong> DIT<br>
        <strong>Auteur:</strong> Eudoxie<br>
        <strong>Date:</strong> Janvier 2026
        </p>
        """, unsafe_allow_html=True)
        
        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("<p style='color: rgba(255,255,255,0.6); text-align: center; font-size: 0.8rem;'>© 2026 DIT</p>", unsafe_allow_html=True)
    
    if page == "Accueil":
        page_accueil()
    elif page == "Scraping":
        page_scraper()
    elif page == "Import":
        page_importer()
    elif page == "Dashboard":
        page_dashboard()
    elif page == "Évaluation":
        page_evaluation()


if __name__ == "__main__":
    main()