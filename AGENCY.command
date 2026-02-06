#!/bin/zsh
set -e
DIR="${0:A:h}"
cd "$DIR"

/usr/bin/env python3 system/web/app.py &
SERVER_PID=$!

sleep 0.8
open "http://127.0.0.1:8765"

echo "Serveur lance (pid $SERVER_PID). Ferme cette fenetre pour arreter."
wait $SERVER_PID
