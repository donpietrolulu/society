"""Artifact generation — one per modality per phase."""


# Artifact templates per modality per phase
ARTIFACT_TEMPLATES = {
    "culture": {
        1: [
            {"title": "Le Chant du Premier Feu", "desc": "Une mélodie rythmique que les veilleurs entonnent à la tombée de la nuit, marquant la fin du labeur et le début du repos. Chaque foyer ajoute un couplet selon ses morts de l'année.", "tags": ["rituel", "musique", "mémoire"]},
            {"title": "La Danse des Empreintes", "desc": "Un rituel où les enfants marchent dans les traces de leurs aînés, gravées dans l'argile humide. Les pas sont séchés au soleil et conservés.", "tags": ["rituel", "transmission", "enfance"]},
        ],
        2: [
            {"title": "Le Tissage des Couleurs", "desc": "Un code de couleurs tissé dans les vêtements qui indique le clan, le métier et l'état civil de chacun.", "tags": ["artisanat", "identité", "clan"]},
            {"title": "La Fête des Récoltes", "desc": "Une célébration annuelle où chaque guilde présente le fruit de son travail. Les meilleurs artisans reçoivent le droit de porter le bandeau rouge.", "tags": ["fête", "compétition", "reconnaissance"]},
        ],
        3: [
            {"title": "Le Théâtre des Jugements", "desc": "Une forme d'art dramatique où les procès célèbres sont rejoués devant la population. Les acteurs portent les masques des accusés et des juges.", "tags": ["théâtre", "justice", "mémoire"]},
        ],
        4: [
            {"title": "L'Académie des Formes", "desc": "Une institution qui enseigne et codifie les arts visuels, la musique et la rhétorique. Seuls ses diplômés peuvent enseigner officiellement.", "tags": ["institution", "éducation", "arts"]},
        ],
    },
    "mythologie": {
        1: [
            {"title": "Le Mythe de la Faille", "desc": "Le récit fondateur selon lequel le monde est né d'une fissure dans la roche, d'où l'eau et la lumière ont jailli simultanément. Les premiers hommes sont nés de la boue qui en a résulté.", "tags": ["création", "origine", "terre"]},
            {"title": "Le Rêve du Cache", "desc": "Un mythe selon lequel les ancêtres ont caché le savoir essentiel dans un lieu que seuls les dignes peuvent trouver. Le Cache est le nom donné à ce trésor invisible.", "tags": ["quête", "savoir", "sacré"]},
        ],
        2: [
            {"title": "Le Cycle des Trois Sœurs", "desc": "Un ensemble de récits sur trois sœurs divines — la Tisseuse (ordre), la Briseuse (chaos) et la Compteuse (équilibre) — qui gouvernent les saisons et les fortunes.", "tags": ["divinités", "cycle", "destin"]},
        ],
        3: [
            {"title": "L'Épopée de Kaël le Marcheur", "desc": "Le récit d'un héros qui a traversé les six territoires pour unifier les peuples, portant un bâton marqué de six entailles — une par modalité de la vie.", "tags": ["héros", "unification", "voyage"]},
        ],
        4: [
            {"title": "Le Canon des Prophéties", "desc": "Un recueil officiel des prophéties reconnues par l'Ordre du Cache, distinguant les « vraies » prophéties des superstitions populaires.", "tags": ["canon", "prophétie", "institution"]},
        ],
    },
    "valeurs_ethique": {
        1: [
            {"title": "Le Serment du Seuil", "desc": "Un pacte oral prononcé sur le seuil d'une maison : quiconque entre s'engage à ne pas nuire à ceux qui y dorment, et le maître s'engage à nourrir le voyageur.", "tags": ["pacte", "hospitalité", "réciprocité"]},
        ],
        2: [
            {"title": "Le Code des Dettes", "desc": "Un système de nœuds sur corde qui enregistre les obligations mutuelles entre familles. Couper un nœud sans accord des deux parties est un déshonneur grave.", "tags": ["dette", "honneur", "système"]},
        ],
        3: [
            {"title": "La Charte des Justes", "desc": "Le premier document écrit énonçant les droits fondamentaux de chaque citoyen : droit à la parole au Conseil, droit à une part des récoltes, devoir de défense commune.", "tags": ["droit", "citoyenneté", "écrit"]},
        ],
        4: [
            {"title": "Le Tribunal des Consciences", "desc": "Une institution où les accusés ne sont pas jugés sur les faits mais sur l'intention. Les juges sont tirés au sort et délibèrent en secret.", "tags": ["tribunal", "intention", "institution"]},
        ],
    },
    "gouvernance": {
        1: [
            {"title": "Le Cercle de Parole", "desc": "Un rituel politique où chacun peut prendre la parole en tenant un bâton sculpté. Tant qu'il tient le bâton, nul ne peut l'interrompre.", "tags": ["assemblée", "parole", "rituel"]},
        ],
        2: [
            {"title": "Le Conseil des Aînés", "desc": "Une institution informelle où les chefs de famille se réunissent sous un arbre spécifique pour trancher les disputes et décider des expéditions.", "tags": ["conseil", "décision", "tradition"]},
        ],
        3: [
            {"title": "Le Protocole des Sceaux", "desc": "Un système de validation des décisions officielles par apposition de sceaux en cire. Trois sceaux minimum sont requis : le dirigeant, le temple, et le peuple.", "tags": ["protocole", "validation", "pouvoir"]},
        ],
        4: [
            {"title": "La Constitution du Fer", "desc": "Le texte fondamental qui définit la séparation des pouvoirs entre la Couronne, le Temple et le Comptoir, et les limites de chacun.", "tags": ["constitution", "séparation", "pouvoir"]},
        ],
    },
    "economie": {
        1: [
            {"title": "Le Troc du Silence", "desc": "Un marché hebdomadaire où les échanges se font sans parole, par gestes codifiés. Parler pendant le troc est considéré comme une tentative de tromperie.", "tags": ["marché", "geste", "confiance"]},
        ],
        2: [
            {"title": "La Mesure du Grain", "desc": "Un étalon de poids et de volume adopté par la Guilde du Sillon, matérialisé par une jarre en pierre conservée au centre du village.", "tags": ["étalon", "mesure", "commerce"]},
        ],
        3: [
            {"title": "La Lettre de Change", "desc": "Un système de promesses écrites sur tablettes d'argile permettant de commercer à distance sans transporter de marchandises.", "tags": ["finance", "crédit", "commerce"]},
        ],
        4: [
            {"title": "La Banque des Semences", "desc": "Un entrepôt centralisé où les excédents de chaque région sont stockés et redistribués en cas de famine, géré par le Grand Comptoir.", "tags": ["réserve", "redistribution", "institution"]},
        ],
    },
    "technique_infrastructure": {
        1: [
            {"title": "Le Pont de Cordes", "desc": "La première construction technique collective : un pont de cordes tressées au-dessus du ravin qui sépare les deux rives du campement principal.", "tags": ["construction", "pont", "collectif"]},
        ],
        2: [
            {"title": "Le Moulin à Eau", "desc": "La première machine de la communauté, construite au bord de la rivière pour moudre le grain sans effort humain.", "tags": ["machine", "agriculture", "innovation"]},
        ],
        3: [
            {"title": "L'Aqueduc des Forges", "desc": "Un système de canaux en pierre qui achemine l'eau depuis les hauteurs vers les forges et les ateliers de la cité.", "tags": ["aqueduc", "ingénierie", "infrastructure"]},
        ],
        4: [
            {"title": "Le Réseau des Tours de Guet", "desc": "Un système de tours reliées par des signaux lumineux (miroirs le jour, feux la nuit) permettant de transmettre un message d'un bout du territoire à l'autre en quelques heures.", "tags": ["communication", "réseau", "défense"]},
        ],
    },
}

