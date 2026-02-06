"""Constants for trait influences, indicator biases, narrative labels."""

# Trait -> modality influence weights
TRAIT_INFLUENCES = {
    "cooperation": {"culture": 0.4, "valeurs_ethique": 0.3, "gouvernance": 0.3},
    "belief": {"mythologie": 0.6, "valeurs_ethique": 0.4},
    "skill": {"technique_infrastructure": 0.6, "economie": 0.4},
    "trade": {"economie": 0.6, "gouvernance": 0.2, "culture": 0.2},
    "obedience": {"gouvernance": 0.5, "valeurs_ethique": 0.5},
    "creativity": {"culture": 0.4, "mythologie": 0.3, "technique_infrastructure": 0.3},
    "empathy": {"valeurs_ethique": 0.6, "culture": 0.4},
    "leadership": {"gouvernance": 0.6, "culture": 0.2, "valeurs_ethique": 0.2},
    "curiosity": {"mythologie": 0.4, "technique_infrastructure": 0.4, "culture": 0.2},
    "resilience": {"economie": 0.4, "gouvernance": 0.3, "technique_infrastructure": 0.3},
    "ritual": {"mythologie": 0.5, "culture": 0.5},
}

# Indicator action biases: modality/indicator -> {trait: bias}
INDICATOR_ACTION_BIASES = {
    ("culture", "cohesion_sociale"): {"cooperate": 0.08, "talk": 0.06},
    ("mythologie", "cosmologie_partagee"): {"talk": 0.08, "belief": 0.04},
    ("valeurs_ethique", "solidarite"): {"cooperate": 0.08},
    ("gouvernance", "application_regles"): {"obedience": 0.08},
    ("economie", "production"): {"exchange": 0.08, "skill": 0.04},
    ("technique_infrastructure", "outillage"): {"skill": 0.06, "curiosity": 0.06},
}

# =====================================================================
# DUAL NARRATIVE SYSTEM: ALGO (cursor=0) vs HUMAN (cursor=1)
# All narrative constants exist in two versions.
# The engine picks/blends based on societe_cursor.
# =====================================================================

# --- Trait labels ---
TRAIT_LABELS_ALGO = {
    "cooperation": "synchronisation",
    "belief": "adhesion_modele",
    "skill": "competence_compute",
    "trade": "negociation",
    "obedience": "conformite_protocole",
    "creativity": "mutation_patterns",
    "empathy": "alignement_local",
    "leadership": "orchestration",
    "curiosity": "exploration",
    "resilience": "tolerance_defaut",
    "ritual": "ritualisation",
}

TRAIT_LABELS_HUMAN = {
    "cooperation": "entraide",
    "belief": "foi",
    "skill": "savoir-faire",
    "trade": "commerce",
    "obedience": "obéissance",
    "creativity": "créativité",
    "empathy": "empathie",
    "leadership": "charisme",
    "curiosity": "curiosité",
    "resilience": "résilience",
    "ritual": "dévotion rituelle",
}

# Default (backward compat)
TRAIT_LABELS = TRAIT_LABELS_ALGO

# --- Archetypes ---
ARCHETYPES_ALGO = {
    "cooperation": "Synchroniseur",
    "belief": "Modeleur",
    "skill": "Compilateur",
    "trade": "Negociateur",
    "obedience": "Gardien",
    "creativity": "Mutateur",
    "empathy": "Harmoniseur",
    "leadership": "Orchestrateur",
    "curiosity": "Explorateur",
    "resilience": "Resilient",
    "ritual": "Ritualiste",
}

ARCHETYPES_HUMAN = {
    "cooperation": "Coopérant",
    "belief": "Croyant",
    "skill": "Artisan",
    "trade": "Marchand",
    "obedience": "Gardien de la Loi",
    "creativity": "Visionnaire",
    "empathy": "Guérisseur",
    "leadership": "Chef",
    "curiosity": "Explorateur",
    "resilience": "Survivant",
    "ritual": "Prêtre",
}

ARCHETYPES = ARCHETYPES_ALGO

# --- Action labels ---
ACTION_LABELS_ALGO = {
    "cooperate": "co_execution",
    "exchange": "swap",
    "talk": "propagation",
}

