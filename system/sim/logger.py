"""Event logging system — writes events.jsonl per phase."""
import json
import os
import time


def make_event(phase, tick, event_type, text, actors=None, location=None,
               modalities=None, consequences=None, meta=None):
    """Create a standardized event dict."""
    return {
        "ts": time.time(),
        "phase": phase,
        "tick": tick,
        "type": event_type,
        "actors": actors or [],
        "location": location or "",
        "modalities": modalities or [],
        "text": text,
        "consequences": consequences or {},
        "meta": meta or {},
    }


def append_event(phase_dir, event_dict):
    """Append a single event to events.jsonl in the given phase directory."""
    os.makedirs(phase_dir, exist_ok=True)
    path = os.path.join(phase_dir, "events.jsonl")
    with open(path, "a", encoding="utf-8") as f:
        f.write(json.dumps(event_dict, ensure_ascii=False) + "\n")


def write_events(phase_dir, events):
    """Write all events for a phase to events.jsonl."""
    os.makedirs(phase_dir, exist_ok=True)
    path = os.path.join(phase_dir, "events.jsonl")
    with open(path, "w", encoding="utf-8") as f:
        for ev in events:
            f.write(json.dumps(ev, ensure_ascii=False) + "\n")
