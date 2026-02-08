"""Modality interconnectivity analysis — narrative explanation of influences."""


def compute_influence_contributions(mod_scores, matrix, order):
    """Compute how much each modality contributes to each other.

    Returns dict: {target_mod: [(source_mod, contribution), ...]} sorted desc.
    """
    contributions = {}
    for i, target in enumerate(order):
        row = matrix[i]
        total_weight = sum(row)
        sources = []
        for j, source in enumerate(order):
            if i == j:
                continue
            contrib = (row[j] * mod_scores.get(source, 0.0)) / total_weight
            sources.append((source, round(contrib, 4)))
        sources.sort(key=lambda x: -x[1])
        contributions[target] = sources
    return contributions


def compute_phase_modality_deltas(prev_mods, mods):
    """Compute score deltas between two phase modality dicts."""
    deltas = {}
    for mod_id in mods:
        current = mods[mod_id].score if hasattr(mods[mod_id], 'score') else mods[mod_id].get("score", 0)
        if mod_id in prev_mods:
            previous = prev_mods[mod_id].score if hasattr(prev_mods[mod_id], 'score') else prev_mods[mod_id].get("score", 0)
        else:
            previous = 0.0
        deltas[mod_id] = round(current - previous, 4)
    return deltas


def detect_feedback_loop(contributions, order):
    """Detect a structural feedback loop (A -> B -> C -> A)."""
    # For each modality, find its top outgoing influence target
    top_target = {}
    for mod in order:
        if mod in contributions:
            # Find where this mod contributes most as a source
            best_target = None
            best_val = -1
            for target in order:
                if target == mod:
                    continue
                for src, val in contributions.get(target, []):
                    if src == mod and val > best_val:
                        best_val = val
                        best_target = target
            if best_target:
                top_target[mod] = best_target

    # Try to find a 3-cycle
    for start in order:
        mid = top_target.get(start)
        if mid and mid != start:
            end = top_target.get(mid)
            if end and end != mid and end != start:
                back = top_target.get(end)
                if back == start:
                    return (start, mid, end)
    # Fallback: return first 3 in chain
    for start in order:
        mid = top_target.get(start)
        if mid:
            end = top_target.get(mid)
            if end and end != start:
                return (start, mid, end)
    return (order[0], order[1], order[2]) if len(order) >= 3 else None


MOD_NAMES = {
    "culture": "Culture",
    "mythologie": "Mythologie",
    "valeurs_ethique": "Valeurs et Éthique",
    "gouvernance": "Gouvernance",
    "economie": "Économie",
    "technique_infrastructure": "Technique et Infrastructure",
}

INFLUENCE_NARRATIVES = {
    ("mythologie", "valeurs_ethique"): "Les récits mythologiques fournissent les modèles moraux qui fondent les valeurs partagées",
    ("valeurs_ethique", "gouvernance"): "Les principes éthiques contraignent et légitiment l'exercice du pouvoir",
    ("gouvernance", "economie"): "Les structures de gouvernance encadrent les échanges et la distribution des ressources",
    ("economie", "technique_infrastructure"): "La prospérité économique finance l'innovation et les grands travaux",
    ("technique_infrastructure", "culture"): "Les avancées techniques transforment les pratiques quotidiennes et les modes de vie",
    ("culture", "mythologie"): "Les pratiques culturelles nourrissent la création de nouveaux mythes et récits fondateurs",
    ("mythologie", "gouvernance"): "Les mythes de fondation légitiment l'autorité des dirigeants",
    ("valeurs_ethique", "culture"): "Les normes éthiques façonnent les rituels et les conventions sociales",
    ("gouvernance", "valeurs_ethique"): "Les lois incarnent et renforcent les principes moraux de la communauté",
    ("culture", "valeurs_ethique"): "Les pratiques culturelles transmettent et enracinent les valeurs collectives",
    ("economie", "gouvernance"): "Les intérêts économiques influencent les décisions politiques et les structures de pouvoir",
    ("technique_infrastructure", "economie"): "Les innovations techniques créent de nouvelles formes de production et d'échange",
}


