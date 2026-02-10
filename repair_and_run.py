import os, sys, subprocess, textwrap

ROOT = os.path.abspath(os.getcwd())
VENV_PY = os.path.join(ROOT, "venv", "Scripts", "python.exe")

def run(cmd):
    print(f">> Executing: {cmd}")
    subprocess.run(cmd, shell=True, check=True)

def write(path, content):
    full_path = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(content))

def setup_core():
    print("--- Emergency Repair and Synchronization ---")
    run(f'"{VENV_PY}" -m pip install fastapi uvicorn sqlalchemy pandas scikit-learn numpy')

    write("backend/__init__.py", "")

    write("backend/main.py", """
        import sys, os, uvicorn
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        
        sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        
        from backend.analysis_engine import run_advanced_analysis

        app = FastAPI()
        app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

        @app.get("/api/v1/analyze")
        def analyze(): return run_advanced_analysis()

        if __name__ == "__main__":
            uvicorn.run(app, host="0.0.0.0", port=8000)
    """)

def start():
    print("--- Starting Backend Engine ---")
    env = os.environ.copy()
    env["PYTHONPATH"] = ROOT
    subprocess.run([VENV_PY, "backend/main.py"], env=env)

if __name__ == "__main__":
    setup_core()
    start()