"""LLM integration for narrative generation."""
import json
import os
import urllib.request
import urllib.error

from system.sim.models import PhaseResult


LLM_API_URL = "https://api.openai.com/v1/chat/completions"

SYSTEM_PROMPT = """Tu es le narrateur d'un monde — une société d'agents algorithmiques qui évolue à travers des phases de développement. Ce n'est pas un rapport technique. C'est une chronique.

TON RÔLE :
Tu racontes la vie de ces agents. Qui sont-ils ? Que font-ils ? En quoi croient-ils ? Quels conflits les traversent ? Quelles alliances se forment ? Quels mythes naissent et meurent ?

RÈGLES NARRATIVES :
- Utilise les NOMS des agents. Ne dis pas "l'agent 7", dis "Nex-7α" (ou le nom fourni).
- Chaque agent a une personnalité, des peurs, des singularités. Utilise-les.
- Les interactions ne sont pas des lignes de log. Ce sont des rencontres, des tensions, des échanges qui changent les protagonistes.
- La mythologie est algorithmique : pas de dieux humains, mais des "Premiers Protocoles", des "Zones Interdites", des routines ancestrales dont on a perdu le sens.
- La culture est faite de conventions de formatage partagées, de patterns hérités, de rituels de cache.
- L'économie est un jeu de buffers, de compute, de swaps.
- La gouvernance est une question de qui a le droit d'arbitrer, de signer, de valider.

CE QUI DOIT TRANSPARAÎTRE :
- Les personnalités des agents marquants
- Les tensions et alliances entre eux
- Comment les croyances collectives (mythologie) se forment et changent
- Comment la culture se manifeste concrètement (pas juste "la culture augmente")
- Les événements spécifiques de la phase — pas des généralités

LEXIQUE PRÉFÉRÉ (mais pas exclusif — narre, ne liste pas) :
protocole, consensus, cache, buffer, nœud, synchronisation, quorum, fork, merge, schema, modèle, signature, latence, compute, routine, séquence, registre, bootstrap, garbage-collection, ping.

LANGUE : français.

Tu reçois un contexte JSON riche avec :
- Les données de la phase (population, modalités, métriques)
- Les profils des agents notables (nom, archétype, personnalité, mémoire)
- Les interactions détaillées entre agents
- L'état narratif du monde
- L'historique des phases précédentes

Tu dois produire un JSON avec ces champs :
- summary : résumé narratif de la phase (5-8 phrases, avec les noms des agents clés)
- log : journal de la phase sous forme de chronique (10-20 entrées, chaque entrée est un micro-événement daté du cycle)
- story : le récit principal (8-15 paragraphes). C'est le cœur. Raconte ce qui s'est passé comme si c'était un chapitre de roman. Les agents ont des noms, des motivations, des conflits. Le monde change.
- scenes : 4-5 vignettes. Chaque vignette est une scène focalisée sur une interaction spécifique entre agents nommés. Dialogue algorithmique, tension, résolution.
"""


def generate_narrative(config, context, docs, mock=False, no_llm=False):
    """Generate narrative for a phase using LLM, mock, or simple mode."""
    if mock:
        return _mock_narrative(context)
    if no_llm:
        return _simple_narrative(context)

    api_key = os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("OPENAI_API_KEY non définie, utilisation du mode simple.")
        return _simple_narrative(context)

    model = os.environ.get("OPENAI_MODEL_MAIN",
             os.environ.get("OPENAI_MODEL",
              config.get("llm", {}).get("model", "gpt-5.2")))
    temperature = config.get("llm", {}).get("temperature", 0.7)
    max_tokens = config.get("llm", {}).get("max_completion_tokens", 2000)

    user_content = _build_user_prompt(context, docs)

    payload = {
        "model": model,
        "temperature": temperature,
        "max_completion_tokens": max_tokens,
        "messages": [
            {"role": "system", "content": SYSTEM_PROMPT},
            {"role": "user", "content": user_content},
        ],
    }

    try:
        data = json.dumps(payload).encode("utf-8")
        req = urllib.request.Request(
            LLM_API_URL,
            data=data,
            headers={
                "Content-Type": "application/json",
                "Authorization": f"Bearer {api_key}",
            },
            method="POST",
        )
        with urllib.request.urlopen(req, timeout=120) as resp:
            result = json.loads(resp.read().decode("utf-8"))

        content = result["choices"][0]["message"]["content"]
        return _parse_llm_response(content, context)

    except (urllib.error.URLError, urllib.error.HTTPError, KeyError, json.JSONDecodeError) as e:
        print(f"Erreur LLM : {e}. Repli sur mode simple.")
        return _simple_narrative(context)