def render_societe_interactions_md(phase, mods, deltas, contributions, order):
    """Render the societe_interactions.md file content."""
    lines = [f"# Interactions entre modalités — Phase {phase}\n"]

    # Overview
    lines.append("## Vue d'ensemble\n")
    lines.append("Cette phase révèle les dynamiques d'influence suivantes entre les six modalités de la société.\n")

    # Deltas
    lines.append("## Évolution des modalités\n")
    for mod_id in order:
        name = MOD_NAMES.get(mod_id, mod_id)
        score = mods[mod_id].score if hasattr(mods[mod_id], 'score') else mods[mod_id].get("score", 0)
        delta = deltas.get(mod_id, 0)
        direction = "en hausse" if delta > 0.005 else "en baisse" if delta < -0.005 else "stable"
        lines.append(f"- **{name}** : {score:.3f} ({direction}, Δ={delta:+.3f})")
    lines.append("")

    # Top 3 incoming influences per modality
    lines.append("## Influences entrantes (qui pousse chaque modalité)\n")
    for mod_id in order:
        name = MOD_NAMES.get(mod_id, mod_id)
        lines.append(f"### {name}\n")
        top3 = contributions.get(mod_id, [])[:3]
        for src, val in top3:
            src_name = MOD_NAMES.get(src, src)
            narrative = INFLUENCE_NARRATIVES.get((src, mod_id), f"{src_name} influence {name}")
            lines.append(f"- **{src_name}** (contribution : {val:.3f}) — {narrative}.")
        lines.append("")

    # Top 3 outgoing influences (who influences the most)
    lines.append("## Influences sortantes (qui influence le plus les autres)\n")
    outgoing = {}
    for target, sources in contributions.items():
        for src, val in sources:
            outgoing[src] = outgoing.get(src, 0) + val
    top_out = sorted(outgoing.items(), key=lambda x: -x[1])[:3]
    for mod_id, total in top_out:
        name = MOD_NAMES.get(mod_id, mod_id)
        lines.append(f"- **{name}** : influence totale sortante = {total:.3f}")
    lines.append("")

    # Feedback loop
    loop = detect_feedback_loop(contributions, order)
    if loop:
        lines.append("## Boucle structurante détectée\n")
        names = [MOD_NAMES.get(m, m) for m in loop]
        lines.append(f"**{names[0]} → {names[1]} → {names[2]} → {names[0]}**\n")

        # Narrative explanation
        lines.append("### Explication\n")
        pairs = [(loop[0], loop[1]), (loop[1], loop[2]), (loop[2], loop[0])]
        for src, tgt in pairs:
            narrative = INFLUENCE_NARRATIVES.get(
                (src, tgt),
                f"{MOD_NAMES.get(src, src)} nourrit {MOD_NAMES.get(tgt, tgt)}"
            )
            lines.append(f"- {narrative}.")
        lines.append("")

        lines.append(
            f"Cette boucle montre comment {names[0]} alimente {names[1]}, "
            f"qui à son tour renforce {names[2]}, lequel en retour soutient {names[0]}. "
            f"C'est un circuit d'auto-renforcement qui stabilise — ou, si l'une des modalités "
            f"faiblit, déstabilise — l'ensemble de la société.\n"
        )

    # Matrix reference
    lines.append("## Matrice d'interdépendances (référence)\n")
    lines.append("Les contributions ci-dessus sont calculées à partir de la matrice d'interdépendances ")
    lines.append("pondérée par les scores actuels de chaque modalité. Chaque cellule `matrix[i][j]` ")
    lines.append("indique le poids de l'influence de la modalité `j` sur la modalité `i`.\n")
    header = "| | " + " | ".join(MOD_NAMES.get(m, m) for m in order) + " |"
    sep = "|---" * (len(order) + 1) + "|"
    lines.append(header)
    lines.append(sep)
    # We don't have the raw matrix here, but we can reference it
    lines.append("*(Voir interdependencies.json pour les valeurs exactes.)*\n")

    return "\n".join(lines)
