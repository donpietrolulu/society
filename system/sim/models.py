"""Data models for the simulation."""
import copy


class Individual:
    """An agent with numeric traits, identity, and memory."""

    def __init__(self, id: int, traits: dict = None, name: str = "",
                 memory: list = None):
        self.id = id
        self.traits = traits or {}
        self.name = name
        self.memory = memory or []

    def to_dict(self):
        return {
            "id": self.id,
            "traits": dict(self.traits),
            "name": self.name,
            "memory": list(self.memory),
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d["id"],
            traits=dict(d["traits"]),
            name=d.get("name", ""),
            memory=list(d.get("memory", [])),
        )


class ModalityState:
    """State of a single modality."""

    def __init__(self, id: str, name: str, definition: str,
                 primitive_application: str, indicators: list,
                 metrics: dict):
        self.id = id
        self.name = name
        self.definition = definition
        self.primitive_application = primitive_application
        self.indicators = list(indicators)
        self.metrics = dict(metrics)

    @property
    def score(self):
        if not self.metrics:
            return 0.0
        return sum(self.metrics.values()) / len(self.metrics)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "definition": self.definition,
            "primitive_application": self.primitive_application,
            "indicators": self.indicators,
            "metrics": dict(self.metrics),
            "score": self.score,
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            id=d["id"], name=d["name"], definition=d["definition"],
            primitive_application=d["primitive_application"],
            indicators=d["indicators"], metrics=dict(d["metrics"]),
        )


class GlobalState:
    """Global simulation state."""

    def __init__(self, population: int, resources: float, education: float):
        self.population = population
        self.resources = resources
        self.education = education

    def to_dict(self):
        return {
            "population": self.population,
            "resources": round(self.resources, 4),
            "education": round(self.education, 4),
        }

    @classmethod
    def from_dict(cls, d):
        return cls(
            population=d["population"],
            resources=d["resources"],
            education=d["education"],
        )


class PhaseResult:
    """Result of a single phase."""

    def __init__(self, phase: int, summary: str = "", log: str = "",
                 story: str = "", scenes: list = None, checks: dict = None):
        self.phase = phase
        self.summary = summary
        self.log = log
        self.story = story
        self.scenes = scenes or []
        self.checks = checks or {}

    def to_dict(self):
        return {
            "phase": self.phase,
            "summary": self.summary,
            "log": self.log,
            "story": self.story,
            "scenes": self.scenes,
            "checks": self.checks,
        }
