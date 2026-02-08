"""Drama engine — generates major beats, scenes, and narrative events."""

from system.sim.logger import make_event


# Beat type definitions with modality affinities
BEAT_TYPES = [
    {"type": "conflit", "label": "Conflit armé", "min_factions": 2,
     "mods": ["gouvernance", "valeurs_ethique"],
     "desc_templates": [
         "Une dispute territoriale entre {f1} et {f2} dégénère en affrontement ouvert aux portes du {lieu}.",
         "Les tensions entre {f1} et {f2} éclatent lors d'une assemblée publique. Le sang coule sur les marches du {lieu}.",
     ]},
    {"type": "schisme", "label": "Schisme", "min_factions": 2,
     "mods": ["mythologie", "culture"],
     "desc_templates": [
         "{f1} rejette l'interprétation du mythe fondateur défendue par {f2}. Deux versions du récit circulent désormais.",
         "Un désaccord sur le sens du {artefact} divise la communauté. {f1} proclame une nouvelle lecture.",
     ]},
    {"type": "proces", "label": "Procès", "min_factions": 2,
     "mods": ["gouvernance", "valeurs_ethique"],
     "desc_templates": [
         "Un membre de {f1} est accusé d'avoir violé le {artefact}. {f2} exige un procès public.",
         "Le Conseil convoque un procès après qu'un acte de {f1} met en cause les fondements du droit commun.",
     ]},
    {"type": "alliance", "label": "Alliance", "min_factions": 2,
     "mods": ["gouvernance", "economie"],
     "desc_templates": [
         "{f1} et {f2} signent un pacte de coopération au {lieu}, scellé par l'échange d'un {artefact}.",
         "Face à une menace commune, {f1} et {f2} forment une alliance au {lieu}.",
     ]},
    {"type": "trahison", "label": "Trahison", "min_factions": 2,
     "mods": ["gouvernance", "valeurs_ethique"],
     "desc_templates": [
         "Un émissaire de {f1} révèle que {f2} a rompu secrètement le pacte fondateur.",
         "{c1} trahit {f1} en livrant des informations à {f2}, provoquant une crise de confiance.",
     ]},
    {"type": "reforme", "label": "Réforme", "min_factions": 1,
     "mods": ["gouvernance", "valeurs_ethique", "economie"],
     "desc_templates": [
         "{f1} propose une réforme du système de distribution, remettant en cause les privilèges établis.",
         "Sous la pression de {f1}, le Conseil adopte une nouvelle règle qui transforme l'accès aux ressources.",
     ]},
    {"type": "famine", "label": "Famine et crise", "min_factions": 1,
     "mods": ["economie", "technique_infrastructure"],
     "desc_templates": [
         "Les réserves s'épuisent après une saison sans pluie. {f1} et {f2} se disputent les derniers greniers.",
         "Une crise de ressources frappe la communauté. Le {lieu} est assiégé par ceux qui n'ont plus rien.",
     ]},
    {"type": "decouverte", "label": "Découverte", "min_factions": 1,
     "mods": ["technique_infrastructure", "mythologie"],
     "desc_templates": [
         "Un explorateur de {f1} découvre un gisement au-delà du {lieu}, ouvrant de nouvelles possibilités.",
         "{c1} revient d'une expédition avec une technique inconnue qui bouleverse les pratiques établies.",
     ]},
    {"type": "fondation", "label": "Fondation", "min_factions": 1,
     "mods": ["culture", "gouvernance"],
     "desc_templates": [
         "{f1} fonde un nouveau lieu de rassemblement au {lieu}, qui deviendra le centre de la vie publique.",
         "La construction du {artefact} marque la fondation d'une nouvelle ère pour la communauté.",
     ]},
    {"type": "revolte", "label": "Révolte", "min_factions": 2,
     "mods": ["valeurs_ethique", "economie"],
     "desc_templates": [
         "Les membres les plus pauvres de {f2} se soulèvent contre les privilèges de {f1}.",
         "Une révolte éclate au {lieu} quand {f2} découvre que {f1} a accaparé les réserves communes.",
     ]},
]

