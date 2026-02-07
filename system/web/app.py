"""Web server for AGENCY simulation — full terminal interface."""
import json
import os
import subprocess
import sys
import threading
import time
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

HOST = "0.0.0.0"
PORT = 8765

# Job storage
_jobs = {}
_jobs_lock = threading.Lock()

# Terminal session storage
_terminals = {}
_terminals_lock = threading.Lock()

# Default paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
PROJECT_DIR = os.path.dirname(BASE_DIR)
EXPERIENCE_DIR = os.path.join(PROJECT_DIR, "experience")
DEFAULT_DATA_DIR = os.path.join(BASE_DIR, "data")


def _next_test_dir():
    """Find next TestN directory number and return its phases path."""
    os.makedirs(EXPERIENCE_DIR, exist_ok=True)
    n = 1
    while os.path.exists(os.path.join(EXPERIENCE_DIR, f"Test{n}")):
        n += 1
    return os.path.join(EXPERIENCE_DIR, f"Test{n}", "phases")


def _clean_validation_files(output_dir):
    """Remove old validation marker files before starting a new simulation."""
    if not os.path.isdir(output_dir):
        return
    for fname in os.listdir(output_dir):
        if fname.startswith("phase_") and fname.endswith("_ok"):
            os.remove(os.path.join(output_dir, fname))
        elif fname.startswith("validate_") and (fname.endswith(".token") or fname.endswith(".ok")):
            os.remove(os.path.join(output_dir, fname))


class TerminalSession:
    """A persistent terminal session with command history."""

    def __init__(self, cwd=None):
        self.cwd = cwd or PROJECT_DIR
        self.history = []
        self.lock = threading.Lock()

    def execute(self, command):
        """Execute a command and return output."""
        with self.lock:
            try:
                env = dict(os.environ)
                env["PYTHONUNBUFFERED"] = "1"
                env["TERM"] = "dumb"
                proc = subprocess.Popen(
                    command,
                    shell=True,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd=self.cwd,
                    env=env,
                    text=True,
                )
                output, _ = proc.communicate(timeout=120)
                # Handle cd commands
                if command.strip().startswith("cd "):
                    target = command.strip()[3:].strip().strip('"').strip("'")
                    if target == "~":
                        target = os.path.expanduser("~")
                    new_dir = os.path.join(self.cwd, target) if not os.path.isabs(target) else target
                    new_dir = os.path.realpath(new_dir)
                    if os.path.isdir(new_dir):
                        self.cwd = new_dir

                entry = {
                    "command": command,
                    "output": output,
                    "return_code": proc.returncode,
                    "cwd": self.cwd,
                    "timestamp": time.strftime("%H:%M:%S"),
                }
                self.history.append(entry)
                return entry
            except subprocess.TimeoutExpired:
                proc.kill()
                return {
                    "command": command,
                    "output": "[Commande interrompue: timeout 120s]",
                    "return_code": -1,
                    "cwd": self.cwd,
                    "timestamp": time.strftime("%H:%M:%S"),
                }
            except Exception as e:
                return {
                    "command": command,
                    "output": f"Erreur: {e}",
                    "return_code": -1,
                    "cwd": self.cwd,
                    "timestamp": time.strftime("%H:%M:%S"),
                }


