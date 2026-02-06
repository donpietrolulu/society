"""Core simulation engine."""
import json
import math
import os
import random
import copy

from system.sim.models import Individual, ModalityState, GlobalState, PhaseResult
from system.sim.constants import (
    TRAIT_INFLUENCES, INDICATOR_ACTION_BIASES, TRAIT_LABELS,
    ARCHETYPES, ACTION_LABELS, ACTION_TRAITS, INDICATOR_LABELS,
    NAME_PREFIXES, NAME_SUFFIXES, ARCHETYPE_PROFILES,
    INTERACTION_VERBS, INTERACTION_OUTCOMES_HIGH,
    INTERACTION_OUTCOMES_MED, INTERACTION_OUTCOMES_LOW,
    MYTHOLOGICAL_CONCEPTS, MODALITY_MANIFESTATIONS,
)
from system.sim.llm import generate_narrative
from system.sim.output import write_phase_outputs, write_state
from system.sim.validation import wait_for_validation


def clamp(v, lo=0.0, hi=1.0):
    return max(lo, min(hi, v))


def deep_merge(base, override):
    """Deep merge override into base, returning new dict."""
    result = dict(base)
    for k, v in override.items():
        if k in result and isinstance(result[k], dict) and isinstance(v, dict):
            result[k] = deep_merge(result[k], v)
        else:
            result[k] = v
    return result


def load_config(config_path=None):
    """Load config with deep merge of defaults + override."""
    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    defaults_path = os.path.join(base_dir, "config", "defaults.json")
    with open(defaults_path, "r", encoding="utf-8") as f:
        defaults = json.load(f)
    if config_path:
        with open(config_path, "r", encoding="utf-8") as f:
            override = json.load(f)
        return deep_merge(defaults, override)
    return defaults


def load_modalities(data_dir):
    """Load modality JSON files from data_dir/modalities/."""
    mod_dir = os.path.join(data_dir, "modalities")
    modalities = {}
    for fname in os.listdir(mod_dir):
        if fname.endswith(".json"):
            fpath = os.path.join(mod_dir, fname)
            with open(fpath, "r", encoding="utf-8") as f:
                data = json.load(f)
            mod_id = fname.replace(".json", "")
            modalities[mod_id] = ModalityState(
                id=mod_id,
                name=data["name"],
                definition=data["definition"],
                primitive_application=data["primitive_application"],
                indicators=data["indicators"],
                metrics=dict(data["initial_metrics"]),
            )
    return modalities


