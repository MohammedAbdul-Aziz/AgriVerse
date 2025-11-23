# train_models.py
import os
import numpy as np
import joblib
from sklearn.ensemble import RandomForestRegressor
from sklearn.model_selection import train_test_split

MODEL_DIR = os.path.join(os.path.dirname(__file__), "models")
os.makedirs(MODEL_DIR, exist_ok=True)

def simple_train(fn, X, y):
    model = RandomForestRegressor(n_estimators=50, random_state=42)
    model.fit(X, y)
    joblib.dump(model, os.path.join(MODEL_DIR, fn))
    print("Saved", fn)

def make_and_save():
    # crop_price model: inputs [month, demand_index, avg_yield]
    X = np.column_stack([
        np.random.randint(1,13,1000),
        np.random.uniform(0.5,1.5,1000),
        np.random.uniform(0.5,2.0,1000),
    ])
    y = 100 * (1 + 0.05*(12 - np.abs(6 - X[:,0]))) * X[:,1] / np.maximum(0.5, X[:,2]) + np.random.normal(0,5,1000)
    simple_train("crop_price.pkl", X, y)

    # yield model: inputs [rainfall_mm, fertilizer_kg_per_ha, soil_index]
    X = np.column_stack([
        np.random.uniform(200,1200,1000),
        np.random.uniform(50,300,1000),
        np.random.uniform(0.7,1.4,1000),
    ])
    y = 0.002*X[:,0] + 0.01*X[:,1]*X[:,2] + np.random.normal(0,0.3,1000)
    simple_train("yield_model.pkl", X, y)

    # pest risk: [humidity, temperature_c, recent_pests]
    X = np.column_stack([
        np.random.uniform(30,95,1000),
        np.random.uniform(15,40,1000),
        np.random.randint(0,5,1000),
    ])
    y = np.clip((X[:,0]/100)*(X[:,1]/35) + 0.1*X[:,2] + np.random.normal(0,0.05,1000), 0, 1)
    simple_train("pest_risk.pkl", X, y)

    # fertilizer_need: [nitrogen_deficit_kg, crop_stage]
    X = np.column_stack([
        np.random.uniform(0,100,1000),
        np.random.randint(1,6,1000),
    ])
    y = X[:,0] * (1 + 0.1*(3 - X[:,1])) + np.random.normal(0,2,1000)
    simple_train("fertilizer_need.pkl", X, y)

    # rainfall_risk: [recent_7days_mm]
    X = np.random.uniform(0,200,(1000,1))
    y = np.clip(X[:,0] / 100 + np.random.normal(0,0.05,1000), 0, 1)
    simple_train("rainfall_risk.pkl", X, y)

if __name__ == "__main__":
    make_and_save()
    print("Demo models trained and saved to models/")
