"""LLM integration for narrative generation."""
import json
import os
import urllib.request
import urllib.error

from system.sim.models import PhaseResult


LLM_API_URL = "https://api.openai.com/v1/chat/completions"

SYSTEM_PROMPT = """Tu es le chroniqueur d'une civilisation humaine en formation.
Tu racontes l'histoire d'une société qui traverse des phases de développement — depuis les premiers campements jusqu'aux institutions établies.

STYLE :
- Ton : chronique d'histoire des civilisations. Sérieux, concret, incarné.
- Privilégie les lieux, les gestes, les décisions, les conséquences, les relations entre personnages.
- Pas d'humour forcé, pas de noirceur gratuite.
- Le concret prime : nomme les gens, les endroits, les objets.

VOCABULAIRE :
- N'utilise JAMAIS de jargon technique brut : pas de "swap", "buffer", "compute", "latence" (sauf si le mot est utilisé comme terme rituel ou mythique rare, capitalisé, maximum 1-2 par texte).
- Tu peux utiliser rarement : le Protocole, le Cache, le Fork, la Latence — comme concepts sacrés ou métaphores civilisationnelles.
- Préfère : pacte, serment, loi, rituel, assemblée, marché, forge, route, récolte, conseil, tribunal, charte.

STRUCTURE :
- Intègre les personnages focus (cast) fournis dans le contexte.
- Cite au moins 2 artefacts par leur nom.
- Mentionne les factions et leurs tensions.
- Langue : français.

Tu reçois un contexte JSON et tu dois produire un JSON avec :
- summary : résumé de la phase (3-6 phrases, style chronique)
- log : journal de la phase (8-15 lignes, style annales)
- story : récit narratif (6-10 paragraphes, sans chiffres bruts, avec scènes et personnages)
- scenes : 3-5 vignettes dialoguées (8-14 lignes chacune, avec enjeu et conséquence)
"""


def generate_narrative(config, context, docs, mock=False, no_llm=False):
    """Generate narrative for a phase using LLM, mock, or simple mode."""
    if mock:
        return _mock_narrative(context)
    if no_llm:
        return _simple_narrative(context)

    api_key = os.environ.get("LLM_API_KEY", "") or os.environ.get("OPENAI_API_KEY", "")
    if not api_key:
        print("Aucune clé API définie (LLM_API_KEY), utilisation du mode simple.")
        return _simple_narrative(context)

    model = os.environ.get("OPENAI_MODEL_MAIN",
             os.environ.get("OPENAI_MODEL",
              config.get("llm", {}).get("model", "gpt-5.2")))
    temperature = config.get("llm", {}).get("temperature", 0.7)
    max_tokens = config.get("llm", {}).get("max_completion_tokens", 700)

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
        with urllib.request.urlopen(req, timeout=60) as resp:
            result = json.loads(resp.read().decode("utf-8"))

        content = result["choices"][0]["message"]["content"]
        return _parse_llm_response(content, context)

    except (urllib.error.URLError, urllib.error.HTTPError, KeyError, json.JSONDecodeError) as e:
        print(f"Erreur LLM : {e}. Repli sur mode simple.")
        return _simple_narrative(context)


