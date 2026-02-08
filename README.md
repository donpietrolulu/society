# AGENCY — Simulation de société d'agents

Prototype CLI pour simuler une société d'agents en phases, structurée par 6 modalités et une validation manuelle entre phases.

## Structure

```
system/
  sim/          # Moteur de simulation
  data/         # Modalités (JSON) + matrice d'interdépendances
  config/       # Configuration par défaut + modificateurs par phase
  docs/         # Documentation des modalités, interdépendances, phases
  tests/        # Tests unitaires
  web/          # Mini serveur + tableau de bord
experience/     # Dossier de sortie par défaut
```

## Dépendances

Python 3.8+ avec la bibliothèque standard uniquement. `certifi` optionnel pour les appels HTTPS.

Les appels LLM utilisent Claude Code CLI (`claude -p`) — aucune clé API à configurer.

## Utilisation

### Lancer la simulation (mode mock, sans LLM)

```bash
python -m system.sim run --mock --seed 42
```

### Lancer avec LLM (via Claude Code)

```bash
python -m system.sim run --seed 42
```

> Nécessite que `claude` soit installé et authentifié (`claude auth login`).

### Options CLI

| Option | Description |
|--------|-------------|
| `--config PATH` | Fichier de config override (JSON) |
| `--seed N` | Graine aléatoire |
| `--output-dir PATH` | Dossier de sortie |
| `--data-dir PATH` | Dossier de données |
| `--mock` | Mode mock (narratif déterministe) |
| `--no-llm` | Mode sans LLM (narratif simplifié) |
| `--phase-start N` | Phase de départ (charge l'état précédent si > 1) |

### Validation entre phases

Par défaut, le système attend une saisie `ok` dans le terminal entre chaque phase.

Mode fichier (pour le web panel) :

```bash
export SIM_VALIDATE_MODE=file
export SIM_VALIDATE_DIR=/chemin/sortie
```

### Tableau de bord web

```bash
python -m system.web.app
```

Ouvre `http://127.0.0.1:8765` dans le navigateur.

### Tests

```bash
python -m unittest system.tests.test_simulation -v
```

## Modalités

1. **Culture** — Pratiques, signatures et conventions d'exécution
2. **Mythologie** — Modèles du monde compacts
3. **Valeurs et Éthique** — Priorités et contraintes d'alignement
4. **Gouvernance** — Règles, arbitrages et coordination
5. **Économie** — Allocation des ressources de calcul
6. **Technique et Infrastructure** — Architecture, mémoire et réseaux

## Phases

1. Protocole et survie système
2. Modèles opératoires et réputation
3. Schismes et guerres d'information
4. Institutions et métriques