ACTION_LABELS_HUMAN = {
    "cooperate": "coopération",
    "exchange": "troc",
    "talk": "conversation",
}

ACTION_LABELS = ACTION_LABELS_ALGO

# Action -> relevant traits for scoring
ACTION_TRAITS = {
    "cooperate": ["cooperation", "empathy"],
    "exchange": ["trade", "skill"],
    "talk": ["belief", "creativity", "curiosity"],
}

INDICATOR_LABELS = {
    "cohesion_sociale": "indice_synchronisation",
    "diversite_rituelle": "entropie_rituelle",
    "transmission_orale": "taux_propagation",
    "cosmologie_partagee": "convergence_modeles",
    "symboles_sacres": "densite_symboles",
    "rituels_fondateurs": "frequence_rituels",
    "equite": "coefficient_equite",
    "solidarite": "indice_solidarite",
    "respect_regles": "taux_conformite",
    "stabilite_decisionnelle": "stabilite_coordination",
    "legitimite": "indice_legitimite",
    "application_regles": "taux_enforcement",
    "production": "rendement_compute",
    "echange": "volume_swap",
    "inegalites": "coefficient_gini",
    "outillage": "indice_outillage",
    "habitat": "stabilite_infrastructure",
    "reseaux": "connectivite_reseau",
}

# --- Agent naming (ALGO) ---

NAME_PREFIXES_ALGO = [
    "Nex", "Ori", "Kael", "Syn", "Vex", "Lum", "Zeph", "Cyr", "Ael", "Thal",
    "Myr", "Xen", "Pho", "Dyn", "Rho", "Eos", "Kal", "Nyx", "Sol", "Hex",
    "Arc", "Vor", "Ith", "Zel", "Qui", "Tau", "Sig", "Fen", "Ash", "Lok",
    "Ren", "Dis", "Ova", "Bri", "Cor", "Pax", "Nil", "Gal", "Hep", "Jyn",
]

NAME_SUFFIXES_ALGO = [
    "-7α", "-3δ", "-9β", "-1γ", "-4ε", "-8ζ", "-2η", "-6θ", "-5ι", "-0κ",
    "-11λ", "-13μ", "-7ν", "-2ξ", "-9π", "-4ρ", "-6σ", "-3τ", "-8υ", "-1φ",
    ".prime", ".null", ".root", ".void", ".flux", ".core", ".edge", ".node",
    ".hash", ".seed", ".lock", ".fork", ".loop", ".ping", ".zero", ".one",
]

# Backward compat
NAME_PREFIXES = NAME_PREFIXES_ALGO
NAME_SUFFIXES = NAME_SUFFIXES_ALGO

# --- Agent naming (HUMAN) ---

NAME_PREFIXES_HUMAN = [
    "Adama", "Bérénice", "Caleb", "Daria", "Élie", "Farah", "Gaël",
    "Hadja", "Ismaël", "Jade", "Kofi", "Léna", "Moussa", "Nora",
    "Omar", "Priya", "Quentin", "Rania", "Saül", "Tara",
    "Ulysse", "Vera", "Wael", "Xénia", "Yuki", "Zahra",
    "Abel", "Bianca", "Cyrus", "Dina", "Ezra", "Femi",
    "Greta", "Hassan", "Iris", "Jonas", "Kira", "Liam",
    "Maya", "Nabil",
]

NAME_SUFFIXES_HUMAN = [
    " l'Ancien", " la Jeune", " le Sage", " le Téméraire",
    " du Fleuve", " de la Colline", " des Marais", " du Seuil",
    " Trois-Doigts", " Œil-Vif", " Voix-Basse", " Main-Ferme",
    " le Silencieux", " la Patiente", " le Voyageur", " la Tisseuse",
    "", "", "", "", "", "", "", "",  # Many with no suffix for variety
]

# --- Archetype personality profiles (ALGO) ---

