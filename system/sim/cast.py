"""Cast system — selects and generates focus characters per phase."""


# Role templates by modality combination
ROLE_POOL = [
    {"role": "Faiseur de serments", "mods": ["valeurs_ethique", "gouvernance"],
     "voice": "proverbes", "desc": "Celui qui scelle les pactes entre familles et clans, d'un geste de la main et d'un mot irrévocable."},
    {"role": "Cartographe des limites", "mods": ["technique_infrastructure", "gouvernance"],
     "voice": "précision froide", "desc": "Elle trace les frontières, mesure les terres et tranche les disputes de voisinage d'un trait de craie."},
    {"role": "Gardienne des chants interdits", "mods": ["culture", "mythologie"],
     "voice": "fragments poétiques", "desc": "Dépositaire des mélodies que l'on ne chante qu'aux morts et aux nouveau-nés."},
    {"role": "Médiatrice des dettes", "mods": ["economie", "valeurs_ethique"],
     "voice": "questions rhétoriques", "desc": "Elle connaît chaque promesse non tenue, chaque grain de blé prêté, et rappelle les comptes à ceux qui oublient."},
    {"role": "Architecte des routes", "mods": ["technique_infrastructure", "economie"],
     "voice": "phrases courtes", "desc": "Il conçoit les chemins qui relient les villages et décide par où passeront les marchandises."},
    {"role": "Briseur de sceaux", "mods": ["mythologie", "gouvernance"],
     "voice": "ton solennel", "desc": "Seul habilité à ouvrir les coffres sacrés où reposent les décrets anciens."},
    {"role": "Tisseuse de pactes", "mods": ["culture", "valeurs_ethique"],
     "voice": "métaphores textiles", "desc": "Elle tisse littéralement les cordages noués qui symbolisent les alliances entre familles."},
    {"role": "Forgeron des seuils", "mods": ["technique_infrastructure", "culture"],
     "voice": "maximes d'atelier", "desc": "Il fabrique les portes, les serrures et les clés — celui qui décide ce qui s'ouvre et ce qui reste fermé."},
    {"role": "Compteur de saisons", "mods": ["mythologie", "economie"],
     "voice": "grandiloquent", "desc": "L'astrologue-comptable qui prédit les récoltes à partir des étoiles et des registres anciens."},
    {"role": "Porteur de griefs", "mods": ["valeurs_ethique", "culture"],
     "voice": "ironie froide", "desc": "Celui que l'on envoie déposer une plainte formelle, capable de transformer l'insulte en procédure."},
    {"role": "Maître des réserves", "mods": ["economie", "gouvernance"],
     "voice": "laconique", "desc": "Il contrôle les greniers et décide qui mange en cas de pénurie."},
    {"role": "Lectrice des failles", "mods": ["mythologie", "technique_infrastructure"],
     "voice": "murmures", "desc": "Elle interprète les signes dans la roche, les fissures des murs, et prédit les effondrements."},
    {"role": "Veilleur des frontières", "mods": ["gouvernance", "technique_infrastructure"],
     "voice": "ordres brefs", "desc": "Sentinelle permanente qui connaît chaque passage et chaque menace aux confins du territoire."},
    {"role": "Conteuse des origines", "mods": ["mythologie", "culture"],
     "voice": "récits enchâssés", "desc": "Celle qui raconte l'histoire de la fondation, et dont chaque version diffère subtilement."},
    {"role": "Arbitre des épreuves", "mods": ["gouvernance", "valeurs_ethique"],
     "voice": "formules juridiques", "desc": "Le juge qui soumet les accusés à des épreuves rituelles pour établir la vérité."},
    {"role": "Guérisseuse des liens", "mods": ["culture", "economie"],
     "voice": "proverbes marchands", "desc": "Elle répare les relations commerciales brisées par la ruse ou l'injustice."},
]

# Desires, fears, secrets, contradictions
DESIRES = [
    "être reconnue comme fondatrice d'une tradition nouvelle",
    "retrouver un texte ancien qui légitimerait son autorité",
    "unifier les factions rivales sous un seul pacte",
    "prouver que l'ancienne voie était la bonne",
    "transmettre son savoir avant qu'il ne soit trop tard",
    "obtenir justice pour un tort subi dans l'ombre",
    "conquérir le droit de parler au Conseil",
    "bâtir un monument qui survive aux générations",
    "mettre fin à une querelle de sang entre deux lignées",
    "découvrir la source véritable de la rivière sacrée",
    "faire abolir une loi qu'il juge injuste",
    "prouver qu'un rival a trahi le serment fondateur",
]

