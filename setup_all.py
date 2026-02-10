import os
import sys
import subprocess
import platform
import shutil
import textwrap

# --- Configuration ---
ROOT_DIR = os.path.abspath(os.getcwd())
VENV_DIR = os.path.join(ROOT_DIR, "venv")
IS_WIN = platform.system() == "Windows"

# OS specific paths
if IS_WIN:
    PY = os.path.join(VENV_DIR, "Scripts", "python.exe")
    NPM = "npm.cmd"
else:
    PY = os.path.join(VENV_DIR, "bin", "python")
    NPM = "npm"

def run(cmd, cwd=None):
    print(f">> Executing: {cmd}")
    try:
        subprocess.run(cmd, shell=True, check=True, cwd=cwd)
    except Exception as e:
        print(f"[CRITICAL ERROR] {e}")
        sys.exit(1)

def write_file(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(content))

def main():
    print(f"--- UMLFI Deployment Started (OS: {platform.system()}) ---")

    # 1. Setup Virtual Environment
    if os.path.exists(VENV_DIR):
        shutil.rmtree(VENV_DIR)
    run(f'"{sys.executable}" -m venv venv')

    # 2. Safe Pip Upgrade & Dependency Install
    run(f'"{PY}" -m pip install --upgrade pip')
    run(f'"{PY}" -m pip install fastapi uvicorn pandas scikit-learn numpy sqlalchemy')

    # 3. Create Backend Infrastructure
    write_file("backend/main.py", """
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        import pandas as pd

        app = FastAPI()
        app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

        @app.get("/api/v1/status")
        def status(): return {"status": "Operational", "engine": "FastAPI 0.1"}

        @app.get("/api/v1/analyze")
        def analyze():
            df = pd.DataFrame({"score": [85, 92, 78, 95]})
            return {"mean_score": float(df["score"].mean()), "algorithm": "Data Analysis Core"}
    """)

    # 4. Create Frontend Infrastructure (Next.js Structure)
    write_file("frontend/package.json", """
        {
          "name": "umlfi-frontend",
          "version": "1.0.0",
          "scripts": { "dev": "next dev" },
          "dependencies": {
            "next": "latest", "react": "latest", "react-dom": "latest", "typescript": "latest"
          }
        }
    """)
    
    write_file("frontend/pages/index.tsx", """
        import React, { useEffect, useState } from 'react';
        export default function Dashboard() {
            const [data, setData] = useState<any>(null);
            useEffect(() => {
                fetch('http://localhost:8000/api/v1/analyze')
                    .then(res => res.json()).then(d => setData(d));
            }, []);
            return (
                <div style={{padding: '50px', backgroundColor: '#f0f2f5', minHeight: '100vh'}}>
                    <h1>UMLFI Multi-Language Infrastructure</h1>
                    <div style={{background: 'white', padding: '20px', borderRadius: '8px'}}>
                        <h2>Real-time Analysis</h2>
                        {data ? <pre>{JSON.stringify(data, null, 2)}</pre> : 'Loading...'}
                    </div>
                </div>
            );
        }
    """)

    # 5. Install Frontend Dependencies
    if shutil.which("npm"):
        run(f"{NPM} install", cwd="frontend")
    else:
        print("[SKIP] Node.js not found. Frontend JS only generated.")

    print("\n" + "="*60)
    print("{Complete} Launch backend by the following command:")
    print(f"1. backend: {PY} backend/main.py")
    print(f"2. frontend: cd frontend && npm run dev")
    print("="*60)

if __name__ == "__main__":
    main()