// src/App.jsx
import React, { useState } from 'react';
import axios from 'axios';
import PredictionForm from './components/PredictionForm';
import ResultDisplay from './components/ResultDisplay';


const initialFormData = {
  radius_mean: 14.12, texture_mean: 19.28, perimeter_mean: 91.96, area_mean: 654.88,
  smoothness_mean: 0.096, compactness_mean: 0.104, concavity_mean: 0.088,
  concave_points_mean: 0.048, symmetry_mean: 0.181, fractal_dimension_mean: 0.062,
  radius_se: 0.405, texture_se: 1.216, perimeter_se: 2.866, area_se: 40.33,
  smoothness_se: 0.007, compactness_se: 0.025, concavity_se: 0.031,
  concave_points_se: 0.011, symmetry_se: 0.020, fractal_dimension_se: 0.003,
  radius_worst: 16.26, texture_worst: 25.67, perimeter_worst: 107.26,
  area_worst: 880.58, smoothness_worst: 0.132, compactness_worst: 0.254,
  concavity_worst: 0.272, concave_points_worst: 0.114, symmetry_worst: 0.290,
  fractal_dimension_worst: 0.083
};

function App() {
  const [formData, setFormData] = useState(initialFormData);
  const [result, setResult] = useState(null);
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState(null);

  // This one function handles all 30 sliders
  const handleChange = (e) => {
    setFormData({
      ...formData,
      [e.target.name]: e.target.value,
    });
  };

  // This function runs when the user clicks "Get Prediction"
  const handleSubmit = async (e) => {
    e.preventDefault(); // Stop the page from reloading
    setIsLoading(true);
    setResult(null);
    setError(null);

    // Convert all form values from strings to numbers
    const processedData = {};
    for (const key in formData) {
      processedData[key] = parseFloat(formData[key]);
    }

    try {
      // --- THIS IS THE API CALL ---
      const response = await axios.post(
        'http://127.0.0.1:8000/predict', // Your backend URL
        processedData
      );
      // -----------------------------

      setResult(response.data); // Save the prediction
    } catch (err) {
      console.error('Error making prediction:', err);
      setError('Could not connect to the prediction server. Is it running?');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <>
      <header>
        <h1>A Comparative Analysis of ML Classifiers</h1>
        <p>Live Diagnosis Tool (using best model: SVM)</p>
      </header>

      <main>
        <PredictionForm
          formData={formData}
          handleChange={handleChange}
          handleSubmit={handleSubmit}
        />
        
        {/* Show an error message if the API call fails */}
        {error && <div className="result-card Malignant"><h3>Error</h3><p>{error}</p></div>}

        {/* Show the result card (or loading) */}
        <ResultDisplay result={result} isLoading={isLoading} />
      </main>
    </>
  );
}

export default App;