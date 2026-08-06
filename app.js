/* ═══════════════════════════════════════════════════════════
   APP.JS — Assistant IA Auchan — GitHub Pages
   La clé API vient de config.js (généré par GitHub Actions)
═══════════════════════════════════════════════════════════ */

'use strict';

// ── Configuration (injectée depuis config.js via GitHub Actions) ──
const CFG = window.APP_CONFIG || {};

// ── État global ──
const state = {
  currentPage: 'accueil',
  chatMessages: [],        // { role, content }
  sourceCode: null,        // index.html chargé depuis GitHub
  sourceLoading: false,
};

// ══════════════════════════════════════════════════════════════
// NAVIGATION
// ══════════════════════════════════════════════════════════════

function navigateTo(pageId) {
  document.querySelectorAll('.page').forEach(p => p.classList.remove('active'));
  document.querySelectorAll('.nav-item').forEach(n => n.classList.remove('active'));

  const page = document.getElementById('page-' + pageId);
  const nav  = document.querySelector(`.nav-item[data-page="${pageId}"]`);

  if (page) page.classList.add('active');
  if (nav)  nav.classList.add('active');

  state.currentPage = pageId;

  // Rendu à la demande
  const renderer = pageRenderers[pageId];
  if (renderer && !page.dataset.rendered) {
    renderer(page);
    page.dataset.rendered = '1';
  }

  // Page assistant : chargement du code source
  if (pageId === 'assistant' && !state.sourceCode && !state.sourceLoading) {
    loadSourceCode();
  }

  // Fermer sidebar mobile
  document.getElementById('sidebar').classList.remove('open');
}

function toggleSidebar() {
  document.getElementById('sidebar').classList.toggle('open');
}

// ══════════════════════════════════════════════════════════════
// HELPERS HTML
// ══════════════════════════════════════════════════════════════

function card(titre, contenuHTML) {
  return `<div class="help-card"><h3>${titre}</h3>${contenuHTML}</div>`;
}

function step(num, titre, desc) {
  return `
  <div class="step-box">
    <div class="step-number">${num}</div>
    <div class="step-content"><h4>${titre}</h4><p>${desc}</p></div>
  </div>`;
}

function alerte(texte, type = 'info') {
  const classes = { erreur: 'alert-rouge', succes: 'alert-verte', info: 'alert-orange' };
  return `<div class="${classes[type] || 'alert-orange'}">${texte}</div>`;
}

function styledTable(headers, rows) {
  const ths = headers.map(h => `<th>${h}</th>`).join('');
  const trs = rows.map(r =>
    `<tr>${r.map(c => `<td>${c}</td>`).join('')}</tr>`
  ).join('');
  return `
  <table class="styled-table">
    <thead><tr>${ths}</tr></thead>
    <tbody>${trs}</tbody>
  </table>`;
}

// ══════════════════════════════════════════════════════════════
// RENDERERS DE PAGES
// ══════════════════════════════════════════════════════════════