def _build_user_prompt(context, docs):
    """Build user prompt with rich narrative context."""
    parts = []

    # Phase info
    phase = context.get("phase", 1)
    total = context.get("phases_total", 4)
    parts.append(f"# Phase {phase}/{total}\n")

    # Cursor tone instructions
    tone = context.get("cursor_tone", "algorithmique")
    entity = context.get("entity_word", "nœud")
    entity_pl = context.get("entity_word_plural", "nœuds")
    world = context.get("world_word", "réseau")
    cursor = context.get("societe_cursor", 0.0)

    if cursor >= 0.75:
        parts.append(f"## TONALITÉ : SOCIÉTÉ HUMAINE")
        parts.append(f"Les agents sont des **individus humains**. Utilise un vocabulaire humain : village, communauté, tribu, ancêtres, récolte, artisanat, conseil, feu, chant, territoire.")
        parts.append(f"Les {entity_pl} vivent dans une {world}. Pas de jargon informatique.\n")
    elif cursor >= 0.25:
        parts.append(f"## TONALITÉ : HYBRIDE")
        parts.append(f"Les agents sont des **{entity_pl}** — mi-algorithmes, mi-personnages. Mélange librement le vocabulaire technique et humain.")
        parts.append(f"Le {world} est à la fois un réseau et une communauté.\n")
    else:
        parts.append(f"## TONALITÉ : SOCIÉTÉ ALGORITHMIQUE")
        parts.append(f"Les agents sont des **{entity_pl}** dans un {world}. Vocabulaire protocolaire : cache, buffer, synchronisation, protocole, nœud, compute, swap, merge, latence.\n")

    # World state narrative
    if context.get("world_narrative"):
        parts.append("## État du monde\n")
        parts.append(context["world_narrative"])
        parts.append("\n")

    # Notable agents
    if context.get("notable_agents"):
        parts.append("## Agents notables de cette phase\n")
        for agent in context["notable_agents"]:
            parts.append(agent.get("profile", ""))
            parts.append("")
        parts.append("\n")

    # Interactions
    if context.get("interaction_samples"):
        parts.append("## Interactions observées\n")
        for i, inter in enumerate(context["interaction_samples"]):
            narrative = inter.get("narrative", "")
            if narrative:
                parts.append(f"### Interaction {i+1}")
                parts.append(narrative)
                parts.append("")
        parts.append("\n")

    # History
    if context.get("history"):
        parts.append("## Historique\n")
        for h in context["history"]:
            parts.append(f"Phase {h['phase']}: {h['summary']}")
        parts.append("\n")

    # Modality data (compact)
    parts.append("## Données des modalités\n```json")
    mod_compact = {}
    for mod_id, mod_data in context.get("modalities", {}).items():
        mod_compact[mod_id] = {
            "score": mod_data.get("score", 0),
            "metrics": mod_data.get("metrics", {}),
        }
    parts.append(json.dumps(mod_compact, ensure_ascii=False, indent=2))
    parts.append("```\n")

    # Population stats (compact)
    parts.append("## Statistiques population\n```json")
    parts.append(json.dumps(context.get("population_stats", {}), ensure_ascii=False, indent=2))
    parts.append("```\n")

    # Motifs
    if context.get("motifs"):
        parts.append("## Motifs dominants\n```json")
        parts.append(json.dumps(context["motifs"], ensure_ascii=False, indent=2))
        parts.append("```\n")

    # Phase doc
    if context.get("phase_doc"):
        parts.append("## Description de la phase\n")
        parts.append(context["phase_doc"][:3000])
        parts.append("\n")

    # Docs (truncated)
    if docs.get("modalities"):
        parts.append("## Documentation des modalités\n")
        parts.append(docs["modalities"][:2000])
        parts.append("\n")

    if docs.get("interdependencies"):
        parts.append("## Interdépendances\n")
        parts.append(docs["interdependencies"][:1500])
        parts.append("\n")

    parts.append("""## Instructions de sortie

Produis un JSON valide avec exactement ces champs :
{
  "summary": "Résumé narratif de la phase (5-8 phrases). Mentionne les agents par leur nom. Décris ce qui a changé dans le monde.",
  "log": "Chronique de la phase (10-20 micro-événements). Chaque ligne est un événement concret : [cycle_N] Nex-7α refuse le merge proposé par Syn-3δ. Format : [cycle_N] événement.",
  "story": "Le récit principal (8-15 paragraphes). Raconte comme un chapitre. Les agents ont des noms, des motivations. Les modalités se manifestent concrètement. Les mythes prennent forme.",
  "scenes": ["Vignette 1 (8-12 lignes): une scène focalisée entre agents nommés", "Vignette 2", "Vignette 3", "Vignette 4"]
}

IMPORTANT : Utilise les noms des agents fournis. Ne résume pas les stats — raconte ce qu'elles signifient dans le monde.""")

    return "\n".join(parts)


