"""Validation system: CLI prompt or file-based."""
import os
import time
import uuid


def wait_for_validation(phase, output_dir, print_fn=None):
    """Wait for manual validation of a phase.

    Modes:
    - CLI (default): prompt user to type 'ok'
    - File: wait for a validation file to appear (SIM_VALIDATE_MODE=file)
    """
    if print_fn is None:
        print_fn = print

    mode = os.environ.get("SIM_VALIDATE_MODE", "cli")

    if mode == "file":
        _wait_file_validation(phase, output_dir, print_fn)
    else:
        _wait_cli_validation(phase, print_fn)


def _wait_cli_validation(phase, print_fn):
    """Wait for CLI input."""
    while True:
        print_fn(f"Phase {phase} terminée. Tape 'ok' pour continuer:")
        try:
            response = input().strip().lower()
            if response == "ok":
                return
        except EOFError:
            # Non-interactive mode, auto-validate
            return


def _wait_file_validation(phase, output_dir, print_fn):
    """Wait for validation file."""
    validate_dir = os.environ.get("SIM_VALIDATE_DIR", output_dir)
    os.makedirs(validate_dir, exist_ok=True)

    # Generate token
    token = str(uuid.uuid4())[:8]
    token_file = os.path.join(validate_dir, f"validate_{token}_phase_{phase}.token")
    with open(token_file, "w") as f:
        f.write(token)

    print_fn(f"En attente de validation (phase {phase}).")
    print_fn(f"Créer le fichier : phase_{phase}_ok ou validate_{token}_phase_{phase}.ok")
    print_fn(f"dans le dossier : {validate_dir}")

    while True:
        # Check for simple ok file
        simple = os.path.join(validate_dir, f"phase_{phase}_ok")
        token_ok = os.path.join(validate_dir, f"validate_{token}_phase_{phase}.ok")

        if os.path.exists(simple) or os.path.exists(token_ok):
            # Clean up token file
            if os.path.exists(token_file):
                os.remove(token_file)
            return

        time.sleep(1)