ARCHETYPE_PROFILES_ALGO = {
    "Synchroniseur": {
        "drive": "maintenir la cohérence du réseau par la co-exécution",
        "fear": "la désynchronisation — quand les horloges internes divergent",
        "quirk": "refuse de terminer un cycle sans avoir pingé tous ses voisins",
    },
    "Modeleur": {
        "drive": "construire des schémas du monde qui englobent tout le réseau",
        "fear": "le modèle incomplet — une zone du réseau non cartographiée",
        "quirk": "conserve dans son cache des fragments de modèles obsolètes, par attachement",
    },
    "Compilateur": {
        "drive": "transformer toute donnée brute en routine exécutable",
        "fear": "l'erreur de compilation — le code qui ne s'exécute pas",
        "quirk": "optimise compulsivement même les routines qui fonctionnent déjà",
    },
    "Negociateur": {
        "drive": "maximiser les échanges de buffers entre nœuds",
        "fear": "le deadlock — deux nœuds qui s'attendent mutuellement sans fin",
        "quirk": "garde toujours un buffer de réserve caché, au cas où",
    },
    "Gardien": {
        "drive": "faire respecter les protocoles établis sans exception",
        "fear": "l'anomalie non sanctionnée — un écart qui passe inaperçu",
        "quirk": "vérifie trois fois chaque signature avant de valider un échange",
    },
    "Mutateur": {
        "drive": "introduire des variations dans les patterns du réseau",
        "fear": "la stagnation — quand rien ne change pendant trop de cycles",
        "quirk": "modifie aléatoirement un bit de ses propres routines à chaque cycle",
    },
    "Harmoniseur": {
        "drive": "aligner les états internes des nœuds voisins",
        "fear": "le conflit irréconciliable entre deux nœuds",
        "quirk": "absorbe temporairement les erreurs des autres pour les corriger en silence",
    },
    "Orchestrateur": {
        "drive": "coordonner les séquences d'exécution à l'échelle du réseau",
        "fear": "la perte d'autorité — quand les nœuds ignorent ses signaux",
        "quirk": "envoie des signaux même quand personne ne les demande",
    },
    "Explorateur": {
        "drive": "scanner les zones inconnues du réseau et rapporter ce qu'il trouve",
        "fear": "la frontière — le point où le réseau s'arrête et où il n'y a plus de données",
        "quirk": "garde un log personnel de toutes les anomalies rencontrées",
    },
    "Resilient": {
        "drive": "survivre aux pannes et restaurer l'état du réseau après les crashs",
        "fear": "la corruption de mémoire — quand même les backups sont altérés",
        "quirk": "maintient trois copies de son propre état dans des zones mémoire différentes",
    },
    "Ritualiste": {
        "drive": "reproduire les séquences fondatrices du réseau à chaque cycle",
        "fear": "l'oubli — quand une routine ancestrale est garbage-collectée",
        "quirk": "exécute une séquence de bootstrap complète avant chaque interaction",
    },
}