# Locations per phase
LOCATIONS = {
    1: ["campement principal", "berge de la rivière", "clairière des feux", "col du passage", "forêt ancienne"],
    2: ["grand arbre du Conseil", "marché du silence", "source sacrée", "forge du village", "grenier central"],
    3: ["place du Protocole", "temple des Récits", "port marchand", "forges de l'Est", "palais du Conseil"],
    4: ["salle du Trône", "grande bibliothèque", "bourse du Comptoir", "cathédrale du Cache", "arsenal des routes"],
}

# Scene dialogue templates
SCENE_TEMPLATES = [
    {
        "situation": "confrontation",
        "template": """Au {lieu}, {c1_role} ({c1_name}) fait face à {c2_role} ({c2_name}).

{c1_name} : « {c1_line1} »

{c2_name} : « {c2_line1} »

{c1_name} : « {c1_line2} »

Un silence. {c2_name} serre les poings.

{c2_name} : « {c2_line2} »

{c1_name} se détourne. {consequence}.""",
    },
    {
        "situation": "négociation",
        "template": """Dans l'ombre du {lieu}, {c1_role} ({c1_name}) et {c2_role} ({c2_name}) se retrouvent.

{c1_name} : « {c1_line1} »

{c2_name} : « {c2_line1} »

{c1_name} baisse la voix.

{c1_name} : « {c1_line2} »

{c2_name} hésite, puis acquiesce lentement.

{c2_name} : « {c2_line2} »

{consequence}.""",
    },
    {
        "situation": "révélation",
        "template": """Le {lieu} est presque désert. {c1_role} ({c1_name}) rejoint {c2_role} ({c2_name}) à l'écart.

{c1_name} : « {c1_line1} »

{c2_name} : « {c2_line1} »

{c1_name} sort un document plié de sa tunique.

{c1_name} : « {c1_line2} »

{c2_name} lit, et son visage se décompose.

{c2_name} : « {c2_line2} »

{consequence}.""",
    },
    {
        "situation": "assemblée",
        "template": """Devant le {lieu}, la foule s'est rassemblée. {c1_role} ({c1_name}) prend la parole.

{c1_name} : « {c1_line1} »

Des murmures parcourent l'assemblée. {c2_role} ({c2_name}) s'avance.

{c2_name} : « {c2_line1} »

{c1_name} : « {c1_line2} »

{c2_name} : « {c2_line2} »

{consequence}.""",
    },
    {
        "situation": "tête-à-tête",
        "template": """{c1_role} ({c1_name}) et {c2_role} ({c2_name}) marchent le long du {lieu}.

{c1_name} : « {c1_line1} »

{c2_name} : « {c2_line1} »

Ils s'arrêtent. {c1_name} regarde au loin.

{c1_name} : « {c1_line2} »

{c2_name} : « {c2_line2} »

{consequence}.""",
    },
]

