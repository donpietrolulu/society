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
