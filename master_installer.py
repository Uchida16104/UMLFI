import os, sys, subprocess, platform, shutil, textwrap, time

ROOT = os.path.abspath(os.getcwd())
VENV = os.path.join(ROOT, "venv")
IS_WIN = platform.system() == "Windows"
PY = os.path.join(VENV, "Scripts", "python.exe") if IS_WIN else os.path.join(VENV, "bin", "python")
NPM = "npm.cmd" if IS_WIN else "npm"

def kill_processes():
    """Finish all running process to unlock file on Windows"""
    if IS_WIN:
        print(">> Releasing file locks...")
        subprocess.run('taskkill /F /IM python.exe /T 2>nul', shell=True)
        subprocess.run('taskkill /F /IM node.exe /T 2>nul', shell=True)
        time.sleep(1)

def run(cmd, cwd=None):
    print(f">> Executing: {cmd}")
    subprocess.run(cmd, shell=True, check=True, cwd=cwd)

def write(path, content):
    full_path = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(content))

def main():
    print(f"=== UMLFI ULTIMATE DEPLOYMENT (OS: {platform.system()}) ===")
    
    kill_processes()
    if os.path.exists(VENV):
        try:
            shutil.rmtree(VENV)
        except Exception as e:
            print(f"[RETRY] Manual cleanup needed or use a different folder: {e}")
            new_venv = f"{VENV}_{int(time.time())}"
            print(f"Switching to new venv path: {new_venv}")

    run(f'"{sys.executable}" -m venv venv')
    run(f'"{PY}" -m pip install --upgrade pip')
    run(f'"{PY}" -m pip install fastapi uvicorn sqlalchemy pandas scikit-learn numpy')

    write("backend/__init__.py", "")
    write("backend/database.py", """
        from sqlalchemy import Column, Integer, Float, create_engine
        from sqlalchemy.orm import declarative_base, sessionmaker
        engine = create_engine("sqlite:///./data/storage.db", connect_args={"check_same_thread": False})
        Base = declarative_base()
        class Stats(Base):
            __tablename__ = "stats"
            id = Column(Integer, primary_key=True)
            val = Column(Float)
        Base.metadata.create_all(bind=engine)
    """)

    write("backend/analysis_engine.py", """
        import pandas as pd
        import numpy as np
        from sklearn.linear_model import LinearRegression
        def run_analysis():
            x = np.array([0, 1, 2, 3, 4]).reshape(-1, 1)
            y = np.array([2, 3, 5, 8, 11])
            model = LinearRegression().fit(x, y)
            return {"prediction": float(model.predict([[5]])[0]), "status": "computed"}
    """)

    write("backend/main.py", """
        import uvicorn
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        try:
            from backend.analysis_engine import run_analysis
        except ImportError:
            from analysis_engine import run_analysis
        
        app = FastAPI()
        app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
        @app.get("/api/data")
        def get_data(): return run_analysis()
        if __name__ == "__main__":
            uvicorn.run(app, host="0.0.0.0", port=8000)
    """)

    write("frontend/package.json", """
        {
          "name": "umlfi-frontend",
          "scripts": { "dev": "next dev" },
          "dependencies": { "next": "latest", "react": "latest", "react-dom": "latest", "typescript": "latest", "@types/react": "latest", "@types/node": "latest" }
        }
    """)
    write("frontend/pages/index.tsx", """
        import React, { useEffect, useState } from 'react';
        export default function Home() {
            const [d, setD] = useState<any>(null);
            useEffect(() => {
                fetch('http://localhost:3000/api/data').then(r => r.json()).then(setD);
            }, []);
            return (
                <div style={{padding: '50px', background: '#1a1a1a', color: 'white', minHeight: '100vh'}}>
                    <h1>UMLFI Full-Stack Infrastructure</h1>
                    <div style={{background: '#333', padding: '20px', borderRadius: '10px'}}>
                        <h2>ML Engine Prediction:</h2>
                        {d ? <code style={{fontSize: '20px'}}>{JSON.stringify(d)}</code> : "Wait..."}
                    </div>
                </div>
            );
        }
    """)

    if shutil.which("npm") or shutil.which("npm.cmd"):
        run(f'"{NPM}" install', cwd=os.path.join(ROOT, "frontend"))

    print("\n" + "="*60)
    print("Completed")
    print(f"terminal 1 (Backend): {PY} -m backend.main")
    print(f"terminal 2 (Frontend): cd frontend && npm run dev")
    print("="*60)

if __name__ == "__main__":
    main()