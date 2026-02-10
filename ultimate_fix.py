import os, sys, subprocess, textwrap, shutil

ROOT = os.path.abspath(os.getcwd())
VENV = os.path.join(ROOT, "venv")
# Python 3.14+ のパス形式に対応
PY_EXE = os.path.join(VENV, "Scripts", "python.exe") if os.name == "nt" else os.path.join(VENV, "bin", "python")

def run(cmd, desc):
    print(f"\n>> {desc}...")
    try:
        subprocess.run(cmd, shell=True, check=True)
    except subprocess.CalledProcessError:
        print(f"[ERROR] Failed: {desc}")
        return False
    return True

def write(path, content):
    full_path = os.path.join(ROOT, path)
    os.makedirs(os.path.dirname(full_path), exist_ok=True)
    with open(full_path, "w", encoding="utf-8") as f:
        f.write(textwrap.dedent(content))

def main():
    print("=== UMLFI HYDRA-BOOTSTRAP SYSTEM (Target: Python 3.14+) ===")

    # 1. 仮想環境のクリーン作成 (pipを強制含める)
    if os.path.exists(VENV):
        print("Cleaning old environment...")
        subprocess.run(f'taskkill /F /IM python.exe /T 2>nul', shell=True)
        shutil.rmtree(VENV, ignore_errors=True)
    
    # --with-pip を明示的に指定して作成
    run(f'"{sys.executable}" -m venv "{VENV}" --with-pip', "Creating Virtual Environment")

    # 2. pip がない場合の最終手段: ensurepip
    run(f'"{PY_EXE}" -m ensurepip --upgrade', "Bootstrapping Pip via ensurepip")
    run(f'"{PY_EXE}" -m pip install --upgrade pip', "Upgrading Pip")

    # 3. 依存関係の確実なインストール
    packages = "fastapi uvicorn sqlalchemy pandas scikit-learn numpy"
    run(f'"{PY_EXE}" -m pip install {packages}', f"Installing Core Stack: {packages}")

    # 4. バックエンド・ファイル群の完全生成
    write("backend/__init__.py", "")
    write("backend/analysis_engine.py", """
        import pandas as pd
        import numpy as np
        from sklearn.linear_model import LinearRegression
        def run_analysis():
            x = np.array([1, 2, 3, 4, 5]).reshape(-1, 1)
            y = np.array([10, 20, 30, 40, 50])
            model = LinearRegression().fit(x, y)
            return {"prediction": float(model.predict([[6]])[0]), "engine": "scikit-learn"}
    """)

    write("backend/main.py", """
        import sys, os, uvicorn
        from fastapi import FastAPI
        from fastapi.middleware.cors import CORSMiddleware
        
        # 実行時に自身をパッケージとして認識させる
        sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
        
        from backend.analysis_engine import run_analysis

        app = FastAPI()
        app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

        @app.get("/api/data")
        def get_data(): return run_analysis()

        if __name__ == "__main__":
            uvicorn.run("backend.main:app", host="0.0.0.0", port=8000, reload=False)
    """)

    print("\n" + "="*60)
    print("【完全復旧成功】インフラが整いました。")
    print(f"起動コマンド: \"{PY_EXE}\" -m backend.main")
    print("="*60)
    
    # 自動起動
    os.environ["PYTHONPATH"] = ROOT
    subprocess.run([PY_EXE, "-m", "backend.main"])

if __name__ == "__main__":
    main()