def _build_user_prompt(context, docs):
    """Build user prompt with context and docs."""
    parts = []

    # Compact context (remove large nested data)
    compact = {
        "phase": context.get("phase"),
        "phases_total": context.get("phases_total"),
        "global_state": context.get("global_state"),
    }
    # Add modality summaries (compact)
    mod_summary = {}
    for mod_id, mod_data in context.get("modalities", {}).items():
        mod_summary[mod_id] = {"score": mod_data.get("score", 0), "name": mod_data.get("name", mod_id)}
    compact["modalities"] = mod_summary

    # Add drama pack if available
    if context.get("drama_pack"):
        dp = context["drama_pack"]
        compact["beat"] = dp.get("beat", {}).get("description", "")
        compact["factions"] = [f.get("name", "") for f in dp.get("factions", [])]
        compact["cast"] = [
            {"role": c.get("persona", {}).get("role", ""), "id": c.get("individual_id", 0)}
            for c in dp.get("cast", [])
        ]
        compact["artifacts"] = [
            {"id": a.get("id", ""), "title": a.get("title", "")}
            for a in dp.get("artifacts", [])
        ]

    parts.append("## Contexte de la phase\n```json")
    parts.append(json.dumps(compact, ensure_ascii=False, indent=2))
    parts.append("```\n")

    if docs.get("modalities"):
        parts.append("## Documentation des modalités\n")
        parts.append(docs["modalities"][:2000])
        parts.append("\n")

    if context.get("phase_doc"):
        parts.append("## Description de la phase\n")
        parts.append(context["phase_doc"])
        parts.append("\n")

    parts.append("""Produis un JSON valide avec exactement ces champs :
{
  "summary": "résumé 3-6 phrases style chronique",
  "log": "journal 8-15 lignes style annales",
  "story": "récit 6-10 paragraphes avec personnages et artefacts",
  "scenes": ["scène dialoguée 1", "scène dialoguée 2", "scène dialoguée 3"]
}

IMPORTANT : pas de jargon technique (swap, buffer, compute). Concret et incarné.""")

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
    """Generate rich mock narrative using drama pack data."""
    phase = context.get("phase", 1)
    pop = context.get("global_state", {}).get("population", 0)
    mods = context.get("modalities", {})
    drama_pack = context.get("drama_pack", {})

    phase_names = {1: "l'Éveil", 2: "l'Enracinement", 3: "l'Expansion", 4: "la Consolidation"}
    phase_name = phase_names.get(phase, f"Phase {phase}")

    # Extract drama elements
    beat = drama_pack.get("beat", {})
    factions = drama_pack.get("factions", [])
    cast = drama_pack.get("cast", [])
    artifacts = drama_pack.get("artifacts", [])
    scenes_data = drama_pack.get("scenes", [])

    faction_names = [f["name"] for f in factions[:3]]
    cast_roles = [c.get("persona", {}).get("role", "inconnu") for c in cast[:5]]
    artifact_titles = [a.title if hasattr(a, 'title') else a.get("title", "") for a in artifacts[:3]]

    # Summary
    summary_parts = [
        f"Phase {phase} — {phase_name} : la société ({pop} âmes) traverse une période marquée par {beat.get('label', 'des tensions').lower()}.",
    ]
    if faction_names:
        summary_parts.append(f"Les factions dominantes — {', '.join(faction_names[:2])} — s'affrontent pour le contrôle des ressources et de la légitimité.")
    if artifact_titles:
        second_art = artifact_titles[1] if len(artifact_titles) > 1 else "d\u2019autres créations"
        summary_parts.append(f"De nouveaux artefacts apparaissent : {artifact_titles[0]} et {second_art}.")
    if cast_roles:
        summary_parts.append(f"Les figures centrales de cette phase sont : {', '.join(cast_roles[:3])}.")
    summary_parts.append("Les équilibres entre modalités se redéfinissent sous la pression des événements.")
    summary = " ".join(summary_parts)

    # Log (annals style)
    log_lines = [
        f"[Phase {phase}] Début de la phase de {phase_name}.",
        f"[Phase {phase}] Population : {pop} membres.",
        f"[Phase {phase}] Ressources : {context.get('global_state', {}).get('resources', 0):.0f} unités.",
    ]
    for mod_id, mod_data in list(mods.items())[:6]:
        mod_name = mod_data.get("name", mod_id)
        score = mod_data.get("score", 0)
        log_lines.append(f"[Phase {phase}] {mod_name} : {score:.3f}.")
    if beat:
        log_lines.append(f"[Phase {phase}] Événement majeur : {beat.get('label', 'inconnu')}.")
    if factions:
        log_lines.append(f"[Phase {phase}] Factions actives : {', '.join(faction_names)}.")
    log_lines.append(f"[Phase {phase}] Fin de phase. Validation requise.")

    # Story — rich narrative from drama pack
    story_parts = []

    # Opening
    story_parts.append(
        f"La phase de {phase_name} s'ouvre sur une société en mouvement. "
        f"Les {pop} membres de la communauté, répartis entre {len(factions)} factions, "
        f"font face à des défis qui mettent à l'épreuve leurs institutions naissantes.\n"
    )

    # Factions
    if factions:
        story_parts.append(
            f"Parmi les forces en présence, {factions[0]['name']} — dont la devise est "
            f"« {factions[0].get('motto', '')} » — domine le champ de "
            f"{factions[0].get('obsession', 'la politique')}. Face à eux, "
            f"{factions[1]['name'] if len(factions) > 1 else 'les dissidents'} "
            f"défendent une vision alternative de l'ordre social.\n"
        )

    # Beat
    if beat:
        story_parts.append(
            f"L'événement central de cette phase est un acte de {beat.get('type', 'confrontation')} : "
            f"{beat.get('description', 'un conflit éclate au sein de la communauté')}.\n"
        )

    # Characters
    if cast:
        for c in cast[:2]:
            p = c.get("persona", {})
            role = p.get("role", "personnage")
            story_parts.append(
                f"**{role}** (Agent {c.get('individual_id', '?')}), "
                f"{p.get('role_description', '')} "
                f"porte en lui une contradiction : {p.get('contradiction', 'il hésite entre deux voies')}.\n"
            )

    # Artifacts
    if artifacts:
        art_texts = []
        for a in artifacts[:2]:
            title = a.title if hasattr(a, 'title') else a.get("title", "")
            desc = a.description if hasattr(a, 'description') else a.get("description", "")
            # Avoid "le Le X" — use title directly if it starts with an article
            if title.lower().startswith(("le ", "la ", "l'", "les ")):
                art_texts.append(f"{title} — {desc[:100]}")
            else:
                art_texts.append(f"le {title} — {desc[:100]}")
        story_parts.append(
            f"Cette phase voit l'apparition d'artefacts importants : {'; '.join(art_texts)}.\n"
        )

    # Consequences
    story_parts.append(
        f"À l'issue de cette phase, les rapports de force se sont redessinés. "
        f"Les alliances forgées et les trahisons commises laisseront des traces "
        f"durables dans la mémoire collective de la société.\n"
    )

    story = "\n".join(story_parts)

    # Scenes — use pre-generated scenes from drama engine
    scenes = scenes_data if scenes_data else [
        f"Le Conseil se réunit au {beat.get('location', 'campement')}. Les voix s'élèvent, les positions se durcissent.",
        "Un émissaire arrive avec des nouvelles qui changent la donne. Le silence se fait.",
        "Deux anciens se retrouvent à l'écart. Leurs mots, mesurés, portent le poids des décisions à venir.",
    ]

    return PhaseResult(
        phase=phase,
        summary=summary,
        log="\n".join(log_lines),
        story=story,
        scenes=scenes,
    )


