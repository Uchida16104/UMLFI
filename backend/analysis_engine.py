import pandas as pd
import numpy as np
from datetime import datetime
import logging

logger = logging.getLogger("uvicorn.error")

# Try sklearn, but provide numpy.polyfit fallback
try:
    from sklearn.linear_model import LinearRegression
    _SKLEARN_AVAILABLE = True
except Exception:
    _SKLEARN_AVAILABLE = False
    logger.warning("scikit-learn not available: using numpy.polyfit fallback")


def run_advanced_analysis():
    """
    Minimal example analysis:
      - fits linear trend to tiny dataset
      - returns next-day prediction and metadata
    """
    data = {"day": [1, 2, 3, 4, 5], "value": [10, 12, 15, 14, 18]}
    df = pd.DataFrame(data)

    try:
        X = df[["day"]].values
        y = df["value"].values
        next_day = int(df["day"].max()) + 1

        if _SKLEARN_AVAILABLE:
            model = LinearRegression()
            model.fit(X, y)
            prediction = model.predict([[next_day]])
            pred_value = float(prediction[0])
            used = "sklearn.LinearRegression"
        else:
            coeffs = np.polyfit(df["day"].values, df["value"].values, 1)
            pred_value = float(coeffs[0] * next_day + coeffs[1])
            used = "numpy.polyfit(deg=1)_fallback"

        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "model_used": used,
            "input_data": data["value"],
            "next_day": next_day,
            "next_prediction": round(pred_value, 4),
            "status": "ok"
        }
    except Exception as e:
        logger.exception("run_advanced_analysis error")
        return {
            "timestamp": datetime.utcnow().isoformat() + "Z",
            "model_used": None,
            "input_data": data["value"],
            "error": str(e),
            "status": "error"
        }