FEARS = [
    "être oubliée par ceux qu'elle a servis",
    "voir son savoir déformé par ses successeurs",
    "perdre le contrôle de ce qu'il a créé",
    "être jugée par les lois qu'elle a contribué à écrire",
    "que le secret qu'il garde soit découvert",
    "assister impuissant à l'effondrement de l'ordre qu'il défend",
    "être trahi par son plus proche allié",
    "que les mythes se vident de sens",
    "devenir ce qu'il a toujours combattu",
    "voir la prochaine génération rejeter tout héritage",
]

SECRETS = [
    "a falsifié un document fondateur pour protéger la paix",
    "entretient une correspondance secrète avec la faction rivale",
    "ne croit pas aux mythes qu'elle enseigne",
    "doit sa position à une dette jamais remboursée",
    "a un enfant élevé dans la faction adverse",
    "a volé une technique à un peuple voisin disparu",
    "connaît l'emplacement d'une réserve cachée que tous croient épuisée",
    "a provoqué l'exil d'un innocent pour couvrir un allié",
    "pratique en secret un rituel interdit par le Conseil",
    "possède la seule copie d'un traité que les dirigeants veulent détruire",
]

CONTRADICTIONS = [
    "prêche la coopération mais agit seul dans les moments décisifs",
    "défend la tradition tout en rêvant de la transformer",
    "exige la transparence des autres mais cache sa propre histoire",
    "protège les faibles mais méprise leur faiblesse",
    "veut la paix mais ne sait vivre qu'en temps de crise",
    "croit au mérite mais a tout hérité",
    "juge les autres sans accepter d'être jugée",
    "cherche la vérité mais craint ce qu'elle pourrait révéler",
    "respecte la loi mais contourne ses propres règles",
    "veut partir mais reste toujours",
]

VOICE_STYLES = {
    "proverbes": "ponctue chaque phrase d'un dicton ancien",
    "phrases courtes": "parle en phrases sèches, jamais plus de six mots quand trois suffisent",
    "grandiloquent": "utilise des formules amples, des périodes longues, comme un orateur né",
    "ironie froide": "dit le contraire de ce qu'il pense avec un demi-sourire",
    "précision froide": "nomme tout par son nom exact, sans métaphore ni détour",
    "métaphores textiles": "compare tout au tissage, au fil, au noeud et à la trame",
    "murmures": "parle si bas qu'il faut se pencher pour entendre, ce qui donne à chaque mot un poids démesuré",
    "ton solennel": "chaque parole semble un décret, même une remarque sur le temps qu'il fait",
    "fragments poétiques": "laisse ses phrases en suspens, comme des vers inachevés",
    "maximes d'atelier": "cite des règles de métier comme des vérités universelles",
    "questions rhétoriques": "pose sans cesse des questions dont elle connaît la réponse",
    "récits enchâssés": "ouvre une histoire dans chaque histoire, et ne ferme jamais tout à fait la première",
    "formules juridiques": "parle comme un acte notarié, avec des 'attendu que' et des 'en conséquence'",
    "ordres brefs": "commande d'un mot, attend l'obéissance, ne répète jamais",
    "laconique": "économise ses mots comme d'autres économisent l'eau",
    "proverbes marchands": "invoque des adages de foire et de comptoir, teintés de sagesse populaire",
}

RELATION_TYPES = [
    ("allié", "Ils se couvrent mutuellement au Conseil"),
    ("rival", "Ils convoitent la même influence"),
    ("dette", "L'un a sauvé la vie de l'autre, et cette dette pèse"),
    ("méfiance", "Un soupçon ancien les sépare"),
    ("mentorat", "L'un a formé l'autre, qui commence à le dépasser"),
    ("attraction", "Une attirance non dite complique chaque négociation"),
    ("trahison passée", "L'un a trahi l'autre, et cela ne s'oublie pas"),
    ("pacte secret", "Un accord clandestin les lie, à l'insu de tous"),
    ("fraternité", "Ils ont grandi ensemble et se considèrent comme frères"),
    ("antagonisme", "Ils représentent deux visions irréconciliables de l'avenir"),
]


