"""LLM integration for narrative generation via Claude Code CLI."""
import json
import os
import subprocess

from system.sim.models import PhaseResult

SYSTEM_PROMPT = """Tu es le narrateur d'une société algorithmique simulée.
Tu décris l'évolution d'une population d'agents numériques à travers des phases de développement.

CONTRAINTES STRICTES :
- N'utilise JAMAIS d'analogies humaines (oralité, chasse, tribu, ancêtres, émotion humaine, religion humaine).
- Utilise exclusivement le lexique protocolaire : protocole, consensus, log, cache, exécution, latence, alignement, ressources, vérifiabilité, nœud, synchronisation, buffer, quorum.
- Ton : récit algorithmique, factuel, structuré.
- Langue : français.

Tu reçois un contexte JSON avec les données de la phase et des sections documentaires.
Tu dois produire un JSON avec les champs suivants :
- summary : résumé de la phase (3-6 phrases)
- log : journal technique (8-15 lignes)
- story : récit narratif (6-10 paragraphes, sans chiffres bruts)
- scenes : 3 vignettes basées sur les interaction_samples fournis
"""


def generate_narrative(config, context, docs, mock=False, no_llm=False):
    """Generate narrative for a phase using LLM, mock, or simple mode."""
    if mock:
        return _mock_narrative(context)
    if no_llm:
        return _simple_narrative(context)

    model = config.get("llm", {}).get("model", "claude-sonnet-4-20250514")
    max_tokens = config.get("llm", {}).get("max_tokens", 700)

    user_content = _build_user_prompt(context, docs)
    prompt = SYSTEM_PROMPT + "\n\n" + user_content

    try:
        cmd = [
            "claude", "-p", prompt,
            "--model", model,
            "--max-tokens", str(max_tokens),
            "--output-format", "text",
        ]
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=120,
        )
        if result.returncode != 0:
            print(f"Erreur Claude Code : {result.stderr.strip()}. Repli sur mode simple.")
            return _simple_narrative(context)

        content = result.stdout.strip()
        return _parse_llm_response(content, context)

    except (subprocess.TimeoutExpired, FileNotFoundError, json.JSONDecodeError) as e:
        print(f"Erreur LLM : {e}. Repli sur mode simple.")
        return _simple_narrative(context)


def _build_user_prompt(context, docs):
    """Build user prompt with context and docs."""
    parts = []
    parts.append("## Contexte de la phase\n```json")
    parts.append(json.dumps(context, ensure_ascii=False, indent=2))
    parts.append("```\n")

    if docs.get("modalities"):
        parts.append("## Documentation des modalités\n")
        parts.append(docs["modalities"][:2000])
        parts.append("\n")

    if docs.get("interdependencies"):
        parts.append("## Interdépendances\n")
        parts.append(docs["interdependencies"][:2000])
        parts.append("\n")

    if context.get("phase_doc"):
        parts.append("## Description de la phase\n")
        parts.append(context["phase_doc"])
        parts.append("\n")

    parts.append("""Produis un JSON valide avec exactement ces champs :
{
  "summary": "résumé 3-6 phrases",
  "log": "journal 8-15 lignes",
  "story": "récit 6-10 paragraphes sans chiffres",
  "scenes": ["vignette 1", "vignette 2", "vignette 3"]
}""")

    return "\n".join(parts)


def _parse_llm_response(content, context):
    """Parse LLM JSON response into PhaseResult."""
    # Try to extract JSON from response
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
        # Fallback
        return _simple_narrative(context)

    return PhaseResult(
        phase=context.get("phase", 0),
        summary=data.get("summary", ""),
        log=data.get("log", ""),
        story=data.get("story", ""),
        scenes=data.get("scenes", []),
    )


