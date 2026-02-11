import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# Running in Render with Root Directory = backend => uvicorn main:app
# so import modules by top-level filename (analysis_engine.py -> module name 'analysis_engine')
try:
    import analysis_engine
except Exception:
    analysis_engine = None

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="UMLFI API", version="1.0.0")

# Read allowed origins from environment variable (comma-separated)
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
if allowed_origins_env:
    allowed_origins = [o.strip() for o in allowed_origins_env.split(",") if o.strip()]
else:
    # safe development defaults
    allowed_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

# Allow everything if explicitly set to "*"
if allowed_origins_env == "*":
    cors_args = dict(allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])
else:
    cors_args = dict(allow_origins=allowed_origins, allow_methods=["GET", "POST", "OPTIONS"], allow_headers=["*"])

app.add_middleware(CORSMiddleware, **cors_args)


@app.get("/api/v1/status")
async def status():
    return {"status": "Operational", "engine": "FastAPI", "allowed_origins": allowed_origins}


@app.get("/api/v1/analyze")
async def analyze():
    import pandas as pd
    try:
        df = pd.DataFrame({"score": [85, 92, 78, 95]})
        mean_score = float(df["score"].mean())
        return {"mean_score": mean_score, "algorithm": "Data Analysis Core"}
    except Exception as e:
        logger.exception("analyze failed")
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/api/v1/advanced")
async def advanced_analysis():
    if analysis_engine is None:
        raise HTTPException(status_code=500, detail="analysis_engine not importable")
    try:
        result = analysis_engine.run_advanced_analysis()
        return result
    except Exception as e:
        logger.exception("advanced analysis failed")
        raise HTTPException(status_code=500, detail=str(e))