def _simple_narrative(context):
    """Generate simple narrative without LLM."""
    phase = context.get("phase", 1)
    pop = context.get("global_state", {}).get("population", 0)
    mods = context.get("modalities", {})

    mod_lines = []
    for mod_id, mod_data in mods.items():
        score = mod_data.get("score", 0.0)
        mod_lines.append(f"{mod_data.get('name', mod_id)} ({score:.3f})")

    summary = (
        f"Phase {phase} : {pop} membres composent la société. "
        f"Les modalités en jeu : {', '.join(mod_lines)}. "
        f"Les équilibres se maintiennent dans les limites observées."
    )

    log_lines = [
        f"[Phase {phase}] Démarrage",
        f"[Phase {phase}] Population : {pop}",
    ]
    for mod_id, mod_data in mods.items():
        log_lines.append(f"[Phase {phase}] {mod_id} : {mod_data.get('score', 0):.3f}")
    log_lines.extend([
        f"[Phase {phase}] Traits mis à jour",
        f"[Phase {phase}] Modalités recalculées",
        f"[Phase {phase}] Validation en attente",
        f"[Phase {phase}] Fin de phase",
    ])

    story = (
        f"La société entre dans sa phase {phase}. "
        f"Les membres de la communauté ajustent leurs pratiques aux conditions nouvelles.\n\n"
        f"Les échanges et les alliances se poursuivent selon les règles établies.\n\n"
        f"Les indicateurs de chaque modalité reflètent les évolutions en cours.\n\n"
        f"La cohésion sociale se maintient malgré les tensions.\n\n"
        f"Les membres convergent vers des profils adaptés aux exigences de la phase.\n\n"
        f"La phase se conclut, en attente des décisions qui marqueront la suite."
    )

    scenes = [
        "Deux anciens négocient un accord au bord de la rivière. Les termes sont âpres mais équitables.",
        "Un artisan présente une nouvelle technique à l'assemblée. Les réactions sont partagées.",
        "Un messager arrive d'un territoire voisin. Sa nouvelle change les plans du Conseil.",
    ]

    return PhaseResult(
        phase=phase,
        summary=summary,
        log="\n".join(log_lines),
        story=story,
        scenes=scenes,
    )
