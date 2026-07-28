import streamlit as st
import os

# ══════════════════════════════════════════════════════════════# CONFIGURATION PAGE# ══════════════════════════════════════════════════════════════
st.set_page_config(    page_title="Aide — Outil de Planification Transport Auchan",
    page_icon="🚚",
    layout="wide",    initial_sidebar_state="expanded"
)

# ══════════════════════════════════════════════════════════════
# CHARTE GRAPHIQUE AUCHAN — THÈME ROUGE
# ══════════════════════════════════════════════════════════════
st.markdown("""<style>
    /* ── Imports & Reset ── */
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700&display=swap');

    html, body, [class*="css"] {
        font-family: 'Inter', sans-serif;
    }

    /* ── Fond général ── */
    .stApp {
        background-color: #F9F9F9;
    }

    /* ── Header principal ── */
    .auchan-header {
        background: linear-gradient(135deg, #7F0000 0%, #D6180B 100%);
        color: white;
        padding: 24px 32px;
        border-radius: 12px;
        margin-bottom: 28px;
        display: flex;
        align-items: center;
        gap: 20px;
        box-shadow: 0 4px 16px rgba(214,24,11,0.25);
    }

    .auchan-header h1 {
        margin: 0;
        font-size: 1.7rem;
        font-weight: 700;
        color: white !important;
    }

    .auchan-header p {
        margin: 4px 0 0 0;
        font-size: 0.95rem;
        color: #FFCDD2;
    }

    /* ── Sidebar ── */
    section[data-testid="stSidebar"] {
        background: linear-gradient(180deg, #7F0000 0%, #B71C1C 100%);
    }

    section[data-testid="stSidebar"] * {
        color: white !important;
    }

    section[data-testid="stSidebar"] .stRadio label {
        color: white !important;
        font-weight: 500;
    }

    section[data-testid="stSidebar"] hr {
        border-color: rgba(255,255,255,0.3);
    }

    /* ── Cartes de section ── */
    .help-card {
        background: white;
        border-left: 5px solid #D6180B;
        border-radius: 8px;
        padding: 20px 24px;
        margin-bottom: 20px;        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    }

    .help-card h3 {        color: #7F0000;        margin-top: 0;
        font-size: 1.1rem;
        font-weight: 700;
    }

    /* ── Cartes KPI / Statistiques ── */    .kpi-card {        background: linear-gradient(135deg, #7F0000, #D6180B);        color: white;
        border-radius: 10px;
        padding: 18px 22px;
        text-align: center;
        box-shadow: 0 4px 12px rgba(214,24,11,0.2);
        margin-bottom: 16px;
    }

    .kpi-card .kpi-value {
        font-size: 2rem;
        font-weight: 700;
    }

    .kpi-card .kpi-label {        font-size: 0.85rem;
        color: #FFCDD2;
        margin-top: 4px;
    }

    /* ── Badges de règles ── */
    .badge-regle {
        display: inline-block;
        background: #D6180B;
        color: white;
        border-radius: 20px;        padding: 3px 12px;
        font-size: 0.8rem;
        font-weight: 600;
        margin-right: 6px;
        margin-bottom: 6px;
    }

    .badge-ok {
        background: #2E7D32;
    }

    .badge-warn {
        background: #E65100;
    }

    .badge-info {
        background: #1565C0;
    }

    /* ── Étapes numérotées ── */    .step-box {
        display: flex;
        align-items: flex-start;
        gap: 16px;
        background: white;
        border-radius: 8px;
        padding: 16px 20px;
        margin-bottom: 14px;
        box-shadow: 0 2px 6px rgba(0,0,0,0.06);
    }

    .step-number {
        background: #D6180B;
        color: white;
        border-radius: 50%;
        width: 34px;
        height: 34px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-weight: 700;        font-size: 1rem;
        flex-shrink: 0;
    }

    .step-content h4 {
        margin: 0 0 6px 0;
        color: #7F0000;
        font-weight: 700;
    }

    .step-content p {
        margin: 0;
        color: #444;
        font-size: 0.92rem;
    }

    /* ── Tableau stylisé ── */
    .styled-table {
        width: 100%;
        border-collapse: collapse;
        font-size: 0.9rem;
        border-radius: 8px;        overflow: hidden;        box-shadow: 0 2px 8px rgba(0,0,0,0.07);
    }

    .styled-table thead tr {
        background: linear-gradient(135deg, #7F0000, #D6180B);
        color: white;
        text-align: left;
    }

    .styled-table th, .styled-table td {        padding: 10px 14px;
    }

    .styled-table tbody tr:nth-child(even) {        background: #FFF5F5;
    }

    .styled-table tbody tr:hover {
        background: #FFCDD2;
    }

    /* ── Alertes personnalisées ── */
    .alert-rouge {
        background: #FFEBEE;
        border-left: 4px solid #D6180B;
        padding: 12px 16px;
        border-radius: 6px;
        margin: 12px 0;        color: #7F0000;
        font-size: 0.92rem;
    }

    .alert-verte {
        background: #E8F5E9;        border-left: 4px solid #2E7D32;
        padding: 12px 16px;
        border-radius: 6px;
        margin: 12px 0;
        color: #1B5E20;
        font-size: 0.92rem;
    }

    .alert-orange {
        background: #FFF3E0;
        border-left: 4px solid #E65100;
        padding: 12px 16px;        border-radius: 6px;
        margin: 12px 0;        color: #BF360C;
        font-size: 0.92rem;
    }

    /* ── Boutons ── */
    .stButton > button {
        background: linear-gradient(135deg, #D6180B, #7F0000) !important;
        color: white !important;
        border: none !important;
        border-radius: 8px !important;
        font-weight: 600 !important;
        padding: 8px 20px !important;
        transition: opacity 0.2s;    }

    .stButton > button:hover {
        opacity: 0.88 !important;
    }

    /* ── Expanders ── */
    .streamlit-expanderHeader {
        background: #FFF5F5 !important;
        border-left: 4px solid #D6180B !important;        border-radius: 6px !important;
        color: #7F0000 !important;
        font-weight: 600 !important;
    }

    /* ── Séparateur ── */
    hr {
        border: none;        border-top: 2px solid #FFCDD2;
        margin: 24px 0;
    }

    /* ── Pied de page ── */    .footer {
        text-align: center;
        color: #999;
        font-size: 0.8rem;
        margin-top: 40px;
        padding-top: 16px;
        border-top: 1px solid #FFCDD2;
    }</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# FONCTIONS UTILITAIRES
# ══════════════════════════════════════════════════════════════

def header():
    """Affiche le header avec logo Auchan."""
    logo_html = ""
    try:
        with open("logo.svg", "r", encoding="utf-8") as f:
            svg_content = f.read()
            logo_html = f'<div style="width:108px;height:37px;flex-shrink:0;filter:brightness(0) invert(1)">{svg_content}</div>'
    except FileNotFoundError:
        logo_html = '<div style="font-size:2.2rem">🚚</div>'

    st.markdown(f"""
    <div class="auchan-header">
        {logo_html}
        <div>
            <h1>Outil de Planification Transport</h1>
            <p>Auchan — Guide d'utilisation & Aide en ligne</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

def card(titre, contenu_html):    st.markdown(f"""
    <div class="help-card">
        <h3>{titre}</h3>
        {contenu_html}
    </div>
    """, unsafe_allow_html=True)

def step(num, titre, description):
    st.markdown(f"""
    <div class="step-box">
        <div class="step-number">{num}</div>        <div class="step-content">
            <h4>{titre}</h4>            <p>{description}</p>
        </div>    </div>
    """, unsafe_allow_html=True)

def badge(texte, couleur="rouge"):
    classes = {"rouge": "badge-regle", "vert": "badge-regle badge-ok",               "orange": "badge-regle badge-warn", "bleu": "badge-regle badge-info"}    
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
        options=[            "🏠 Accueil",            "🚀 Démarrage rapide",
            "📦 Gestion des flux",
            "🗺️ Planification des tournées",
            "⚖️ Règles métier",
            "📊 Indicateurs KPI",
            "💾 Sauvegarde & Export",
            "❓ FAQ",
        ],
        label_visibility="collapsed"    )    
    st.markdown("---")    
    st.markdown("**Version** : Flux Hebdo Flotte 2027")    
    st.markdown("**Moteur** : code.js v7.1")
    st.markdown("**Support** : transport@auchan.fr")    
    st.markdown("---")    
    st.markdown(        '<div style="font-size:0.78rem;color:#FFCDD2;text-align:center">'        '© 2026 Auchan Transport<br>Région Nord</div>',
        unsafe_allow_html=True    )

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
            <div class="kpi-value">11</div>
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

    card("🎯 À quoi sert cet outil ?", """    <p>L'outil de planification transport Auchan permet de :</p>
    <ul>
        <li>Créer et optimiser les <strong>tournées de livraison</strong> vers les magasins</li>
        <li>Valider automatiquement les <strong>règles métier</strong> (capacité, compatibilité, horaires)</li>
        <li>Gérer les <strong>flux de marchandises</strong> (PGC, NAL, BSA, FL, PF, SURG)</li>
        <li>Calculer les <strong>KPI de coût</strong> par unité de transport (UT)</li>
        <li>Assurer la conformité réglementaire (pauses chauffeur, livraisons frais de nuit)</li>
    </ul>
    """)

    card("📂 Fichier source", """
    <p>L'application lit ses données depuis le fichier Excel <code>Flux Hebdo Flotte 2027.xlsx</code>    situé dans le même dossier que l'application.</p>
    """)

