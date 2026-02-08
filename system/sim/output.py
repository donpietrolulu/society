"""Output file writing for simulation phases."""
import json
import os

from system.sim.constants import TRAIT_LABELS, ARCHETYPES, INDICATOR_LABELS
from system.sim.logger import write_events


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def write_state(output_dir, phase, state_dict):
    """Write phase state JSON."""
    phase_dir = os.path.join(output_dir, f"phase_{phase}")
    ensure_dir(phase_dir)
    path = os.path.join(phase_dir, "state.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state_dict, f, ensure_ascii=False, indent=2)


def write_phase_outputs(output_dir, phase, result, metrics, state,
                        individuals, interactions, modalities_detail,
                        ordered_mods, drama_pack=None, chronique_md=None,
                        interactions_md=None, cast_md=None, artifacts_md=None,
                        events=None):
    """Write all output files for a phase."""
    phase_dir = os.path.join(output_dir, f"phase_{phase}")
    ensure_dir(phase_dir)

    # metrics.json
    _write_json(phase_dir, "metrics.json", metrics)

    # checks.json
    _write_json(phase_dir, "checks.json", result.checks)

    # state.json
    _write_json(phase_dir, "state.json", state)

    # summary.md
    _write_md(phase_dir, "summary.md",
              f"# Résumé — Phase {phase}\n\n{result.summary}")

    # log.md
    _write_md(phase_dir, "log.md",
              f"# Journal — Phase {phase}\n\n{result.log}")

    # story.md
    _write_md(phase_dir, "story.md",
              f"# Récit — Phase {phase}\n\n{result.story}")

    # agents.md
    agents_md = _format_agents(phase, individuals)
    _write_md(phase_dir, "agents.md", agents_md)

    # interactions.md (legacy agent interactions)
    inter_md = _format_interactions(phase, interactions)
    _write_md(phase_dir, "interactions.md", inter_md)

    # journal.md
    _write_md(phase_dir, "journal.md",
              f"# Journal de phase — Phase {phase}\n\n{result.log}")

    # modalites.md
    mod_content = _format_modalities(phase, modalities_detail, ordered_mods)
    _write_md(phase_dir, "modalites.md", mod_content)

    # --- New narrative files ---

    # chronique.md
    if chronique_md:
        _write_md(phase_dir, "chronique.md", chronique_md)

    # societe_interactions.md
    if interactions_md:
        _write_md(phase_dir, "societe_interactions.md", interactions_md)

    # cast.md
    if cast_md:
        _write_md(phase_dir, "cast.md", cast_md)

    # artifacts.md
    if artifacts_md:
        _write_md(phase_dir, "artifacts.md", artifacts_md)

    # events.jsonl
    if events:
        write_events(phase_dir, events)

    # compte_rendu.md (enriched)
    cr_content = _format_compte_rendu(phase, result, drama_pack)
    _write_md(phase_dir, "compte_rendu.md", cr_content)


def _write_json(directory, filename, data):
    path = os.path.join(directory, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _write_md(directory, filename, content):
    path = os.path.join(directory, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _format_agents(phase, individuals):
    lines = [f"# Agents — Phase {phase}\n"]
    lines.append(f"Population : {len(individuals)} agents\n")
    for ind in individuals[:50]:  # Cap display at 50
        archetype = ARCHETYPES.get(
            max(ind.traits, key=ind.traits.get) if ind.traits else "",
            "Agent"
        )
        traits_str = ", ".join(
            f"{TRAIT_LABELS.get(t, t)}: {v:.3f}" for t, v in sorted(ind.traits.items())
        )
        lines.append(f"## Agent {ind.id} — {archetype}")
        lines.append(f"Traits : {traits_str}\n")
    if len(individuals) > 50:
        lines.append(f"\n... et {len(individuals) - 50} agents supplémentaires.")
    return "\n".join(lines)


def _format_interactions(phase, interactions):
    lines = [f"# Interactions — Phase {phase}\n"]
    for i, inter in enumerate(interactions):
        a = inter["agent_a"]
        b = inter["agent_b"]
        lines.append(f"## Interaction {i+1}")
        lines.append(
            f"Agent {a['id']} ({a['archetype']}) — {inter['action_a']} "
            f"↔ Agent {b['id']} ({b['archetype']}) — {inter['action_b']}"
        )
        lines.append(f"Affinité : {inter['affinity']:.3f}\n")
    return "\n".join(lines)


def _format_modalities(phase, modalities_detail, ordered_mods):
    lines = [f"# Modalités — Phase {phase}\n"]
    for mod_id in ordered_mods:
        mod = modalities_detail[mod_id]
        lines.append(f"## {mod.name}")
        lines.append(f"**Score global** : {mod.score:.3f}\n")
        lines.append(f"**Définition** : {mod.definition}\n")
        lines.append("**Indicateurs** :")
        for ind in mod.indicators:
            label = INDICATOR_LABELS.get(ind, ind)
            val = mod.metrics.get(ind, 0.0)
            lines.append(f"  - {label} ({ind}) : {val:.3f}")
        lines.append("")
    return "\n".join(lines)


def _format_compte_rendu(phase, result, drama_pack=None):
    """Format enriched compte_rendu.md with drama pack data."""
    lines = [f"# Compte rendu — Phase {phase}\n"]

    # Summary
    lines.append(f"## Résumé\n{result.summary}\n")

    if drama_pack:
        # Grand événement
        beat = drama_pack.get("beat", {})
        if beat:
            lines.append(f"## Grand événement : {beat.get('label', 'Inconnu')}\n")
            lines.append(f"{beat.get('description', '')}\n")

        # Cast focus
        cast = drama_pack.get("cast", [])
        if cast:
            lines.append("## Personnages focus\n")
            for c in cast[:5]:
                p = c.get("persona", {})
                lines.append(f"- **{p.get('role', 'Inconnu')}** (Agent {c.get('individual_id', '?')}, "
                             f"faction : {c.get('faction', 'aucune')})")
            lines.append("")

        # Artifacts
        artifacts = drama_pack.get("artifacts", [])
        if artifacts:
            lines.append("## Artefacts\n")
            for a in artifacts:
                title = a.get("title", "") if isinstance(a, dict) else getattr(a, "title", "")
                aid = a.get("id", "") if isinstance(a, dict) else getattr(a, "id", "")
                lines.append(f"- `{aid}` — {title}")
            lines.append("")

        # Factions
        factions = drama_pack.get("factions", [])
        if factions:
            lines.append("## Factions actives\n")
            for f in factions:
                lines.append(f"- **{f['name']}** — « {f.get('motto', '')} »")
            lines.append("")

    # Scenes
    lines.append("## Scènes\n")
    for i, scene in enumerate(result.scenes):
        lines.append(f"### Scène {i+1}\n{scene}\n")

    return "\n".join(lines)