const pageRenderers = {

  // ── ACCUEIL ──────────────────────────────────────────────
  accueil(el) {
    el.innerHTML = `
    <h2>Bienvenue dans l'Outil de Planification Transport Auchan</h2>
    <div class="kpi-grid">
      <div class="kpi-card"><div class="kpi-value">12</div><div class="kpi-label">Règles métier validées</div></div>
      <div class="kpi-card"><div class="kpi-value">6</div><div class="kpi-label">Types de marchandises</div></div>
      <div class="kpi-card"><div class="kpi-value">33 UT</div><div class="kpi-label">Capacité max remorque</div></div>
    </div>
    <hr />
    ${card('🎯 À quoi sert cet outil ?', `
      <p>L'outil de planification transport Auchan permet de :</p>
      <ul>
        <li>Créer et optimiser les <strong>tournées de livraison</strong> vers les magasins</li>
        <li>Visualiser les flux sur un <strong>Gantt interactif</strong> (vue Modules, Remorques, Magasins)</li>
        <li>Valider automatiquement les <strong>règles métier</strong> (R1–R12)</li>
        <li>Gérer les <strong>flux de marchandises</strong> (PGC, NAL, BSA, FL, PF, SURG)</li>
        <li>Planifier des <strong>navettisations</strong> via des entrepôts relay</li>
        <li>Calculer les <strong>KPI de coût</strong> selon le modèle trinôme A + B·km + C·h</li>
        <li>Exporter le plan en <strong>JSON</strong> ou en <strong>CSV</strong></li>
      </ul>
    `)}
    ${card('⚙️ Architecture technique', `
      <p>L'application fonctionne <strong>entièrement dans le navigateur</strong>, sans serveur :</p>
      <ul>
        <li>Les fichiers sont lus localement via l'API <code>FileReader</code></li>
        <li>La bibliothèque <strong>SheetJS</strong> (CDN) parse les fichiers Excel</li>
        <li>Toute la logique métier s'exécute en JavaScript côté client</li>
        <li>Les fichiers Distancier et Cartographie sont <strong>mémorisés dans le localStorage</strong></li>
      </ul>
    `)}`;
  },

  // ── FICHIERS D'ENTRÉE ─────────────────────────────────────
  fichiers(el) {
    el.innerHTML = `
    <h2>📂 Fichiers d'entrée</h2>
    ${alerte("⚠️ Les deux premiers fichiers sont <strong>obligatoires</strong>. La cartographie est fortement recommandée.", 'info')}
    <hr />
    ${card("1️⃣ Fichier Excel Flux (obligatoire)", `
      <p><strong>Bouton :</strong> <code>📂 Charger Excel</code></p>
      <p>Fichier <code>.xlsx</code> ou <code>.xls</code>. Onglet nommé <strong>Flux</strong> ou premier onglet.</p>
      ${styledTable(
        ['Index', 'Contenu attendu', 'Exemple'],
        [
          ['<code>[0]</code>', 'Zone Entrepôt', 'LESQUIN'],
          ['<code>[1]</code>', 'Entrepôt de départ', 'ENT IENA1'],
          ['<code>[2]</code>', 'Zone de Livraison', 'ZONE NORD'],
          ['<code>[3]</code>', 'Centre Commercial', 'CC Grand Littoral'],
          ['<code>[4]</code>', 'Lieu de livraison', 'Auchan Englos'],
          ['<code>[5]</code>', 'Type de marchandise', 'PGC'],
          ['<code>[6]</code>', 'Volume en UT', '18'],
          ['<code>[7]</code>', 'Jour de chargement', 'Lundi'],
        ]
      )}
    `)}
    ${card("2️⃣ Distancier REFLEX (obligatoire)", `
      <p><strong>Bouton :</strong> <code>📏 Distancier</code></p>
      ${styledTable(
        ['Index', 'Contenu attendu', 'Exemple'],
        [
          ['<code>[0]</code>', 'Lieu de départ', 'ENT IENA'],
          ['<code>[1]</code>', "Lieu d'arrivée", 'Auchan Englos'],
          ['<code>[2]</code>', 'Distance en km', '23'],
          ['<code>[3]</code>', 'Durée en minutes', '34'],
        ]
      )}
      <p style="margin-top:12px;font-size:0.88rem;color:#666">
        ℹ️ Mémorisé dans le <strong>localStorage</strong> après le premier chargement.<br>
        ℹ️ L'alias <strong>ENT IENA</strong> est dupliqué automatiquement en ENT IENA1 et ENT IENA2.
      </p>
    `)}
    ${card("3️⃣ Cartographie réception magasins (recommandé)", `
      <p><strong>Bouton :</strong> <code>📋 Cartographie</code> — fichier <code>.csv</code> délimité par <code>;</code></p>
      ${styledTable(
        ['Index', 'Contenu', 'Détail'],
        [
          ['<code>[0]</code>', 'Nom du magasin', 'Doit correspondre exactement aux noms Flux'],
          ['<code>[1]–[6]</code>', 'Créneaux SEC — Lun à Sam', 'Format : HH:MM - HH:MM ou Fermé'],
          ['<code>[7]–[12]</code>', 'Créneaux Frais (PF/FL) — Lun à Sam', 'Créneaux nocturnes acceptés'],
          ['<code>[13]–[18]</code>', 'Créneaux Surgelés — Lun à Sam', 'Idem'],
        ]
      )}
    `)}
    ${card("4️⃣ Fichier de session JSON (optionnel)", `
      <p><strong>Bouton :</strong> <code>📥 Importer</code></p>
      <p>Restaure intégralement l'état : flux assignés, modules, offsets, navettes, paramètres KPI.</p>
    `)}`;
  },

  // ── DÉMARRAGE RAPIDE ──────────────────────────────────────
  demarrage(el) {
    el.innerHTML = `
    <h2>🚀 Démarrage rapide</h2>
    ${alerte("⏱️ Suivez ces étapes dans l'ordre pour planifier votre première journée.", 'info')}
    ${step(1, 'Charger le fichier Excel Flux', 'Cliquez sur 📂 Charger Excel et sélectionnez votre fichier .xlsx.')}
    ${step(2, 'Charger le Distancier', 'Cliquez sur 📏 Distancier. Ce fichier est mémorisé pour les sessions suivantes.')}
    ${step(3, 'Charger la Cartographie', 'Cliquez sur 📋 Cartographie et sélectionnez le fichier CSV des créneaux d\'ouverture.')}
    ${step(4, 'Sélectionner le jour', 'Dans la barre d\'outils, choisissez le jour (Lundi, Mardi…).')}
    ${step(5, 'Créer les modules et tournées', 'Cliquez sur + Module puis + Tournée. Définissez l\'heure de départ et la capacité.')}
    ${step(6, 'Assigner les flux', 'Glissez les blocs de flux vers les barres de tournée dans le Gantt.')}
    ${step(7, 'Valider les règles métier', 'Cliquez sur 🔍 Valider → Tout valider. R1 à R12 sont vérifiées.')}
    ${step(8, 'Consulter les KPI', 'Consultez le coût par UT, le taux de remplissage et le % km à vide.')}
    ${step(9, 'Exporter le plan', 'Cliquez sur 💾 Exporter JSON ou 📋 CSV.')}
    <hr />
    ${alerte('✅ Le plan est prêt à être transmis aux équipes terrain.', 'succes')}`;
  },

  // ── GESTION DES FLUX ──────────────────────────────────────
  flux(el) {
    el.innerHTML = `
    <h2>📦 Gestion des flux de marchandises</h2>
    ${card('Types de marchandises', styledTable(
      ['Code', 'Libellé', 'Contrainte principale'],
      [
        ['<strong>PGC</strong>', 'Produits Grande Consommation', 'Chargement de jour uniquement (06h–22h) — incompatible avec FL, PF, SURG'],
        ['<strong>NAL</strong>', 'Non Alimentaire', 'Chargement de jour uniquement — incompatible avec FL, PF, SURG'],
        ['<strong>BSA</strong>', 'Boissons Sans Alcool', 'Chargement de jour uniquement — incompatible avec FL, PF, SURG'],
        ['<strong>FL</strong>', 'Fruits &amp; Légumes 🌙', 'Tracteur indissociable pendant le chargement — compatible avec PF uniquement'],
        ['<strong>PF</strong>', 'Produits Frais 🌙', 'Tracteur indissociable — compatible avec FL uniquement'],
        ['<strong>SURG</strong>', 'Surgelés', 'Tracteur indissociable — incompatible avec toutes les autres familles'],
      ]
    ))}
    <hr />
    ${card('Matrice de compatibilité (R2)', styledTable(
      ['', 'PGC', 'NAL', 'BSA', 'FL', 'PF', 'SURG'],
      [
        ['<strong>PGC</strong>',  '✅','✅','✅','🚫','🚫','🚫'],
        ['<strong>NAL</strong>',  '✅','✅','✅','🚫','🚫','🚫'],
        ['<strong>BSA</strong>',  '✅','✅','✅','🚫','🚫','🚫'],
        ['<strong>FL</strong>',   '🚫','🚫','🚫','✅','✅','🚫'],
        ['<strong>PF</strong>',   '🚫','🚫','🚫','✅','✅','🚫'],
        ['<strong>SURG</strong>', '🚫','🚫','🚫','🚫','🚫','✅'],
      ]
    ))}
    <hr />
    ${card('Calcul du temps de déchargement (UT → minutes)', styledTable(
      ['Quantité (UT)', 'Temps alloué'],
      [
        ['0 UT', '0 minute'],
        ['1 – 9 UT', '15 minutes'],
        ['10 – 18 UT', '30 minutes'],
        ['19 – 33 UT', '45 minutes'],
      ]
    ))}
    <hr />
    ${card('Navettisation', `
      <p>Permet de livrer un magasin via un <strong>entrepôt relay intermédiaire</strong>.</p>
      <p>Crée automatiquement :</p>
      <ul>
        <li>Une <strong>navette</strong> (entrepôt origine → relay) à assigner à T1</li>
        <li>Un <strong>flux dérivé</strong> (relay → magasin) à assigner à T2</li>
      </ul>
      <p>⚠️ T1 doit être planifiée et terminée avant le début du chargement de T2 (règle R_NAV).</p>
    `)}`;
  },

  // ── PLANIFICATION DES TOURNÉES ───────────────────────────
  tournees(el) {
    el.innerHTML = `
    <h2>🗺️ Planification des tournées</h2>
    ${card('Structure d\'un module', `
      <p>Un <strong>module</strong> représente un binôme chauffeur + tracteur.</p>
      ${styledTable(
        ['Attribut', 'Description'],
        [
          ['ID module', 'Identifiant automatique (M1, M2…). L\'atelier de construction est M0.'],
          ['Tournées', 'Liste ordonnée des tournées du module pour la journée'],
          ['Offset', 'Heure de début de chaque tournée (en minutes depuis minuit)'],
        ]
      )}
    `)}
    <hr />
    ${card('Structure d\'une tournée', styledTable(
      ['Attribut', 'Description', 'Valeur par défaut'],
      [
        ['ID tournée', 'Identifiant unique (ex. TL01)', 'Généré automatiquement'],
        ['Capacité', 'Capacité max de la remorque en UT', '33 UT'],
        ['Retour', 'Entrepôt de retour après la dernière livraison', 'Premier entrepôt connu'],
        ['Accrochage (admDur)', 'Temps d\'accrochage de la remorque en minutes', '15 min'],
        ['Chargement (chgtDur)', 'Durée du chargement à l\'entrepôt en minutes', '30 min'],
        ['Jour', 'Jour d\'exécution de la tournée', 'Jour actif sélectionné'],
      ]
    ))}
    <hr />
    ${card('Calcul automatique des pauses (R6 / R7)', styledTable(
      ['Règle', 'Déclencheur', 'Durée insérée', 'Impact'],
      [
        ['<span class="badge-regle">R6</span>', '4h30 de conduite continue (270 min)', '45 min (ou 30 min si pause service déjà effectuée)', 'Remet à zéro conduite ET service'],
        ['<span class="badge-regle">R7</span>', '6h de service continu (360 min)', '30 min', 'Remet à zéro le compteur service uniquement'],
      ]
    ))}
    <hr />
    ${card('Vues Gantt disponibles', styledTable(
      ['Vue', 'Description'],
      [
        ['⚡ <strong>Flux</strong>', 'Timeline des flux + Gantt de l\'atelier (M0). Zone de glisser-déposer.'],
        ['📦 <strong>Modules</strong>', 'Une ligne par module. Barres de tournées avec segments chargement, trajets, livraisons, pauses.'],
        ['🚛 <strong>Remorques</strong>', 'Planning des chargements. Détecte les chargements simultanés.'],
        ['🏪 <strong>Magasins</strong>', 'Vue par magasin avec créneaux d\'ouverture. Livraisons groupées par type.'],
      ]
    ))}`;
  },

  // ── RÈGLES MÉTIER ─────────────────────────────────────────
  regles(el) {
    const regles = [
      ['R1',    'Capacité remorque',         'Le total des UT chargées ne doit pas dépasser la capacité de la remorque (33 UT par défaut).', 'ERREUR'],
      ['R2',    'Compatibilité marchandises', 'SEC (PGC/NAL/BSA) est incompatible avec Frais (FL/PF) et Surgelés. SURG est incompatible avec tout le reste.', 'ERREUR'],
      ['R3',    'Chargement PGC/NAL/BSA de jour', 'Ces marchandises ne peuvent être chargées qu\'entre 06h00 et 22h00.', 'ERREUR'],
      ['R4',    'Temps de déchargement', 'Calculé automatiquement : 15 min (1–9 UT), 30 min (10–18 UT), 45 min (19–33 UT).', 'INFO'],
      ['R6',    'Pause conduite (4h30)', 'Après 4h30 de conduite continue, une pause de 45 min est obligatoire (réduite à 30 min si pause service déjà effectuée).', 'AVERTISSEMENT'],
      ['R7',    'Pause service (6h)', 'Après 6h de service continu, une pause de 30 min est obligatoire.', 'AVERTISSEMENT'],
      ['R8',    'Durée de shift', 'La durée totale d\'un shift ne doit pas dépasser 11h (jour) ou 10h (nuit).', 'ERREUR'],
      ['R9',    'Minimum 2 tournées par module', 'Chaque module doit comporter au moins 2 tournées dans la journée.', 'AVERTISSEMENT'],
      ['R10',   'Créneaux d\'ouverture magasin', 'La livraison doit arriver dans les créneaux d\'ouverture déclarés.', 'ERREUR'],
      ['R11',   'Reprise des emballages', 'Chaque magasin actif doit recevoir au moins un passage de flotte propre par jour.', 'AVERTISSEMENT'],
      ['R12',   'Pas de chevauchement tracteur', 'Deux tournées d\'un même module ne peuvent pas se chevaucher temporellement.', 'ERREUR'],
      ['R13',   'Le chauffeur revient bien à son point de départ', 'Le chauffeur doit revenir là où il a garé sa voiture à la fin de son shift', 'AVERTISSEMENT'],
      ['R_NAV', 'Chronologie navettisation', 'La navette T1 doit être planifiée et terminée avant le début du chargement du flux dérivé T2.', 'ERREUR'],
    ];

    const niveauClass = { ERREUR: 'erreur', AVERTISSEMENT: 'info', INFO: 'succes' };

    const items = regles.map(([code, titre, desc, niveau]) => `
      <details>
        <summary><strong>${code}</strong> — ${titre}</summary>
        <div class="details-body">
          ${alerte(`<strong>Niveau :</strong> ${niveau}`, niveauClass[niveau] || 'info')}
          <p>${desc}</p>
        </div>
      </details>
    `).join('');

    el.innerHTML = `<h2>⚖️ Règles métier</h2>${items}`;
  },

  // ── KPI ───────────────────────────────────────────────────
  kpi(el) {
    el.innerHTML = `
    <h2>📊 Indicateurs KPI</h2>
    <div class="help-card">
      <h3>Modèle de coût trinôme</h3>
      <pre>Coût = A
     + B_sec   × km_sec    + B_frais × km_frais
     + C_jour  × heures_jour
     + C_nuit  × heures_nuit</pre>
      ${styledTable(
        ['Paramètre', 'Description', 'Valeur par défaut'],
        [
          ['<strong>A</strong>', 'Coût fixe par module', '10 €'],
          ['<strong>B sec</strong>', 'Coût kilométrique SEC (PGC/NAL/BSA)', '0,45 €/km'],
          ['<strong>B frais</strong>', 'Coût kilométrique Frais/SURG (FL/PF/SURG)', '0,55 €/km'],
          ['<strong>C jour</strong>', 'Coût horaire shift de jour (06h–22h)', '35 €/h'],
          ['<strong>C nuit</strong>', 'Coût horaire shift de nuit (22h–06h)', '47 €/h'],
          ['<strong>CO₂/km</strong>', 'Émissions CO₂ par km (semi-remorque 35t)', '900 g/km'],
          ['<strong>Prix carbone</strong>', 'Coût de la tonne de CO₂', '50 €/t'],
        ]
      )}
      <p style="margin-top:12px;font-size:0.88rem;color:#666">ℹ️ Tous les paramètres sont modifiables dans le panneau KPI.</p>
    </div>
    <hr />
    ${card('Indicateurs calculés', styledTable(
      ['Indicateur', 'Description'],
      [
        ['Coût financier / UT', 'Coût total divisé par le nombre d\'UT livrées (hors navettes)'],
        ['Coût carbone / UT', 'Coût CO₂ (km × g/km → tonnes × prix/t) divisé par les UT livrées'],
        ['Taux de remplissage global', 'Moyenne pondérée par km : UT à bord × km / (capacité × km)'],
        ['Taux de remplissage au départ', 'UT chargées au départ / capacité remorque'],
        ['% km à vide', 'Kilomètres de retour à vide / total km × 100'],
      ]
    ))}`;
  },

  // ── SAUVEGARDE & EXPORT ───────────────────────────────────
  export(el) {
    el.innerHTML = `
    <h2>💾 Sauvegarde & Export</h2>
    ${card('Formats d\'export disponibles', styledTable(
      ['Format', 'Bouton', 'Contenu'],
      [
        ['<strong>JSON</strong>', '<code>💾 Exporter JSON</code>', 'Session complète : flux planifiés, modules, offsets, navettes, paramètres KPI. Réimportable.'],
        ['<strong>CSV</strong>', '<code>📋 CSV</code>', 'Planning des livraisons : Module, Tournée, Remorque, Magasin, Marchandise, UT, Heure estimée.'],
      ]
    ))}
    <hr />
    ${step(1, 'Valider toutes les tournées', 'Cliquez sur 🔍 Valider → Tout valider. Assurez-vous qu\'il n\'y a aucune erreur R1–R12.')}
    ${step(2, 'Exporter la session JSON', 'Cliquez sur 💾 Exporter JSON. Un fichier session_transport_[Jour]_[Date].json est téléchargé.')}
    ${step(3, 'Exporter le CSV si nécessaire', 'Cliquez sur 📋 CSV pour obtenir un tableau des livraisons planifiées.')}
    ${step(4, 'Réimporter une session', 'Cliquez sur 📥 Importer et sélectionnez un fichier .json précédemment exporté.')}
    <hr />
    ${card('Auto-sauvegarde', `
      <p>L'outil sauvegarde automatiquement dans le <strong>localStorage</strong> toutes les 60 secondes.</p>
      <p>Au démarrage, une bannière propose de <strong>Restaurer</strong> ou <strong>Ignorer</strong> la session précédente.</p>
      <p style="font-size:0.88rem;color:#666">⚠️ Utilisez l'export JSON pour transférer une session entre postes.</p>
    `)}`;
  },

  // ── FAQ ───────────────────────────────────────────────────
  faq(el) {
    const faqs = [
      ['Le fichier Excel ne se charge pas',
       'Vérifiez que le fichier est au format <code>.xlsx</code> ou <code>.xls</code> et que les colonnes sont dans l\'ordre attendu.'],
      ['Le distancier affiche "Distance introuvable"',
       'Le nom du lieu dans le fichier Flux doit correspondre <strong>exactement</strong> au nom dans le distancier (casse incluse).'],
      ['Une tournée affiche une erreur R2 (incompatibilité)',
       'FL et PF ne peuvent pas être mélangées avec PGC, NAL, BSA ou SURG. SURG doit toujours être seul.'],
      ['Les pauses R6/R7 allongent trop la tournée',
       'Réduisez le nombre d\'arrêts ou découpez la tournée en deux. Les pauses sont repositionnables par glisser-déposer.'],
      ['Comment gérer une livraison via un entrepôt intermédiaire ?',
       'Utilisez la fonction de <strong>navettisation</strong> : bouton ⇄ sur le flux concerné. Planifiez T1 avant T2 (règle R_NAV).'],
      ['Le Gantt Magasins n\'affiche pas les créneaux d\'ouverture',
       'Chargez le fichier Cartographie via 📋. Vérifiez que les noms de magasins correspondent exactement au fichier Flux.'],
      ['Comment modifier les paramètres KPI ?',
       'Dans le panneau de validation (🔍 Valider), modifiez A, B sec, B frais, C jour, C nuit, CO₂/km et Prix carbone, puis cliquez sur 🔄 Recalculer.'],
      ['La session n\'est pas restaurée au démarrage',
       'L\'auto-sauvegarde utilise le localStorage, perdu si vous videz le cache. Utilisez l\'export JSON pour transférer entre postes.'],
    ];

    const items = faqs.map(([q, r]) => `
      <details>
        <summary>❓ ${q}</summary>
        <div class="details-body"><p>${r}</p></div>
      </details>
    `).join('');

    el.innerHTML = `<h2>❓ Questions fréquentes</h2>${items}`;
  },

  // ── ASSISTANT IA ──────────────────────────────────────────
  assistant(el) {
    el.innerHTML = `
    <h2>🤖 Assistant IA — Outil de Planification Transport</h2>
    <p>Posez vos questions sur le code, les règles métier, les fichiers d'entrée, les vues Gantt, les KPI, etc.</p>

    <div id="source-status" class="alert-orange">
      ⏳ Chargement du code source depuis GitHub...
    </div>

    <hr />

    <div id="chat-container"></div>
    <div class="chat-status" id="chat-status"></div>

    <div id="chat-input-area">
      <input
        type="text"
        id="chat-input"
        placeholder="Posez votre question sur l'outil ou le code..."
        onkeydown="if(event.key==='Enter' && !event.shiftKey){ event.preventDefault(); sendChatMessage(); }"
      />
      <button class="btn-primary" onclick="sendChatMessage()">Envoyer ➤</button>
    </div>

    <div style="margin-top:16px">
      <button class="btn-danger" onclick="clearChat()">🗑️ Effacer la conversation</button>
    </div>`;

    // Restaurer l'historique existant
    renderChatHistory();
  },
};