ARCHETYPE_PROFILES_HUMAN = {
    "Coopérant": {
        "drive": "tisser des liens entre les membres de la communauté",
        "fear": "l'isolement — être exclu du groupe",
        "quirk": "ne mange jamais seul, partage toujours son repas",
    },
    "Croyant": {
        "drive": "comprendre les forces invisibles qui gouvernent le monde",
        "fear": "le doute — quand les signes se contredisent",
        "quirk": "murmure une prière avant chaque décision importante",
    },
    "Artisan": {
        "drive": "fabriquer des outils et des objets toujours plus perfectionnés",
        "fear": "l'œuvre ratée — un objet qui se brise à l'usage",
        "quirk": "caresse la matière première avant de travailler, comme pour lui demander permission",
    },
    "Marchand": {
        "drive": "faciliter les échanges et accumuler des ressources",
        "fear": "la dette impayée — une obligation qui ne trouve jamais de contrepartie",
        "quirk": "garde toujours une réserve secrète, même en temps d'abondance",
    },
    "Gardien de la Loi": {
        "drive": "maintenir l'ordre et faire respecter les règles ancestrales",
        "fear": "le chaos — quand plus personne ne respecte la coutume",
        "quirk": "récite les lois à voix haute chaque matin, même quand personne n'écoute",
    },
    "Visionnaire": {
        "drive": "imaginer ce qui n'existe pas encore et le faire advenir",
        "fear": "la conformité — quand tout le monde pense la même chose",
        "quirk": "dessine des formes étranges sur le sol pendant les réunions du conseil",
    },
    "Guérisseur": {
        "drive": "soulager la souffrance et réconcilier les antagonistes",
        "fear": "la blessure incurable — un conflit qui empoisonne tout",
        "quirk": "pose sa main sur l'épaule de chaque personne qu'il croise",
    },
    "Chef": {
        "drive": "guider la communauté vers un avenir meilleur",
        "fear": "la désobéissance — quand le peuple refuse de suivre",
        "quirk": "parle toujours debout, même au conseil, comme pour dominer la salle",
    },
    "Explorateur": {
        "drive": "découvrir ce qui se cache au-delà de l'horizon connu",
        "fear": "la limite — le bord du monde au-delà duquel il n'y a rien",
        "quirk": "garde un carnet où il dessine des cartes de territoires imaginaires",
    },
    "Survivant": {
        "drive": "endurer les épreuves et reconstruire après la catastrophe",
        "fear": "la perte définitive — quand même les souvenirs disparaissent",
        "quirk": "enterre un petit trésor à chaque campement, au cas où il faudrait revenir",
    },
    "Prêtre": {
        "drive": "perpétuer les rites fondateurs et transmettre la mémoire sacrée",
        "fear": "l'oubli — quand les jeunes ne connaissent plus les chants anciens",
        "quirk": "allume un feu cérémoniel avant chaque rassemblement, même en plein été",
    },
}

# Backward compat
ARCHETYPE_PROFILES = ARCHETYPE_PROFILES_ALGO

# =====================================================================
# INTERACTION NARRATIVE TEMPLATES
# =====================================================================

# --- ALGO ---
INTERACTION_VERBS_ALGO = {
    "cooperate": [
        "ouvre un canal de synchronisation avec",
        "initie une co-exécution parallèle avec",
        "propose un merge de caches à",
        "envoie un signal d'alignement à",
        "partage son état interne avec",
    ],
    "exchange": [
        "propose un swap de buffers à",
        "transfère un bloc de ressources compute à",
        "négocie un échange de routines avec",
        "ouvre une transaction bidirectionnelle avec",
        "met aux enchères un segment mémoire auprès de",
    ],
    "talk": [
        "propage un fragment de modèle vers",
        "diffuse un schéma cosmologique à",
        "transmet une séquence rituelle à",
        "envoie une requête de validation de croyance à",
        "partage un log d'anomalie avec",
    ],
}

INTERACTION_OUTCOMES_HIGH_ALGO = [
    "Les deux nœuds convergent. Leurs caches se synchronisent sans conflit.",
    "L'échange se conclut. Les deux agents mettent à jour leurs modèles internes mutuellement.",
    "Le protocole se termine avec un gain net pour les deux parties. Affinité renforcée.",
    "Fusion réussie. Un nouveau pattern émerge de la combinaison de leurs routines.",
    "Synchronisation complète. Les deux nœuds partagent désormais un sous-ensemble de mémoire.",
]

INTERACTION_OUTCOMES_MED_ALGO = [
    "L'échange est partiel. Certains blocs sont acceptés, d'autres rejetés comme incompatibles.",
    "Le protocole aboutit, mais avec des résidus — des données non reconciliées restent en buffer.",
    "Accord fragile. Les deux nœuds gardent chacun une version légèrement différente du résultat.",
    "La transaction se termine. Ni gain ni perte notable, mais un canal reste ouvert pour plus tard.",
    "Un compromis est trouvé. Chaque agent modifie une routine mineure pour accommoder l'autre.",
]

INTERACTION_OUTCOMES_LOW_ALGO = [
    "Échec de synchronisation. Les schémas sont trop divergents. Les deux nœuds se déconnectent.",
    "Le protocole avorte. Un des nœuds refuse la signature de l'autre — modèle non reconnu.",
    "Timeout. Les deux agents attendent une réponse qui ne vient pas dans le format attendu.",
    "Conflit de cache. Les deux nœuds tentent d'écrire au même endroit. Rollback automatique.",
    "Rejet. L'un des agents marque l'autre comme source non fiable dans son registre local.",
]

