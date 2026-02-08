"""Tests for the AGENCY simulation engine."""
import json
import os
import shutil
import tempfile
import unittest

from system.sim.models import Individual, ModalityState, GlobalState, PhaseResult, Artifact
from system.sim.engine import (
    load_config, load_modalities, load_interdependencies,
    create_individual, compute_weighted_modality_score,
    clamp, deep_merge, _average_traits, _update_modalities,
    compute_affinity, sample_interactions, get_archetype,
    choose_action, run_simulation,
)
from system.sim.constants import TRAIT_INFLUENCES, INDICATOR_ACTION_BIASES
from system.sim.llm import _mock_narrative, _simple_narrative
from system.sim.factions import generate_factions, assign_factions
from system.sim.cast import select_focus_cast
from system.sim.artifacts import generate_phase_artifacts
from system.sim.drama import choose_major_beat, generate_scenes
from system.sim.interconnectivity import compute_influence_contributions
import random


class TestModels(unittest.TestCase):

    def test_individual_roundtrip(self):
        ind = Individual(id=0, traits={"cooperation": 0.5, "belief": 0.3})
        d = ind.to_dict()
        ind2 = Individual.from_dict(d)
        self.assertEqual(ind2.id, 0)
        self.assertAlmostEqual(ind2.traits["cooperation"], 0.5)

    def test_individual_with_persona_roundtrip(self):
        ind = Individual(
            id=1, traits={"cooperation": 0.5},
            persona={"role": "Gardien", "desire": "paix"},
            relationships={"2": 0.5},
            faction="Les Veilleurs",
        )
        d = ind.to_dict()
        ind2 = Individual.from_dict(d)
        self.assertEqual(ind2.faction, "Les Veilleurs")
        self.assertEqual(ind2.persona["role"], "Gardien")
        self.assertAlmostEqual(ind2.relationships["2"], 0.5)

    def test_artifact_roundtrip(self):
        art = Artifact(id="CUL-P1-01", modality="culture",
                       title="Le Chant", description="Un chant ancien",
                       tags=["rituel"])
        d = art.to_dict()
        art2 = Artifact.from_dict(d)
        self.assertEqual(art2.id, "CUL-P1-01")
        self.assertEqual(art2.title, "Le Chant")

    def test_modality_score(self):
        mod = ModalityState(
            id="test", name="Test", definition="d",
            primitive_application="p",
            indicators=["a", "b"],
            metrics={"a": 0.4, "b": 0.6},
        )
        self.assertAlmostEqual(mod.score, 0.5)

    def test_global_state_roundtrip(self):
        gs = GlobalState(population=20, resources=100.0, education=0.1)
        d = gs.to_dict()
        gs2 = GlobalState.from_dict(d)
        self.assertEqual(gs2.population, 20)
        self.assertAlmostEqual(gs2.resources, 100.0)