def select_focus_cast(individuals, phase, modalities, factions, rng, k=5):
    """Select k focus characters and generate rich personas.

    Returns list of persona dicts with all narrative details.
    """
    if not individuals:
        return []

    # Select diverse individuals: one per faction if possible, then top-trait diversity
    faction_reps = {}
    for ind in individuals:
        if ind.faction and ind.faction not in faction_reps:
            faction_reps[ind.faction] = ind

    candidates = list(faction_reps.values())
    remaining = [ind for ind in individuals if ind not in candidates]
    rng.shuffle(remaining)
    candidates.extend(remaining)
    candidates = candidates[:k]

    # Ensure we have exactly k (pad if needed)
    while len(candidates) < k and individuals:
        extra = rng.choice(individuals)
        if extra not in candidates:
            candidates.append(extra)
        elif len(individuals) <= len(candidates):
            break

    # Assign roles from pool
    available_roles = list(ROLE_POOL)
    rng.shuffle(available_roles)

    cast = []
    used_role_indices = set()
    for i, ind in enumerate(candidates[:k]):
        # Pick a role that matches dominant modalities
        role_template = _pick_role(ind, available_roles, used_role_indices, rng)
        used_role_indices.add(available_roles.index(role_template))

        desire = rng.choice(DESIRES)
        fear = rng.choice(FEARS)
        secret = rng.choice(SECRETS)
        contradiction = rng.choice(CONTRADICTIONS)
        voice_key = role_template["voice"]
        voice_desc = VOICE_STYLES.get(voice_key, voice_key)

        # Build 2 relationships with other cast members
        relations = []
        other_candidates = [c for c in candidates[:k] if c is not ind]
        rel_targets = rng.sample(other_candidates, min(2, len(other_candidates)))
        used_rel_types = set()
        for target in rel_targets:
            rel_type, rel_desc = _pick_relation(rng, used_rel_types)
            used_rel_types.add(rel_type)
            relations.append({
                "target_id": target.id,
                "type": rel_type,
                "description": rel_desc,
            })
            # Update relationship scores on individuals
            ind.relationships[str(target.id)] = 0.5 if rel_type in ("allié", "mentorat", "fraternité", "pacte secret") else -0.3

        persona = {
            "role": role_template["role"],
            "role_description": role_template["desc"],
            "desire": desire,
            "fear": fear,
            "secret": secret,
            "contradiction": contradiction,
            "voice": voice_key,
            "voice_description": voice_desc,
            "signature_modalities": role_template["mods"],
            "relations": relations,
        }
        ind.persona = persona
        cast.append({
            "individual_id": ind.id,
            "faction": ind.faction,
            "persona": persona,
        })

    return cast


def _pick_role(individual, roles, used_indices, rng):
    """Pick a role template that fits the individual's dominant traits."""
    # Score each role by trait overlap
    best = None
    best_score = -1
    for i, role in enumerate(roles):
        if i in used_indices:
            continue
        score = 0
        for mod in role["mods"]:
            if mod == "culture":
                score += individual.traits.get("cooperation", 0) + individual.traits.get("creativity", 0)
            elif mod == "mythologie":
                score += individual.traits.get("belief", 0) + individual.traits.get("ritual", 0)
            elif mod == "valeurs_ethique":
                score += individual.traits.get("empathy", 0) + individual.traits.get("obedience", 0)
            elif mod == "gouvernance":
                score += individual.traits.get("leadership", 0) + individual.traits.get("obedience", 0)
            elif mod == "economie":
                score += individual.traits.get("trade", 0) + individual.traits.get("skill", 0)
            elif mod == "technique_infrastructure":
                score += individual.traits.get("skill", 0) + individual.traits.get("curiosity", 0)
        score += rng.uniform(0, 0.2)  # tiebreaker
        if score > best_score:
            best_score = score
            best = role
    return best if best else roles[0]


def _pick_relation(rng, used_types):
    """Pick a relation type not already used."""
    available = [r for r in RELATION_TYPES if r[0] not in used_types]
    if not available:
        available = RELATION_TYPES
    return rng.choice(available)


def render_cast_md(phase, cast):
    """Render cast.md content."""
    lines = [f"# Personnages focus — Phase {phase}\n"]

    for entry in cast:
        p = entry["persona"]
        lines.append(f"## {p['role']} (Agent {entry['individual_id']})\n")
        lines.append(f"**Faction** : {entry['faction'] or 'Aucune'}\n")
        lines.append(f"*{p['role_description']}*\n")
        lines.append(f"- **Désir** : {p['desire']}")
        lines.append(f"- **Peur** : {p['fear']}")
        lines.append(f"- **Contradiction** : {p['contradiction']}")
        lines.append(f"- **Secret** : {p['secret']}")
        lines.append(f"- **Voix** : {p['voice_description']}\n")

        if p.get("relations"):
            lines.append("**Relations** :\n")
            for rel in p["relations"]:
                lines.append(f"- *{rel['type']}* avec Agent {rel['target_id']} — {rel['description']}")
            lines.append("")
        lines.append("---\n")

    return "\n".join(lines)