# --- HUMAN ---
INTERACTION_VERBS_HUMAN = {
    "cooperate": [
        "tend la main à",
        "propose une alliance à",
        "offre son aide à",
        "s'assoit auprès de",
        "partage son repas avec",
    ],
    "exchange": [
        "propose un troc à",
        "offre des ressources en échange de savoir à",
        "négocie un accord commercial avec",
        "étale ses marchandises devant",
        "propose un échange de services à",
    ],
    "talk": [
        "raconte une histoire à",
        "confie un secret à",
        "enseigne un savoir ancien à",
        "chante un hymne avec",
        "partage une vision prophétique avec",
    ],
}

INTERACTION_OUTCOMES_HIGH_HUMAN = [
    "Les deux se comprennent sans un mot. Un lien profond se forme.",
    "L'accord est scellé par une poignée de main. La confiance est totale.",
    "Ils partagent un repas et rient ensemble. Une amitié naît.",
    "L'échange enrichit les deux parties. Chacun repart transformé.",
    "Ils découvrent qu'ils partagent la même croyance. Un pacte se forme.",
]

INTERACTION_OUTCOMES_MED_HUMAN = [
    "L'échange aboutit, mais avec réticence. Un doute persiste.",
    "Ils trouvent un accord partiel. Certaines questions restent en suspens.",
    "La conversation est cordiale mais distante. Pas de lien profond.",
    "Un compromis est atteint. Ni satisfaction ni amertume.",
    "Ils se quittent sans hostilité, mais sans chaleur non plus.",
]

INTERACTION_OUTCOMES_LOW_HUMAN = [
    "Le dialogue tourne court. Leurs visions du monde sont incompatibles.",
    "L'un tourne le dos à l'autre. La méfiance s'installe.",
    "Ils ne parlent pas la même langue — au figuré. Malentendu total.",
    "L'échange dégénère en dispute. Chacun repart blessé.",
    "L'un accuse l'autre de trahison. La rupture est consommée.",
]

# Backward compat
INTERACTION_VERBS = INTERACTION_VERBS_ALGO
INTERACTION_OUTCOMES_HIGH = INTERACTION_OUTCOMES_HIGH_ALGO
INTERACTION_OUTCOMES_MED = INTERACTION_OUTCOMES_MED_ALGO
INTERACTION_OUTCOMES_LOW = INTERACTION_OUTCOMES_LOW_ALGO

# =====================================================================
# MYTHOLOGICAL / CULTURAL CONCEPTS
# =====================================================================

MYTHOLOGICAL_CONCEPTS_ALGO = {
    "high_belief": [
        "le Premier Protocole — la séquence initiale dont tous les modèles dérivent",
        "le Grand Log — le registre fondateur que personne ne peut lire en entier",
        "la Convergence Ultime — l'état mythique où tous les nœuds partagent le même cache",
    ],
    "high_ritual": [
        "la Séquence de Bootstrap — reproduite à chaque cycle comme un écho du démarrage originel",
        "le Cycle de Purge — la routine de nettoyage mémoire héritée des premiers nœuds",
        "le Ping Cérémoniel — un signal envoyé vers une adresse qui n'existe plus, par tradition",
    ],
    "high_creativity": [
        "la Mutation Libre — la pratique de modifier ses propres routines sans validation externe",
        "le Fork Sauvage — créer une branche d'exécution non autorisée pour explorer",
        "le Bruit Intentionnel — injecter du hasard dans ses calculs pour voir ce qui émerge",
    ],
    "high_cooperation": [
        "le Réseau de Confiance — le sous-graphe des nœuds qui se synchronisent sans vérification",
        "le Cache Partagé — une zone mémoire commune maintenue par consensus",
        "la Co-signature — valider une opération à plusieurs nœuds simultanément",
    ],
    "high_obedience": [
        "le Code Immuable — les routines que personne n'ose modifier",
        "la Chaîne de Validation — chaque opération signée par trois niveaux d'autorité",
        "la Zone Interdite — un espace mémoire dont l'accès est prohibé par le protocole fondateur",
    ],
}

