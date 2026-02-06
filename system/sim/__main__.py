"""CLI entrypoint: python -m system.sim run"""
import sys
from system.sim.cli import main

if __name__ == "__main__":
    main(sys.argv[1:])