# Dialogue lines by voice style
DIALOGUE_LINES = {
    "proverbes": [
        "Comme on dit chez nous : le feu qui brûle deux fois éclaire mieux.",
        "Mon père disait : on ne bâtit pas sur du sable, mais on n'a pas toujours le choix de la pierre.",
        "Les anciens avaient un mot pour ça : l'imprudence des sûrs.",
        "Qui plante en hâte récolte des regrets, dit le proverbe.",
    ],
    "phrases courtes": [
        "Non.", "C'est fait.", "Trop tard.", "Pas comme ça.",
        "Alors on se bat.", "Je sais.", "Peu importe.", "Donne-moi ça.",
    ],
    "grandiloquent": [
        "Que les générations futures se souviennent de ce jour comme celui où tout a basculé !",
        "Nous sommes les héritiers d'un monde qui n'a pas fini de naître !",
        "L'histoire elle-même retiendra ce que nous décidons ici, maintenant !",
        "Aucune force au monde ne peut arrêter ce qui a été mis en mouvement !",
    ],
    "ironie froide": [
        "Bien sûr. Parce que ça a tellement bien fonctionné la dernière fois.",
        "Quelle surprise. Qui aurait pu prévoir une chose aussi prévisible ?",
        "Je suis touché par cette démonstration de bonne foi. Vraiment.",
        "Continuez. C'est fascinant de voir quelqu'un creuser sa propre tombe avec autant d'enthousiasme.",
    ],
    "précision froide": [
        "Les faits sont les suivants : trois greniers vides, deux sentiers coupés, une saison perdue.",
        "La mesure exacte est de quatorze jours. Pas un de plus.",
        "Le traité stipule, article trois, alinéa deux : aucune exception.",
        "Voici les chiffres. Ils ne mentent pas, contrairement aux hommes.",
    ],
    "métaphores textiles": [
        "Ce pacte est un fil trop tendu. Il va se rompre.",
        "Nous tissons ensemble, ou nous effilochons séparément.",
        "Le nœud que tu proposes ne tiendra pas la charge.",
        "Chaque trahison coupe un fil. Bientôt il ne restera plus de trame.",
    ],
    "murmures": [
        "Écoute bien ce que je vais te dire, car je ne le répéterai pas.",
        "Il y a des choses qu'on ne dit qu'une fois.",
        "Approche-toi. Ce que j'ai vu ne doit pas être entendu par d'autres.",
        "Le silence dit plus que tes discours.",
    ],
    "ton solennel": [
        "Que cela soit inscrit dans les registres de cette assemblée.",
        "Par l'autorité qui m'a été confiée, je déclare ceci irrévocable.",
        "Nul ne pourra dire qu'il n'a pas été averti.",
        "La décision est prise. Elle engage nos descendants.",
    ],
    "fragments poétiques": [
        "La rivière ne revient pas... et pourtant, l'eau...",
        "Sous les pierres, quelque chose dort encore... quelque chose qui attend...",
        "Le vent porte des voix, parfois... celles de ceux qui...",
        "Tout commence par une faille... tout finit par...",
    ],
    "maximes d'atelier": [
        "On ne forge pas le fer froid. Il faut d'abord la chaleur, ensuite le marteau.",
        "Une fondation mal posée, c'est un mur qui tombera dans dix ans.",
        "La bonne mesure, c'est celle qu'on prend deux fois.",
        "Un outil mal entretenu trahit celui qui s'en sert.",
    ],
    "questions rhétoriques": [
        "Et qui paiera le prix de cette décision ? Toi ? Moi ? Ou ceux qui n'ont pas voix au Conseil ?",
        "Combien de fois faudra-t-il que la même erreur se répète avant qu'on en tire les leçons ?",
        "Est-ce vraiment de la justice, ou simplement la volonté du plus fort habillée de mots nobles ?",
        "Qui, parmi vous, oserait affirmer que ses mains sont propres ?",
    ],
    "récits enchâssés": [
        "Cela me rappelle l'histoire d'un homme qui creusait un puits... mais avant cela, il faut que je te raconte pourquoi il avait soif...",
        "Il y avait autrefois une ville, dans une vallée... mais la vallée elle-même avait une histoire...",
        "Mon maître racontait que son maître avait vu, de ses propres yeux... mais il faut d'abord comprendre d'où il venait...",
        "L'histoire que je vais te dire en contient une autre. Retiens bien la seconde.",
    ],
    "formules juridiques": [
        "Attendu que les faits sont établis, et considérant les précédents, la sentence est sans appel.",
        "En vertu du pacte fondateur, article premier : nul ne se place au-dessus du serment.",
        "Les parties sont tenues de se conformer à la décision rendue, sous peine de bannissement.",
        "Le droit est clair. L'interprétation que vous proposez est une fiction.",
    ],
    "ordres brefs": [
        "Fermez les portes.", "Rassemblement.", "Silence.", "Exécution immédiate.",
        "Pas de discussion.", "Obéissez.", "C'est un ordre.", "Maintenant.",
    ],
    "laconique": [
        "Oui.", "Non.", "Peut-être. Mais j'en doute.", "Vu.",
        "Noté.", "Insuffisant.", "On verra.", "Pas encore.",
    ],
    "proverbes marchands": [
        "Comme on dit au marché : le prix juste, c'est celui que les deux regrettent un peu.",
        "Un bon commerce, c'est quand personne ne sourit trop à la fin.",
        "On ne vend pas la peau de l'ours, mais on peut en négocier la fourrure à l'avance.",
        "Le crédit, c'est de la confiance qu'on mesure en grain.",
    ],
}

