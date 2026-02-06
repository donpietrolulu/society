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

# Narrative labels
TRAIT_LABELS = {
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

ARCHETYPES = {
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

ACTION_LABELS = {
    "cooperate": "co_execution",
    "exchange": "swap",
    "talk": "propagation",
}

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

# --- Agent naming ---

NAME_PREFIXES = [
    "Nex", "Ori", "Kael", "Syn", "Vex", "Lum", "Zeph", "Cyr", "Ael", "Thal",
    "Myr", "Xen", "Pho", "Dyn", "Rho", "Eos", "Kal", "Nyx", "Sol", "Hex",
    "Arc", "Vor", "Ith", "Zel", "Qui", "Tau", "Sig", "Fen", "Ash", "Lok",
    "Ren", "Dis", "Ova", "Bri", "Cor", "Pax", "Nil", "Gal", "Hep", "Jyn",
]

NAME_SUFFIXES = [
    "-7α", "-3δ", "-9β", "-1γ", "-4ε", "-8ζ", "-2η", "-6θ", "-5ι", "-0κ",
    "-11λ", "-13μ", "-7ν", "-2ξ", "-9π", "-4ρ", "-6σ", "-3τ", "-8υ", "-1φ",
    ".prime", ".null", ".root", ".void", ".flux", ".core", ".edge", ".node",
    ".hash", ".seed", ".lock", ".fork", ".loop", ".ping", ".zero", ".one",
]

# --- Archetype personality profiles ---

ARCHETYPE_PROFILES = {
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

# --- Interaction narrative templates ---

# What agents actually do/say during each action type
INTERACTION_VERBS = {
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

# Possible outcomes based on affinity
INTERACTION_OUTCOMES_HIGH = [
    "Les deux nœuds convergent. Leurs caches se synchronisent sans conflit.",
    "L'échange se conclut. Les deux agents mettent à jour leurs modèles internes mutuellement.",
    "Le protocole se termine avec un gain net pour les deux parties. Affinité renforcée.",
    "Fusion réussie. Un nouveau pattern émerge de la combinaison de leurs routines.",
    "Synchronisation complète. Les deux nœuds partagent désormais un sous-ensemble de mémoire.",
]

INTERACTION_OUTCOMES_MED = [
    "L'échange est partiel. Certains blocs sont acceptés, d'autres rejetés comme incompatibles.",
    "Le protocole aboutit, mais avec des résidus — des données non reconciliées restent en buffer.",
    "Accord fragile. Les deux nœuds gardent chacun une version légèrement différente du résultat.",
    "La transaction se termine. Ni gain ni perte notable, mais un canal reste ouvert pour plus tard.",
    "Un compromis est trouvé. Chaque agent modifie une routine mineure pour accommoder l'autre.",
]

INTERACTION_OUTCOMES_LOW = [
    "Échec de synchronisation. Les schémas sont trop divergents. Les deux nœuds se déconnectent.",
    "Le protocole avorte. Un des nœuds refuse la signature de l'autre — modèle non reconnu.",
    "Timeout. Les deux agents attendent une réponse qui ne vient pas dans le format attendu.",
    "Conflit de cache. Les deux nœuds tentent d'écrire au même endroit. Rollback automatique.",
    "Rejet. L'un des agents marque l'autre comme source non fiable dans son registre local.",
]

# --- Mythological/cultural concept generators ---

MYTHOLOGICAL_CONCEPTS = {
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

# What a given modality looks like concretely in the agent world
MODALITY_MANIFESTATIONS = {
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
