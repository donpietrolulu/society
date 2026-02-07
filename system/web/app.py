"""Minimal web server for AGENCY simulation dashboard."""
import json
import os
import subprocess
import sys
import threading
import time
import uuid
from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs

HOST = "127.0.0.1"
PORT = 8765

# Job storage
_jobs = {}
_jobs_lock = threading.Lock()

# Default paths
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_OUTPUT_DIR = os.path.join(os.path.dirname(BASE_DIR), "experience", "Test1", "phases")
DEFAULT_DATA_DIR = os.path.join(BASE_DIR, "data")


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
        self.send_header("Access-Control-Allow-Methods", "GET, POST, OPTIONS")
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
        elif path == "/api/pick-directory":
            self._api_pick_directory()
        elif path == "/api/validate":
            self._api_validate()
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
        output_dir = params.get("dir", [DEFAULT_OUTPUT_DIR])[0]
        if not os.path.isdir(output_dir):
            self._send_json({"files": []})
            return
        files = []
        for root, dirs, filenames in os.walk(output_dir):
            for fname in sorted(filenames):
                rel = os.path.relpath(os.path.join(root, fname), output_dir)
                files.append(rel)
        self._send_json({"files": files, "output_dir": output_dir})

    def _api_jobs_list(self):
        with _jobs_lock:
            jobs = [{"id": jid, "status": j["status"], "started": j["started"]}
                    for jid, j in _jobs.items()]
        self._send_json({"jobs": jobs})

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
        })

    def _serve_file(self, name):
        # Serve files from default output dir
        fpath = os.path.join(DEFAULT_OUTPUT_DIR, name)
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
        output_dir = body.get("output_dir", DEFAULT_OUTPUT_DIR)
        data_dir = body.get("data_dir", DEFAULT_DATA_DIR)
        mock = body.get("mock", False)
        no_llm = body.get("no_llm", False)
        phase_start = body.get("phase_start", 1)
        societe_cursor = body.get("societe_cursor")

        job_id = str(uuid.uuid4())[:8]
        with _jobs_lock:
            _jobs[job_id] = {
                "status": "running",
                "started": time.strftime("%Y-%m-%d %H:%M:%S"),
                "log": "",
                "return_code": None,
            }

        # Build command
        cmd = [sys.executable, "-m", "system.sim", "run",
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
        if societe_cursor is not None:
            cmd.extend(["--societe-cursor", str(float(societe_cursor))])

        # Set env for file-based validation
        env = dict(os.environ)
        env["SIM_VALIDATE_MODE"] = "file"
        env["SIM_VALIDATE_DIR"] = output_dir

        def run_job():
            try:
                proc = subprocess.Popen(
                    cmd,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.STDOUT,
                    cwd=os.path.dirname(BASE_DIR),
                    env=env,
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
                    _jobs[job_id]["log"] = "".join(output)
            except Exception as e:
                with _jobs_lock:
                    _jobs[job_id]["status"] = "failed"
                    _jobs[job_id]["log"] += f"\nErreur: {e}"

        t = threading.Thread(target=run_job, daemon=True)
        t.start()

        self._send_json({"job_id": job_id, "status": "running"})

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
                    cwd=os.path.dirname(BASE_DIR),
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

    def _api_pick_directory(self):
        """Use AppleScript to pick directory (macOS only)."""
        try:
            result = subprocess.run(
                ["osascript", "-e",
                 'tell application "Finder" to return POSIX path of '
                 '(choose folder with prompt "Choisir le dossier de sortie")'],
                capture_output=True, text=True, timeout=30,
            )
            if result.returncode == 0:
                self._send_json({"directory": result.stdout.strip()})
            else:
                self._send_json({"error": "Annulé ou non disponible"}, 400)
        except (FileNotFoundError, subprocess.TimeoutExpired):
            self._send_json({"error": "osascript non disponible (non macOS?)"}, 400)

    def _api_validate(self):
        body = self._read_body()
        phase = body.get("phase")
        output_dir = body.get("output_dir", DEFAULT_OUTPUT_DIR)
        if phase is None:
            self._send_json({"error": "phase requise"}, 400)
            return
        os.makedirs(output_dir, exist_ok=True)
        ok_path = os.path.join(output_dir, f"phase_{phase}_ok")
        with open(ok_path, "w") as f:
            f.write("ok")
        self._send_json({"validated": phase})


def run_server(host=HOST, port=PORT):
    """Start the web server."""
    server = HTTPServer((host, port), SimHandler)
    print(f"AGENCY Dashboard: http://{host}:{port}")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        print("\nArrêt du serveur.")
        server.server_close()


if __name__ == "__main__":
    run_server()