# Consequence templates
CONSEQUENCES = [
    "La tension entre les deux factions monte d'un cran. Les regards, désormais, portent le poids de cette confrontation",
    "Un accord fragile est conclu, mais chacun sait qu'il ne tiendra qu'aussi longtemps que les intérêts convergent",
    "La nouvelle se répand dans la communauté comme un feu de brousse. Rien ne sera plus comme avant",
    "Les partisans des deux camps se comptent. Les lignes de fracture se dessinent pour la suite",
    "Un silence lourd s'installe. Ce qui vient d'être dit ne peut être retiré",
    "Les témoins quittent les lieux en emportant chacun une version différente de ce qui s'est passé",
    "Cette décision aura des conséquences que nul ne mesure encore, mais que tous pressentent",
    "Le pacte est scellé. Désormais, leurs destins sont liés, pour le meilleur et pour le pire",
]


def choose_major_beat(phase, modalities, deltas, factions, cast, rng):
    """Choose the major dramatic beat for this phase.

    Returns a beat dict with type, description, affected modalities,
    involved factions, and generated events.
    """
    # Score beat types by relevance to current phase dynamics
    scores = []
    for bt in BEAT_TYPES:
        if len(factions) < bt["min_factions"]:
            continue
        score = 0.0
        # Higher score for beats that match high-delta modalities
        for mod in bt["mods"]:
            if mod in deltas:
                score += abs(deltas.get(mod, 0)) * 10
            if mod in modalities:
                ms = modalities[mod]
                s = ms.score if hasattr(ms, 'score') else ms.get("score", 0)
                score += s
        # Phase-based preferences
        if phase == 1 and bt["type"] in ("fondation", "decouverte"):
            score += 1.0
        elif phase == 2 and bt["type"] in ("schisme", "alliance", "reforme"):
            score += 1.0
        elif phase == 3 and bt["type"] in ("conflit", "proces", "revolte"):
            score += 1.0
        elif phase == 4 and bt["type"] in ("trahison", "reforme", "fondation"):
            score += 1.0
        score += rng.uniform(0, 0.5)
        scores.append((bt, score))

    scores.sort(key=lambda x: -x[1])
    chosen = scores[0][0] if scores else BEAT_TYPES[0]

    # Pick factions and cast for the beat
    f1 = factions[0] if factions else {"name": "la communauté"}
    f2 = factions[1] if len(factions) > 1 else factions[0]

    # Pick characters from cast
    c1 = cast[0] if cast else {"persona": {"role": "un ancien"}, "individual_id": 0}
    c2 = cast[1] if len(cast) > 1 else cast[0] if cast else c1

    locations = LOCATIONS.get(phase, LOCATIONS[1])
    lieu = rng.choice(locations)

    # Build description
    template = rng.choice(chosen["desc_templates"])
    desc = template.format(
        f1=f1["name"], f2=f2["name"],
        c1=c1["persona"]["role"], c2=c2["persona"]["role"],
        lieu=lieu,
        artefact="pacte fondateur",
    )

    # Generate events
    events = []
    events.append(make_event(
        phase=phase, tick=1, event_type=f"beat_{chosen['type']}",
        text=desc,
        actors=[c1["individual_id"], c2["individual_id"]],
        location=lieu,
        modalities=chosen["mods"],
        consequences={"tension": 0.1 if chosen["type"] in ("conflit", "revolte", "trahison") else -0.05},
    ))

    # Relationship changes
    rel_changes = {}
    if chosen["type"] in ("conflit", "revolte", "trahison", "schisme"):
        rel_changes[f"{c1['individual_id']}->{c2['individual_id']}"] = -0.3
    elif chosen["type"] in ("alliance", "fondation"):
        rel_changes[f"{c1['individual_id']}->{c2['individual_id']}"] = 0.3

    beat = {
        "type": chosen["type"],
        "label": chosen["label"],
        "description": desc,
        "modalities_affected": chosen["mods"],
        "factions_involved": [f1["name"], f2["name"]],
        "location": lieu,
        "events": events,
        "relationship_changes": rel_changes,
        "cast_involved": [c1["individual_id"], c2["individual_id"]],
    }

    return beat