MOD_PREFIXES = {
    "culture": "CUL",
    "mythologie": "MYT",
    "valeurs_ethique": "ETH",
    "gouvernance": "GOV",
    "economie": "ECO",
    "technique_infrastructure": "TEC",
}


def generate_phase_artifacts(phase, modalities, factions, cast, rng):
    """Generate at least 1 artifact per modality for the phase.

    Returns list of Artifact model instances.
    """
    from system.sim.models import Artifact

    artifacts = []
    mod_order = ["culture", "mythologie", "valeurs_ethique", "gouvernance",
                 "economie", "technique_infrastructure"]

    for mod_id in mod_order:
        prefix = MOD_PREFIXES.get(mod_id, "UNK")
        templates = ARTIFACT_TEMPLATES.get(mod_id, {}).get(phase, [])
        if not templates:
            # Fallback: use phase 1 templates
            templates = ARTIFACT_TEMPLATES.get(mod_id, {}).get(1, [])
        if not templates:
            continue

        template = rng.choice(templates)
        artifact_id = f"{prefix}-P{phase}-{len(artifacts)+1:02d}"

        artifacts.append(Artifact(
            id=artifact_id,
            modality=mod_id,
            title=template["title"],
            description=template["desc"],
            tags=template.get("tags", []),
        ))

    return artifacts


def render_artifacts_md(phase, artifacts):
    """Render artifacts.md content."""
    lines = [f"# Artefacts — Phase {phase}\n"]
    lines.append(f"*{len(artifacts)} artefacts produits durant cette phase.*\n")

    for art in artifacts:
        mod_name = {
            "culture": "Culture",
            "mythologie": "Mythologie",
            "valeurs_ethique": "Valeurs et Éthique",
            "gouvernance": "Gouvernance",
            "economie": "Économie",
            "technique_infrastructure": "Technique et Infrastructure",
        }.get(art.modality, art.modality)

        lines.append(f"## {art.title}")
        lines.append(f"**ID** : `{art.id}` | **Modalité** : {mod_name}\n")
        lines.append(f"{art.description}\n")
        if art.tags:
            lines.append(f"*Tags : {', '.join(art.tags)}*\n")
        lines.append("---\n")

    return "\n".join(lines)