class TestEngine(unittest.TestCase):

    def setUp(self):
        self.base_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        self.data_dir = os.path.join(self.base_dir, "data")

    def test_load_config(self):
        config = load_config()
        self.assertEqual(config["phases"], 4)
        self.assertEqual(config["initial_population"], 20)
        self.assertIn("growth", config)
        self.assertIn("societe_cursor", config)

    def test_load_modalities(self):
        mods = load_modalities(self.data_dir)
        self.assertEqual(len(mods), 6)
        self.assertIn("culture", mods)
        self.assertIn("economie", mods)

    def test_load_interdependencies(self):
        order, matrix = load_interdependencies(self.data_dir)
        self.assertEqual(len(order), 6)
        self.assertEqual(len(matrix), 6)
        self.assertEqual(len(matrix[0]), 6)
        for i in range(6):
            self.assertAlmostEqual(matrix[i][i], 1.0)

    def test_clamp(self):
        self.assertEqual(clamp(1.5), 1.0)
        self.assertEqual(clamp(-0.1), 0.0)
        self.assertEqual(clamp(0.5), 0.5)

    def test_deep_merge(self):
        base = {"a": 1, "b": {"c": 2, "d": 3}}
        override = {"b": {"c": 5}, "e": 6}
        result = deep_merge(base, override)
        self.assertEqual(result["a"], 1)
        self.assertEqual(result["b"]["c"], 5)
        self.assertEqual(result["b"]["d"], 3)
        self.assertEqual(result["e"], 6)

    def test_create_individual(self):
        rng = random.Random(42)
        ind = create_individual(0, ["cooperation", "belief", "skill"], rng)
        self.assertEqual(ind.id, 0)
        self.assertEqual(len(ind.traits), 3)
        for t, v in ind.traits.items():
            self.assertGreaterEqual(v, 0.2)
            self.assertLessEqual(v, 0.6)

    def test_compute_weighted_modality_score(self):
        mods = load_modalities(self.data_dir)
        score = compute_weighted_modality_score("cooperation", mods)
        self.assertGreater(score, 0.0)
        self.assertLess(score, 1.0)

    def test_affinity(self):
        a = Individual(0, {"cooperation": 0.5, "belief": 0.5})
        b = Individual(1, {"cooperation": 0.5, "belief": 0.5})
        self.assertAlmostEqual(compute_affinity(a, b), 1.0)

        c = Individual(2, {"cooperation": 0.0, "belief": 1.0})
        aff = compute_affinity(a, c)
        self.assertLess(aff, 1.0)

    def test_get_archetype(self):
        ind = Individual(0, {"cooperation": 0.8, "belief": 0.2})
        self.assertEqual(get_archetype(ind), "Pacificateur")

    def test_choose_action(self):
        ind = Individual(0, {"cooperation": 0.9, "empathy": 0.9, "trade": 0.1})
        action = choose_action(ind)
        self.assertEqual(action, "cooperate")

    def test_trait_influences_completeness(self):
        """All traits should have influence mappings."""
        expected = ["cooperation", "belief", "skill", "trade", "obedience",
                    "creativity", "empathy", "leadership", "curiosity",
                    "resilience", "ritual"]
        for trait in expected:
            self.assertIn(trait, TRAIT_INFLUENCES)

    def test_modality_metrics_range(self):
        """Initial metrics should be in [0, 1]."""
        mods = load_modalities(self.data_dir)
        for mod_id, mod in mods.items():
            for ind, val in mod.metrics.items():
                self.assertGreaterEqual(val, 0.0, f"{mod_id}/{ind}")
                self.assertLessEqual(val, 1.0, f"{mod_id}/{ind}")


class TestFactions(unittest.TestCase):

    def test_generate_factions_per_phase(self):
        rng = random.Random(42)
        for phase in range(1, 5):
            factions = generate_factions(phase, rng)
            self.assertGreaterEqual(len(factions), 2, f"Phase {phase}: too few factions")
            for f in factions:
                self.assertIn("name", f)
                self.assertIn("motto", f)
                self.assertIn("obsession", f)

    def test_assign_factions(self):
        rng = random.Random(42)
        individuals = [
            Individual(i, {"cooperation": rng.random(), "belief": rng.random(), "skill": rng.random()})
            for i in range(10)
        ]
        factions = generate_factions(1, rng)
        assign_factions(individuals, factions, {}, rng)
        for ind in individuals:
            self.assertIsNotNone(ind.faction)


class TestCast(unittest.TestCase):

    def test_select_focus_cast(self):
        rng = random.Random(42)
        individuals = [
            Individual(i, {
                "cooperation": rng.random(), "belief": rng.random(),
                "skill": rng.random(), "trade": rng.random(),
            })
            for i in range(20)
        ]
        factions = generate_factions(1, rng)
        assign_factions(individuals, factions, {}, rng)
        cast = select_focus_cast(individuals, 1, {}, factions, rng, k=5)
        self.assertEqual(len(cast), 5)
        for c in cast:
            self.assertIn("persona", c)
            p = c["persona"]
            self.assertIn("role", p)
            self.assertIn("desire", p)
            self.assertIn("fear", p)
            self.assertIn("secret", p)
            self.assertIn("voice", p)
            self.assertIn("relations", p)
            self.assertGreaterEqual(len(p["relations"]), 1)


class TestArtifacts(unittest.TestCase):

    def test_generate_artifacts(self):
        rng = random.Random(42)
        for phase in range(1, 5):
            artifacts = generate_phase_artifacts(phase, {}, [], [], rng)
            self.assertGreaterEqual(len(artifacts), 6, f"Phase {phase}: fewer than 6 artifacts")
            modalities_covered = set(a.modality for a in artifacts)
            self.assertEqual(len(modalities_covered), 6, f"Phase {phase}: not all modalities covered")
            for a in artifacts:
                self.assertTrue(a.id.startswith(("CUL", "MYT", "ETH", "GOV", "ECO", "TEC")))


