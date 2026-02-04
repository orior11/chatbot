"""
One-command startup for the full-stack chatbot.
Runs backend (FastAPI + uvicorn) and frontend (Vite dev server) simultaneously.
Press Ctrl+C to stop both processes cleanly.
"""
import os
import sys
import subprocess
from pathlib import Path

# Project root (directory containing run_app.py)
ROOT = Path(__file__).resolve().parent
BACKEND_DIR = ROOT / "backend"
FRONTEND_DIR = ROOT / "frontend"


def load_env():
    """Load .env from project root into os.environ."""
    env_file = ROOT / ".env"
    if not env_file.exists():
        return
    with open(env_file, encoding="utf-8") as f:
        for line in f:
            line = line.strip()
            if line and "=" in line and not line.startswith("#"):
                key, _, value = line.partition("=")
                key, value = key.strip(), value.strip().strip("'\"")
                if key:
                    os.environ[key] = value


def get_backend_python():
    """Use backend venv or .venv if present; otherwise current Python."""
    for venv_name in ("venv", ".venv"):
        venv_dir = BACKEND_DIR / venv_name
        if not venv_dir.is_dir():
            continue
        if os.name == "nt":
            exe = venv_dir / "Scripts" / "python.exe"
        else:
            exe = venv_dir / "bin" / "python"
        if exe.exists():
            return [str(exe)]
    return [sys.executable]


def main():
    load_env()
    if not os.getenv("GEMINI_API_KEY") or not os.getenv("GEMINI_API_KEY").strip():
        print("GEMINI_API_KEY is missing in .env. Add it to the project root .env file.")
        sys.exit(1)

    if not BACKEND_DIR.is_dir():
        print(f"Backend folder not found: {BACKEND_DIR}")
        sys.exit(1)
    if not FRONTEND_DIR.is_dir():
        print(f"Frontend folder not found: {FRONTEND_DIR}")
        sys.exit(1)

    python_cmd = get_backend_python()
    backend_cmd = python_cmd + ["-m", "uvicorn", "main:app", "--reload", "--host", "0.0.0.0", "--port", "3002"]
    # Frontend: Vite uses "npm run dev" (no "start" script in package.json)
    frontend_cmd = ["npm", "run", "dev"]

    print("Starting backend (FastAPI) and frontend (Vite)...")
    print("Backend: http://localhost:3002  |  Frontend: http://localhost:5173")
    print("Press Ctrl+C to stop both.\n")

    # Start both processes; use creationflags on Windows so we can terminate the process tree
    creation_flags = subprocess.CREATE_NEW_PROCESS_GROUP if os.name == "nt" else 0
    backend_proc = subprocess.Popen(
        backend_cmd,
        cwd=str(BACKEND_DIR),
        stdout=sys.stdout,
        stderr=sys.stderr,
        creationflags=creation_flags,
    )
    frontend_proc = subprocess.Popen(
        frontend_cmd,
        cwd=str(FRONTEND_DIR),
        stdout=sys.stdout,
        stderr=sys.stderr,
        shell=(os.name == "nt"),
        creationflags=creation_flags,
    )

    def shutdown():
        for proc, name in [(backend_proc, "Backend"), (frontend_proc, "Frontend")]:
            if proc.poll() is None:
                print(f"\nStopping {name}...")
                proc.terminate()
                try:
                    proc.wait(timeout=5)
                except subprocess.TimeoutExpired:
                    proc.kill()
                    proc.wait()

    try:
        backend_proc.wait()
        frontend_proc.wait()
    except KeyboardInterrupt:
        shutdown()
    finally:
        shutdown()


if __name__ == "__main__":
    main()
