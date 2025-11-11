// src/components/ResultDisplay.jsx
import React from 'react';

function ResultDisplay({ result, isLoading }) {
  if (isLoading) {
    return <div className="result-card"><h2>Loading...</h2></div>;
  }

  if (!result) {
    return null; // Don't show anything if there's no result yet
  }

  // Use the prediction as a CSS class for styling (e.g., "Benign" or "Malignant")
  return (
    <div className={`result-card ${result.prediction}`}>
      <h2>Prediction: {result.prediction}</h2>
      <p>Confidence: {result.confidence}%</p>
    </div>
  );
}

export default ResultDisplay;