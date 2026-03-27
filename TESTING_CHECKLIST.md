# ✅ Testing & Verification Checklist

## Pre-Flight Checks

- [ ] Backend syntax is valid: `python -m py_compile backend/main.py`
- [ ] Frontend components exist:
  - [ ] `src/components/ModelMetrics.jsx`
  - [ ] `src/components/ExportResults.jsx`
  - [ ] `src/components/RetrainModel.jsx`
- [ ] Model files exist in backend folder:
  - [ ] `breast_cancer_model.pkl`
  - [ ] `scaler.pkl`
- [ ] Requirements updated: `pip install -r requirements.txt`

---

## Backend Testing

### Test 1: Server Starts
```bash
cd backend
uvicorn main:app --reload
```
✓ Should see: "Uvicorn running on http://127.0.0.1:8000"
✓ Should see: "Model and scaler loaded successfully"

### Test 2: Root Endpoint
```
GET http://127.0.0.1:8000/
Expected: {"message": "Breast Cancer Diagnosis API is running!"}
```

### Test 3: Feature Ranges Endpoint
```
GET http://127.0.0.1:8000/feature-ranges
Expected: JSON with 30 features and their min/max values
Example: {"radius_mean": {"min": 6, "max": 29}, ...}
```

### Test 4: Metrics Endpoint
```
GET http://127.0.0.1:8000/metrics
Expected: {"accuracy": X, "precision": X, "recall": X, "timestamp": "..."}
Note: Initially might show 0 values until model is retrained
```

### Test 5: Predict Endpoint (Existing)
```
POST http://127.0.0.1:8000/predict
Body: {all 30 features with valid values}
Expected: {"prediction": "Benign|Malignant", "confidence": X, "timestamp": "..."}
```

### Test 6: Export Predictions (CSV)
```
GET http://127.0.0.1:8000/export-predictions?format=csv
Expected: {"data": "CSV content", "filename": "predictions_...csv"}
Note: Requires at least one prediction first
```

### Test 7: Export Predictions (JSON)
```
GET http://127.0.0.1:8000/export-predictions?format=json
Expected: {"predictions": [array of prediction objects]}
```

### Test 8: Retrain Model
```
POST http://127.0.0.1:8000/retrain-model
Body: multipart/form-data with CSV file
Expected: {
  "message": "Model retrained successfully",
  "accuracy": X,
  "precision": X,
  "recall": X,
  "samples_used": N
}
```

---

## Frontend Testing

### Test 1: Frontend Starts
```bash
cd frontend
npm run dev
```
✓ Should see: "Local: http://localhost:5173/"

### Test 2: ModelMetrics Component
- [ ] Loads on page startup (no manual refresh)
- [ ] Displays "Model Performance Metrics" header
- [ ] Shows 3 metric cards: Accuracy, Precision, Recall
- [ ] All values formatted as percentages (X.XX%)
- [ ] Cards have proper styling

### Test 3: PredictionForm Enhancement
- [ ] Each slider shows range label above it
- [ ] Range format: "Range: X - Y"
- [ ] Ranges match backend feature-ranges endpoint
- [ ] All 3 tabs work (Mean, SE, Worst)
- [ ] Slider values update in real-time

### Test 4: Make a Prediction
- [ ] Adjust a few sliders
- [ ] Click "Get Prediction"
- [ ] See result card appear with prediction and confidence
- [ ] Result shows timestamp

### Test 5: Export Results
- [ ] After making ≥1 prediction
- [ ] Click "Download as CSV"
- [ ] File downloads with timestamp filename
- [ ] CSV contains: prediction, confidence, timestamp
- [ ] Click "Download as JSON"
- [ ] File downloads with proper JSON formatting
- [ ] See success message

### Test 6: Retrain Model
- [ ] Prepare test CSV file with:
  - 31 columns (30 features + diagnosis)
  - At least 10 rows of data
  - diagnosis column with M or B values