// ══════════════════════════════════════════════════════════════
// CHARGEMENT DU CODE SOURCE DEPUIS GITHUB
// ══════════════════════════════════════════════════════════════

async function loadSourceCode() {
  state.sourceLoading = true;
  const statusEl = document.getElementById('source-status');

  try {
    const url = CFG.GITHUB_RAW_URL || 'https://raw.githubusercontent.com/aribert-ux/Output/main/index.html';
    const response = await fetch(url + '?t=' + Date.now()); // cache-busting

    if (!response.ok) throw new Error(`HTTP ${response.status}`);

    state.sourceCode = await response.text();
    const lines = state.sourceCode.split('\n').length;

    if (statusEl) {
      statusEl.className = 'alert-verte';
      statusEl.innerHTML = `✅ index.html chargé (${lines.toLocaleString('fr-FR')} lignes) — ${new Date().toLocaleTimeString('fr-FR')}
        <button class="btn-primary" style="margin-left:16px;padding:4px 12px;font-size:0.82rem" onclick="reloadSourceCode()">🔄 Recharger</button>`;
    }
  } catch (err) {
    if (statusEl) {
      statusEl.className = 'alert-rouge';
      statusEl.innerHTML = `❌ Erreur de chargement : ${err.message}
        <button class="btn-primary" style="margin-left:16px;padding:4px 12px;font-size:0.82rem" onclick="reloadSourceCode()">🔄 Réessayer</button>`;
    }
  } finally {
    state.sourceLoading = false;
  }
}