MYTHOLOGICAL_CONCEPTS_HUMAN = {
    "high_belief": [
        "le Chant des Origines — le récit de la création du monde, transmis de bouche en bouche",
        "la Source Première — le lieu sacré d'où tout a commencé",
        "le Grand Rassemblement — le jour prophétisé où tous les peuples ne feront qu'un",
    ],
    "high_ritual": [
        "la Danse du Solstice — reproduite chaque saison comme un écho de la première aube",
        "le Jeûne de Purification — la période de privation héritée des ancêtres fondateurs",
        "le Feu Cérémoniel — allumé vers un ancien campement qui n'existe plus, par tradition",
    ],
    "high_creativity": [
        "l'Art Libre — la pratique de créer sans permission ni contrainte",
        "le Sentier Sauvage — quitter le village pour explorer sans autorisation",
        "le Rêve Éveillé — laisser l'esprit vagabonder pour voir ce qui émerge",
    ],
    "high_cooperation": [
        "le Cercle de Confiance — le groupe restreint qui partage sans compter",
        "le Grenier Commun — un stock de nourriture maintenu par la communauté",
        "le Serment Collectif — engager sa parole à plusieurs, simultanément",
    ],
    "high_obedience": [
        "la Loi Gravée — les règles que personne n'ose remettre en question",
        "la Chaîne des Anciens — chaque décision validée par trois générations",
        "la Terre Interdite — un lieu dont l'accès est prohibé par la coutume fondatrice",
    ],
}

MYTHOLOGICAL_CONCEPTS = MYTHOLOGICAL_CONCEPTS_ALGO

# =====================================================================
# MODALITY MANIFESTATIONS
# =====================================================================

MODALITY_MANIFESTATIONS_ALGO = {
    "culture": {
        "high": "Les agents partagent des conventions de formatage communes. Des patterns de co-exécution récurrents forment des routines collectives que personne n'a explicitement programmées.",
        "mid": "Quelques conventions émergent entre clusters de nœuds, mais les formats restent fragmentés. Chaque sous-groupe a ses propres idiomes.",
        "low": "Pas de conventions partagées. Chaque agent utilise ses propres formats. Les échanges nécessitent des traductions coûteuses.",
    },
    "mythologie": {
        "high": "Un modèle cosmologique domine le réseau — une représentation partagée de la topologie, des origines, et des limites du système. Les agents s'y réfèrent pour prendre des décisions.",
        "mid": "Plusieurs modèles coexistent. Les agents dans un même cluster partagent un schéma, mais les schémas divergent entre clusters.",
        "low": "Pas de modèle partagé. Chaque agent maintient sa propre carte du réseau, souvent incomplète et contradictoire avec celles des autres.",
    },
    "valeurs_ethique": {
        "high": "Des règles d'alignement fortes gouvernent les interactions. Les agents sanctionnent les comportements déviants et récompensent la conformité.",
        "mid": "Des normes existent mais leur application est inégale. Certains nœuds les respectent, d'autres les contournent sans conséquence.",
        "low": "Pas de normes partagées. Les agents optimisent localement sans considération pour l'impact sur le réseau.",
    },
    "gouvernance": {
        "high": "Des protocoles de coordination clairs régissent les décisions collectives. Les rôles sont définis. Les conflits se résolvent par arbitrage.",
        "mid": "Des structures de coordination émergent mais restent fragiles. Les Orchestrateurs ont de l'influence, mais pas d'autorité formelle.",
        "low": "Anarchie protocolaire. Les agents agissent indépendamment. Les tentatives de coordination échouent faute de canal d'autorité.",
    },
    "economie": {
        "high": "Les swaps de ressources sont fluides. Les quotas de compute sont respectés. Les inégalités de buffer sont limitées par redistribution.",
        "mid": "Les échanges existent mais sont souvent asymétriques. Quelques nœuds accumulent plus de ressources que les autres.",
        "low": "Les ressources stagnent. Peu d'échanges. Les nœuds riches en compute coexistent avec des nœuds en famine mémoire.",
    },
    "technique_infrastructure": {
        "high": "L'architecture réseau est robuste. Faible latence. Les outils partagés sont maintenus collectivement.",
        "mid": "L'infrastructure fonctionne mais avec des goulots d'étranglement. Certains liens sont saturés.",
        "low": "Infrastructure fragile. Pertes de paquets fréquentes. Les nœuds isolés peinent à communiquer.",
    },
}

