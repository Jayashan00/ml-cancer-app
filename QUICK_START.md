# Quick Start - New Features

## What's New

✅ **Export Results** - Download all predictions as CSV/JSON  
✅ **Feature Ranges** - See min/max values for each slider  
✅ **Model Metrics** - View accuracy, precision, recall  
✅ **Model Retraining** - Upload new data to update the model  

---

## Running the App

### Terminal 1 - Backend (port 8000)
```bash
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
uvicorn main:app --reload
```

### Terminal 2 - Frontend (port 5173)
```bash
cd frontend
npm install
npm run dev
```

Open: **http://localhost:5173**

---

## New Components

### 1. Model Metrics Card (Top)
Shows current model performance:
- **Accuracy**: Correct predictions %
- **Precision**: True positives / all positives
- **Recall**: True positives / all malignant cases

### 2. Feature Sliders (Enhanced)
- Each slider now shows: **Range: min - max**
- Backend validates inputs within these ranges
- Invalid values are rejected

### 3. Export Results Card
- **Download as CSV**: Timestamped data file
- **Download as JSON**: Formatted prediction array
- Shows success/error messages

### 4. Retrain Model Card
- Upload CSV file with training data
- CSV must have 30 features + 'diagnosis' column
- Shows new metrics after training
- Automatically saves updated model

---

## File Structures

### CSV Format for Retraining
```
radius_mean,texture_mean,perimeter_mean,...,diagnosis
14.12,19.28,91.96,...,B
15.4,20.5,100.2,...,M
...
```
- 31 columns total (30 features + diagnosis)
- diagnosis: M (malignant) or B (benign)

### Export Output Files
**CSV**: `predictions_20260211_143022.csv`
```
prediction,confidence,timestamp
Benign,92.45,2026-02-11T14:30:22.123456
Malignant,87.32,2026-02-11T14:31:45.654321
```

**JSON**: `predictions_1707685422123.json`
```json
[
  {
    "prediction": "Benign",
    "confidence": 92.45,
    "timestamp": "2026-02-11T14:30:22.123456"
  },
  ...
]
```

---

## Backend Endpoints

| Method | Endpoint | Purpose |
|--------|----------|---------|
| GET | `/` | Check API status |
| GET | `/metrics` | Get model accuracy/precision/recall |
| GET | `/feature-ranges` | Get min/max for all features |
| POST | `/predict` | Make a prediction (existing) |
| GET | `/export-predictions` | Download predictions as CSV/JSON |
| POST | `/retrain-model` | Upload CSV to retrain model |

---

## Troubleshooting

**"Model or scaler not loaded"**
- Check backend logs
- Ensure `.pkl` files exist in backend folder
- Restart backend server

**"No predictions to export yet"**
- Make at least one prediction first
- Predictions stored in memory during session

**"CSV validation failed"**
- Check CSV has 31 columns (30 features + diagnosis)
- Ensure 'diagnosis' column exists
- Values must be M or B

**Range validation error**
- Feature values outside min/max are rejected
- Check slider range labels
- Use backend endpoint `/feature-ranges` to verify

---

## Files Modified
- ✏️ `backend/main.py` - Added 4 endpoints
- ✏️ `backend/requirements.txt` - Cleaned up
- ✏️ `frontend/src/App.jsx` - Integrated components
- ✏️ `frontend/src/index.css` - New styling
- ✏️ `frontend/src/components/PredictionForm.jsx` - Fetch ranges
- 📄 `frontend/src/components/ModelMetrics.jsx` - NEW
- 📄 `frontend/src/components/ExportResults.jsx` - NEW
- 📄 `frontend/src/components/RetrainModel.jsx` - NEW

---

## Performance Tips

- Model metrics load automatically on startup
- Feature ranges cached from backend
- Predictions stored in memory (cleared on refresh)
- Export handles large prediction lists efficiently
- Model retraining uses optimized SVM parameters

---

Generated: February 11, 2026
