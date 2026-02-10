import os
import logging
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

# absolute import (safer for different invocation methods)
from backend import analysis_engine

logger = logging.getLogger("uvicorn.error")

app = FastAPI(title="UMLFI API", version="1.0.0")

# Read allowed origins from environment variable (comma-separated)
allowed_origins_env = os.getenv("ALLOWED_ORIGINS", "")
if allowed_origins_env:
    allowed_origins = [o.strip() for o in allowed_origins_env.split(",") if o.strip()]
else:
    allowed_origins = ["http://localhost:3000", "http://127.0.0.1:3000"]

# If you want to allow everything (not recommended in production), set ALLOWED_ORIGINS="*"
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
    try:
        result = analysis_engine.run_advanced_analysis()
        return result
    except Exception as e:
        logger.exception("advanced analysis failed")
        raise HTTPException(status_code=500, detail=str(e))