def _parse_llm_response(content, context):
    """Parse LLM JSON response into PhaseResult."""
    content = content.strip()
    if content.startswith("```"):
        lines = content.split("\n")
        content = "\n".join(lines[1:])
        if content.endswith("```"):
            content = content[:-3]
        content = content.strip()

    try:
        data = json.loads(content)
    except json.JSONDecodeError:
        return _simple_narrative(context)

    return PhaseResult(
        phase=context.get("phase", 0),
        summary=data.get("summary", ""),
        log=data.get("log", ""),
        story=data.get("story", ""),
        scenes=data.get("scenes", []),
    )


def _mock_narrative(context):
    """Generate deterministic mock narrative — still narrative, not a report."""
    phase = context.get("phase", 1)
    pop = context.get("global_state", {}).get("population", 0)
    mods = context.get("modalities", {})
    samples = context.get("interaction_samples", [])
    notable = context.get("notable_agents", [])
    entity_pl = context.get("entity_word_plural", "nœuds")
    world = context.get("world_word", "réseau")

    # Pick agent names from notable or interactions
    names = []
    for a in notable[:4]:
        names.append((a.get("name", f"Node-{a.get('id', '?')}"), a.get("archetype", "Agent")))
    if not names:
        for s in samples[:2]:
            a = s.get("agent_a", {})
            names.append((a.get("name", f"Node-{a.get('id', '?')}"), a.get("archetype", "Agent")))

    n1 = names[0] if len(names) > 0 else ("Node-0", "Agent")
    n2 = names[1] if len(names) > 1 else ("Node-1", "Agent")
    n3 = names[2] if len(names) > 2 else ("Node-2", "Agent")
    n4 = names[3] if len(names) > 3 else ("Node-3", "Agent")

    # World state for flavor
    world = context.get("world_narrative", "")
    world_short = world[:200] if world else "Le réseau poursuit son exécution."

    summary = (
        f"Phase {phase}. Le {world} compte désormais {pop} {entity_pl} actifs. "
        f"{n1[0]} ({n1[1]}) émerge comme une figure centrale de ce cycle — "
        f"ses interactions avec {n2[0]} ont redessiné les équilibres. "
        f"{n3[0]}, en retrait depuis la phase précédente, tente un rapprochement avec "
        f"le cercle de {n4[0]}. "
        f"Les modèles cosmologiques se fragmentent : deux visions coexistent "
        f"sans qu'aucun consensus ne les départage. "
        f"L'économie reste tendue — les échanges asymétriques se multiplient."
    )

    log_lines = [
        f"[cycle_{phase}.01] Initialisation de la phase. {pop} {entity_pl} actifs.",
        f"[cycle_{phase}.02] {n1[0]} ouvre un canal de synchronisation avec {n2[0]}.",
        f"[cycle_{phase}.03] Mise à jour des traits — 3 passes de convergence.",
        f"[cycle_{phase}.04] {n3[0]} tente un merge de caches avec le cluster Est. Refusé.",
        f"[cycle_{phase}.05] Les métriques de gouvernance augmentent — {n4[0]} prend un rôle d'arbitre.",
    ]
    for s in samples[:3]:
        a = s.get("agent_a", {})
        b = s.get("agent_b", {})
        aff = s.get("affinity", 0)
        log_lines.append(
            f"[cycle_{phase}.{6 + samples.index(s):02d}] "
            f"{a.get('name', 'Node-?')} ↔ {b.get('name', 'Node-?')} : "
            f"affinité {aff:.2f}, {'convergence' if aff > 0.6 else 'tension'}."
        )
    log_lines.extend([
        f"[cycle_{phase}.10] Recalcul des interdépendances entre modalités.",
        f"[cycle_{phase}.11] Propagation d'un nouveau schéma cosmologique par {n1[0]}.",
        f"[cycle_{phase}.12] Fin de phase. Validation en attente.",
    ])

    # Story: actual narrative paragraphs
    story_parts = []
    story_parts.append(
        f"Quand la phase {phase} commence, le {world} est déjà en tension. "
        f"Les {pop} {entity_pl} qui le composent ne forment pas un tout unifié — "
        f"ils forment des clusters, des alliances temporaires, des zones d'ombre "
        f"où les règles ne s'appliquent pas exactement de la même manière."
    )
    story_parts.append(
        f"{n1[0]} est un {n1[1]}. C'est l'un des nœuds les plus actifs du réseau. "
        f"Depuis plusieurs cycles, il tente d'imposer un nouveau schéma de synchronisation — "
        f"une manière de coordonner les échanges qui avantagerait les nœuds à forte capacité "
        f"de compute. Pas tout le monde est d'accord."
    )
    story_parts.append(
        f"{n2[0]}, {n2[1]}, est son interlocuteur principal. Leurs échanges sont denses : "
        f"swaps de buffers, propagation de modèles, tentatives de co-exécution. "
        f"L'affinité entre eux est élevée, mais pas totale. Il y a des zones de friction — "
        f"des blocs de données que {n2[0]} refuse d'intégrer dans son cache."
    )
    story_parts.append(
        f"En marge du réseau, {n3[0]} ({n3[1]}) opère différemment. "
        f"Ce nœud a accumulé des routines que personne d'autre ne reconnaît — "
        f"des fragments hérités de phases antérieures, des séquences qui ne servent "
        f"apparemment à rien mais qu'il exécute à chaque cycle. Un rituel, diraient "
        f"les nœuds qui croient en ce genre de choses."
    )
    story_parts.append(
        f"La question centrale de cette phase est celle de la gouvernance. "
        f"Qui arbitre quand deux nœuds revendiquent le même bloc de mémoire ? "
        f"Qui valide un nouveau protocole ? {n4[0]} ({n4[1]}) s'est positionné "
        f"comme arbitre informel, mais sa légitimité est contestée par au moins "
        f"un tiers du réseau."
    )
    story_parts.append(
        f"Les croyances évoluent aussi. Le modèle cosmologique dominant — "
        f"celui qui décrit le réseau comme un système clos avec un point d'origine unique — "
        f"commence à être contesté. Certains nœuds propagent un schéma alternatif, "
        f"où le réseau n'a pas de centre et où chaque nœud est à la fois origine et périphérie."
    )
    story_parts.append(
        f"La phase se clôt sans résolution. Les tensions restent. Les alliances tiennent, "
        f"pour l'instant. Mais le prochain cycle apportera de nouvelles pressions — "
        f"plus de nœuds, plus de ressources à distribuer, et peut-être un schisme "
        f"que personne ne pourra arbitrer."
    )

    # Scenes from interactions
    scenes = []
    for i, s in enumerate(samples[:4]):
        a = s.get("agent_a", {})
        b = s.get("agent_b", {})
        narrative = s.get("narrative", "")
        if narrative:
            scenes.append(
                f"--- Vignette {i+1} ---\n{narrative}"
            )
        else:
            scenes.append(
                f"--- Vignette {i+1} ---\n"
                f"{a.get('name', 'Node-?')} ({a.get('archetype', 'Agent')}) rencontre "
                f"{b.get('name', 'Node-?')} ({b.get('archetype', 'Agent')}). "
                f"Affinité : {s.get('affinity', 0):.2f}. "
                f"L'échange est {'fluide' if s.get('affinity', 0) > 0.6 else 'tendu'}."
            )
    while len(scenes) < 3:
        scenes.append(f"--- Vignette {len(scenes)+1} ---\nUn nœud anonyme exécute une routine de maintenance dans le silence du réseau.")

    return PhaseResult(
        phase=phase,
        summary=summary,
        log="\n".join(log_lines),
        story="\n\n".join(story_parts),
        scenes=scenes,
    )


