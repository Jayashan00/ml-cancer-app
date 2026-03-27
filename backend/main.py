# main.py

# 1. Import necessary libraries
from fastapi import FastAPI, File, UploadFile
from pydantic import BaseModel, Field
import joblib
import numpy as np
import pandas as pd
from fastapi.middleware.cors import CORSMiddleware
from sklearn.metrics import accuracy_score, precision_score, recall_score
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.model_selection import train_test_split
from io import StringIO
from datetime import datetime
import json
import os

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

# --- Startup event to load model metrics ---
@app.on_event("startup")
async def startup_event():
    """Load model metrics from the trained model on startup."""
    global model_metrics
    
    if model and scaler:
        try:
            # Try to load metrics from a saved file if it exists
            if os.path.exists('model_metrics.json'):
                with open('model_metrics.json', 'r') as f:
                    model_metrics = json.load(f)
                    print(f"Metrics loaded: Accuracy={model_metrics['accuracy']}")
            else:
                # If no saved metrics, you can calculate them by loading test data
                # For now, we'll set default values
                print("No saved metrics found. Please retrain the model with new data to populate metrics.")
        except Exception as e:
            print(f"Error loading metrics: {e}")

# --- Feature ranges (min/max) derived from the dataset ---
FEATURE_RANGES = {
    'radius_mean': {'min': 6, 'max': 29},
    'texture_mean': {'min': 9, 'max': 40},
    'perimeter_mean': {'min': 40, 'max': 190},
    'area_mean': {'min': 140, 'max': 2500},
    'smoothness_mean': {'min': 0.05, 'max': 0.17},
    'compactness_mean': {'min': 0.01, 'max': 0.35},
    'concavity_mean': {'min': 0, 'max': 0.45},
    'concave_points_mean': {'min': 0, 'max': 0.21},
    'symmetry_mean': {'min': 0.1, 'max': 0.31},
    'fractal_dimension_mean': {'min': 0.04, 'max': 0.1},
    'radius_se': {'min': 0.1, 'max': 2.9},
    'texture_se': {'min': 0.3, 'max': 4.9},
    'perimeter_se': {'min': 0.7, 'max': 22},
    'area_se': {'min': 6, 'max': 550},
    'smoothness_se': {'min': 0.001, 'max': 0.03},
    'compactness_se': {'min': 0.002, 'max': 0.14},
    'concavity_se': {'min': 0, 'max': 0.4},
    'concave_points_se': {'min': 0, 'max': 0.05},
    'symmetry_se': {'min': 0.007, 'max': 0.08},
    'fractal_dimension_se': {'min': 0.0008, 'max': 0.03},
    'radius_worst': {'min': 7, 'max': 37},
    'texture_worst': {'min': 12, 'max': 50},
    'perimeter_worst': {'min': 50, 'max': 250},
    'area_worst': {'min': 180, 'max': 4250},
    'smoothness_worst': {'min': 0.07, 'max': 0.23},
    'compactness_worst': {'min': 0.02, 'max': 1.1},
    'concavity_worst': {'min': 0, 'max': 1.3},
    'concave_points_worst': {'min': 0, 'max': 0.3},
    'symmetry_worst': {'min': 0.15, 'max': 0.67},
    'fractal_dimension_worst': {'min': 0.05, 'max': 0.21},
}

# --- Store prediction history and model metrics ---
prediction_history = []
model_metrics = {"accuracy": 0, "precision": 0, "recall": 0}

# --- 5. Define the input data model using Pydantic ---
# This creates a "shape" for the data we expect to receive.
# FastAPI will automatically validate incoming data against this.
# These are your 30 features with min/max constraints.
class CancerInput(BaseModel):
    radius_mean: float = Field(..., ge=6, le=29)
    texture_mean: float = Field(..., ge=9, le=40)
    perimeter_mean: float = Field(..., ge=40, le=190)
    area_mean: float = Field(..., ge=140, le=2500)
    smoothness_mean: float = Field(..., ge=0.05, le=0.17)
    compactness_mean: float = Field(..., ge=0.01, le=0.35)
    concavity_mean: float = Field(..., ge=0, le=0.45)
    concave_points_mean: float = Field(..., ge=0, le=0.21)
    symmetry_mean: float = Field(..., ge=0.1, le=0.31)
    fractal_dimension_mean: float = Field(..., ge=0.04, le=0.1)
    radius_se: float = Field(..., ge=0.1, le=2.9)
    texture_se: float = Field(..., ge=0.3, le=4.9)
    perimeter_se: float = Field(..., ge=0.7, le=22)
    area_se: float = Field(..., ge=6, le=550)
    smoothness_se: float = Field(..., ge=0.001, le=0.03)
    compactness_se: float = Field(..., ge=0.002, le=0.14)
    concavity_se: float = Field(..., ge=0, le=0.4)
    concave_points_se: float = Field(..., ge=0, le=0.05)
    symmetry_se: float = Field(..., ge=0.007, le=0.08)
    fractal_dimension_se: float = Field(..., ge=0.0008, le=0.03)
    radius_worst: float = Field(..., ge=7, le=37)
    texture_worst: float = Field(..., ge=12, le=50)
    perimeter_worst: float = Field(..., ge=50, le=250)
    area_worst: float = Field(..., ge=180, le=4250)
    smoothness_worst: float = Field(..., ge=0.07, le=0.23)
    compactness_worst: float = Field(..., ge=0.02, le=1.1)
    concavity_worst: float = Field(..., ge=0, le=1.3)
    concave_points_worst: float = Field(..., ge=0, le=0.3)
    symmetry_worst: float = Field(..., ge=0.15, le=0.67)
    fractal_dimension_worst: float = Field(..., ge=0.05, le=0.21)

