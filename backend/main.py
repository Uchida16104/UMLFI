
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