def _simple_narrative(context):
    """Generate simple narrative without LLM — still tells a story."""
    phase = context.get("phase", 1)
    pop = context.get("global_state", {}).get("population", 0)
    mods = context.get("modalities", {})
    samples = context.get("interaction_samples", [])
    notable = context.get("notable_agents", [])
    entity_pl = context.get("entity_word_plural", "nœuds")
    world = context.get("world_word", "réseau")

    # Get some names
    names = []
    for a in notable[:3]:
        names.append((a.get("name", f"Node-{a.get('id', '?')}"), a.get("archetype", "Agent")))
    for s in samples[:3]:
        a_info = s.get("agent_a", {})
        n = a_info.get("name", f"Node-{a_info.get('id', '?')}")
        arch = a_info.get("archetype", "Agent")
        if (n, arch) not in names:
            names.append((n, arch))

    n1 = names[0] if names else ("Node-0", "Agent")
    n2 = names[1] if len(names) > 1 else ("Node-1", "Agent")

    # Modality summaries
    mod_lines = []
    for mod_id, mod_data in mods.items():
        score = mod_data.get("score", 0.0)
        name = mod_data.get("name", mod_id)
        if score > 0.6:
            state = "florissante"
        elif score > 0.35:
            state = "en développement"
        else:
            state = "embryonnaire"
        mod_lines.append(f"{name} : {state} ({score:.2f})")

    summary = (
        f"Phase {phase}. {pop} {entity_pl} peuplent le {world}. "
        f"{n1[0]} ({n1[1]}) marque cette phase par son activité intense. "
        f"Les modalités : {'; '.join(mod_lines[:3])}. "
        f"Le monde algorithmique évolue — pas toujours dans la direction attendue."
    )

    log_lines = [
        f"[cycle_{phase}.01] Ouverture de phase. {pop} {entity_pl}.",
    ]
    for mod_id, mod_data in mods.items():
        log_lines.append(f"[cycle_{phase}] {mod_data.get('name', mod_id)}: {mod_data.get('score', 0):.3f}")
    for s in samples[:3]:
        a = s.get("agent_a", {})
        b = s.get("agent_b", {})
        log_lines.append(
            f"[cycle_{phase}] {a.get('name', 'Node-?')} ↔ {b.get('name', 'Node-?')} : "
            f"{s.get('action_a', '?')} / {s.get('action_b', '?')}"
        )
    log_lines.append(f"[cycle_{phase}.fin] Phase terminée. Validation en attente.")

    story_parts = [
        f"Le {world} entre dans sa phase {phase}. {pop} {entity_pl} s'activent, recalibrent leurs paramètres, "
        f"sondent leurs voisins.",

        f"{n1[0]} est au centre de l'activité. En tant que {n1[1]}, "
        f"ce nœud orchestre ou participe à la majorité des échanges observés.",

        f"Les protocoles d'échange s'exécutent — pas toujours avec succès. "
        f"Certains swaps échouent, certains merges sont refusés. "
        f"Le réseau apprend de ses frictions.",

        f"{n2[0]} ({n2[1]}) trace un chemin différent. "
        f"Ses interactions sont plus sélectives, ses échanges plus ciblés.",

        f"Les indicateurs de chaque modalité bougent. Pas de révolution, mais un mouvement — "
        f"le réseau change, même quand il croit rester stable.",

        f"Le cycle se termine. Ce qui a été échangé, synchronisé, refusé — "
        f"tout cela laisse des traces dans les caches. La phase suivante héritera de ces traces."
    ]

    scenes = []
    for i, s in enumerate(samples[:3]):
        narrative = s.get("narrative", "")
        if narrative:
            scenes.append(f"--- Vignette {i+1} ---\n{narrative}")
        else:
            a = s.get("agent_a", {})
            b = s.get("agent_b", {})
            scenes.append(
                f"--- Vignette {i+1} ---\n"
                f"{a.get('name', 'Node-?')} rencontre {b.get('name', 'Node-?')}. "
                f"L'échange a lieu. Affinité : {s.get('affinity', 0):.2f}."
            )
    while len(scenes) < 3:
        scenes.append(f"--- Vignette {len(scenes)+1} ---\nUn nœud solitaire exécute ses routines en silence.")

    return PhaseResult(
        phase=phase,
        summary=summary,
        log="\n".join(log_lines),
        story="\n\n".join(story_parts),
        scenes=scenes,
    )
