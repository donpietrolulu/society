"""Output file writing for simulation phases."""
import json
import os

from system.sim.constants import (
    TRAIT_LABELS, ARCHETYPES, INDICATOR_LABELS,
    ARCHETYPE_PROFILES, MODALITY_MANIFESTATIONS,
)


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
                        ordered_mods):
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

    # agents.md — now with rich profiles
    agents_md = _format_agents(phase, individuals)
    _write_md(phase_dir, "agents.md", agents_md)

    # interactions.md — now with full narratives
    inter_md = _format_interactions(phase, interactions)
    _write_md(phase_dir, "interactions.md", inter_md)

    # compte_rendu.md
    cr_content = (
        f"# Compte rendu — Phase {phase}\n\n"
        f"## Résumé\n{result.summary}\n\n"
        f"## Vignettes\n"
    )
    for i, scene in enumerate(result.scenes):
        cr_content += f"\n### Vignette {i+1}\n{scene}\n"
    _write_md(phase_dir, "compte_rendu.md", cr_content)

    # journal.md
    _write_md(phase_dir, "journal.md",
              f"# Journal de phase — Phase {phase}\n\n{result.log}")

    # modalites.md — now with narrative manifestations
    mod_content = _format_modalities(phase, modalities_detail, ordered_mods)
    _write_md(phase_dir, "modalites.md", mod_content)


def _write_json(directory, filename, data):
    path = os.path.join(directory, filename)
    with open(path, "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)


def _write_md(directory, filename, content):
    path = os.path.join(directory, filename)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content)


def _format_agents(phase, individuals):
    """Format agents with rich narrative profiles."""
    lines = [f"# Agents — Phase {phase}\n"]
    lines.append(f"*{len(individuals)} nœuds composent le réseau.*\n")

    for ind in individuals[:50]:
        archetype = ARCHETYPES.get(
            max(ind.traits, key=ind.traits.get) if ind.traits else "",
            "Agent"
        )
        profile = ARCHETYPE_PROFILES.get(archetype, {})
        name = ind.name or f"Node-{ind.id}"

        lines.append(f"---\n")
        lines.append(f"## {name} — *{archetype}*\n")

        # Personality
        if profile.get("drive"):
            lines.append(f"**Fonction** : {profile['drive']}")
        if profile.get("fear"):
            lines.append(f"**Vulnérabilité** : {profile['fear']}")
        if profile.get("quirk"):
            lines.append(f"**Singularité** : {profile['quirk']}")
        lines.append("")

        # Traits as narrative, not just numbers
        sorted_traits = sorted(ind.traits.items(), key=lambda x: -x[1])
        if sorted_traits:
            top = sorted_traits[0]
            top_label = TRAIT_LABELS.get(top[0], top[0])
            lines.append(f"**Trait dominant** : {top_label} ({top[1]:.2f})")

            if len(sorted_traits) > 1:
                second = sorted_traits[1]
                second_label = TRAIT_LABELS.get(second[0], second[0])
                lines.append(f"**Trait secondaire** : {second_label} ({second[1]:.2f})")

            weakest = sorted_traits[-1]
            weak_label = TRAIT_LABELS.get(weakest[0], weakest[0])
            lines.append(f"**Point faible** : {weak_label} ({weakest[1]:.2f})")
        lines.append("")

        # Full trait table (compact)
        traits_str = " | ".join(
            f"{TRAIT_LABELS.get(t, t)}: {v:.2f}"
            for t, v in sorted_traits
        )
        lines.append(f"<details><summary>Tous les traits</summary>\n")
        lines.append(f"{traits_str}")
        lines.append(f"\n</details>\n")

        # Memory
        if ind.memory:
            lines.append(f"**Mémoire** ({len(ind.memory)} entrées) :")
            for mem in ind.memory[-5:]:
                lines.append(f"  - {mem}")
            lines.append("")

    if len(individuals) > 50:
        lines.append(f"\n---\n*... et {len(individuals) - 50} nœuds supplémentaires dans le réseau.*")
    return "\n".join(lines)


def _format_interactions(phase, interactions):
    """Format interactions with full narrative exchanges."""
    lines = [f"# Interactions — Phase {phase}\n"]
    lines.append(f"*{len(interactions)} échanges observés durant cette phase.*\n")

    for i, inter in enumerate(interactions):
        a = inter["agent_a"]
        b = inter["agent_b"]
        a_name = a.get("name", f"Node-{a['id']}")
        b_name = b.get("name", f"Node-{b['id']}")

        lines.append(f"---\n")
        lines.append(f"## Interaction {i+1}")
        lines.append(
            f"**{a_name}** ({a['archetype']}) ↔ **{b_name}** ({b['archetype']})"
        )
        lines.append(f"Affinité : **{inter['affinity']:.2f}**\n")

        # Full narrative
        narrative = inter.get("narrative", "")
        if narrative:
            lines.append(f"### Déroulement\n")
            lines.append(narrative)
            lines.append("")
        else:
            lines.append(
                f"{a_name} — {inter['action_a']} ↔ "
                f"{b_name} — {inter['action_b']}\n"
            )

    return "\n".join(lines)


def _format_modalities(phase, modalities_detail, ordered_mods):
    """Format modalities with narrative manifestations."""
    lines = [f"# Modalités — Phase {phase}\n"]
    lines.append("*Comment le monde algorithmique se manifeste concrètement.*\n")

    for mod_id in ordered_mods:
        mod = modalities_detail[mod_id]
        score = mod.score
        lines.append(f"---\n")
        lines.append(f"## {mod.name}")
        lines.append(f"**Score global** : {score:.3f}\n")

        # Narrative manifestation
        manifests = MODALITY_MANIFESTATIONS.get(mod_id, {})
        if score > 0.6:
            desc = manifests.get("high", "")
        elif score > 0.35:
            desc = manifests.get("mid", "")
        else:
            desc = manifests.get("low", "")
        if desc:
            lines.append(f"**Ce que ça signifie** : {desc}\n")

        lines.append(f"**Définition** : {mod.definition}\n")
        lines.append("**Indicateurs** :")
        for ind in mod.indicators:
            label = INDICATOR_LABELS.get(ind, ind)
            val = mod.metrics.get(ind, 0.0)
            # Add a qualitative descriptor
            if val > 0.7:
                qual = "fort"
            elif val > 0.4:
                qual = "modéré"
            else:
                qual = "faible"
            lines.append(f"  - {label} : {val:.3f} (*{qual}*)")
        lines.append("")

    return "\n".join(lines)