# ══════════════════════════════════════════════════════════════
# PAGE — DÉMARRAGE RAPIDE
# ══════════════════════════════════════════════════════════════

elif page == "🚀 Démarrage rapide":
    st.markdown("## 🚀 Démarrage rapide")    
    alerte("⏱️ Suivez ces étapes dans l'ordre pour planifier votre première journée en moins de 5 minutes.", "info")

    step(1, "Vérifier le fichier Excel",         "Assurez-vous que Flux Hebdo Flotte 2027.xlsx est présent dans le dossier de l'application "         "et que tous les onglets requis sont renseignés.")

    step(2, "Sélectionner le jour de planification",
         "Dans l'interface principale, choisissez le jour (Lundi, Mardi, …) "
         "pour filtrer les tournées et créneaux correspondants.")

    step(3, "Vérifier les flux de marchandises",
         "Consultez l'onglet 'Gestion des flux' pour confirmer que chaque magasin "
         "a bien des flux assignés avec les bonnes marchandises et quantités (UT).")

    step(4, "Lancer la validation des tournées",
         "Cliquez sur 'Valider les tournées'. Le moteur vérifie automatiquement "         "R1 (capacité), R2 (compatibilité), R3/R4 (chargement), R6/R7 (pauses), "
         "R9 (frais de nuit), R10 (créneaux), R11 (emballages).")

    step(5, "Corriger les erreurs signalées",
         "Les violations apparaissent en rouge. Ajustez les horaires, "         "l'ordre des arrêts ou les affectations de flux selon les recommandations.")

    step(6, "Consulter les KPI",
         "Vérifiez le coût moyen par UT, le taux de flotte propre "         "et le taux de remplissage des remorques dans l'onglet KPI.")

    step(7, "Sauvegarder le plan",
         "Cliquez sur 'Sauvegarder le plan'. Les données sont écrites "         "dans l'onglet Plan du fichier Excel.")

    st.markdown("---")    
    alerte("✅ Le plan est prêt à être transmis aux équipes terrain.", "succes")

