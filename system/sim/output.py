"""Output file writing for simulation phases."""
import json
import os

from system.sim.constants import TRAIT_LABELS, ARCHETYPES, INDICATOR_LABELS


def ensure_dir(path):
    os.makedirs(path, exist_ok=True)


def write_state(output_dir, phase, state_dict):
    """Write phase state JSON."""
    ensure_dir(output_dir)
    path = os.path.join(output_dir, f"phase_{phase}_state.json")
    with open(path, "w", encoding="utf-8") as f:
        json.dump(state_dict, f, ensure_ascii=False, indent=2)


def write_phase_outputs(output_dir, phase, result, metrics, state,
                        individuals, interactions, modalities_detail,
                        ordered_mods):
    """Write all output files for a phase."""
    ensure_dir(output_dir)
    cr_dir = os.path.join(output_dir, "comptes_rendus")
    mod_dir = os.path.join(output_dir, "modalites")
    ensure_dir(cr_dir)
    ensure_dir(mod_dir)

    # phase_N_metrics.json
    _write_json(output_dir, f"phase_{phase}_metrics.json", metrics)

    # phase_N_checks.json
    _write_json(output_dir, f"phase_{phase}_checks.json", result.checks)

    # phase_N_state.json
    _write_json(output_dir, f"phase_{phase}_state.json", state)

    # phase_N_summary.md
    _write_md(output_dir, f"phase_{phase}_summary.md",
              f"# Résumé — Phase {phase}\n\n{result.summary}")

    # phase_N_log.md
    _write_md(output_dir, f"phase_{phase}_log.md",
              f"# Journal — Phase {phase}\n\n{result.log}")

    # phase_N_story.md
    _write_md(output_dir, f"phase_{phase}_story.md",
              f"# Récit — Phase {phase}\n\n{result.story}")

    # phase_N_agents.md
    agents_md = _format_agents(phase, individuals)
    _write_md(output_dir, f"phase_{phase}_agents.md", agents_md)

    # phase_N_interactions.md
    inter_md = _format_interactions(phase, interactions)
    _write_md(output_dir, f"phase_{phase}_interactions.md", inter_md)

    # comptes_rendus/phase_N_compte_rendu.md
    cr_content = (
        f"# Compte rendu — Phase {phase}\n\n"
        f"## Résumé\n{result.summary}\n\n"
        f"## Vignettes\n"
    )
    for i, scene in enumerate(result.scenes):
        cr_content += f"\n### Vignette {i+1}\n{scene}\n"
    _write_md(cr_dir, f"phase_{phase}_compte_rendu.md", cr_content)

    # comptes_rendus/phase_N_journal.md
    _write_md(cr_dir, f"phase_{phase}_journal.md",
              f"# Journal de phase — Phase {phase}\n\n{result.log}")

    # modalites/phase_N_modalites.md
    mod_content = _format_modalities(phase, modalities_detail, ordered_mods)
    _write_md(mod_dir, f"phase_{phase}_modalites.md", mod_content)


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