class SimHandler(BaseHTTPRequestHandler):
    """HTTP request handler for the simulation dashboard."""

    def log_message(self, format, *args):
        pass  # Suppress default logging

    def _send_json(self, data, status=200):
        body = json.dumps(data, ensure_ascii=False, indent=2).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()
        self.wfile.write(body)

    def _send_html(self, content, status=200):
        body = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _send_text(self, content, status=200, content_type="text/plain"):
        body = content.encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", f"{content_type}; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def _read_body(self):
        length = int(self.headers.get("Content-Length", 0))
        if length:
            return json.loads(self.rfile.read(length).decode("utf-8"))
        return {}

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, POST, DELETE, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/":
            self._serve_index()
        elif path == "/api/outputs":
            self._api_outputs(parse_qs(parsed.query))
        elif path == "/api/jobs":
            self._api_jobs_list()
        elif path.startswith("/api/jobs/"):
            job_id = path.split("/")[-1]
            self._api_job_detail(job_id)
        elif path == "/api/browse":
            self._api_browse(parse_qs(parsed.query))
        elif path == "/api/file":
            self._api_read_file(parse_qs(parsed.query))
        elif path == "/api/config":
            self._api_get_config()
        elif path == "/api/modalities":
            self._api_get_modalities()
        elif path.startswith("/files/"):
            self._serve_file(path[7:])
        else:
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        parsed = urlparse(self.path)
        path = parsed.path

        if path == "/api/simulate":
            self._api_simulate()
        elif path == "/api/test":
            self._api_test()
        elif path == "/api/validate":
            self._api_validate()
        elif path == "/api/terminal/exec":
            self._api_terminal_exec()
        elif path == "/api/file/save":
            self._api_save_file()
        else:
            self.send_response(404)
            self.end_headers()

    def _serve_index(self):
        html_path = os.path.join(os.path.dirname(__file__), "index.html")
        if os.path.exists(html_path):
            with open(html_path, "r", encoding="utf-8") as f:
                self._send_html(f.read())
        else:
            self._send_html("<h1>AGENCY Dashboard</h1><p>index.html introuvable</p>", 404)

    def _api_outputs(self, params):
        output_dir = params.get("dir", [EXPERIENCE_DIR])[0]
        if not os.path.isdir(output_dir):
            self._send_json({"files": [], "output_dir": output_dir})
            return
        files = []
        for root, dirs, filenames in os.walk(output_dir):
            for fname in sorted(filenames):
                rel = os.path.relpath(os.path.join(root, fname), output_dir)
                files.append(rel)
        self._send_json({"files": files, "output_dir": output_dir})

    def _api_jobs_list(self):
        with _jobs_lock:
            jobs = [{"id": jid, "status": j["status"], "started": j["started"],
                     "output_dir": j.get("output_dir", "")}
                    for jid, j in _jobs.items()]
        self._send_json({"jobs": sorted(jobs, key=lambda j: j["started"], reverse=True)})

    def _api_job_detail(self, job_id):
        with _jobs_lock:
            job = _jobs.get(job_id)
        if not job:
            self._send_json({"error": "Job introuvable"}, 404)
            return
        self._send_json({
            "id": job_id,
            "status": job["status"],
            "started": job["started"],
            "log": job.get("log", ""),
            "return_code": job.get("return_code"),
            "output_dir": job.get("output_dir", ""),
        })

    def _serve_file(self, name):
        fpath = os.path.join(EXPERIENCE_DIR, name)
        if not os.path.isfile(fpath):
            self.send_response(404)
            self.end_headers()
            return
        ct = "text/plain"
        if fpath.endswith(".json"):
            ct = "application/json"
        elif fpath.endswith(".md"):
            ct = "text/markdown"
        with open(fpath, "r", encoding="utf-8") as f:
            self._send_text(f.read(), content_type=ct)

    def _api_simulate(self):
        body = self._read_body()
        config_path = body.get("config")
        seed = body.get("seed")
        data_dir = body.get("data_dir", DEFAULT_DATA_DIR)
        mock = body.get("mock", False)
        no_llm = body.get("no_llm", False)
        phase_start = body.get("phase_start", 1)

        # Auto-increment output dir if not specified
        output_dir = body.get("output_dir", "").strip()
        if not output_dir:
            output_dir = _next_test_dir()

        # Clean old validation files to prevent auto-skip
        _clean_validation_files(output_dir)

        job_id = str(uuid.uuid4())[:8]
        with _jobs_lock:
            _jobs[job_id] = {
                "status": "running",
                "started": time.strftime("%Y-%m-%d %H:%M:%S"),
                "log": "",
                "return_code": None,
                "output_dir": output_dir,
            }

        cmd = [sys.executable, "-u", "-m", "system.sim", "run",
               "--output-dir", output_dir,
               "--data-dir", data_dir,
               "--phase-start", str(phase_start)]
        if config_path:
            cmd.extend(["--config", config_path])
        if seed is not None:
            cmd.extend(["--seed", str(seed)])
        if mock:
            cmd.append("--mock")
        if no_llm:
            cmd.append("--no-llm")

        env = dict(os.environ)
        env["SIM_VALIDATE_MODE"] = "file"
        env["SIM_VALIDATE_DIR"] = output_dir
        env["PYTHONUNBUFFERED"] = "1"

        def run_job():
            try:
                proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    stdin=subprocess.DEVNULL,
                    cwd=PROJECT_DIR,
                    env=env,
                    text=True,
                )
                log_lines = []
                for line in proc.stdout:
                    log_lines.append(line)
                    with _jobs_lock:
                        _jobs[job_id]["log"] = "".join(log_lines)
                proc.wait()
                with _jobs_lock:
                    _jobs[job_id]["status"] = "completed" if proc.returncode == 0 else "failed"
                    _jobs[job_id]["return_code"] = proc.returncode
                    _jobs[job_id]["log"] = "".join(log_lines)
            except Exception as e:
                with _jobs_lock:
                    _jobs[job_id]["status"] = "failed"
                    _jobs[job_id]["log"] += f"\nErreur: {e}"

        t = threading.Thread(target=run_job, daemon=True)
        t.start()

        self._send_json({"job_id": job_id, "status": "running", "output_dir": output_dir})

    def _api_test(self):
        job_id = f"test-{uuid.uuid4().hex[:6]}"
        with _jobs_lock:
            _jobs[job_id] = {
                "status": "running",
                "started": time.strftime("%Y-%m-%d %H:%M:%S"),
                "log": "",
                "return_code": None,
            }

        def run_tests():
            try:
                proc = subprocess.Popen(
                    [sys.executable, "-m", "unittest", "system.tests.test_simulation", "-v"],
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd=PROJECT_DIR,
                    text=True,
                )
                output = []
                for line in proc.stdout:
                    output.append(line)
                    with _jobs_lock:
                        _jobs[job_id]["log"] = "".join(output)
                proc.wait()
                with _jobs_lock:
                    _jobs[job_id]["status"] = "completed" if proc.returncode == 0 else "failed"
                    _jobs[job_id]["return_code"] = proc.returncode
            except Exception as e:
                with _jobs_lock:
                    _jobs[job_id]["status"] = "failed"
                    _jobs[job_id]["log"] += f"\nErreur: {e}"

        t = threading.Thread(target=run_tests, daemon=True)
        t.start()

        self._send_json({"job_id": job_id, "status": "running"})

    def _api_validate(self):
        body = self._read_body()
        phase = body.get("phase")
        output_dir = body.get("output_dir", "").strip()

        # If no output_dir specified, find it from the latest running job
        if not output_dir:
            with _jobs_lock:
                for jid, j in sorted(_jobs.items(), key=lambda x: x[1]["started"], reverse=True):
                    if j.get("output_dir"):
                        output_dir = j["output_dir"]
                        break

        if not output_dir:
            self._send_json({"error": "output_dir requis (aucun job actif)"}, 400)
            return
        if phase is None:
            self._send_json({"error": "phase requise"}, 400)
            return

        os.makedirs(output_dir, exist_ok=True)
        ok_path = os.path.join(output_dir, f"phase_{phase}_ok")
        with open(ok_path, "w") as f:
            f.write("ok")
        self._send_json({"validated": phase, "output_dir": output_dir})

    # --- Terminal API ---

    def _api_terminal_exec(self):
        """Execute a command in the terminal session."""
        body = self._read_body()
        command = body.get("command", "").strip()
        session_id = body.get("session_id", "default")

        if not command:
            self._send_json({"error": "Commande vide"}, 400)
            return

        with _terminals_lock:
            if session_id not in _terminals:
                _terminals[session_id] = TerminalSession(cwd=PROJECT_DIR)
            session = _terminals[session_id]

        result = session.execute(command)
        self._send_json(result)

    # --- File browser API ---

    def _api_browse(self, params):
        """Browse directory contents."""
        dir_path = params.get("path", [PROJECT_DIR])[0]
        if not os.path.isdir(dir_path):
            self._send_json({"error": "Dossier introuvable", "path": dir_path}, 404)
            return

        entries = []
        try:
            for name in sorted(os.listdir(dir_path)):
                full = os.path.join(dir_path, name)
                if name.startswith(".") and name not in (".gitignore",):
                    continue
                is_dir = os.path.isdir(full)
                size = 0
                if not is_dir:
                    try:
                        size = os.path.getsize(full)
                    except OSError:
                        pass
                entries.append({
                    "name": name,
                    "is_dir": is_dir,
                    "size": size,
                    "path": full,
                })
        except PermissionError:
            self._send_json({"error": "Permission refusée"}, 403)
            return

        self._send_json({
            "path": dir_path,
            "parent": os.path.dirname(dir_path),
            "entries": entries,
        })

    def _api_read_file(self, params):
        """Read a file's content."""
        file_path = params.get("path", [""])[0]
        if not file_path or not os.path.isfile(file_path):
            self._send_json({"error": "Fichier introuvable"}, 404)
            return
        try:
            size = os.path.getsize(file_path)
            if size > 1_000_000:
                self._send_json({"error": "Fichier trop volumineux (>1Mo)"}, 400)
                return
            with open(file_path, "r", encoding="utf-8", errors="replace") as f:
                content = f.read()
            self._send_json({
                "path": file_path,
                "content": content,
                "size": size,
            })
        except Exception as e:
            self._send_json({"error": str(e)}, 500)

    def _api_save_file(self):
        """Save content to a file."""
        body = self._read_body()
        file_path = body.get("path", "")
        content = body.get("content", "")
        if not file_path:
            self._send_json({"error": "Chemin requis"}, 400)
            return
        try:
            os.makedirs(os.path.dirname(file_path), exist_ok=True)
            with open(file_path, "w", encoding="utf-8") as f:
                f.write(content)
            self._send_json({"saved": file_path, "size": len(content)})
        except Exception as e:
            self._send_json({"error": str(e)}, 500)

    # --- Config & Modalities API ---

    def _api_get_config(self):
        """Return current default config."""
        config_path = os.path.join(BASE_DIR, "config", "defaults.json")
        try:
            with open(config_path, "r", encoding="utf-8") as f:
                self._send_json(json.load(f))
        except Exception as e:
            self._send_json({"error": str(e)}, 500)

    def _api_get_modalities(self):
        """Return all modality definitions."""
        mod_dir = os.path.join(DEFAULT_DATA_DIR, "modalities")
        result = {}
        if os.path.isdir(mod_dir):
            for fname in sorted(os.listdir(mod_dir)):
                if fname.endswith(".json"):
                    with open(os.path.join(mod_dir, fname), "r", encoding="utf-8") as f:
                        result[fname.replace(".json", "")] = json.load(f)
        self._send_json(result)


def run_server(host=HOST, port=PORT):
    """Start the web server."""
    server = HTTPServer((host, port), SimHandler)
    print(f"AGENCY Terminal: http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nArret du serveur.")
        server.server_close()


if __name__ == "__main__":
    run_server()