# ══════════════════════════════════════════════════════════════
# PAGE — GESTION DES FLUX
# ══════════════════════════════════════════════════════════════

elif page == "📦 Gestion des flux":
    st.markdown("## 📦 Gestion des flux de marchandises")

    card("Types de marchandises", """    <table class="styled-table">
        <thead>
            <tr>                <th>Code</th><th>Libellé</th><th>Contrainte principale</th>
            </tr>
        </thead>
        <tbody>            <tr><td><strong>PGC</strong></td><td>Produits Grande Consommation</td><td>Livraison de jour uniquement (06h–22h)</td></tr>            <tr><td><strong>NAL</strong></td><td>Non Alimentaire</td><td>Livraison de jour uniquement (06h–22h)</td></tr>
            <tr><td><strong>BSA</strong></td><td>Bazar / Saisonnier</td><td>Livraison de jour uniquement (06h–22h)</td></tr>
            <tr><td><strong>FL</strong></td><td>Frais Libre-service</td><td>Livraison de nuit obligatoire (22h–06h)</td></tr>            <tr><td><strong>PF</strong></td><td>Produits Frais</td><td>Livraison de nuit obligatoire (22h–06h)</td></tr>
            <tr><td><strong>SURG</strong></td><td>Surgelés</td><td>Compartiment dédié — incompatible avec tout</td></tr>
        </tbody>
    </table>    """)

    st.markdown("---")

    card("Matrice de compatibilité des marchandises (R2)", """
    <table class="styled-table">        <thead>
            <tr><th></th><th>PGC</th><th>NAL</th><th>BSA</th><th>FL</th><th>PF</th><th>SURG</th></tr>        </thead>
        <tbody>
            <tr><td><strong>PGC</strong></td><td>✅</td><td>✅</td><td>✅</td><td>🚫</td><td>🚫</td><td>🚫</td></tr>
            <tr><td><strong>NAL</strong></td><td>✅</td><td>✅</td><td>✅</td><td>🚫</td><td>🚫</td><td>🚫</td></tr>
            <tr><td><strong>BSA</strong></td><td>✅</td><td>✅</td><td>✅</td><td>🚫</td><td>🚫</td><td>🚫</td></tr>
            <tr><td><strong>FL</strong></td><td>🚫</td><td>🚫</td><td>🚫</td><td>✅</td><td>✅</td><td>🚫</td></tr>            <tr><td><strong>PF</strong></td><td>🚫</td><td>🚫</td><td>🚫</td><td>✅</td><td>✅</td><td>🚫</td></tr>
            <tr><td><strong>SURG</strong></td><td>🚫</td><td>🚫</td><td>🚫</td><td>🚫</td><td>🚫</td><td>✅</td></tr>        </tbody>
    </table>
    """)

    st.markdown("---")

    card("Calcul du temps de déchargement (UT → minutes)", """
    <table class="styled-table">
        <thead><tr><th>Quantité (UT)</th><th>Temps alloué</th></tr></thead>
        <tbody>
            <tr><td>1 – 9 UT</td><td>15 minutes</td></tr>
            <tr><td>10 – 18 UT</td><td>30 minutes</td></tr>
            <tr><td>19 – 33 UT</td><td>45 minutes</td></tr>
        </tbody>
    </table>
    """)