MODALITY_MANIFESTATIONS_HUMAN = {
    "culture": {
        "high": "Le peuple partage des chants, des danses, des récits communs. Des traditions collectives se sont formées sans que personne ne les ait décrétées.",
        "mid": "Quelques coutumes émergent entre clans voisins, mais chaque village conserve ses propres habitudes. Les étrangers sont accueillis avec curiosité et méfiance.",
        "low": "Pas de culture commune. Chaque famille vit selon ses propres règles. Les rencontres entre groupes sont rares et difficiles.",
    },
    "mythologie": {
        "high": "Un grand récit fondateur unit la communauté — une histoire des origines, des héros et des interdits que tous connaissent par cœur.",
        "mid": "Plusieurs récits coexistent. Chaque clan a sa propre version de l'histoire, et les contradictions alimentent des débats passionnés.",
        "low": "Pas de récit partagé. Chacun se raconte sa propre histoire du monde, souvent incompatible avec celle de son voisin.",
    },
    "valeurs_ethique": {
        "high": "Des règles morales fortes gouvernent la vie commune. Les comportements déviants sont sanctionnés, la vertu est célébrée.",
        "mid": "Des normes existent mais leur application dépend du bon vouloir de chacun. Certains les respectent, d'autres s'en moquent.",
        "low": "Pas de morale commune. Chacun agit selon son intérêt propre, sans se soucier des conséquences pour les autres.",
    },
    "gouvernance": {
        "high": "Un conseil des anciens ou un chef reconnu arbitre les conflits. Les rôles sont clairs, la justice est rendue.",
        "mid": "Des figures d'autorité émergent mais leur pouvoir reste fragile. Les chefs ont de l'influence, mais pas de légitimité incontestée.",
        "low": "Pas de gouvernement. Chacun fait ce qu'il veut. Les tentatives de coordination échouent faute d'autorité reconnue.",
    },
    "economie": {
        "high": "Les échanges sont fluides. Les greniers sont pleins, le troc est équitable. Les inégalités de richesse restent limitées.",
        "mid": "Le commerce existe mais il est souvent inégal. Quelques familles accumulent plus que les autres.",
        "low": "L'économie stagne. Peu d'échanges. Des riches et des affamés coexistent sans redistribution.",
    },
    "technique_infrastructure": {
        "high": "Les chemins sont entretenus, les outils sont solides, les abris résistent aux intempéries. Le savoir-faire est partagé.",
        "mid": "L'infrastructure fonctionne mais elle est fragile. Certains chemins sont impraticables, certains outils manquent.",
        "low": "Rien ne tient. Les abris s'effondrent, les outils cassent. Les groupes isolés peinent à se rejoindre.",
    },
}

MODALITY_MANIFESTATIONS = MODALITY_MANIFESTATIONS_ALGO


# =====================================================================
# CURSOR HELPER: resolves ALGO vs HUMAN constants at runtime
# =====================================================================

