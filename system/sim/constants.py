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

# Narrative labels (civilisation style)
TRAIT_LABELS = {
    "cooperation": "coopération",
    "belief": "croyance",
    "skill": "savoir-faire",
    "trade": "négoce",
    "obedience": "obéissance",
    "creativity": "créativité",
    "empathy": "empathie",
    "leadership": "commandement",
    "curiosity": "curiosité",
    "resilience": "résilience",
    "ritual": "ritualité",
}

ARCHETYPES = {
    "cooperation": "Pacificateur",
    "belief": "Gardien des récits",
    "skill": "Artisan",
    "trade": "Marchand",
    "obedience": "Légaliste",
    "creativity": "Inventeur",
    "empathy": "Médiateur",
    "leadership": "Meneur",
    "curiosity": "Explorateur",
    "resilience": "Endurant",
    "ritual": "Ritualiste",
}

ACTION_LABELS = {
    "cooperate": "entraide",
    "exchange": "échange",
    "talk": "transmission",
}

# Action -> relevant traits for scoring
ACTION_TRAITS = {
    "cooperate": ["cooperation", "empathy"],
    "exchange": ["trade", "skill"],
    "talk": ["belief", "creativity", "curiosity"],
}

INDICATOR_LABELS = {
    "cohesion_sociale": "cohésion sociale",
    "diversite_rituelle": "diversité rituelle",
    "transmission_orale": "transmission orale",
    "cosmologie_partagee": "cosmologie partagée",
    "symboles_sacres": "symboles sacrés",
    "rituels_fondateurs": "rituels fondateurs",
    "equite": "équité",
    "solidarite": "solidarité",
    "respect_regles": "respect des règles",
    "stabilite_decisionnelle": "stabilité décisionnelle",
    "legitimite": "légitimité",
    "application_regles": "application des règles",
    "production": "production",
    "echange": "échange",
    "inegalites": "inégalités",
    "outillage": "outillage",
    "habitat": "habitat",
    "reseaux": "réseaux",
}
