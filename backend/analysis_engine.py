import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from datetime import datetime

def run_advanced_analysis():
    # 1. Keep data 1-dimensional for Pandas
    data = {
        "day": [1, 2, 3, 4, 5],
        "value": [10, 12, 15, 14, 18]
    }
    df = pd.DataFrame(data)
    
    # 2. Reshape to 2D only for the Scikit-Learn fit method
    X = df[['day']].values # This automatically handles the 2D requirement
    y = df['value'].values
    
    model = LinearRegression()
    model.fit(X, y)
    
    # 3. Predict for day 6
    prediction = model.predict([[6]])
    
    return {
        "timestamp": datetime.now().isoformat(),
        "model": "LinearRegression",
        "input_data": data["value"],
        "next_prediction": round(float(prediction[0]), 2),
        "status": "calculated_by_sklearn"
    }