# --- 6. Create a "root" endpoint ---
# This is just a simple endpoint to check if the API is running.
@app.get("/")
def read_root():
    return {"message": "Breast Cancer Diagnosis API is running!"}

# --- NEW: Get feature ranges endpoint ---
@app.get("/feature-ranges")
def get_feature_ranges():
    """Returns min/max ranges for all 30 features for frontend validation."""
    return FEATURE_RANGES

# --- NEW: Get model metrics endpoint ---
@app.get("/metrics")
def get_metrics():
    """Returns the model's accuracy, precision, and recall on test data."""
    if not model or not scaler:
        return {"error": "Model or scaler not loaded"}
    
    return {
        "accuracy": round(model_metrics["accuracy"], 4),
        "precision": round(model_metrics["precision"], 4),
        "recall": round(model_metrics["recall"], 4),
        "timestamp": "Trained on initialization"
    }

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

    result = {
        "prediction": prediction,
        "confidence": round(confidence, 2),
        "timestamp": datetime.now().isoformat()
    }
    
    # 6. Store in prediction history
    prediction_history.append(result)

    # 7. Return the result as JSON
    return result

# --- NEW: Export predictions endpoint ---
@app.get("/export-predictions")
def export_predictions(format: str = "csv"):
    """Export prediction history as CSV or JSON."""
    if not prediction_history:
        return {"error": "No predictions to export yet"}
    
    if format == "json":
        return {"predictions": prediction_history}
    
    elif format == "csv":
        # Convert to DataFrame and then to CSV string
        df = pd.DataFrame(prediction_history)
        csv_string = df.to_csv(index=False)
        
        # Return as a downloadable response
        return {
            "data": csv_string,
            "filename": f"predictions_{datetime.now().strftime('%Y%m%d_%H%M%S')}.csv"
        }
    
    else:
        return {"error": "Invalid format. Use 'csv' or 'json'"}

# --- NEW: Retrain model endpoint ---
@app.post("/retrain-model")
async def retrain_model(file: UploadFile = File(...)):
    """
    Retrain the model with new data from a CSV file.
    CSV must have the same 31 columns (30 features + 'diagnosis' target).
    """
    global model, scaler, model_metrics
    
    try:
        # Read the uploaded CSV file
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode('utf-8')))
        
        # Validate the dataset
        if 'diagnosis' not in df.columns:
            return {"error": "CSV must contain 'diagnosis' column"}
        
        if len(df.columns) < 31:
            return {"error": f"CSV must have 31 columns (30 features + diagnosis). Got {len(df.columns)}"}
        
        # Prepare the data
        if 'id' in df.columns:
            df = df.drop(['id'], axis=1)
        
        # Encode target variable
        from sklearn.preprocessing import LabelEncoder
        encoder = LabelEncoder()
        df['diagnosis'] = encoder.fit_transform(df['diagnosis'])
        
        X = df.drop('diagnosis', axis=1)
        y = df['diagnosis']
        
        # Split data
        X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
        
        # Scale data
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        # Train new model
        model = SVC(kernel='rbf', C=10, probability=True)
        model.fit(X_train_scaled, y_train)
        
        # Calculate metrics
        y_pred = model.predict(X_test_scaled)
        model_metrics["accuracy"] = accuracy_score(y_test, y_pred)
        model_metrics["precision"] = precision_score(y_test, y_pred, zero_division=0)
        model_metrics["recall"] = recall_score(y_test, y_pred, zero_division=0)
        
        # Save the new model and scaler
        joblib.dump(model, 'breast_cancer_model.pkl')
        joblib.dump(scaler, 'scaler.pkl')
        
        return {
            "message": "Model retrained successfully",
            "accuracy": round(model_metrics["accuracy"], 4),
            "precision": round(model_metrics["precision"], 4),
            "recall": round(model_metrics["recall"], 4),
            "samples_used": len(df)
        }
    
    except Exception as e:
        return {"error": f"Error retraining model: {str(e)}"}