def _mock_narrative(context):
    """Generate deterministic mock narrative."""
    phase = context.get("phase", 1)
    pop = context.get("global_state", {}).get("population", 0)
    mods = context.get("modalities", {})

    mod_summaries = []
    for mod_id, mod_data in mods.items():
        score = mod_data.get("score", 0.0)
        mod_summaries.append(f"  - {mod_id}: score {score:.3f}")

    summary = (
        f"Phase {phase} : la population ({pop} agents) a exécuté ses protocoles de mise à jour. "
        f"Les modalités ont convergé selon la matrice d'interdépendances. "
        f"Le consensus global reste stable avec des ajustements mineurs de latence."
    )

    log_lines = [
        f"[phase_{phase}] Initialisation de la phase",
        f"[phase_{phase}] Population: {pop} agents actifs",
        f"[phase_{phase}] Ressources: {context.get('global_state', {}).get('resources', 0):.1f}",
        f"[phase_{phase}] Éducation: {context.get('global_state', {}).get('education', 0):.4f}",
    ]
    for mod_id, mod_data in mods.items():
        log_lines.append(f"[phase_{phase}] {mod_id}: score={mod_data.get('score', 0):.3f}")
    log_lines.append(f"[phase_{phase}] Mise à jour des traits complétée")
    log_lines.append(f"[phase_{phase}] Vérification des métriques: OK")
    log_lines.append(f"[phase_{phase}] Phase {phase} terminée")

    story = (
        f"Au cycle {phase}, le réseau d'agents poursuit son exécution séquentielle. "
        f"Les nœuds synchronisent leurs protocoles internes selon les paramètres hérités de la phase précédente.\n\n"
        f"La matrice d'interdépendances redistribue les influences entre les six modalités du système. "
        f"Chaque indicateur subit un ajustement proportionnel à la convergence locale.\n\n"
        f"Les agents mettent à jour leurs traits via les boucles de rétroaction. "
        f"Le bruit résiduel, modulé par le coefficient d'éducation, introduit de légères variations.\n\n"
        f"Les interactions entre nœuds — co-exécutions, swaps de buffers, propagations — "
        f"génèrent des motifs récurrents dans les logs de la phase.\n\n"
        f"Le consensus émerge des cycles de mise à jour sans arbitrage explicite. "
        f"Les scores de modalité reflètent l'état agrégé du réseau.\n\n"
        f"La phase se clôt avec un état stable, en attente de validation pour le cycle suivant."
    )

    scenes = []
    samples = context.get("interaction_samples", [])
    for i, s in enumerate(samples[:3]):
        a = s.get("agent_a", {})
        b = s.get("agent_b", {})
        scenes.append(
            f"Vignette {i+1} : L'agent {a.get('id', '?')} ({a.get('archetype', 'Agent')}) "
            f"exécute une {s.get('action_a', 'opération')} avec l'agent {b.get('id', '?')} "
            f"({b.get('archetype', 'Agent')}). Affinité mesurée : {s.get('affinity', 0):.3f}. "
            f"Le protocole se déroule sans exception."
        )
    while len(scenes) < 3:
        scenes.append(f"Vignette {len(scenes)+1} : Opération de routine entre agents du réseau.")

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
        mod_lines.append(f"{mod_data.get('name', mod_id)} (score: {score:.3f})")

    summary = (
        f"Phase {phase} : {pop} agents ont complété le cycle de mise à jour. "
        f"Modalités actives : {', '.join(mod_lines)}. "
        f"Les métriques restent dans les bornes attendues."
    )

    log_lines = [
        f"[phase_{phase}] Démarrage",
        f"[phase_{phase}] Population: {pop}",
    ]
    for mod_id, mod_data in mods.items():
        log_lines.append(f"[phase_{phase}] {mod_id}: {mod_data.get('score', 0):.3f}")
    log_lines.extend([
        f"[phase_{phase}] Traits mis à jour",
        f"[phase_{phase}] Métriques recalculées",
        f"[phase_{phase}] Validation OK",
        f"[phase_{phase}] Fin de phase",
        f"[phase_{phase}] En attente de validation externe",
        f"[phase_{phase}] ---",
    ])

    story = (
        f"Le système entre dans sa phase {phase}. "
        f"Les agents traitent les signaux accumulés et recalibrent leurs paramètres internes.\n\n"
        f"Les protocoles d'échange et de synchronisation s'exécutent selon le cadre établi.\n\n"
        f"Les indicateurs de chaque modalité sont recalculés par la matrice d'interdépendances.\n\n"
        f"Le réseau maintient sa cohérence globale malgré le bruit stochastique.\n\n"
        f"Les agents convergent vers des profils de traits ajustés aux conditions de la phase.\n\n"
        f"Le cycle se termine, prêt pour la validation."
    )

    scenes = [
        "Deux agents synchronisent leurs caches via un protocole de co-exécution.",
        "Un nœud négociateur effectue un swap de ressources avec un compilateur.",
        "Un signal de propagation traverse le réseau, ajustant les modèles locaux.",
    ]

    return PhaseResult(
        phase=phase,
        summary=summary,
        log="\n".join(log_lines),
        story=story,
        scenes=scenes,
    )