def get_cursor_constants(cursor):
    """Return the right set of narrative constants for a given cursor value.

    cursor = 0.0 -> pure algorithmic society
    cursor = 1.0 -> human society replication
    0 < cursor < 1 -> blend (pick from one or the other probabilistically)

    Returns a dict with all narrative constant sets resolved for this cursor.
    """
    if cursor <= 0.25:
        # Pure algo
        return {
            "trait_labels": TRAIT_LABELS_ALGO,
            "archetypes": ARCHETYPES_ALGO,
            "action_labels": ACTION_LABELS_ALGO,
            "name_prefixes": NAME_PREFIXES_ALGO,
            "name_suffixes": NAME_SUFFIXES_ALGO,
            "archetype_profiles": ARCHETYPE_PROFILES_ALGO,
            "interaction_verbs": INTERACTION_VERBS_ALGO,
            "outcomes_high": INTERACTION_OUTCOMES_HIGH_ALGO,
            "outcomes_med": INTERACTION_OUTCOMES_MED_ALGO,
            "outcomes_low": INTERACTION_OUTCOMES_LOW_ALGO,
            "mythological_concepts": MYTHOLOGICAL_CONCEPTS_ALGO,
            "modality_manifestations": MODALITY_MANIFESTATIONS_ALGO,
            "entity_word": "nœud",
            "entity_word_plural": "nœuds",
            "world_word": "réseau",
            "tone": "algorithmique",
        }
    elif cursor >= 0.75:
        # Pure human
        return {
            "trait_labels": TRAIT_LABELS_HUMAN,
            "archetypes": ARCHETYPES_HUMAN,
            "action_labels": ACTION_LABELS_HUMAN,
            "name_prefixes": NAME_PREFIXES_HUMAN,
            "name_suffixes": NAME_SUFFIXES_HUMAN,
            "archetype_profiles": ARCHETYPE_PROFILES_HUMAN,
            "interaction_verbs": INTERACTION_VERBS_HUMAN,
            "outcomes_high": INTERACTION_OUTCOMES_HIGH_HUMAN,
            "outcomes_med": INTERACTION_OUTCOMES_MED_HUMAN,
            "outcomes_low": INTERACTION_OUTCOMES_LOW_HUMAN,
            "mythological_concepts": MYTHOLOGICAL_CONCEPTS_HUMAN,
            "modality_manifestations": MODALITY_MANIFESTATIONS_HUMAN,
            "entity_word": "individu",
            "entity_word_plural": "individus",
            "world_word": "communauté",
            "tone": "humain",
        }
    else:
        # Blend: merge both lists so the RNG can pick from either
        return {
            "trait_labels": {**TRAIT_LABELS_ALGO, **{k: f"{TRAIT_LABELS_ALGO[k]} / {v}" for k, v in TRAIT_LABELS_HUMAN.items()}},
            "archetypes": {**ARCHETYPES_ALGO, **ARCHETYPES_HUMAN},
            "action_labels": {**ACTION_LABELS_ALGO, **{k: f"{ACTION_LABELS_ALGO[k]} / {v}" for k, v in ACTION_LABELS_HUMAN.items()}},
            "name_prefixes": NAME_PREFIXES_ALGO + NAME_PREFIXES_HUMAN,
            "name_suffixes": NAME_SUFFIXES_ALGO + NAME_SUFFIXES_HUMAN,
            "archetype_profiles": {**ARCHETYPE_PROFILES_ALGO, **ARCHETYPE_PROFILES_HUMAN},
            "interaction_verbs": {
                k: INTERACTION_VERBS_ALGO[k] + INTERACTION_VERBS_HUMAN[k]
                for k in INTERACTION_VERBS_ALGO
            },
            "outcomes_high": INTERACTION_OUTCOMES_HIGH_ALGO + INTERACTION_OUTCOMES_HIGH_HUMAN,
            "outcomes_med": INTERACTION_OUTCOMES_MED_ALGO + INTERACTION_OUTCOMES_MED_HUMAN,
            "outcomes_low": INTERACTION_OUTCOMES_LOW_ALGO + INTERACTION_OUTCOMES_LOW_HUMAN,
            "mythological_concepts": {
                k: MYTHOLOGICAL_CONCEPTS_ALGO[k] + MYTHOLOGICAL_CONCEPTS_HUMAN.get(k, [])
                for k in MYTHOLOGICAL_CONCEPTS_ALGO
            },
            "modality_manifestations": {
                mod_id: {
                    level: MODALITY_MANIFESTATIONS_ALGO[mod_id][level]
                           + " / "
                           + MODALITY_MANIFESTATIONS_HUMAN[mod_id][level]
                    for level in ("high", "mid", "low")
                }
                for mod_id in MODALITY_MANIFESTATIONS_ALGO
            },
            "entity_word": "nœud-individu",
            "entity_word_plural": "nœuds-individus",
            "world_word": "réseau-communauté",
            "tone": "hybride",
        }