class TestDrama(unittest.TestCase):

    def test_choose_major_beat(self):
        rng = random.Random(42)
        factions = generate_factions(2, rng)
        individuals = [Individual(i, {"cooperation": 0.5}) for i in range(10)]
        assign_factions(individuals, factions, {}, rng)
        cast = select_focus_cast(individuals, 2, {}, factions, rng, k=5)
        deltas = {"culture": 0.02, "mythologie": -0.01, "gouvernance": 0.05,
                  "valeurs_ethique": 0.0, "economie": 0.03, "technique_infrastructure": 0.01}
        beat = choose_major_beat(2, {}, deltas, factions, cast, rng)
        self.assertIn("type", beat)
        self.assertIn("description", beat)
        self.assertIn("events", beat)
        self.assertGreaterEqual(len(beat["events"]), 1)

    def test_generate_scenes(self):
        rng = random.Random(42)
        factions = generate_factions(1, rng)
        individuals = [Individual(i, {"cooperation": 0.5}) for i in range(10)]
        assign_factions(individuals, factions, {}, rng)
        cast = select_focus_cast(individuals, 1, {}, factions, rng, k=5)
        artifacts = generate_phase_artifacts(1, {}, factions, cast, rng)
        beat = {"type": "conflit", "location": "campement"}
        scenes, events = generate_scenes(1, beat, cast, factions, artifacts, rng, count=5)
        self.assertGreaterEqual(len(scenes), 3, "Fewer than 3 scenes generated")
        self.assertGreaterEqual(len(events), 3)


class TestInterconnectivity(unittest.TestCase):

    def test_compute_contributions(self):
        order = ["culture", "mythologie", "valeurs_ethique",
                 "gouvernance", "economie", "technique_infrastructure"]
        matrix = [
            [1.0, 0.4, 0.5, 0.4, 0.3, 0.2],
            [0.4, 1.0, 0.6, 0.3, 0.2, 0.2],
            [0.5, 0.6, 1.0, 0.5, 0.3, 0.2],
            [0.4, 0.3, 0.5, 1.0, 0.4, 0.3],
            [0.3, 0.2, 0.3, 0.4, 1.0, 0.5],
            [0.2, 0.2, 0.2, 0.3, 0.5, 1.0],
        ]
        scores = {m: 0.3 for m in order}
        contributions = compute_influence_contributions(scores, matrix, order)
        self.assertEqual(len(contributions), 6)
        for mod_id, sources in contributions.items():
            self.assertGreaterEqual(len(sources), 1)


class TestNarrative(unittest.TestCase):

    def test_mock_narrative_with_drama_pack(self):
        context = {
            "phase": 1,
            "phases_total": 4,
            "global_state": {"population": 20, "resources": 100.0, "education": 0.1},
            "modalities": {
                "culture": {"name": "Culture", "score": 0.28},
                "mythologie": {"name": "Mythologie", "score": 0.30},
            },
            "interaction_samples": [],
            "motifs": [],
            "drama_pack": {
                "beat": {"type": "fondation", "label": "Fondation", "description": "Un lieu est fondé."},
                "factions": [{"name": "Les Veilleurs du Feu", "motto": "Garder la flamme", "obsession": "culture"}],
                "cast": [{"individual_id": 0, "faction": "Les Veilleurs", "persona": {"role": "Gardien des chants", "role_description": "desc", "contradiction": "test", "voice": "proverbes"}}],
                "artifacts": [{"id": "CUL-P1-01", "title": "Le Chant du Feu", "description": "Un chant ancien."}],
                "scenes": ["Scène 1 test", "Scène 2 test", "Scène 3 test"],
            },
        }
        result = _mock_narrative(context)
        self.assertIsInstance(result, PhaseResult)
        self.assertTrue(len(result.summary) > 0)
        self.assertTrue(len(result.log) > 0)
        self.assertTrue(len(result.story) > 0)
        self.assertGreaterEqual(len(result.scenes), 3)
        # Check no forbidden jargon in story
        forbidden = ["swap", "buffer", "compute"]
        for word in forbidden:
            self.assertNotIn(word, result.story.lower(),
                             f"Forbidden word '{word}' found in story")

    def test_simple_narrative(self):
        context = {
            "phase": 2,
            "global_state": {"population": 25},
            "modalities": {
                "culture": {"name": "Culture", "score": 0.3},
            },
        }
        result = _simple_narrative(context)
        self.assertTrue(len(result.summary) > 0)
        # Check no forbidden jargon
        forbidden = ["swap", "buffer", "compute"]
        for word in forbidden:
            self.assertNotIn(word, result.story.lower(),
                             f"Forbidden word '{word}' found in simple story")


