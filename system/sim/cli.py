"""CLI interface for the simulation."""
import argparse
import sys

from system.sim.engine import load_config, run_simulation


def main(argv=None):
    parser = argparse.ArgumentParser(
        prog="system.sim",
        description="AGENCY — Simulation de société d'agents",
    )
    subparsers = parser.add_subparsers(dest="command")

    run_parser = subparsers.add_parser("run", help="Lancer la simulation")
    run_parser.add_argument("--config", type=str, default=None,
                            help="Chemin vers un fichier de config override (JSON)")
    run_parser.add_argument("--seed", type=int, default=None,
                            help="Graine aléatoire pour la reproductibilité")
    run_parser.add_argument("--output-dir", type=str, default=None,
                            help="Dossier de sortie")
    run_parser.add_argument("--data-dir", type=str, default=None,
                            help="Dossier de données (modalities, interdependencies)")
    run_parser.add_argument("--mock", action="store_true",
                            help="Mode mock (narratif déterministe, pas d'appel LLM)")
    run_parser.add_argument("--no-llm", action="store_true",
                            help="Mode sans LLM (narratif simplifié)")
    run_parser.add_argument("--phase-start", type=int, default=1,
                            help="Phase de départ (charge l'état précédent si > 1)")

    args = parser.parse_args(argv)

    if args.command != "run":
        parser.print_help()
        sys.exit(1)

    config = load_config(args.config)

    run_simulation(
        config=config,
        seed=args.seed,
        output_dir=args.output_dir,
        data_dir=args.data_dir,
        mock=args.mock,
        no_llm=args.no_llm or args.mock,
        phase_start=args.phase_start,
    )


if __name__ == "__main__":
    main()