def load_interdependencies(data_dir):
    """Load interdependencies matrix."""
    fpath = os.path.join(data_dir, "interdependencies.json")
    with open(fpath, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data["modalities"], data["matrix"]


def load_phase_modifiers(config, base_dir):
    """Load phase modifiers."""
    rel = config.get("phase_modifiers_path", "config/phase_modifiers.json")
    fpath = os.path.join(base_dir, rel)
    with open(fpath, "r", encoding="utf-8") as f:
        return json.load(f)


def load_docs(config, base_dir):
    """Load doc files for LLM context."""
    docs = {}
    docs_cfg = config.get("docs", {})
    for key in ["modalities", "interdependencies"]:
        path = os.path.join(base_dir, docs_cfg.get(key, ""))
        if os.path.exists(path):
            with open(path, "r", encoding="utf-8") as f:
                docs[key] = f.read()
    return docs


def load_phase_doc(config, base_dir, phase):
    """Load phase-specific doc."""
    docs_cfg = config.get("docs", {})
    phases_dir = os.path.join(base_dir, docs_cfg.get("phases", "docs/phases"))
    path = os.path.join(phases_dir, f"phase_{phase}.md")
    if os.path.exists(path):
        with open(path, "r", encoding="utf-8") as f:
            return f.read()
    return ""


def generate_name(id: int, rng: random.Random, used_names: set = None):
    """Generate a unique algorithmic name for an agent."""
    if used_names is None:
        used_names = set()
    for _ in range(50):
        prefix = rng.choice(NAME_PREFIXES)
        suffix = rng.choice(NAME_SUFFIXES)
        name = f"{prefix}{suffix}"
        if name not in used_names:
            used_names.add(name)
            return name
    # Fallback: use id
    return f"Node-{id}"


def create_individual(id: int, traits_list: list, rng: random.Random,
                      used_names: set = None):
    """Create individual with random traits in [0.2, 0.6] and a name."""
    traits = {}
    for t in traits_list:
        traits[t] = rng.random() * 0.4 + 0.2
    name = generate_name(id, rng, used_names)
    return Individual(id=id, traits=traits, name=name)


def compute_weighted_modality_score(trait_name, modalities):
    """Compute weighted score for a trait based on modality influences."""
    influences = TRAIT_INFLUENCES.get(trait_name, {})
    if not influences:
        return 0.5
    total = 0.0
    for mod_id, weight in influences.items():
        if mod_id in modalities:
            total += weight * modalities[mod_id].score
    return total


def get_archetype(individual):
    """Get the archetype name based on dominant trait."""
    if not individual.traits:
        return "Agent"
    top_trait = max(individual.traits, key=individual.traits.get)
    return ARCHETYPES.get(top_trait, "Agent")


def choose_action(individual):
    """Choose action based on trait scores."""
    best_action = "cooperate"
    best_score = -1.0
    for action, traits in ACTION_TRAITS.items():
        score = sum(individual.traits.get(t, 0.0) for t in traits) / max(len(traits), 1)
        if score > best_score:
            best_score = score
            best_action = action
    return best_action


def compute_affinity(a: Individual, b: Individual):
    """Affinity = 1 - mean absolute trait difference."""
    common = set(a.traits.keys()) & set(b.traits.keys())
    if not common:
        return 0.5
    diff = sum(abs(a.traits[t] - b.traits[t]) for t in common) / len(common)
    return 1.0 - diff


def sample_interactions(individuals, rng, count=5):
    """Sample interaction pairs and generate rich narrative exchanges."""
    if len(individuals) < 2:
        return []
    interactions = []
    for idx in range(min(count, len(individuals))):
        a, b = rng.sample(individuals, 2)
        affinity = compute_affinity(a, b)
        action_a = choose_action(a)
        action_b = choose_action(b)
        arch_a = get_archetype(a)
        arch_b = get_archetype(b)

        # Generate narrative exchange
        verb_a = rng.choice(INTERACTION_VERBS.get(action_a, ["contacte"]))
        verb_b = rng.choice(INTERACTION_VERBS.get(action_b, ["répond à"]))

        if affinity > 0.75:
            outcome = rng.choice(INTERACTION_OUTCOMES_HIGH)
        elif affinity > 0.5:
            outcome = rng.choice(INTERACTION_OUTCOMES_MED)
        else:
            outcome = rng.choice(INTERACTION_OUTCOMES_LOW)

        # Build the narrative
        narrative_lines = [
            f"{a.name} ({arch_a}) {verb_a} {b.name} ({arch_b}).",
        ]

        # Add detail based on actions
        detail_a = _action_detail(a, action_a, rng)
        if detail_a:
            narrative_lines.append(detail_a)

        narrative_lines.append(
            f"{b.name} répond — {verb_b} {a.name}."
        )

        detail_b = _action_detail(b, action_b, rng)
        if detail_b:
            narrative_lines.append(detail_b)

        narrative_lines.append(f"Résultat (affinité: {affinity:.2f}): {outcome}")

        # Memory entry for both agents
        memory_entry = f"Phase interaction avec {b.name}: {outcome[:60]}"
        a.memory.append(memory_entry)
        b.memory.append(f"Phase interaction avec {a.name}: {outcome[:60]}")

        interactions.append({
            "agent_a": {"id": a.id, "name": a.name, "archetype": arch_a},
            "agent_b": {"id": b.id, "name": b.name, "archetype": arch_b},
            "affinity": round(affinity, 3),
            "action_a": ACTION_LABELS.get(action_a, action_a),
            "action_b": ACTION_LABELS.get(action_b, action_b),
            "narrative": "\n".join(narrative_lines),
        })
    return interactions


def _action_detail(agent, action, rng):
    """Generate a specific detail about what the agent does during the action."""
    arch = get_archetype(agent)
    profile = ARCHETYPE_PROFILES.get(arch, {})
    quirk = profile.get("quirk", "")

    if action == "cooperate":
        options = [
            f"{agent.name} expose son état interne : synchronisation={agent.traits.get('cooperation', 0):.2f}, alignement={agent.traits.get('empathy', 0):.2f}.",
            f"{agent.name} ouvre ses registres. Comme tout {arch}, {quirk}." if quirk else None,
            f"{agent.name} partage un fragment de cache — une routine héritée de la phase précédente.",
        ]
    elif action == "exchange":
        options = [
            f"{agent.name} met sur le canal : {rng.randint(2, 12)} blocs de compute contre un index de routines.",
            f"{agent.name}, en bon {arch}, {quirk}." if quirk else None,
            f"{agent.name} propose un swap asymétrique — plus de mémoire contre moins de latence.",
        ]
    else:  # talk
        options = [
            f"{agent.name} transmet un schéma : un modèle partiel du réseau tel qu'il le perçoit.",
            f"{agent.name}, fidèle à son rôle de {arch}, {quirk}." if quirk else None,
            f"{agent.name} diffuse une séquence — un fragment de ce que d'autres nœuds appellent déjà un 'modèle fondateur'.",
        ]

    valid = [o for o in options if o]
    return rng.choice(valid) if valid else ""


def generate_agent_profile(individual, phase):
    """Generate a narrative profile for an agent based on their traits and memory."""
    arch = get_archetype(individual)
    profile = ARCHETYPE_PROFILES.get(arch, {})
    traits = individual.traits

    # Find top 3 traits
    sorted_traits = sorted(traits.items(), key=lambda x: -x[1])
    top_traits = sorted_traits[:3]
    low_traits = sorted_traits[-2:] if len(sorted_traits) > 2 else []

    lines = []
    lines.append(f"**{individual.name}** — *{arch}*")
    lines.append(f"")

    # Drive and personality
    if profile.get("drive"):
        lines.append(f"Fonction première : {profile['drive']}.")
    if profile.get("fear"):
        lines.append(f"Vulnérabilité : {profile['fear']}.")
    if profile.get("quirk"):
        lines.append(f"Singularité : {profile['quirk']}.")

    # Trait narrative
    lines.append(f"")
    dominant = TRAIT_LABELS.get(top_traits[0][0], top_traits[0][0])
    lines.append(
        f"Trait dominant : {dominant} ({top_traits[0][1]:.2f}). "
        f"Ce nœud se définit avant tout par sa capacité de {dominant}."
    )

    if low_traits:
        weak = TRAIT_LABELS.get(low_traits[-1][0], low_traits[-1][0])
        lines.append(
            f"Point faible : {weak} ({low_traits[-1][1]:.2f}) — "
            f"une lacune qui oriente ses interactions."
        )

    # Memory / history
    if individual.memory:
        lines.append(f"")
        lines.append(f"Mémoire récente ({len(individual.memory)} entrées) :")
        for mem in individual.memory[-3:]:
            lines.append(f"  — {mem}")

    return "\n".join(lines)


def identify_notable_agents(individuals, prev_individuals=None, count=8):
    """Identify the most narratively interesting agents."""
    scored = []
    prev_map = {}
    if prev_individuals:
        prev_map = {ind.id: ind for ind in prev_individuals}

    for ind in individuals:
        score = 0.0
        # Extreme traits are interesting
        for t, v in ind.traits.items():
            if v > 0.8 or v < 0.15:
                score += 2.0
            elif v > 0.7 or v < 0.25:
                score += 1.0

        # Agents with lots of memory are interesting
        score += len(ind.memory) * 0.5

        # Agents who changed a lot are interesting
        if ind.id in prev_map:
            prev = prev_map[ind.id]
            for t in ind.traits:
                if t in prev.traits:
                    delta = abs(ind.traits[t] - prev.traits[t])
                    if delta > 0.15:
                        score += 3.0
                    elif delta > 0.08:
                        score += 1.5

        scored.append((ind, score))

    scored.sort(key=lambda x: -x[1])
    return [ind for ind, _ in scored[:count]]


def generate_world_state_narrative(modalities, ordered_mods, individuals, rng):
    """Generate a narrative description of the world state from modalities."""
    lines = []
    for mod_id in ordered_mods:
        mod = modalities[mod_id]
        score = mod.score
        manifests = MODALITY_MANIFESTATIONS.get(mod_id, {})
        if score > 0.6:
            desc = manifests.get("high", "")
        elif score > 0.35:
            desc = manifests.get("mid", "")
        else:
            desc = manifests.get("low", "")
        if desc:
            lines.append(f"**{mod.name}** (score: {score:.2f}) — {desc}")

    # Add mythological layer based on population traits
    avg_traits = _average_traits(individuals)
    myth_lines = []
    for trait_key, threshold_name in [
        ("belief", "high_belief"), ("ritual", "high_ritual"),
        ("creativity", "high_creativity"), ("cooperation", "high_cooperation"),
        ("obedience", "high_obedience"),
    ]:
        val = avg_traits.get(trait_key, 0)
        if val > 0.5:
            concepts = MYTHOLOGICAL_CONCEPTS.get(threshold_name, [])
            if concepts:
                myth_lines.append(rng.choice(concepts))

    if myth_lines:
        lines.append("")
        lines.append("**Croyances et mythes actifs dans le réseau :**")
        for m in myth_lines:
            lines.append(f"  — {m}")

    return "\n\n".join(lines)


def compute_dominant_motifs(modalities, mod_order, matrix):
    """Derive narrative motifs from highest-scoring modalities."""
    scored = [(mod_id, modalities[mod_id].score) for mod_id in mod_order if mod_id in modalities]
    scored.sort(key=lambda x: -x[1])
    motifs = []
    for mod_id, score in scored[:3]:
        motifs.append({
            "modality": mod_id,
            "score": round(score, 3),
            "effect": _motif_effect(mod_id),
        })
    return motifs


def _motif_effect(mod_id):
    effects = {
        "culture": "gain_coherence",
        "mythologie": "consolidation_modeles",
        "valeurs_ethique": "renforcement_alignement",
        "gouvernance": "stabilisation_coordination",
        "economie": "optimisation_ressources",
        "technique_infrastructure": "baisse_latence",
    }
    return effects.get(mod_id, "effet_neutre")


def _next_test_dir(experience_dir):
    """Find next TestN directory number and return its phases path."""
    os.makedirs(experience_dir, exist_ok=True)
    n = 1
    while os.path.exists(os.path.join(experience_dir, f"Test{n}")):
        n += 1
    return os.path.join(experience_dir, f"Test{n}", "phases")


def run_simulation(config, seed=None, output_dir=None, data_dir=None,
                   mock=False, no_llm=False, phase_start=1, print_fn=None):
    """Run the full simulation pipeline."""
    if print_fn is None:
        print_fn = print

    base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    if data_dir is None:
        data_dir = os.path.join(base_dir, "data")
    if output_dir is None:
        output_dir = _next_test_dir(os.path.join(os.path.dirname(base_dir), "experience"))

    rng = random.Random(seed)

    # 1. Load config
    phases_count = config.get("phases", 4)
    growth = config.get("growth", {})

    # 2. Load modalities and interdependencies
    modalities = load_modalities(data_dir)
    mod_order, matrix = load_interdependencies(data_dir)

    # Order modalities
    ordered_mods = [m for m in mod_order if m in modalities]

    # 3. Load phase modifiers
    phase_modifiers = load_phase_modifiers(config, base_dir)

    # 4. Load docs
    docs = load_docs(config, base_dir)

    # 5. Init global state
    global_state = GlobalState(
        population=config.get("initial_population", 20),
        resources=config.get("initial_resources", 100.0),
        education=config.get("initial_education", 0.1),
    )

    # 6. Create initial individuals
    initial_traits = config.get("traits", {}).get("initial", ["cooperation", "belief", "skill"])
    used_names = set()
    individuals = []
    for i in range(global_state.population):
        individuals.append(create_individual(i, initial_traits, rng, used_names))

    # Load previous state if phase_start > 1
    history = []
    if phase_start > 1:
        prev_state_path = os.path.join(output_dir, f"phase_{phase_start - 1}", "state.json")
        if os.path.exists(prev_state_path):
            with open(prev_state_path, "r", encoding="utf-8") as f:
                prev = json.load(f)
            global_state = GlobalState.from_dict(prev["global_state"])
            individuals = [Individual.from_dict(d) for d in prev["individuals"]]
            for mod_id, md in prev.get("modalities", {}).items():
                if mod_id in modalities:
                    modalities[mod_id] = ModalityState.from_dict(md)
            history = prev.get("history", [])
        else:
            print_fn(f"Attention : état précédent introuvable ({prev_state_path}), démarrage frais.")

    # Write phase_0_state if starting from phase 1
    if phase_start == 1:
        state_0 = _build_state_dict(0, global_state, individuals, modalities, ordered_mods, history)
        write_state(output_dir, 0, state_0)

    # 7. Run phases
    per_phase_traits = config.get("traits", {}).get("per_phase", {})
    update_steps = config.get("individual_update_steps_per_phase", 3)

    for phase in range(phase_start, phases_count + 1):
        print_fn(f"\n=== Phase {phase}/{phases_count} ===")

        # Apply growth
        new_pop = round(global_state.population * (1 + growth.get("population", 0.25)))
        global_state.resources *= (1 + growth.get("resources", 0.20))
        global_state.education = clamp(
            global_state.education * (1 + growth.get("education", 0.15))
        )

        # Adjust population
        if new_pop > global_state.population:
            # Collect existing names
            used_names = {ind.name for ind in individuals if ind.name}
            avg_traits = _average_traits(individuals)
            for i in range(global_state.population, new_pop):
                traits = {}
                for t, v in avg_traits.items():
                    traits[t] = clamp(v + rng.uniform(-0.08, 0.08))
                name = generate_name(i, rng, used_names)
                individuals.append(Individual(id=i, traits=traits, name=name))
        global_state.population = new_pop

        # Add phase traits
        phase_traits = per_phase_traits.get(str(phase), [])
        for ind in individuals:
            for t in phase_traits:
                if t not in ind.traits:
                    base = compute_weighted_modality_score(t, modalities)
                    ind.traits[t] = clamp(base + rng.uniform(-0.1, 0.1))

        # Get phase modifiers
        pm = phase_modifiers.get(str(phase), {})
        bias = pm.get("bias", {})
        extra_noise = pm.get("extra_noise", {})

        # Update traits
        for _step in range(update_steps):
            for ind in individuals:
                for t in list(ind.traits.keys()):
                    target = compute_weighted_modality_score(t, modalities)
                    base_noise = 0.06 * (1 - global_state.education)
                    noise_scale = base_noise + extra_noise.get(t, 0.0)
                    noise = rng.uniform(-noise_scale, noise_scale)
                    b = bias.get(t, 0.0)
                    ind.traits[t] = clamp(ind.traits[t] + 0.2 * (target - ind.traits[t]) + noise + b)

        # Update modalities
        _update_modalities(modalities, ordered_mods, matrix, individuals, global_state, rng)

        # Collect context
        phase_doc = load_phase_doc(config, base_dir, phase)
        interaction_samples = sample_interactions(individuals, rng, count=8)
        motifs = compute_dominant_motifs(modalities, ordered_mods, matrix)

        # Identify notable agents and generate profiles
        notable = identify_notable_agents(individuals, count=8)
        agent_profiles = [generate_agent_profile(ind, phase) for ind in notable]
        world_narrative = generate_world_state_narrative(
            modalities, ordered_mods, individuals, rng
        )

        narrative_context = {
            "phase": phase,
            "phases_total": phases_count,
            "global_state": global_state.to_dict(),
            "modalities": {m: modalities[m].to_dict() for m in ordered_mods},
            "population_stats": _population_stats(individuals),
            "interaction_samples": interaction_samples,
            "motifs": motifs,
            "phase_doc": phase_doc,
            "history": history,
            "notable_agents": [{"id": ind.id, "name": ind.name,
                                "archetype": get_archetype(ind),
                                "profile": prof}
                               for ind, prof in zip(notable, agent_profiles)],
            "world_narrative": world_narrative,
        }

        # Generate narrative
        result = generate_narrative(
            config=config,
            context=narrative_context,
            docs=docs,
            mock=mock,
            no_llm=no_llm,
        )

        # Validate
        checks = _validate_phase(result, global_state, modalities)
        result.phase = phase
        result.checks = checks

        # History
        history.append({"phase": phase, "summary": result.summary})

        # Write outputs
        metrics = {m: modalities[m].to_dict() for m in ordered_mods}
        state_dict = _build_state_dict(phase, global_state, individuals, modalities, ordered_mods, history)

        write_phase_outputs(
            output_dir=output_dir,
            phase=phase,
            result=result,
            metrics=metrics,
            state=state_dict,
            individuals=individuals,
            interactions=interaction_samples,
            modalities_detail=modalities,
            ordered_mods=ordered_mods,
        )

        print_fn(f"Phase {phase} terminée. Fichiers écrits dans {output_dir}")

        # Wait for validation if not last phase
        if phase < phases_count:
            print_fn("Validation requise pour continuer.")
            wait_for_validation(phase, output_dir, print_fn)
            print_fn(f"Phase {phase} validée.")

    print_fn("\n=== Simulation terminée ===")
    return history


def _average_traits(individuals):
    """Compute average trait values across population."""
    if not individuals:
        return {}
    totals = {}
    counts = {}
    for ind in individuals:
        for t, v in ind.traits.items():
            totals[t] = totals.get(t, 0.0) + v
            counts[t] = counts.get(t, 0) + 1
    return {t: totals[t] / counts[t] for t in totals}


def _population_stats(individuals):
    """Compute population statistics."""
    if not individuals:
        return {}
    avg = _average_traits(individuals)
    # Compute variance
    var = {}
    for t in avg:
        vals = [ind.traits.get(t, 0.0) for ind in individuals if t in ind.traits]
        if vals:
            mean = avg[t]
            var[t] = sum((v - mean) ** 2 for v in vals) / len(vals)
    return {
        "count": len(individuals),
        "trait_means": {t: round(v, 4) for t, v in avg.items()},
        "trait_variance": {t: round(v, 4) for t, v in var.items()},
    }


def _update_modalities(modalities, mod_order, matrix, individuals, global_state, rng):
    """Update modality metrics based on traits and interdependencies."""
    avg_traits = _average_traits(individuals)

    # Compute modality scores for interdependency
    mod_scores = {m: modalities[m].score for m in mod_order}

    for i, mod_id in enumerate(mod_order):
        mod = modalities[mod_id]

        # Interdependency influence
        total_weight = sum(matrix[i])
        influence = sum(matrix[i][j] * mod_scores[mod_order[j]] for j in range(len(mod_order))) / total_weight

        # Extra influence based on modality type
        extra = 0.0
        if mod_id == "technique_infrastructure":
            extra = 0.02 * avg_traits.get("skill", 0.0)
        elif mod_id == "economie":
            extra = 0.02 * avg_traits.get("trade", 0.0)
        elif mod_id == "gouvernance":
            extra = 0.02 * avg_traits.get("obedience", 0.0)

        for indicator in mod.indicators:
            current = mod.metrics.get(indicator, 0.0)

            # Indicator action bias
            ind_bias = 0.0
            biases = INDICATOR_ACTION_BIASES.get((mod_id, indicator), {})
            for action_or_trait, bval in biases.items():
                if action_or_trait in avg_traits:
                    ind_bias += bval * avg_traits[action_or_trait]
                elif action_or_trait in ACTION_TRAITS:
                    # Action: use average of relevant traits
                    rel_traits = ACTION_TRAITS[action_or_trait]
                    action_avg = sum(avg_traits.get(t, 0.0) for t in rel_traits) / max(len(rel_traits), 1)
                    ind_bias += bval * action_avg

            noise = rng.uniform(-0.03, 0.03)
            updated = current + 0.3 * (influence - current) + extra + noise + ind_bias
            mod.metrics[indicator] = clamp(updated)


def _validate_phase(result, global_state, modalities):
    """Validate phase results."""
    checks = {}
    checks["summary_non_empty"] = len(result.summary.strip()) > 0
    checks["log_non_empty"] = len(result.log.strip()) > 0
    checks["story_non_empty"] = len(result.story.strip()) > 0
    checks["population_coherent"] = global_state.population > 0
    checks["metrics_in_range"] = all(
        0.0 <= v <= 1.0
        for mod in modalities.values()
        for v in mod.metrics.values()
    )
    checks["all_passed"] = all(checks.values())
    return checks


def _build_state_dict(phase, global_state, individuals, modalities, ordered_mods, history):
    """Build full state dict for serialization."""
    return {
        "phase": phase,
        "global_state": global_state.to_dict(),
        "individuals": [ind.to_dict() for ind in individuals],
        "modalities": {m: modalities[m].to_dict() for m in ordered_mods},
        "history": history,
    }