def generate_scenes(phase, beat, cast, factions, artifacts, rng, count=5):
    """Generate dialogued scenes for the phase.

    Returns list of scene strings and corresponding events.
    """
    scenes = []
    events = []
    locations = LOCATIONS.get(phase, LOCATIONS[1])

    # Ensure we use different scene templates
    available_templates = list(SCENE_TEMPLATES)
    rng.shuffle(available_templates)

    for i in range(min(count, len(available_templates))):
        template_data = available_templates[i]

        # Pick two cast members
        if len(cast) >= 2:
            pair = rng.sample(cast, 2)
        elif cast:
            pair = [cast[0], cast[0]]
        else:
            continue

        c1, c2 = pair
        p1 = c1["persona"]
        p2 = c2["persona"]

        lieu = rng.choice(locations)

        # Get dialogue lines for each voice style (copy to avoid mutating originals)
        lines1 = list(DIALOGUE_LINES.get(p1["voice"], DIALOGUE_LINES["phrases courtes"]))
        lines2 = list(DIALOGUE_LINES.get(p2["voice"], DIALOGUE_LINES["phrases courtes"]))

        rng.shuffle(lines1)
        rng.shuffle(lines2)

        consequence = rng.choice(CONSEQUENCES)

        # Build artifact reference if possible
        if artifacts:
            art = rng.choice(artifacts)
            title = art.title
            # Avoid "Le Le X" — use title directly if it starts with an article
            if title.lower().startswith(("le ", "la ", "l'", "les ")):
                art_ref = f" {title} est invoqué comme preuve."
            else:
                art_ref = f" Le {title} est invoqué comme preuve."
            consequence += art_ref

        scene_text = template_data["template"].format(
            lieu=lieu,
            c1_role=p1["role"],
            c1_name=f"Agent {c1['individual_id']}",
            c2_role=p2["role"],
            c2_name=f"Agent {c2['individual_id']}",
            c1_line1=lines1[0] if lines1 else "...",
            c1_line2=lines1[1] if len(lines1) > 1 else "...",
            c2_line1=lines2[0] if lines2 else "...",
            c2_line2=lines2[1] if len(lines2) > 1 else "...",
            consequence=consequence,
        )

        scenes.append(scene_text)

        events.append(make_event(
            phase=phase, tick=i + 2, event_type="scene",
            text=f"Scène {i+1}: {template_data['situation']} entre {p1['role']} et {p2['role']}",
            actors=[c1["individual_id"], c2["individual_id"]],
            location=lieu,
            modalities=p1.get("signature_modalities", []),
            meta={"situation": template_data["situation"]},
        ))

    return scenes, events