- [ ] Use file picker to select CSV
- [ ] Click "Retrain Model"
- [ ] See loading state
- [ ] Success message appears
- [ ] New metrics display below
- [ ] ModelMetrics component updates at top

### Test 7: Validation Testing
- [ ] Try entering value outside range for a feature
- [ ] Should see validation error (handled by backend)
- [ ] Try uploading wrong CSV format
- [ ] Should see error message from backend

---

## Integration Testing

### Test 1: Full User Journey
1. [ ] Open app → See initial metrics
2. [ ] Adjust sliders → See ranges working
3. [ ] Get prediction → See result with timestamp
4. [ ] Make another prediction → See in export
5. [ ] Export as CSV → Verify file contains both predictions
6. [ ] Prepare CSV training data → Upload
7. [ ] See retrain progress → See new metrics
8. [ ] Make prediction with new model → Verify it works

### Test 2: Feature Independence
- [ ] MetricsComponent works without predictions
- [ ] Ranges load independently
- [ ] Export shows error when no predictions exist
- [ ] Retrain works with fresh model
- [ ] Each feature independently validates

### Test 3: Error Handling
- [ ] Disconnect backend → Frontend shows error
- [ ] Invalid CSV → Clear error message
- [ ] Validation failure → Backend returns 422
- [ ] Network timeout → Graceful error handling

---

## Performance Checks

- [ ] App loads in <2 seconds
- [ ] Metrics endpoint responds in <100ms
- [ ] Feature-ranges endpoint responds in <50ms
- [ ] Prediction responds in <500ms
- [ ] Export download is fast (<1 second)
- [ ] Model retrain completes in <30 seconds

---

## Browser DevTools Checks

**Console Tab**:
- [ ] No JavaScript errors
- [ ] No 404 errors for files
- [ ] API calls successful (200/422 status codes)
- [ ] Network requests completed

**Network Tab**:
- [ ] GET /metrics → 200 (on load)
- [ ] GET /feature-ranges → 200 (on form mount)
- [ ] POST /predict → 200 with prediction
- [ ] GET /export-predictions → 200 with data
- [ ] POST /retrain-model → 200 with new metrics

**Application Tab**:
- [ ] Component state updates properly
- [ ] No memory leaks on repeated actions

---

## Edge Cases to Test

- [ ] Make 100+ predictions → Export still works
- [ ] Rapidly click predict → Handled correctly
- [ ] Multiple browsers → Data isolated per session
- [ ] Server restart → Metrics reset (expected)
- [ ] Browser refresh → Session data cleared (expected)
- [ ] Very large CSV upload → Handled gracefully

---

## Documentation Checks

- [ ] IMPLEMENTATION_GUIDE.md is complete
- [ ] QUICK_START.md is helpful
- [ ] ARCHITECTURE.md shows flow clearly
- [ ] CHANGES.md documents all modifications
- [ ] Code comments are clear and helpful

---

## Final Sign-Off

When ALL checkboxes above are completed:

- ✅ Backend endpoints working correctly
- ✅ Frontend components rendering properly
- ✅ API communication functioning
- ✅ Validation preventing invalid data
- ✅ Export functionality saving files
- ✅ Retrain updating model correctly
- ✅ Metrics displaying accurately
- ✅ Ranges showing on sliders
- ✅ No console errors
- ✅ All features production-ready

**Status**: Ready for Deployment ✨

---

## Troubleshooting Common Issues

| Issue | Solution |
|-------|----------|
| "Model not loaded" | Restart backend, check .pkl files exist |
| Ranges not showing | Check /feature-ranges endpoint, browser cache |
| Export shows error | Make at least 1 prediction first |
| Retrain fails | Verify CSV has 31 cols + diagnosis column |
| Metrics all zeros | Retrain model to populate metrics |
| Validation error on predict | Check slider values within range |
| CORS error | Verify backend CORS origins include 5173 |
| File won't download | Check browser download settings |

---

**Generated**: February 11, 2026  
**Last Updated**: [Auto-generated on test completion]
