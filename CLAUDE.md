# AGENCY — Simulation de société d'agents

## Architecture

```
system/
  sim/           # Moteur de simulation
    engine.py    # Coeur : run_simulation(), create_individual(), sample_interactions(), etc.
    models.py    # Individual, ModalityState, GlobalState, PhaseResult (dataclasses-like)
    constants.py # Traits, archétypes, narratif dual ALGO/HUMAN, get_cursor_constants()
    llm.py       # Génération narrative (mock / simple / LLM OpenAI)
    output.py    # Écriture des fichiers de sortie par phase (JSON + texte)
    cli.py       # CLI : python -m system.sim run [options]
    validation.py# Validation inter-phase (file-based ou input)
  web/
    app.py       # Serveur HTTP dashboard (port 8765)
    index.html   # Interface web mono-page
  config/
    defaults.json     # Config par défaut (phases, population, traits, LLM, societe_cursor)
    phase_modifiers.json  # Modificateurs par phase
  data/
    modalities/       # Définitions des 6 modalités (JSON)
    interdependencies.json  # Matrice 6×6 de couplage
  tests/
    test_simulation.py  # 18 tests unitaires + 1 test intégration mock
```

## Concepts clés

- **6 modalités** : culture, mythologie, valeurs_ethique, gouvernance, economie, technique_infrastructure
- **11 traits** : cooperation, belief, skill, trade, obedience, creativity, empathy, leadership, curiosity, resilience, ritual — injectés progressivement par phase
- **11 archétypes** : chaque trait dominant mappe sur un archétype (dual algo/humain)
- **4 phases** de développement avec validation inter-phase
- **societe_cursor** (0.0→1.0) : contrôle le registre narratif entier
  - ≤0.25 → algorithmique (nœuds, réseau, protocoles)
  - ≥0.75 → humain (individus, communauté, rituels)
  - entre → hybride (mélange des deux vocabulaires)
- **Matrice d'interdépendance** : couplage entre modalités (6×6)

## societe_cursor — comment ça traverse le code

1. `defaults.json` → valeur par défaut (0.0)
2. `cli.py` → arg `--societe-cursor` override la config
3. `engine.py:run_simulation()` → `cc = get_cursor_constants(cursor)`
4. `cc` est passé à TOUTES les fonctions : noms, archétypes, interactions, profils, narratif
5. `llm.py` → tonalité du prompt LLM adaptée au curseur
6. `output.py` → formatage des sorties adapté
7. `web/index.html` → slider "Agents ↔ Humains"
8. `web/app.py` → passe `--societe-cursor` au CLI

## Conventions

- **Python 3.8+**, aucune dépendance externe (stdlib only + openai optionnel)
- **Tests** : `python -m unittest system.tests.test_simulation -v` (18 tests)
- **Lancer** : `python -m system.sim run --mock` (mode déterministe sans LLM)
- **Dashboard** : `python -m system.web.app` → http://127.0.0.1:8765
- **Langue** : tout le narratif est en français
- Les agents ont un **nom** (généré), une **mémoire** (liste d'événements), un **archétype**
- Les interactions génèrent des **récits narratifs** (pas des stats)
- Trois modes narratifs : `mock` (déterministe), `simple` (sans LLM), `llm` (OpenAI API)

## Règles de développement

- Toujours faire passer les 18 tests avant de commit
- Le `cc` (cursor constants) doit être threadé partout où du texte narratif est produit
- Les constantes duales (ALGO/HUMAN) doivent rester symétriques en structure
- `get_cursor_constants()` est le point d'entrée unique pour résoudre le curseur
- Ne pas casser la rétrocompatibilité des alias (`ARCHETYPES = ARCHETYPES_ALGO`, etc.)

## Branche active

- `claude/enhance-simulation-narrative-WR5JY` — narratif riche + societe_cursor + slider web