class TestFullSimulation(unittest.TestCase):

    def test_mock_simulation(self):
        """Run a full simulation in mock mode with narrative outputs."""
        output_dir = tempfile.mkdtemp()
        try:
            config = load_config()
            os.environ["SIM_VALIDATE_MODE"] = "file"
            os.environ["SIM_VALIDATE_DIR"] = output_dir

            for phase in range(1, config["phases"]):
                with open(os.path.join(output_dir, f"phase_{phase}_ok"), "w") as f:
                    f.write("ok")

            logs = []
            history = run_simulation(
                config=config,
                seed=42,
                output_dir=output_dir,
                mock=True,
                print_fn=lambda msg: logs.append(msg),
            )

            self.assertEqual(len(history), 4)

            for phase in range(1, 5):
                phase_dir = os.path.join(output_dir, f"phase_{phase}")

                # Legacy files
                for fname in ["state.json", "metrics.json", "summary.md",
                              "log.md", "story.md", "agents.md", "interactions.md",
                              "compte_rendu.md", "modalites.md"]:
                    self.assertTrue(
                        os.path.exists(os.path.join(phase_dir, fname)),
                        f"phase_{phase}/{fname} manquant"
                    )

                # New narrative files
                for fname in ["artifacts.md", "cast.md",
                              "societe_interactions.md", "events.jsonl",
                              "chronique.md"]:
                    self.assertTrue(
                        os.path.exists(os.path.join(phase_dir, fname)),
                        f"phase_{phase}/{fname} manquant"
                    )

                # Validate events.jsonl is valid JSONL
                events_path = os.path.join(phase_dir, "events.jsonl")
                with open(events_path, "r", encoding="utf-8") as f:
                    event_lines = f.readlines()
                self.assertGreaterEqual(len(event_lines), 3,
                                        f"phase_{phase}/events.jsonl has fewer than 3 events")
                for line in event_lines:
                    ev = json.loads(line)
                    self.assertIn("type", ev)
                    self.assertIn("phase", ev)

                # Check story and compte_rendu for forbidden words
                for fname in ["story.md", "compte_rendu.md"]:
                    fpath = os.path.join(phase_dir, fname)
                    with open(fpath, "r", encoding="utf-8") as f:
                        content = f.read().lower()
                    for word in ["swap", "buffer", "compute"]:
                        self.assertNotIn(word, content,
                                         f"Forbidden word '{word}' in phase_{phase}/{fname}")

                # Check scenes count >= 3
                with open(os.path.join(phase_dir, "compte_rendu.md"), "r", encoding="utf-8") as f:
                    cr = f.read()
                scene_count = cr.count("### Scène")
                self.assertGreaterEqual(scene_count, 3,
                                        f"phase_{phase}/compte_rendu.md has fewer than 3 scenes")

            # Check phase_0/state.json
            self.assertTrue(os.path.exists(os.path.join(output_dir, "phase_0", "state.json")))

            # Check final state
            with open(os.path.join(output_dir, "phase_4", "state.json"), "r") as f:
                state = json.load(f)
            for mod_id, mod in state["modalities"].items():
                for ind, val in mod["metrics"].items():
                    self.assertGreaterEqual(val, 0.0, f"{mod_id}/{ind} < 0")
                    self.assertLessEqual(val, 1.0, f"{mod_id}/{ind} > 1")
            self.assertGreater(state["global_state"]["population"], 20)

        finally:
            os.environ.pop("SIM_VALIDATE_MODE", None)
            os.environ.pop("SIM_VALIDATE_DIR", None)
            shutil.rmtree(output_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