function reloadSourceCode() {
  state.sourceCode = null;
  loadSourceCode();
}

// ══════════════════════════════════════════════════════════════
// CHAT — RENDU
// ══════════════════════════════════════════════════════════════

function renderChatHistory() {
  const container = document.getElementById('chat-container');
  if (!container) return;

  container.innerHTML = state.chatMessages.map(msg => `
    <div class="chat-msg ${msg.role}">
      <div class="chat-avatar">${msg.role === 'user' ? '👤' : '🤖'}</div>
      <div class="chat-bubble">${escapeHtml(msg.content)}</div>
    </div>
  `).join('');

  container.scrollTop = container.scrollHeight;
}

function appendChatMessage(role, content) {
  state.chatMessages.push({ role, content });
  renderChatHistory();
}

function escapeHtml(str) {
  return str
    .replace(/&/g, '&amp;')
    .replace(/</g, '&lt;')
    .replace(/>/g, '&gt;')
    .replace(/"/g, '&quot;')
    .replace(/\n/g, '<br>');
}

// ══════════════════════════════════════════════════════════════
// CHAT — ENVOI
// ══════════════════════════════════════════════════════════════

async function sendChatMessage() {
  const input  = document.getElementById('chat-input');
  const status = document.getElementById('chat-status');
  const prompt = input.value.trim();

  if (!prompt) return;

  // Vérification de la configuration
  if (!CFG.LITELLM_API_KEY || !CFG.LITELLM_API_BASE) {
    appendChatMessage('assistant', '❌ Configuration manquante. Vérifiez les secrets GitHub (LITELLM_API_KEY, LITELLM_API_BASE).');
    return;
  }

  input.value = '';
  appendChatMessage('user', prompt);

  if (status) status.textContent = '⏳ L\'IA analyse votre question...';

  // Construction du system prompt
  const nbLignes = state.sourceCode ? state.sourceCode.split('\n').length : 0;
  const systemPrompt = [
    'Tu es un assistant expert de l\'outil de planification transport Auchan Région Nord.',
    state.sourceCode
      ? `Tu as accès au code source complet de l\'application (index.html, ${nbLignes} lignes).`
      : 'Le code source n\'a pas pu être chargé. Réponds sur la base de tes connaissances générales.',
    'Quand tu réponds :',
    '- Cite la section concernée si pertinent',
    '- Donne des exemples concrets tirés du code réel',
    '- Réponds en français, de façon concise et pratique',
    '- Si une question concerne une règle (R1 à R12), explique son implémentation',
    state.sourceCode ? `\nVoici le code source complet :\n\n${state.sourceCode}` : '',
  ].join('\n');

  // Construction des messages (historique complet)
  const messages = [
    { role: 'system', content: systemPrompt },
    ...state.chatMessages.slice(0, -1).map(m => ({ role: m.role, content: m.content })),
    { role: 'user', content: prompt },
  ];

  try {
    const response = await fetch(`${CFG.LITELLM_API_BASE}/v1/chat/completions`, {
      method: 'POST',
      headers: {
        'Content-Type':  'application/json',
        'Authorization': `Bearer ${CFG.LITELLM_API_KEY}`,
      },
      body: JSON.stringify({
        model:    CFG.LITELLM_MODEL || 'gpt-4o',
        messages: messages,
      }),
    });

    if (!response.ok) {
      const errText = await response.text();
      throw new Error(`HTTP ${response.status} — ${errText}`);
    }

    const data   = await response.json();
    const answer = data.choices?.[0]?.message?.content || '(réponse vide)';

    appendChatMessage('assistant', answer);
    if (status) status.textContent = '';

  } catch (err) {
    appendChatMessage('assistant', `❌ Erreur Gateway : ${err.message}`);
    if (status) status.textContent = '';
  }
}

function clearChat() {
  state.chatMessages = [];
  renderChatHistory();
}

// ══════════════════════════════════════════════════════════════
// LOGO SVG (optionnel)
// ══════════════════════════════════════════════════════════════

async function tryLoadLogo() {
  try {
    const r = await fetch('logo.svg');
    if (!r.ok) return;
    const svg = await r.text();
    const el  = document.getElementById('logo-container');
    if (el) el.innerHTML = `<div style="width:108px;height:27px;filter:brightness(0) invert(1)">${svg}</div>`;
  } catch (_) { /* logo optionnel */ }
}

// ══════════════════════════════════════════════════════════════
// INIT
// ══════════════════════════════════════════════════════════════

document.addEventListener('DOMContentLoaded', () => {

  // Attacher les événements de navigation
  document.querySelectorAll('.nav-item').forEach(item => {
    item.addEventListener('click', () => navigateTo(item.dataset.page));
  });

  // Rendu initial
  navigateTo('accueil');

  // Charger le logo si disponible
  tryLoadLogo();
});
