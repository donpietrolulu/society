"""Tests for the AGENCY simulation engine."""
import json
import os
import shutil
import tempfile
import unittest

from system.sim.models import Individual, ModalityState, GlobalState, PhaseResult
from system.sim.engine import (
    load_config, load_modalities, load_interdependencies,
    create_individual, compute_weighted_modality_score,
    clamp, deep_merge, _average_traits, _update_modalities,
    compute_affinity, sample_interactions, get_archetype,
    choose_action, run_simulation,
)
from system.sim.constants import TRAIT_INFLUENCES, INDICATOR_ACTION_BIASES
from system.sim.llm import _mock_narrative, _simple_narrative
import random


class TestModels(unittest.TestCase):

    def test_individual_roundtrip(self):
        ind = Individual(id=0, traits={"cooperation": 0.5, "belief": 0.3})
        d = ind.to_dict()
        ind2 = Individual.from_dict(d)
        self.assertEqual(ind2.id, 0)
        self.assertAlmostEqual(ind2.traits["cooperation"], 0.5)

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
        # Diagonal should be 1.0
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
        self.assertEqual(get_archetype(ind), "Synchroniseur")

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


class TestNarrative(unittest.TestCase):

    def test_mock_narrative(self):
        context = {
            "phase": 1,
            "phases_total": 4,
            "global_state": {"population": 20, "resources": 100.0, "education": 0.1},
            "modalities": {
                "culture": {"name": "Culture", "score": 0.28},
            },
            "interaction_samples": [],
            "motifs": [],
        }
        result = _mock_narrative(context)
        self.assertIsInstance(result, PhaseResult)
        self.assertTrue(len(result.summary) > 0)
        self.assertTrue(len(result.log) > 0)
        self.assertTrue(len(result.story) > 0)
        self.assertEqual(len(result.scenes), 3)

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


class TestFullSimulation(unittest.TestCase):

    def test_mock_simulation(self):
        """Run a full simulation in mock mode."""
        output_dir = tempfile.mkdtemp()
        try:
            config = load_config()
            # Set env for auto-validation
            os.environ["SIM_VALIDATE_MODE"] = "file"
            os.environ["SIM_VALIDATE_DIR"] = output_dir

            # Pre-create validation files
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

            # Check outputs exist
            self.assertEqual(len(history), 4)
            for phase in range(1, 5):
                phase_dir = os.path.join(output_dir, f"phase_{phase}")
                self.assertTrue(
                    os.path.exists(os.path.join(phase_dir, "state.json")),
                    f"phase_{phase}/state.json manquant"
                )
                self.assertTrue(
                    os.path.exists(os.path.join(phase_dir, "metrics.json")),
                    f"phase_{phase}/metrics.json manquant"
                )
                self.assertTrue(
                    os.path.exists(os.path.join(phase_dir, "summary.md")),
                    f"phase_{phase}/summary.md manquant"
                )

            # Check phase_0/state.json
            self.assertTrue(os.path.exists(os.path.join(output_dir, "phase_0", "state.json")))

            # Check final state metrics are in range
            with open(os.path.join(output_dir, "phase_4", "state.json"), "r") as f:
                state = json.load(f)
            for mod_id, mod in state["modalities"].items():
                for ind, val in mod["metrics"].items():
                    self.assertGreaterEqual(val, 0.0, f"{mod_id}/{ind} < 0")
                    self.assertLessEqual(val, 1.0, f"{mod_id}/{ind} > 1")

            # Check population grew
            self.assertGreater(state["global_state"]["population"], 20)

        finally:
            # Cleanup env
            os.environ.pop("SIM_VALIDATE_MODE", None)
            os.environ.pop("SIM_VALIDATE_DIR", None)
            shutil.rmtree(output_dir, ignore_errors=True)


if __name__ == "__main__":
    unittest.main()
