# main.py

# 1. Import necessary libraries
from fastapi import FastAPI
from pydantic import BaseModel
import joblib
import numpy as np
from fastapi.middleware.cors import CORSMiddleware

# 2. Initialize the FastAPI app
app = FastAPI()

# --- 3. Set up CORS (Cross-Origin Resource Sharing) ---
# This is crucial for allowing your frontend (running on a different port)
# to make requests to this backend.
origins = [
    "http://localhost",
    "http://localhost:5173",  # This is the default port for a Vite/React app
    "http://localhost:3000",  # This is the default port for a Create-React-App
    # Add your deployed frontend URL here when you deploy
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Allows specified origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# --- 4. Load the saved model and scaler ---
# These are loaded ONCE when the app starts, not on every request.
try:
    model = joblib.load('breast_cancer_model.pkl')
    scaler = joblib.load('scaler.pkl')
    print("Model and scaler loaded successfully.")
except Exception as e:
    print(f"Error loading model or scaler: {e}")
    model = None
    scaler = None

# --- 5. Define the input data model using Pydantic ---
# This creates a "shape" for the data we expect to receive.
# FastAPI will automatically validate incoming data against this.
# These are your 30 features.
class CancerInput(BaseModel):
    radius_mean: float
    texture_mean: float
    perimeter_mean: float
    area_mean: float
    smoothness_mean: float
    compactness_mean: float
    concavity_mean: float
    concave_points_mean: float
    symmetry_mean: float
    fractal_dimension_mean: float
    radius_se: float
    texture_se: float
    perimeter_se: float
    area_se: float
    smoothness_se: float
    compactness_se: float
    concavity_se: float
    concave_points_se: float
    symmetry_se: float
    fractal_dimension_se: float
    radius_worst: float
    texture_worst: float
    perimeter_worst: float
    area_worst: float
    smoothness_worst: float
    compactness_worst: float
    concavity_worst: float
    concave_points_worst: float
    symmetry_worst: float
    fractal_dimension_worst: float

# --- 6. Create a "root" endpoint ---
# This is just a simple endpoint to check if the API is running.
@app.get("/")
def read_root():
    return {"message": "Breast Cancer Diagnosis API is running!"}

# --- 7. Create the "/predict" endpoint ---
# This is where the magic happens.
@app.post("/predict")
def predict_cancer(data: CancerInput):
    if not model or not scaler:
        return {"error": "Model or scaler not loaded. Check server logs."}

    # 1. Convert the Pydantic data into a 2D NumPy array
    # The model expects a 2D array, so we wrap it in an extra pair of []
    input_data = np.array([[
        data.radius_mean, data.texture_mean, data.perimeter_mean, data.area_mean,
        data.smoothness_mean, data.compactness_mean, data.concavity_mean,
        data.concave_points_mean, data.symmetry_mean, data.fractal_dimension_mean,
        data.radius_se, data.texture_se, data.perimeter_se, data.area_se,
        data.smoothness_se, data.compactness_se, data.concavity_se,
        data.concave_points_se, data.symmetry_se, data.fractal_dimension_se,
        data.radius_worst, data.texture_worst, data.perimeter_worst,
        data.area_worst, data.smoothness_worst, data.compactness_worst,
        data.concavity_worst, data.concave_points_worst, data.symmetry_worst,
        data.fractal_dimension_worst
    ]])

    # 2. Scale the input data using the *loaded* scaler
    input_scaled = scaler.transform(input_data)

    # 3. Make the prediction
    prediction_raw = model.predict(input_scaled)
    
    # 4. Get the probability (confidence score)
    # .predict_proba() returns probabilities for [Benign, Malignant]
    probability = model.predict_proba(input_scaled)

    # 5. Format the output
    prediction = "Malignant" if prediction_raw[0] == 1 else "Benign"
    # Get the highest probability score and format as percentage
    confidence = float(np.max(probability[0])) * 100 

    # 6. Return the result as JSON
    return {
        "prediction": prediction,
        "confidence": round(confidence, 2)
    }