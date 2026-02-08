#!/usr/bin/env python3
"""Lanceur AGENCY — demarre le serveur et ouvre le navigateur."""
import os
import sys
import threading
import webbrowser
import time

# S'assurer qu'on est dans le bon dossier
os.chdir(os.path.dirname(os.path.abspath(__file__)))

# Ajouter le dossier au path pour les imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from system.web.app import run_server, HOST, PORT


def open_browser():
    """Ouvre le navigateur apres un court delai."""
    time.sleep(1.2)
    url = f"http://127.0.0.1:{PORT}"
    print(f"Ouverture du navigateur: {url}")
    webbrowser.open(url)


if __name__ == "__main__":
    print("AGENCY — Demarrage...")
    threading.Thread(target=open_browser, daemon=True).start()
    run_server()