# ══════════════════════════════════════════════════════════════
# PAGE — PLANIFICATION DES TOURNÉES
# ══════════════════════════════════════════════════════════════
elif page == "🗺️ Planification des tournées":    
    st.markdown("## 🗺️ Planification des tournées")

    card("Structure d'une tournée", """    <p>Chaque tournée est définie par les attributs suivants :</p>    <table class="styled-table">        <thead><tr><th>Attribut</th><th>Description</th></tr></thead>        <tbody>
            <tr><td><code>id</code></td><td>Identifiant unique de la tournée</td></tr>            <tr><td><code>capacite</code></td><td>Capacité max de la remorque (défaut : 33 UT)</td></tr>
            <tr><td><code>retour</code></td><td>Lieu de retour (défaut : ENTREPOT)</td></tr>
            <tr><td><code>adminMin</code></td><td>Temps administratif en minutes</td></tr>
            <tr><td><code>chgtMin</code></td><td>Temps de chargement en minutes</td></tr>            <tr><td><code>repriseEmballage</code></td><td>Oui / Non</td></tr>            <tr><td><code>zone</code></td><td>Zone géographique</td></tr>
            <tr><td><code>jour</code></td><td>Jour d'exécution</td></tr>
        </tbody>
    </table>
    """)

    st.markdown("---")

    card("Calcul automatique des pauses (R6 / R7)", """
    <p>Le moteur insère automatiquement les pauses légales :</p>
    <table class="styled-table">        <thead><tr><th>Règle</th><th>Déclencheur</th><th>Durée insérée</th></tr></thead>
        <tbody>            <tr><td><span class="badge-regle">R6</span></td>                <td>Après 4h30 de conduite continue (270 min)</td>
                <td>45 min (ou 30 min si pause service déjà effectuée)</td></tr>
            <tr><td><span class="badge-regle">R7</span></td>
                <td>Après 6h de service continu (360 min)</td>
                <td>30 min</td></tr>
        </tbody>
    </table>    <p style="margin-top:12px;font-size:0.88rem;color:#666">    ⚠️ Ces pauses sont injectées automatiquement dans le planning — elles allongent l'heure de retour à l'entrepôt.    </p>
    """)

    st.markdown("---")

    card("Contrainte de chevauchement magasin", """
    <p>Un magasin ne peut recevoir <strong>qu'une seule livraison à la fois</strong>.    Le moteur détecte automatiquement les chevauchements entre tournées sur la même plage horaire    et génère une alerte <code>R_OVERLAP</code>.</p>
    """)

