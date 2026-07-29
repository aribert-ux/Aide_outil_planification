import streamlit as st
import os
import requests                         
import google.generativeai as genai     
from datetime import datetime  

# ══════════════════════════════════════════════════════════════
# CHARGEMENT DU CODE GITHUB (NOUVEAU)
# ══════════════════════════════════════════════════════════════
@st.cache_data(ttl=600)  # Cache 10 minutes
def charger_code_depuis_github():
    url = "https://github.com/aribert-ux/Output/blob/main/index.html"
    try:
        r = requests.get(url, timeout=15)
        if r.ok:
            return r.text
        return f"Erreur de chargement : {r.status_code}"
    except Exception as e:
        return f"Erreur réseau : {e}"

GEMINI_API_KEY = st.secrets.get("GEMINI_API_KEY", "")

# ══════════════════════════════════════════════════════════════
# CONFIGURATION PAGE
# ══════════════════════════════════════════════════════════════
st.set_page_config(
    page_title="Aide — Outil de Planification Transport Auchan",
    page_icon="🚚",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════
# CHARTE GRAPHIQUE AUCHAN — THÈME ROUGE
# ══════════════════════════════════════════════════════════════
st.markdown("""<style>
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] { font-family: 'Inter', sans-serif; }

    .stApp { background-color: #F9F9F9; }

    .auchan-header {
        background: linear-gradient(135deg, #7F0000 0%, #D6180B 100%);
        color: white; padding: 24px 32px; border-radius: 12px;
        margin-bottom: 28px; display: flex; align-items: center;
        gap: 20px; box-shadow: 0 4px 16px rgba(214,24,11,0.25);
    }
    .auchan-header h1 { margin: 0; font-size: 1.7rem; font-weight: 700; color: white !important; }
    .auchan-header p  { margin: 4px 0 0 0; font-size: 0.95rem; color: #FFCDD2; }

    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #7F0000 0%, #B71C1C 100%);
    }
    section[data-testid="stSidebar"] * { color: white !important; }
    section[data-testid="stSidebar"] .stRadio label { color: white !important; font-weight: 500; }
    section[data-testid="stSidebar"] hr { border-color: rgba(255,255,255,0.3); }

    .help-card {
        background: white; border-left: 5px solid #D6180B;
        border-radius: 8px; padding: 20px 24px; margin-bottom: 20px;
        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    }
    .help-card h3 { color: #7F0000; margin-top: 0; font-size: 1.1rem; font-weight: 700; }

    .kpi-card {
        background: linear-gradient(135deg, #7F0000, #D6180B);
        color: white; border-radius: 10px; padding: 18px 22px;
        text-align: center; box-shadow: 0 4px 12px rgba(214,24,11,0.2);
        margin-bottom: 16px;
    }
    .kpi-card .kpi-value { font-size: 2rem; font-weight: 700; }
    .kpi-card .kpi-label { font-size: 0.85rem; color: #FFCDD2; margin-top: 4px; }

    .badge-regle {
        display: inline-block; background: #D6180B; color: white;
        border-radius: 20px; padding: 3px 12px; font-size: 0.8rem;
        font-weight: 600; margin-right: 6px; margin-bottom: 6px;
    }
    .badge-ok   { background: #2E7D32; }
    .badge-warn { background: #E65100; }
    .badge-info { background: #1565C0; }

    .step-box {
        display: flex; align-items: flex-start; gap: 16px;
        background: white; border-radius: 8px; padding: 16px 20px;
        margin-bottom: 14px; box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }
    .step-number {
        background: #D6180B; color: white; border-radius: 50%;
        width: 34px; height: 34px; display: flex; align-items: center;
        justify-content: center; font-weight: 700; font-size: 1rem; flex-shrink: 0;
    }
    .step-content h4 { margin: 0 0 6px 0; color: #7F0000; font-weight: 700; }
    .step-content p  { margin: 0; color: #444; font-size: 0.92rem; }

    .styled-table {
        width: 100%; border-collapse: collapse; font-size: 0.9rem;
        border-radius: 8px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    }
    .styled-table thead tr {
        background: linear-gradient(135deg, #7F0000, #D6180B);
        color: white; text-align: left;
    }
    .styled-table th, .styled-table td { padding: 10px 14px; }
    .styled-table tbody tr:nth-child(even) { background: #FFF5F5; }
    .styled-table tbody tr:hover { background: #FFCDD2; }

    .alert-rouge {
        background: #FFEBEE; border-left: 4px solid #D6180B;
        padding: 12px 16px; border-radius: 6px; margin: 12px 0;
        color: #7F0000; font-size: 0.92rem;
    }
    .alert-verte {
        background: #E8F5E9; border-left: 4px solid #2E7D32;
        padding: 12px 16px; border-radius: 6px; margin: 12px 0;
        color: #1B5E20; font-size: 0.92rem;
    }
    .alert-orange {
        background: #FFF3E0; border-left: 4px solid #E65100;
        padding: 12px 16px; border-radius: 6px; margin: 12px 0;
        color: #BF360C; font-size: 0.92rem;
    }

    .stButton > button {
        background: linear-gradient(135deg, #D6180B, #7F0000) !important;
        color: white !important; border: none !important;
        border-radius: 8px !important; font-weight: 600 !important;
        padding: 8px 20px !important; transition: opacity 0.2s;
    }
    .stButton > button:hover { opacity: 0.88 !important; }

    .streamlit-expanderHeader {
        background: #FFF5F5 !important; border-left: 4px solid #D6180B !important;
        border-radius: 6px !important; color: #7F0000 !important; font-weight: 600 !important;
    }

    hr { border: none; border-top: 2px solid #FFCDD2; margin: 24px 0; }

    .footer {
        text-align: center; color: #999; font-size: 0.8rem;
        margin-top: 40px; padding-top: 16px; border-top: 1px solid #FFCDD2;
    }
</style>""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# FONCTIONS UTILITAIRES
# ══════════════════════════════════════════════════════════════

def header():
    logo_html = ""
    try:
        with open("logo.svg", "r", encoding="utf-8") as f:
            svg_content = f.read()
            logo_html = f'<div style="width:108px;height:27px;flex-shrink:0;filter:brightness(0) invert(1)">{svg_content}</div>'
    except FileNotFoundError:
        logo_html = '<div style="font-size:2.2rem">🚚</div>'

    st.markdown(f"""
    <div class="auchan-header">
        {logo_html}
        <div>
            <h1>Outil de Planification Transport</h1>
            <p>Auchan — Guide d'utilisation &amp; Aide en ligne</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def card(titre, contenu_html):
    st.markdown(f"""
    <div class="help-card">
        <h3>{titre}</h3>
        {contenu_html}
    </div>
    """, unsafe_allow_html=True)

def step(num, titre, description):
    st.markdown(f"""
    <div class="step-box">
        <div class="step-number">{num}</div>
        <div class="step-content">
            <h4>{titre}</h4>
            <p>{description}</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def badge(texte, couleur="rouge"):
    classes = {
        "rouge": "badge-regle",
        "vert":  "badge-regle badge-ok",
        "orange":"badge-regle badge-warn",
        "bleu":  "badge-regle badge-info"
    }
    cls = classes.get(couleur, "badge-regle")
    st.markdown(f'<span class="{cls}">{texte}</span>', unsafe_allow_html=True)

def alerte(texte, type_="info"):
    classes = {"erreur": "alert-rouge", "succes": "alert-verte", "info": "alert-orange"}
    cls = classes.get(type_, "alert-orange")
    st.markdown(f'<div class="{cls}">{texte}</div>', unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# SIDEBAR — NAVIGATION
# ══════════════════════════════════════════════════════════════

with st.sidebar:
    st.markdown("### 📋 Navigation")
    st.markdown("---")
    page = st.radio(
        "Choisir une section :",
        options=[
            "🏠 Accueil",
            "📂 Fichiers d'entrée",
            "🚀 Démarrage rapide",
            "📦 Gestion des flux",
            "🗺️ Planification des tournées",
            "⚖️ Règles métier",
            "📊 Indicateurs KPI",
            "💾 Sauvegarde & Export",
            "❓ FAQ",
            "🤖 Assistant IA",           # ← AJOUTER ICI
        ],
        label_visibility="collapsed"
    )
    st.markdown("---")
    st.markdown("**Version** : Outil Planification Transport")
    st.markdown("**Moteur** : 100% navigateur (SheetJS)")
    st.markdown("**Support** : transport@auchan.fr")
    st.markdown("---")
    st.markdown(
        '<div style="font-size:0.78rem;color:#FFCDD2;text-align:center">'
        '© Auchan Transport<br>Région Nord</div>',
        unsafe_allow_html=True
    )

# ══════════════════════════════════════════════════════════════
# HEADER GLOBAL
# ══════════════════════════════════════════════════════════════

header()

# ══════════════════════════════════════════════════════════════
# PAGE — ACCUEIL
# ══════════════════════════════════════════════════════════════
if page == "🏠 Accueil":
    st.markdown("## Bienvenue dans l'Outil de Planification Transport Auchan")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-value">12</div>
            <div class="kpi-label">Règles métier validées</div>
        </div>""", unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-value">6</div>
            <div class="kpi-label">Types de marchandises</div>
        </div>""", unsafe_allow_html=True)
    with col3:
        st.markdown("""
        <div class="kpi-card">
            <div class="kpi-value">33 UT</div>
            <div class="kpi-label">Capacité max remorque</div>
        </div>""", unsafe_allow_html=True)

    st.markdown("---")

    card("🎯 À quoi sert cet outil ?", """
    <p>L'outil de planification transport Auchan permet de :</p>
    <ul>
        <li>Créer et optimiser les <strong>tournées de livraison</strong> vers les magasins</li>
        <li>Visualiser les flux sur un <strong>Gantt interactif</strong> (vue Modules, Remorques, Magasins)</li>
        <li>Valider automatiquement les <strong>règles métier</strong> (capacité, compatibilité, horaires, pauses)</li>
        <li>Gérer les <strong>flux de marchandises</strong> (PGC, NAL, BSA, FL, PF, SURG)</li>
        <li>Planifier des <strong>navettisations</strong> via des entrepôts relay</li>
        <li>Calculer les <strong>KPI de coût</strong> selon le modèle trinôme A + B·km + C·h</li>
        <li>Exporter le plan en <strong>JSON</strong> (session complète) ou en <strong>CSV</strong></li>
    </ul>
    """)

    card("⚙️ Architecture technique", """
    <p>L'application fonctionne <strong>entièrement dans le navigateur</strong>, sans serveur :</p>
    <ul>
        <li>Les fichiers sont lus localement via l'API <code>FileReader</code></li>
        <li>La bibliothèque <strong>SheetJS</strong> (CDN) parse les fichiers Excel</li>
        <li>Toute la logique métier (calcul des pauses, validation, KPI, optimisation) s'exécute en JavaScript côté client</li>
        <li>Les fichiers Distancier et Cartographie sont <strong>mémorisés dans le localStorage</strong> du navigateur entre les sessions</li>
    </ul>
    """)

# ══════════════════════════════════════════════════════════════
# PAGE — FICHIERS D'ENTRÉE
# ══════════════════════════════════════════════════════════════
elif page == "📂 Fichiers d'entrée":
    st.markdown("## 📂 Fichiers d'entrée")

    alerte(
        "⚠️ Les deux premiers fichiers sont <strong>obligatoires</strong>. "
        "La cartographie est fortement recommandée pour afficher les créneaux de livraison.",
        "info"
    )

    st.markdown("---")

    card("1️⃣ Fichier Excel Flux (obligatoire)", """
    <p><strong>Bouton :</strong> <code>📂 Charger Excel</code></p>
    <p>Fichier <code>.xlsx</code> ou <code>.xls</code> contenant les flux de transport à planifier.
    L'outil lit l'onglet nommé <strong>Flux</strong> s'il existe, sinon le <strong>premier onglet</strong> disponible.</p>
    <p>La première ligne est considérée comme l'en-tête et ignorée. Les colonnes doivent être dans cet ordre :</p>
    <table class="styled-table">
        <thead>
            <tr><th>Index</th><th>Contenu attendu</th><th>Exemple</th></tr>
        </thead>
        <tbody>
            <tr><td><code>[0]</code></td><td>Zone Entrepôt</td><td>LESQUIN</td></tr>
            <tr><td><code>[1]</code></td><td>Entrepôt de départ</td><td>ENT IENA1</td></tr>
            <tr><td><code>[2]</code></td><td>Zone de Livraison</td><td>ZONE NORD</td></tr>
            <tr><td><code>[3]</code></td><td>Centre Commercial</td><td>CC Grand Littoral</td></tr>
            <tr><td><code>[4]</code></td><td>Lieu de livraison (Magasin)</td><td>Auchan Englos</td></tr>
            <tr><td><code>[5]</code></td><td>Type de marchandise</td><td>PGC</td></tr>
            <tr><td><code>[6]</code></td><td>Volume en UT</td><td>18</td></tr>
            <tr><td><code>[7]</code></td><td>Jour de chargement</td><td>Lundi</td></tr>
        </tbody>
    </table>
    <p style="margin-top:12px;font-size:0.88rem;color:#666">
        ℹ️ Les jours sont normalisés automatiquement (ex. LUNDI → Lundi).
        Le code FLEG est converti en FL. Les valeurs d'UT avec virgule décimale sont acceptées.
    </p>
    """)

    st.markdown("---")

    card("2️⃣ Distancier REFLEX (obligatoire)", """
    <p><strong>Bouton :</strong> <code>📏 Distancier</code></p>
    <p>Fichier <code>.xlsx</code> ou <code>.xls</code> contenant les distances et durées entre lieux.
    Le premier onglet est toujours utilisé. La première ligne (en-tête) est ignorée.</p>
    <table class="styled-table">
        <thead>
            <tr><th>Index</th><th>Contenu attendu</th><th>Exemple</th></tr>
        </thead>
        <tbody>
            <tr><td><code>[0]</code></td><td>Lieu de départ</td><td>ENT IENA</td></tr>
            <tr><td><code>[1]</code></td><td>Lieu d'arrivée</td><td>Auchan Englos</td></tr>
            <tr><td><code>[2]</code></td><td>Distance en km</td><td>23</td></tr>
            <tr><td><code>[3]</code></td><td>Durée en minutes</td><td>34</td></tr>
        </tbody>
    </table>
    <p style="margin-top:12px;font-size:0.88rem;color:#666">
        ℹ️ Ce fichier est <strong>mémorisé dans le navigateur</strong> (localStorage) après le premier chargement.
        Il n'est pas nécessaire de le recharger à chaque session.<br>
        ℹ️ L'alias <strong>ENT IENA</strong> est automatiquement dupliqué en <strong>ENT IENA1</strong> et <strong>ENT IENA2</strong>.
    </p>
    """)

    st.markdown("---")

    card("3️⃣ Cartographie réception magasins (recommandé)", """
    <p><strong>Bouton :</strong> <code>📋 Cartographie</code></p>
    <p>Fichier <code>.csv</code> ou <code>.txt</code> délimité par des <strong>points-virgules</strong> (;),
    encodé en UTF-8. Contient les créneaux d'ouverture des magasins par jour et par type de marchandise.</p>
    <p><strong>Structure des colonnes :</strong></p>
    <table class="styled-table">
        <thead>
            <tr><th>Index</th><th>Contenu</th><th>Détail</th></tr>
        </thead>
        <tbody>
            <tr><td><code>[0]</code></td><td>Nom du magasin</td><td>Doit correspondre exactement aux noms dans le fichier Flux</td></tr>
            <tr><td><code>[1] à [6]</code></td><td>Créneaux SEC — Lun à Sam</td><td>Format : <code>HH:MM - HH:MM</code> ou <code>Fermé</code></td></tr>
            <tr><td><code>[7] à [12]</code></td><td>Créneaux Frais (PF/FL) — Lun à Sam</td><td>Idem. Créneaux nocturnes acceptés (ex. 22:00 - 05:00)</td></tr>
            <tr><td><code>[13] à [18]</code></td><td>Créneaux Surgelés — Lun à Sam</td><td>Idem</td></tr>
        </tbody>
    </table>
    <p style="margin-top:12px;font-size:0.88rem;color:#666">
        ℹ️ Ce fichier est également <strong>mémorisé dans le navigateur</strong> après le premier chargement.<br>
        ℹ️ Plusieurs créneaux par jour sont séparés par <code>/</code> (ex. <code>06:00 - 09:00 / 14:00 - 17:00</code>).<br>
        ℹ️ Les créneaux avant 07h30 sont automatiquement décalés de +24h pour s'inscrire dans la fenêtre de planification.
    </p>
    """)

    st.markdown("---")

    card("4️⃣ Fichier de session JSON (optionnel)", """
    <p><strong>Bouton :</strong> <code>📥 Importer</code></p>
    <p>Fichier <code>.json</code> exporté par l'outil lors d'une session précédente.
    Restaure intégralement l'état de la planification : flux assignés, modules, offsets, navettes,
    paramètres KPI, overrides de tournées.</p>
    <p style="font-size:0.88rem;color:#666">
        ℹ️ L'outil sauvegarde également automatiquement la session dans le localStorage du navigateur
        toutes les 60 secondes. Une bannière de restauration s'affiche au démarrage si une
        auto-sauvegarde est détectée.
    </p>
    """)

# ══════════════════════════════════════════════════════════════
# PAGE — DÉMARRAGE RAPIDE
# ══════════════════════════════════════════════════════════════
elif page == "🚀 Démarrage rapide":
    st.markdown("## 🚀 Démarrage rapide")
    alerte("⏱️ Suivez ces étapes dans l'ordre pour planifier votre première journée.", "info")

    step(1, "Charger le fichier Excel Flux",
         "Cliquez sur 📂 Charger Excel et sélectionnez votre fichier .xlsx contenant les flux de transport.")

    step(2, "Charger le Distancier",
         "Cliquez sur 📏 Distancier et sélectionnez le fichier Excel contenant les distances et durées "
         "entre entrepôts et magasins. Ce fichier est mémorisé pour les sessions suivantes.")

    step(3, "Charger la Cartographie (recommandé)",
         "Cliquez sur 📋 Cartographie et sélectionnez le fichier CSV des créneaux d'ouverture magasins. "
         "Sans ce fichier, les créneaux ne sont pas affichés dans le Gantt Magasins.")

    step(4, "Sélectionner le jour de planification",
         "Dans la barre d'outils, choisissez le jour (Lundi, Mardi…) pour filtrer "
         "les flux et les tournées correspondants.")

    step(5, "Créer les modules et les tournées",
         "Cliquez sur + Module pour créer un module (chauffeur + tracteur), puis + Tournée "
         "pour y ajouter une tournée. Définissez l'heure de départ, la capacité et le temps d'accrochage.")

    step(6, "Assigner les flux par glisser-déposer",
         "Dans la vue Flux, glissez les blocs de flux vers les barres de tournée dans le Gantt. "
         "Une fenêtre vous permet de saisir la fraction d'UT à assigner.")

    step(7, "Valider les règles métier",
         "Cliquez sur 🔍 Valider puis Tout valider. Le moteur vérifie R1 à R12 "
         "et signale les violations en rouge.")

    step(8, "Consulter les KPI",
         "Dans le panneau de validation, consultez le coût par UT, le taux de remplissage "
         "et le pourcentage de km à vide.")

    step(9, "Exporter le plan",
         "Cliquez sur 💾 Exporter JSON pour sauvegarder la session complète, "
         "ou sur 📋 CSV pour exporter le planning des livraisons.")

    st.markdown("---")
    alerte("✅ Le plan est prêt à être transmis aux équipes terrain.", "succes")

# ══════════════════════════════════════════════════════════════
# PAGE — GESTION DES FLUX
# ══════════════════════════════════════════════════════════════
elif page == "📦 Gestion des flux":
    st.markdown("## 📦 Gestion des flux de marchandises")

    card("Types de marchandises", """
    <table class="styled-table">
        <thead>
            <tr><th>Code</th><th>Libellé</th><th>Contrainte principale</th></tr>
        </thead>
        <tbody>
            <tr><td><strong>PGC</strong></td><td>Produits Grande Consommation</td><td>Chargement de jour uniquement (06h–22h) — incompatible avec FL, PF, SURG</td></tr>
            <tr><td><strong>NAL</strong></td><td>Non Alimentaire</td><td>Chargement de jour uniquement (06h–22h) — incompatible avec FL, PF, SURG</td></tr>
            <tr><td><strong>BSA</strong></td><td>Boissons Sans Alcool</td><td>Chargement de jour uniquement (06h–22h) — incompatible avec FL, PF, SURG</td></tr>
            <tr><td><strong>FL</strong></td><td>Fruits &amp; Légumes 🌙</td><td>Tracteur indissociable pendant le chargement — compatible avec PF uniquement</td></tr>
            <tr><td><strong>PF</strong></td><td>Produits Frais 🌙</td><td>Tracteur indissociable pendant le chargement — compatible avec FL uniquement</td></tr>
            <tr><td><strong>SURG</strong></td><td>Surgelés</td><td>Tracteur indissociable — incompatible avec toutes les autres familles</td></tr>
        </tbody>
    </table>
    """)

    st.markdown("---")

    card("Matrice de compatibilité des marchandises (R2)", """
    <table class="styled-table">
        <thead>
            <tr><th></th><th>PGC</th><th>NAL</th><th>BSA</th><th>FL</th><th>PF</th><th>SURG</th></tr>
        </thead>
        <tbody>
            <tr><td><strong>PGC</strong></td><td>✅</td><td>✅</td><td>✅</td><td>🚫</td><td>🚫</td><td>🚫</td></tr>
            <tr><td><strong>NAL</strong></td><td>✅</td><td>✅</td><td>✅</td><td>🚫</td><td>🚫</td><td>🚫</td></tr>
            <tr><td><strong>BSA</strong></td><td>✅</td><td>✅</td><td>✅</td><td>🚫</td><td>🚫</td><td>🚫</td></tr>
            <tr><td><strong>FL</strong></td><td>🚫</td><td>🚫</td><td>🚫</td><td>✅</td><td>✅</td><td>🚫</td></tr>
            <tr><td><strong>PF</strong></td><td>🚫</td><td>🚫</td><td>🚫</td><td>✅</td><td>✅</td><td>🚫</td></tr>
            <tr><td><strong>SURG</strong></td><td>🚫</td><td>🚫</td><td>🚫</td><td>🚫</td><td>🚫</td><td>✅</td></tr>
        </tbody>
    </table>
    """)

    st.markdown("---")

    card("Calcul du temps de déchargement (UT → minutes)", """
    <table class="styled-table">
        <thead><tr><th>Quantité (UT)</th><th>Temps alloué</th></tr></thead>
        <tbody>
            <tr><td>0 UT</td><td>0 minute</td></tr>
            <tr><td>1 – 9 UT</td><td>15 minutes</td></tr>
            <tr><td>10 – 18 UT</td><td>30 minutes</td></tr>
            <tr><td>19 – 33 UT</td><td>45 minutes</td></tr>
        </tbody>
    </table>
    """)

    st.markdown("---")

    card("Navettisation", """
    <p>La navettisation permet de livrer un magasin via un <strong>entrepôt relay intermédiaire</strong>
    lorsque l'entrepôt d'origine ne peut pas assurer la livraison directement.</p>
    <p>Elle crée automatiquement deux éléments :</p>
    <ul>
        <li>Une <strong>navette</strong> (entrepôt origine → entrepôt relay) à assigner à une tournée T1</li>
        <li>Un <strong>flux dérivé</strong> (entrepôt relay → magasin) à assigner à une tournée T2</li>
    </ul>
    <p>⚠️ La navette T1 doit impérativement être <strong>planifiée et terminée avant</strong>
    le début du chargement de la tournée T2 (règle R_NAV).</p>
    <p>Il est également possible de créer une <strong>navette à vide</strong> pour déplacer
    uniquement le tracteur entre deux entrepôts, sans marchandises.</p>
    """)

# ══════════════════════════════════════════════════════════════
# PAGE — PLANIFICATION DES TOURNÉES
# ══════════════════════════════════════════════════════════════
elif page == "🗺️ Planification des tournées":
    st.markdown("## 🗺️ Planification des tournées")

    card("Structure d'un module", """
    <p>Un <strong>module</strong> représente un binôme chauffeur + tracteur.
    Chaque module peut contenir plusieurs tournées enchaînées dans la journée.</p>
    <table class="styled-table">
        <thead><tr><th>Attribut</th><th>Description</th></tr></thead>
        <tbody>
            <tr><td>ID module</td><td>Identifiant automatique (M1, M2…). L'atelier de construction est M0.</td></tr>
            <tr><td>Tournées</td><td>Liste ordonnée des tournées du module pour la journée</td></tr>
            <tr><td>Offset</td><td>Heure de début de chaque tournée (en minutes depuis minuit)</td></tr>
        </tbody>
    </table>
    """)

    st.markdown("---")

    card("Structure d'une tournée", """
    <p>Chaque tournée est définie par les attributs suivants :</p>
    <table class="styled-table">
        <thead><tr><th>Attribut</th><th>Description</th><th>Valeur par défaut</th></tr></thead>
        <tbody>
            <tr><td>ID tournée</td><td>Identifiant unique (ex. TL01)</td><td>Généré automatiquement</td></tr>
            <tr><td>Capacité</td><td>Capacité max de la remorque en UT</td><td>33 UT</td></tr>
            <tr><td>Retour</td><td>Entrepôt de retour après la dernière livraison</td><td>Premier entrepôt connu</td></tr>
            <tr><td>Accrochage (admDur)</td><td>Temps d'accrochage de la remorque en minutes</td><td>15 min</td></tr>
            <tr><td>Chargement (chgtDur)</td><td>Durée du chargement à l'entrepôt en minutes</td><td>30 min</td></tr>
            <tr><td>Jour</td><td>Jour d'exécution de la tournée</td><td>Jour actif sélectionné</td></tr>
        </tbody>
    </table>
    <p style="margin-top:12px;font-size:0.88rem;color:#666">
        ℹ️ Pour les marchandises FL, PF et SURG, le tracteur reste attelé pendant le chargement
        (le bloc chargement est visible dans le Gantt). Pour PGC, NAL et BSA, le chargement
        se fait sans tracteur (visible uniquement dans la vue Remorques).
    </p>
    """)

    st.markdown("---")

    card("Calcul automatique des pauses (R6 / R7)", """
    <p>Le moteur insère automatiquement les pauses légales dans le planning :</p>
    <table class="styled-table">
        <thead><tr><th>Règle</th><th>Déclencheur</th><th>Durée insérée</th><th>Impact</th></tr></thead>
        <tbody>
            <tr>
                <td><span class="badge-regle">R6</span></td>
                <td>4h30 de conduite continue (270 min)</td>
                <td>45 min (ou 30 min si pause service déjà effectuée dans le shift)</td>
                <td>Remet à zéro le compteur conduite ET service</td>
            </tr>
            <tr>
                <td><span class="badge-regle">R7</span></td>
                <td>6h de service continu (360 min)</td>
                <td>30 min</td>
                <td>Remet à zéro le compteur service uniquement</td>
            </tr>
        </tbody>
    </table>
    <p style="margin-top:12px;font-size:0.88rem;color:#666">
        ℹ️ Les pauses peuvent être <strong>parallèles</strong> (pendant un déchargement assez long)
        ou <strong>dures</strong> (insérées dans le planning, allongeant l'heure de retour).<br>
        ℹ️ L'état conduite/service est <strong>chaîné entre les tournées</strong> d'un même module
        (sauf coupure manuelle de shift).<br>
        ℹ️ Les pauses sont repositionnables par glisser-déposer et peuvent être scindées (45 min → 15+30 min).
    </p>
    """)

    st.markdown("---")

    card("Vues Gantt disponibles", """
    <table class="styled-table">
        <thead><tr><th>Vue</th><th>Description</th></tr></thead>
        <tbody>
            <tr><td>⚡ <strong>Flux</strong></td><td>Timeline des flux à planifier + Gantt de l'atelier (M0). Zone de construction et de glisser-déposer.</td></tr>
            <tr><td>📦 <strong>Modules</strong></td><td>Une ligne par module chauffeur. Affiche les barres de tournées avec segments chargement, accrochage, trajets, livraisons, pauses et retour. Barre de shift chauffeur.</td></tr>
            <tr><td>🚛 <strong>Remorques</strong></td><td>Vue par module avec planning des chargements. Détecte les chargements simultanés. Bilan dans le panneau latéral.</td></tr>
            <tr><td>🏪 <strong>Magasins</strong></td><td>Vue par magasin avec créneaux d'ouverture (cartographie). Livraisons groupées par type SEC / Frais / Surgelés. Filtres et tri dans le panneau latéral.</td></tr>
        </tbody>
    </table>
    """)

# ══════════════════════════════════════════════════════════════
# PAGE — RÈGLES MÉTIER
# ══════════════════════════════════════════════════════════════
elif page == "⚖️ Règles métier":
    st.markdown("## ⚖️ Règles métier")

    regles = [
        ("R1",    "Capacité remorque",
         "Le total des UT chargées ne doit pas dépasser la capacité de la remorque (33 UT par défaut, modifiable par tournée).",
         "ERREUR"),
        ("R2",    "Compatibilité marchandises",
         "Les marchandises incompatibles ne peuvent pas être chargées ensemble sur la même remorque. "
         "SEC (PGC/NAL/BSA) est incompatible avec Frais (FL/PF) et Surgelés. SURG est incompatible avec tout le reste.",
         "ERREUR"),
        ("R3",    "Chargement PGC/NAL/BSA de jour",
         "Les marchandises PGC, NAL et BSA ne peuvent être chargées qu'entre 06h00 et 22h00. "
         "Un chargement avant 06h00 pour ces familles génère une erreur.",
         "ERREUR"),
        ("R4",    "Temps de déchargement",
         "Le temps de déchargement est calculé automatiquement selon le volume : 15 min (1–9 UT), "
         "30 min (10–18 UT), 45 min (19–33 UT). Ce barème est appliqué à chaque arrêt.",
         "INFO"),
        ("R6",    "Pause conduite (4h30)",
         "Après 4h30 de conduite continue, une pause de 45 min est obligatoire "
         "(réduite à 30 min si une pause service a déjà été effectuée dans le shift). "
         "Cette pause est insérée automatiquement dans le planning.",
         "AVERTISSEMENT"),
        ("R7",    "Pause service (6h)",
         "Après 6h de service continu (conduite + déchargements + emballages), "
         "une pause de 30 min est obligatoire. Insérée automatiquement.",
         "AVERTISSEMENT"),
        ("R8",    "Durée de shift",
         "La durée totale d'un shift ne doit pas dépasser 11h pour un shift de jour "
         "ou 10h pour un shift de nuit. Les coupures manuelles de shift permettent de scinder "
         "le travail d'un module en plusieurs shifts.",
         "ERREUR"),
        ("R9",    "Minimum 2 tournées par module",
         "Chaque module opérationnel doit comporter au moins 2 tournées dans la journée "
         "pour justifier l'immobilisation d'un binôme chauffeur-tracteur.",
         "AVERTISSEMENT"),
        ("R10",   "Créneaux d'ouverture magasin",
         "La livraison doit arriver dans les créneaux d'ouverture déclarés du magasin "
         "(issus du fichier Cartographie). Une livraison hors créneau génère une erreur.",
         "ERREUR"),
        ("R11",   "Reprise des emballages",
         "Chaque magasin actif doit recevoir au moins un passage de flotte propre par jour "
         "pour assurer la reprise des emballages.",
         "AVERTISSEMENT"),
        ("R12",   "Pas de chevauchement tracteur",
         "Deux tournées d'un même module ne peuvent pas se chevaucher temporellement. "
         "Un chevauchement est signalé par un contour rouge sur les barres concernées dans le Gantt.",
         "ERREUR"),
        ("R_NAV", "Chronologie navettisation",
         "Lorsqu'un flux est navettisé, la navette (T1) doit être planifiée et terminée "
         "avant le début du chargement du flux dérivé (T2). "
         "L'outil vérifie cette contrainte au moment du glisser-déposer.",
         "ERREUR"),
    ]

    couleurs = {"ERREUR": "erreur", "AVERTISSEMENT": "info", "INFO": "succes"}

    for code, titre, desc, niveau in regles:
        with st.expander(f"**{code}** — {titre}"):
            alerte(f"<strong>Niveau :</strong> {niveau}", couleurs.get(niveau, "info"))
            st.markdown(desc)

# ══════════════════════════════════════════════════════════════
# PAGE — INDICATEURS KPI
# ══════════════════════════════════════════════════════════════
elif page == "📊 Indicateurs KPI":
    st.markdown("## 📊 Indicateurs KPI")

    card("Modèle de coût trinôme", """
    <p>Le coût d'un module est calculé selon la formule :</p>
    <pre style="background:#FFF5F5;padding:12px;border-radius:6px;border-left:4px solid #D6180B">
Coût = A
     + B_sec   × km_sec
     + B_frais × km_frais
     + C_jour  × heures_jour
     + C_nuit  × heures_nuit</pre>
    <table class="styled-table">
        <thead><tr><th>Paramètre</th><th>Description</th><th>Valeur par défaut</th></tr></thead>
        <tbody>
            <tr><td><strong>A</strong></td><td>Coût fixe par module</td><td>10 €</td></tr>
            <tr><td><strong>B sec</strong></td><td>Coût kilométrique SEC (PGC/NAL/BSA)</td><td>0,45 €/km</td></tr>
            <tr><td><strong>B frais</strong></td><td>Coût kilométrique Frais/SURG (FL/PF/SURG)</td><td>0,55 €/km</td></tr>
            <tr><td><strong>C jour</strong></td><td>Coût horaire shift de jour (06h–22h)</td><td>35 €/h</td></tr>
            <tr><td><strong>C nuit</strong></td><td>Coût horaire shift de nuit (22h–06h)</td><td>47 €/h</td></tr>
            <tr><td><strong>CO₂/km</strong></td><td>Émissions CO₂ par km (semi-remorque 35t)</td><td>900 g/km</td></tr>
            <tr><td><strong>Prix carbone</strong></td><td>Coût de la tonne de CO₂</td><td>50 €/t</td></tr>
        </tbody>
    </table>
    <p style="margin-top:12px;font-size:0.88rem;color:#666">
        ℹ️ Tous les paramètres sont modifiables directement dans le panneau KPI de l'interface.
    </p>
    """)

    st.markdown("---")

    card("Indicateurs calculés", """
    <table class="styled-table">
        <thead><tr><th>Indicateur</th><th>Description</th></tr></thead>
        <tbody>
            <tr><td>Coût financier / UT</td><td>Coût total divisé par le nombre d'UT livrées (hors navettes)</td></tr>
            <tr><td>Coût carbone / UT</td><td>Coût CO₂ (km × g/km → tonnes × prix/t) divisé par les UT livrées</td></tr>
            <tr><td>Taux de remplissage global</td><td>Moyenne pondérée par km : UT à bord × km / (capacité × km). Les retours à vide pénalisent ce taux.</td></tr>
            <tr><td>Taux de remplissage au départ</td><td>UT chargées au départ / capacité remorque, sans pondération km</td></tr>
            <tr><td>% km à vide</td><td>Kilomètres de retour à vide / total km × 100</td></tr>
        </tbody>
    </table>
    """)

# ══════════════════════════════════════════════════════════════
# PAGE — SAUVEGARDE & EXPORT
# ══════════════════════════════════════════════════════════════
elif page == "💾 Sauvegarde & Export":
    st.markdown("## 💾 Sauvegarde & Export")

    card("Formats d'export disponibles", """
    <table class="styled-table">
        <thead><tr><th>Format</th><th>Bouton</th><th>Contenu</th></tr></thead>
        <tbody>
            <tr>
                <td><strong>JSON</strong></td>
                <td><code>💾 Exporter JSON</code></td>
                <td>Session complète : flux planifiés, modules, offsets, navettes, overrides de tournées, paramètres KPI. Peut être réimporté.</td>
            </tr>
            <tr>
                <td><strong>CSV</strong></td>
                <td><code>📋 CSV</code></td>
                <td>Planning des livraisons : Module, Tournée, Remorque, Magasin, Marchandise, UT, Heure estimée.</td>
            </tr>
        </tbody>
    </table>
    """)

    st.markdown("---")

    step(1, "Valider toutes les tournées",
         "Cliquez sur 🔍 Valider → Tout valider. Assurez-vous qu'il n'y a aucune erreur R1–R12 avant d'exporter.")
    step(2, "Exporter la session JSON",
         "Cliquez sur 💾 Exporter JSON. Un fichier session_transport_[Jour]_[Date].json est téléchargé.")
    step(3, "Exporter le CSV si nécessaire",
         "Cliquez sur 📋 CSV pour obtenir un tableau des livraisons planifiées avec les heures estimées.")
    step(4, "Réimporter une session",
         "Cliquez sur 📥 Importer et sélectionnez un fichier .json précédemment exporté "
         "pour restaurer intégralement l'état de la planification.")

    st.markdown("---")

    card("Auto-sauvegarde", """
    <p>L'outil sauvegarde automatiquement la session dans le <strong>localStorage du navigateur</strong>
    toutes les 60 secondes. Un badge vert <code>💾 HH:MM</code> s'affiche dans la barre d'outils
    pour confirmer la dernière sauvegarde.</p>
    <p>Au démarrage, si une auto-sauvegarde est détectée, une bannière jaune propose de
    <strong>Restaurer</strong> ou <strong>Ignorer</strong> la session précédente.</p>
    <p style="font-size:0.88rem;color:#666">
        ⚠️ Le localStorage est propre à chaque navigateur et à chaque domaine.
        Utilisez l'export JSON pour transférer une session entre postes.
    </p>
    """)

# ══════════════════════════════════════════════════════════════
# PAGE — FAQ
# ══════════════════════════════════════════════════════════════
elif page == "❓ FAQ":
    st.markdown("## ❓ Questions fréquentes")

    faqs = [
        ("Le fichier Excel ne se charge pas",
         "Vérifiez que le fichier est au format <code>.xlsx</code> ou <code>.xls</code>. "
         "Assurez-vous que les données commencent bien à la première ligne (ligne d'en-tête) "
         "et que les colonnes sont dans l'ordre attendu (voir section 📂 Fichiers d'entrée)."),

        ("Le distancier affiche 'Distance introuvable'",
         "Le nom du lieu dans le fichier Flux doit correspondre <strong>exactement</strong> "
         "au nom dans le distancier (casse incluse). "
         "Vérifiez les espaces et accents. L'alias ENT IENA est automatiquement dupliqué "
         "en ENT IENA1 et ENT IENA2."),

        ("Une tournée affiche une erreur R2 (incompatibilité)",
         "Vérifiez que les marchandises affectées à la même tournée sont compatibles. "
         "FL et PF ne peuvent pas être mélangées avec PGC, NAL, BSA ou SURG. "
         "SURG doit toujours être seul sur sa remorque."),

        ("Les pauses R6/R7 allongent trop la tournée",
         "Réduisez le nombre d'arrêts ou découpez la tournée en deux. "
         "Vous pouvez aussi repositionner les pauses par glisser-déposer dans le Gantt, "
         "ou les scinder (45 min → 15+30 min) via le bouton ✂ sur le bloc de pause."),

        ("Comment gérer une livraison via un entrepôt intermédiaire ?",
         "Utilisez la fonction de <strong>navettisation</strong> : bouton ⇄ sur le flux concerné "
         "dans la liste ou dans la timeline. Sélectionnez l'entrepôt relay et les UT à navetter. "
         "Deux éléments sont créés : une navette (T1) et un flux dérivé (T2). "
         "Planifiez T1 avant T2 pour respecter la règle R_NAV."),

        ("Le Gantt Magasins n'affiche pas les créneaux d'ouverture",
         "Chargez le fichier Cartographie via le bouton 📋 Cartographie. "
         "Sans ce fichier, les plages vertes d'ouverture ne sont pas affichées. "
         "Vérifiez que les noms de magasins dans le CSV correspondent exactement "
         "à ceux du fichier Flux."),

        ("Comment modifier les paramètres KPI (coût fixe, coût km…) ?",
         "Dans le panneau de validation (bouton 🔍 Valider), modifiez directement "
         "les champs A, B sec, B frais, C jour, C nuit, CO₂/km et Prix carbone, "
         "puis cliquez sur 🔄 Recalculer."),

        ("Comment modifier les couleurs de l'interface ?",
         "Modifiez les valeurs hexadécimales dans le bloc <code>&lt;style&gt;</code> du fichier HTML. "
         "Le thème rouge Auchan utilise <code>#D6180B</code> (rouge principal) et <code>#7F0000</code> (rouge foncé)."),

        ("La session n'est pas restaurée au démarrage",
         "L'auto-sauvegarde utilise le localStorage du navigateur. "
         "Elle est perdue si vous videz le cache ou changez de navigateur. "
         "Pour transférer une session entre postes, utilisez l'export JSON (💾 Exporter JSON) "
         "puis l'import (📥 Importer)."),
    ]

    for question, reponse in faqs:
        with st.expander(f"❓ {question}"):
            st.markdown(reponse, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PAGE — ASSISTANT IA
# ══════════════════════════════════════════════════════════════
elif page == "🤖 Assistant IA":
    st.markdown("## 🤖 Assistant IA — Outil de Planification Transport")
    st.markdown(
        "Posez vos questions sur le code, les règles métier, "
        "les fichiers d'entrée, les vues Gantt, les KPI, etc."
    )

    # Chargement du code source depuis GitHub
    with st.spinner("Chargement du code source depuis GitHub..."):
        code_source = charger_code_depuis_github()

    nb_lignes = code_source.count('\n')
    st.success(f"✅ index.html chargé ({nb_lignes:,} lignes)")
    st.caption(f"Mis à jour : {datetime.now().strftime('%H:%M:%S')}")

    if st.button("🔄 Forcer le rechargement"):
        st.cache_data.clear()
        st.rerun()

    # Vérification clé API
    if not GEMINI_API_KEY:
        st.warning(
            "⚠️ Clé API Gemini non configurée. "
            "Ajoutez GEMINI_API_KEY dans .streamlit/secrets.toml"
        )
        st.code(
            '[secrets]\nGEMINI_API_KEY = "AIza..."',
            language="toml"
        )
        st.stop()

    # Prompt système avec le code injecté
    SYSTEM_PROMPT = (
        f"Tu es un assistant expert de l'outil de planification transport Auchan Région Nord.\n"
        f"Tu as accès au code source complet de l'application (index.html, {nb_lignes} lignes).\n\n"
        f"Le code est découpé en sections commentées.\n"
        f"Quand tu réponds :\n"
        f"- Cite la section concernée si pertinent\n"
        f"- Donne des exemples concrets tirés du code réel\n"
        f"- Réponds en français, de façon concise et pratique\n"
        f"- Si une question concerne une règle (R1 à R12), explique son implémentation\n\n"
        f"Voici le code source complet :\n\n"
        f"{code_source}"
    )

    # Initialisation du modèle et de l'historique
    if "chat_messages" not in st.session_state:
        st.session_state.chat_messages = []

    if "gemini_chat" not in st.session_state:
        genai.configure(api_key=GEMINI_API_KEY)
        model = genai.GenerativeModel(
            model_name="gemini-2.0-flash-exp",
            system_instruction=SYSTEM_PROMPT
        )
        st.session_state.gemini_chat = model.start_chat(history=[])

    # Affichage de l'historique de conversation
    for msg in st.session_state.chat_messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Saisie utilisateur
    if prompt := st.chat_input("Posez votre question sur l'outil ou le code..."):

        st.session_state.chat_messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Gemini analyse le code..."):
                try:
                    response = st.session_state.gemini_chat.send_message(prompt)
                    answer = response.text
                except Exception as e:
                    answer = f"Erreur Gemini : {e}"
                st.markdown(answer)

        st.session_state.chat_messages.append({"role": "assistant", "content": answer})

    # Bouton reset conversation
    if st.session_state.get("chat_messages"):
        st.markdown("---")
        if st.button("🗑️ Effacer la conversation"):
            st.session_state.chat_messages = []
            if "gemini_chat" in st.session_state:
                del st.session_state.gemini_chat
            st.rerun()

# ══════════════════════════════════════════════════════════════
# PIED DE PAGE
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
    Auchan Transport — Outil de Planification Transport &nbsp;|&nbsp;
    Région Nord &nbsp;|&nbsp;
    Support : transport@auchan.fr
</div>
""", unsafe_allow_html=True)
