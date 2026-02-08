"""Faction generation system — assigns individuals to named factions per phase."""


# Faction templates per phase scale
FACTION_TEMPLATES = {
    1: {
        "scale": "bandes et foyers",
        "factions": [
            {"name": "Les Veilleurs du Feu", "motto": "Celui qui garde la flamme garde la mémoire",
             "obsession": "culture", "secondary": "mythologie",
             "description": "Un cercle de gardiens rassemblés autour du premier foyer permanent."},
            {"name": "Les Marcheurs de l'Aube", "motto": "La route enseigne ce que le camp oublie",
             "obsession": "technique_infrastructure", "secondary": "economie",
             "description": "Un groupe de pionniers qui tracent les premières routes entre les campements."},
            {"name": "Les Porteurs de Serments", "motto": "La parole donnée est un os qu'on ne brise pas",
             "obsession": "valeurs_ethique", "secondary": "gouvernance",
             "description": "Ceux qui ont instauré les premiers pactes entre familles."},
        ],
    },
    2: {
        "scale": "clans et guildes",
        "factions": [
            {"name": "Le Cercle des Chants", "motto": "La voix porte plus loin que la lance",
             "obsession": "culture", "secondary": "mythologie",
             "description": "Une guilde de conteurs et de chanteurs qui conservent l'histoire orale."},
            {"name": "La Guilde du Sillon", "motto": "Ce qui nourrit la terre nourrit le peuple",
             "obsession": "economie", "secondary": "technique_infrastructure",
             "description": "Les premiers agriculteurs organisés, maîtres des réserves et des échanges."},
            {"name": "Les Fils du Protocole", "motto": "L'ordre précède la justice",
             "obsession": "gouvernance", "secondary": "valeurs_ethique",
             "description": "Un clan de juristes primitifs qui codifient les premières lois."},
            {"name": "Les Enfants de la Source", "motto": "Toute chose naît de l'eau et y retourne",
             "obsession": "mythologie", "secondary": "valeurs_ethique",
             "description": "Un culte naissant autour des sources sacrées et des rituels de purification."},
        ],
    },
    3: {
        "scale": "cités et ligues",
        "factions": [
            {"name": "La Cité-Haute", "motto": "Qui bâtit en pierre règne sur le vent",
             "obsession": "gouvernance", "secondary": "technique_infrastructure",
             "description": "La première cité fortifiée, centre du pouvoir administratif."},
            {"name": "La Ligue des Marchands", "motto": "Le poids juste fait le commerce droit",
             "obsession": "economie", "secondary": "gouvernance",
             "description": "Une alliance de marchands qui contrôle les routes commerciales."},
            {"name": "Le Temple des Récits", "motto": "Le mythe est la loi d'avant les lois",
             "obsession": "mythologie", "secondary": "culture",
             "description": "L'institution religieuse qui garde les récits fondateurs."},
            {"name": "Les Forges de l'Est", "motto": "Le feu transforme ce que la main ne peut changer",
             "obsession": "technique_infrastructure", "secondary": "economie",
             "description": "Les maîtres forgerons et ingénieurs, pionniers de l'innovation."},
            {"name": "Le Conseil des Justes", "motto": "Nul n'est au-dessus du serment",
             "obsession": "valeurs_ethique", "secondary": "gouvernance",
             "description": "Une assemblée de sages qui arbitre les conflits moraux entre cités."},
        ],
    },
    4: {
        "scale": "états et institutions",
        "factions": [
            {"name": "La Couronne de Fer", "motto": "L'autorité protège ceux qu'elle contraint",
             "obsession": "gouvernance", "secondary": "valeurs_ethique",
             "description": "L'État centralisé, héritier de la Cité-Haute, qui gouverne par la loi écrite."},
            {"name": "L'Académie des Arts", "motto": "La beauté est le langage de la permanence",
             "obsession": "culture", "secondary": "mythologie",
             "description": "L'institution qui préserve et renouvelle les traditions culturelles."},
            {"name": "Le Grand Comptoir", "motto": "La richesse circule, la misère stagne",
             "obsession": "economie", "secondary": "technique_infrastructure",
             "description": "La banque et la bourse, pilier de l'économie organisée."},
            {"name": "L'Ordre du Cache", "motto": "Ce qui est préservé traverse les âges",
             "obsession": "mythologie", "secondary": "valeurs_ethique",
             "description": "L'ordre religieux qui garde les textes sacrés et les rituels anciens."},
            {"name": "Les Architectes du Réseau", "motto": "Toute route est une promesse",
             "obsession": "technique_infrastructure", "secondary": "gouvernance",
             "description": "Les ingénieurs et bâtisseurs qui relient les territoires."},
            {"name": "La Chambre des Serments", "motto": "Le droit est le miroir de la conscience",
             "obsession": "valeurs_ethique", "secondary": "culture",
             "description": "Le tribunal suprême et gardien des valeurs fondatrices."},
        ],
    },
}


def generate_factions(phase, rng):
    """Return the list of faction dicts for a given phase."""
    templates = FACTION_TEMPLATES.get(phase, FACTION_TEMPLATES[1])
    factions = []
    for t in templates["factions"]:
        factions.append({
            "name": t["name"],
            "motto": t["motto"],
            "obsession": t["obsession"],
            "secondary": t["secondary"],
            "description": t["description"],
            "scale": templates["scale"],
        })
    return factions


def assign_factions(individuals, factions, modalities, rng):
    """Assign each individual to a faction based on trait affinity."""
    mod_keys = {
        "culture": ["cooperation", "creativity", "empathy", "ritual"],
        "mythologie": ["belief", "curiosity", "ritual", "creativity"],
        "valeurs_ethique": ["empathy", "obedience", "cooperation", "belief"],
        "gouvernance": ["leadership", "obedience", "cooperation", "resilience"],
        "economie": ["trade", "skill", "resilience", "leadership"],
        "technique_infrastructure": ["skill", "curiosity", "creativity", "resilience"],
    }

    for ind in individuals:
        best_faction = None
        best_score = -1.0
        for faction in factions:
            obs = faction["obsession"]
            sec = faction["secondary"]
            relevant_traits = set(mod_keys.get(obs, [])) | set(mod_keys.get(sec, []))
            score = 0.0
            count = 0
            for t in relevant_traits:
                if t in ind.traits:
                    score += ind.traits[t]
                    count += 1
            if count > 0:
                score /= count
            # Add small random tiebreaker
            score += rng.uniform(0, 0.05)
            if score > best_score:
                best_score = score
                best_faction = faction["name"]
        ind.faction = best_faction