# ══════════════════════════════════════════════════════════════
# PAGE — RÈGLES MÉTIER
# ══════════════════════════════════════════════════════════════
elif page == "⚖️ Règles métier":
    st.markdown("## ⚖️ Règles métier")

    regles = [
        ("R1", "Capacité remorque",         "Le total des UT chargées ne doit pas dépasser la capacité de la remorque (max 33 UT par défaut).",         "ERREUR"),        ("R2", "Compatibilité marchandises",
         "Les marchandises incompatibles (ex: FL et PGC) ne peuvent pas être chargées ensemble.",
         "ERREUR"),
        ("R3", "Chargement PGC/NAL/BSA de jour",
         "Les marchandises PGC, NAL et BSA ne peuvent être chargées qu'entre 06h00 et 22h00.",         "ERREUR"),        ("R4", "Chargement frais",         "Les produits frais (FL, PF) peuvent être chargés à tout moment.",
         "INFO"),
        ("R6", "Pause conduite",
         "Après 4h30 de conduite continue, une pause de 45 min (ou 30 min) est obligatoire.",
         "AVERTISSEMENT"),
        ("R7", "Pause service",         "Après 6h de service continu, une pause de 30 min est obligatoire.",
         "AVERTISSEMENT"),
        ("R9", "Livraison frais de nuit",
         "Les produits FL et PF doivent impérativement être livrés entre 22h00 et 06h00.",
         "ERREUR"),
        ("R10", "Créneaux d'ouverture magasin",
         "La livraison doit arriver dans les créneaux d'ouverture déclarés du magasin.",
         "ERREUR"),
        ("R11", "Reprise des emballages",
         "Chaque magasin actif doit recevoir au moins un passage de flotte propre par jour pour la reprise des emballages.",
         "AVERTISSEMENT"),
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

    card("KPI disponibles", """
    <table class="styled-table">        <thead><tr><th>Indicateur</th><th>Description</th><th>Source</th></tr></thead>        <tbody>
            <tr><td>Coût total</td><td>Somme des coûts flotte propre + affrètements</td><td>Couts_Modules + Affretements</td></tr>
            <tr><td>Coût moyen / UT</td><td>Coût total divisé par le nombre d'UT livrées</td><td>Calculé</td></tr>
            <tr><td>Taux flotte propre</td><td>% d'UT livrées par la flotte Auchan</td><td>Calculé</td></tr>
            <tr><td>Taux de remplissage</td><td>UT chargées / capacité remorque × 100</td><td>R1</td></tr>
            <tr><td>Nb violations R9</td><td>Livraisons frais planifiées de jour</td><td>Moteur R9</td></tr>            <tr><td>Nb violations R10</td><td>Livraisons hors créneaux magasin</td><td>Moteur R10</td></tr>
        </tbody>
    </table>
    """)

    st.markdown("---")

    card("Formule du coût module", """
    <p>Le coût d'un module (tournée flotte propre) est calculé comme suit :</p>
    <pre style="background:#FFF5F5;padding:12px;border-radius:6px;border-left:4px solid #D6180B">Coût = Coût fixe     + (Coût / km  × km total)
     + (Coût / heure × durée totale en heures)
    </pre>
    """)

# ══════════════════════════════════════════════════════════════
# PAGE — SAUVEGARDE & EXPORT
# ══════════════════════════════════════════════════════════════

elif page == "💾 Sauvegarde & Export":
    st.markdown("## 💾 Sauvegarde & Export")

    card("Sauvegarder le plan", """    <p>La fonction <code>sauvegarderPlan(donnees)</code> écrit les données planifiées    dans l'onglet <strong>Plan</strong> du fichier <code>Flux Hebdo Flotte 2027.xlsx</code>.</p>
    <p>⚠️ Cette opération <strong>écrase</strong> le contenu précédent de l'onglet Plan.</p>
    """)

    step(1, "Valider toutes les tournées",         "Assurez-vous qu'il n'y a aucune erreur R1–R11 avant de sauvegarder.")    
    step(2, "Cliquer sur 'Sauvegarder le plan'",
         "Le moteur écrit les données dans l'onglet Plan du fichier Excel.")
    step(3, "Vérifier le fichier Excel",
         "Ouvrez Flux Hebdo Flotte 2027.xlsx et consultez l'onglet Plan pour confirmer la sauvegarde.")
    step(4, "Exporter si besoin",
         "Depuis Excel, exportez en PDF ou partagez le fichier avec les équipes terrain.")

    st.markdown("---")    
    alerte(        "💡 <strong>Conseil :</strong> Faites une copie de sauvegarde du fichier Excel "        "avant toute modification importante.",
        "info"
    )

# ══════════════════════════════════════════════════════════════
# PAGE — FAQ
# ══════════════════════════════════════════════════════════════
elif page == "❓ FAQ":
    st.markdown("## ❓ Questions fréquentes")

    faqs = [
        ("Le fichier Excel n'est pas trouvé",         "Vérifiez que <code>Flux Hebdo Flotte 2027.xlsx</code> est dans le même dossier que l'application. "         "Le chemin est défini par la constante <code>FILE_EXCEL</code> dans <code>code.js</code>."),
        ("Une tournée affiche une erreur R2 (incompatibilité)",         "Vérifiez que les marchandises affectées à la même tournée sont compatibles. "
         "FL/PF ne peuvent pas être mélangées avec PGC/NAL/BSA/SURG."),
        ("Les pauses R6/R7 allongent trop la tournée",
         "Réduisez le nombre d'arrêts ou découpez la tournée en deux. "
         "Les pauses sont obligatoires et ne peuvent pas être supprimées."),
        ("L'erreur R9 apparaît sur une livraison FL",         "Les produits FL et PF doivent arriver au magasin entre 22h00 et 06h00. "
         "Avancez l'heure de départ de la tournée ou réorganisez l'ordre des arrêts."),        ("Comment ajouter un nouveau magasin ?",
         "Ajoutez le magasin dans les onglets <code>Lieux</code>, <code>PlagesOuverture</code> "         "et <code>Distancier</code> (toutes les distances depuis/vers ce magasin)."),
        ("Le diagnostic complet ne retourne rien",
         "Exécutez <code>diagnosticComplet()</code> depuis Node.js. "
         "Il liste tous les onglets détectés et le nombre de lignes de données par onglet."),
        ("Comment modifier les couleurs de l'interface ?",
         "Modifiez les valeurs hexadécimales dans le bloc <code>&lt;style&gt;</code> du fichier HTML. "
         "Le thème rouge Auchan utilise <code>#D6180B</code> (rouge principal) et <code>#7F0000</code> (rouge foncé)."),
    ]

    for question, reponse in faqs:        
        with st.expander(f"❓ {question}"):            
            st.markdown(reponse, unsafe_allow_html=True)

# ══════════════════════════════════════════════════════════════
# PIED DE PAGE
# ══════════════════════════════════════════════════════════════
st.markdown("""
<div class="footer">
    Auchan Transport — Outil de Planification Flux Hebdo Flotte 2027 &nbsp;|&nbsp;    Région Nord &nbsp;|&nbsp;    Support : transport@auchan.fr</div>
""", unsafe_allow_html=True)