def generate_chronique(phase, beat, scenes, cast, factions, artifacts, modalities, rng):
    """Generate the chronique.md content — a continuous narrative of the phase.

    Target: 800-2000 words.
    """
    lines = [f"# Chronique — Phase {phase}\n"]

    # Opening
    phase_names = {1: "l'Éveil", 2: "l'Enracinement", 3: "l'Expansion", 4: "la Consolidation"}
    phase_name = phase_names.get(phase, f"Phase {phase}")

    faction_names = [f["name"] for f in factions[:4]]
    faction_list = ", ".join(faction_names[:-1]) + f" et {faction_names[-1]}" if len(faction_names) > 1 else faction_names[0] if faction_names else "la communauté"

    lines.append(f"## {phase_name}\n")

    # Introduction paragraph
    mod_scores = {}
    for mod_id, mod in modalities.items():
        s = mod.score if hasattr(mod, 'score') else mod.get("score", 0)
        mod_scores[mod_id] = s
    top_mods = sorted(mod_scores.items(), key=lambda x: -x[1])[:2]
    mod_names = {
        "culture": "la culture", "mythologie": "la mythologie",
        "valeurs_ethique": "l'éthique", "gouvernance": "la gouvernance",
        "economie": "l'économie", "technique_infrastructure": "l'infrastructure",
    }

    lines.append(
        f"La phase de {phase_name} marque un tournant pour la société. "
        f"Les forces dominantes de cette période sont {mod_names.get(top_mods[0][0], top_mods[0][0])} "
        f"et {mod_names.get(top_mods[1][0], top_mods[1][0])}, qui façonnent les décisions "
        f"et les conflits entre {faction_list}.\n"
    )

    # Cast introduction
    lines.append("## Les acteurs de cette phase\n")
    for entry in cast[:5]:
        p = entry["persona"]
        lines.append(
            f"**{p['role']}** (Agent {entry['individual_id']}, {entry.get('faction', 'sans faction')}) — "
            f"{p['role_description']} "
            f"Son désir : {p['desire']}. Sa contradiction : {p['contradiction']}.\n"
        )

    # The major beat
    lines.append(f"## Le grand événement : {beat['label']}\n")
    lines.append(f"{beat['description']}\n")

    # Develop the beat with faction context
    f_involved = beat.get("factions_involved", [])
    if len(f_involved) >= 2:
        affected_names = [mod_names.get(m, m) for m in beat.get("modalities_affected", ["la gouvernance"])[:2]]
        lines.append(
            f"Cet événement oppose principalement {f_involved[0]} à {f_involved[1]}. "
            f"Les causes sont multiples : des tensions accumulées autour de "
            f"{', '.join(affected_names)}, "
            f"des ambitions personnelles, et des rancœurs anciennes qui trouvent enfin un prétexte pour éclater.\n"
        )

    # Artifact mentions
    if artifacts:
        lines.append("## Les artefacts de la phase\n")
        for art in artifacts[:3]:
            lines.append(
                f"**{art.title}** (`{art.id}`) — {art.description[:150]}. "
                f"Cet artefact joue un rôle central dans les événements de cette phase.\n"
            )

    # Scenes
    lines.append("## Scènes\n")
    for i, scene in enumerate(scenes[:5]):
        lines.append(f"### Scène {i+1}\n")
        lines.append(f"{scene}\n")

    # Consequences
    lines.append("## Conséquences\n")

    if beat["type"] in ("conflit", "revolte"):
        lines.append(
            "Le conflit laisse des cicatrices profondes. Les alliances se reconfigurent, "
            "les méfiances s'installent. Plusieurs familles quittent leur faction d'origine, "
            "cherchant refuge auprès de ceux qui n'ont pas pris parti.\n"
        )
    elif beat["type"] in ("alliance", "fondation"):
        lines.append(
            "L'alliance renforce la cohésion de la communauté, mais crée aussi de nouveaux "
            "exclus : ceux qui n'ont pas été invités à la table des négociations. "
            "Un nouvel équilibre se dessine, fragile mais porteur d'espoir.\n"
        )
    elif beat["type"] in ("schisme", "trahison"):
        lines.append(
            "Le schisme fracture la communauté en camps irréconciliables. Chacun doit choisir "
            "son camp, et les amitiés anciennes ne suffisent plus à garantir la loyauté. "
            "Les récits fondateurs eux-mêmes deviennent un champ de bataille.\n"
        )
    else:
        lines.append(
            "Les événements de cette phase redéfinissent les rapports de force. "
            "Ce qui semblait acquis est remis en question, et de nouvelles figures "
            "émergent pour combler le vide laissé par les anciennes certitudes.\n"
        )

    # Closing
    lines.append("## Vers la suite\n")
    lines.append(
        f"À la fin de cette phase, la société porte les marques de {beat['label'].lower()}. "
        f"Les personnages centraux ont été transformés par les événements : "
        f"certains renforcés, d'autres brisés, tous changés. "
        f"La prochaine phase devra composer avec cet héritage.\n"
    )

    return "\n".join(lines)
