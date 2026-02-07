#!/bin/bash
# AGENCY — Lancement du dashboard
cd "$(dirname "$0")"
echo "AGENCY — Démarrage du serveur sur http://127.0.0.1:8765"
open "http://127.0.0.1:8765" &
python3 -m system.web.app
