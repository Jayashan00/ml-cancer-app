// src/components/PredictionForm.jsx
import React, { useState, useEffect } from 'react';

// A helper component to avoid repeating slider code
const SliderInput = ({ name, label, value, onChange, min, max, step }) => (
  <div className="form-group">
    <label htmlFor={name}>{label}</label>
    <div className="slider-info">
      <span className="range-label">Range: {min} - {max}</span>
      <span className="slider-value">{parseFloat(value).toFixed(4)}</span>
    </div>
    <div className="slider-container">
      <input
        type="range"
        id={name}
        name={name}
        min={min}
        max={max}
        step={step}
        value={value}
        onChange={onChange}
      />
    </div>
  </div>
);

// Helper object with all feature names and their slider ranges (based on dataset's .describe())
// This is a *huge* UI/UX improvement.
const features = {
  mean: [
    { name: 'radius_mean', label: 'Radius (Mean)', min: 6, max: 29, step: 0.1 },
    { name: 'texture_mean', label: 'Texture (Mean)', min: 9, max: 40, step: 0.1 },
    { name: 'perimeter_mean', label: 'Perimeter (Mean)', min: 40, max: 190, step: 0.1 },
    { name: 'area_mean', label: 'Area (Mean)', min: 140, max: 2500, step: 1 },
    { name: 'smoothness_mean', label: 'Smoothness (Mean)', min: 0.05, max: 0.17, step: 0.001 },
    { name: 'compactness_mean', label: 'Compactness (Mean)', min: 0.01, max: 0.35, step: 0.001 },
    { name: 'concavity_mean', label: 'Concavity (Mean)', min: 0, max: 0.45, step: 0.001 },
    { name: 'concave_points_mean', label: 'Concave Points (Mean)', min: 0, max: 0.21, step: 0.001 },
    { name: 'symmetry_mean', label: 'Symmetry (Mean)', min: 0.1, max: 0.31, step: 0.001 },
    { name: 'fractal_dimension_mean', label: 'Fractal Dimension (Mean)', min: 0.04, max: 0.1, step: 0.0001 },
  ],
  se: [
    { name: 'radius_se', label: 'Radius (SE)', min: 0.1, max: 2.9, step: 0.01 },
    { name: 'texture_se', label: 'Texture (SE)', min: 0.3, max: 4.9, step: 0.01 },
    { name: 'perimeter_se', label: 'Perimeter (SE)', min: 0.7, max: 22, step: 0.01 },
    { name: 'area_se', label: 'Area (SE)', min: 6, max: 550, step: 1 },
    { name: 'smoothness_se', label: 'Smoothness (SE)', min: 0.001, max: 0.03, step: 0.0001 },
    { name: 'compactness_se', label: 'Compactness (SE)', min: 0.002, max: 0.14, step: 0.0001 },
    { name: 'concavity_se', label: 'Concavity (SE)', min: 0, max: 0.4, step: 0.001 },
    { name: 'concave_points_se', label: 'Concave Points (SE)', min: 0, max: 0.05, step: 0.0001 },
    { name: 'symmetry_se', label: 'Symmetry (SE)', min: 0.007, max: 0.08, step: 0.0001 },
    { name: 'fractal_dimension_se', label: 'Fractal Dimension (SE)', min: 0.0008, max: 0.03, step: 0.00001 },
  ],
  worst: [
    { name: 'radius_worst', label: 'Radius (Worst)', min: 7, max: 37, step: 0.1 },
    { name: 'texture_worst', label: 'Texture (Worst)', min: 12, max: 50, step: 0.1 },
    { name: 'perimeter_worst', label: 'Perimeter (Worst)', min: 50, max: 250, step: 0.1 },
    { name: 'area_worst', label: 'Area (Worst)', min: 180, max: 4250, step: 1 },
    { name: 'smoothness_worst', label: 'Smoothness (Worst)', min: 0.07, max: 0.23, step: 0.001 },
    { name: 'compactness_worst', label: 'Compactness (Worst)', min: 0.02, max: 1.1, step: 0.001 },
    { name: 'concavity_worst', label: 'Concavity (Worst)', min: 0, max: 1.3, step: 0.01 },
    { name: 'concave_points_worst', label: 'Concave Points (Worst)', min: 0, max: 0.3, step: 0.001 },
    { name: 'symmetry_worst', label: 'Symmetry (Worst)', min: 0.15, max: 0.67, step: 0.001 },
    { name: 'fractal_dimension_worst', label: 'Fractal Dimension (Worst)', min: 0.05, max: 0.21, step: 0.001 },
  ]
};

function PredictionForm({ formData, handleChange, handleSubmit }) {
  const [activeTab, setActiveTab] = useState('mean');
  const [featureRanges, setFeatureRanges] = useState({});
  const [isApiLoaded, setIsApiLoaded] = useState(false);

  // Fetch feature ranges from backend (non-blocking)
  useEffect(() => {
    const fetchRanges = async () => {
      try {
        const response = await fetch('http://127.0.0.1:8000/feature-ranges');
        if (response.ok) {
          const data = await response.json();
          setFeatureRanges(data);
          setIsApiLoaded(true);
        }
      } catch (error) {
        console.error('Using hardcoded ranges:', error);
      }
    };

    // Try to fetch but don't block rendering
    fetchRanges();
  }, []);

  const renderSliders = (type) => {
    return features[type].map(feature => {
      const range = featureRanges && featureRanges[feature.name];
      const min = range ? range.min : feature.min;
      const max = range ? range.max : feature.max;

      return (
        <SliderInput
          key={feature.name}
          name={feature.name}
          label={feature.label}
          value={formData[feature.name]}
          onChange={handleChange}
          min={min}
          max={max}
          step={feature.step}
        />
      );
    });
  };

  return (
    <form onSubmit={handleSubmit}>
      <div className="tabs">
        <button type="button" className={`tab-button ${activeTab === 'mean' ? 'active' : ''}`} onClick={() => setActiveTab('mean')}>
          Mean Values
        </button>
        <button type="button" className={`tab-button ${activeTab === 'se' ? 'active' : ''}`} onClick={() => setActiveTab('se')}>
          Standard Error
        </button>
        <button type="button" className={`tab-button ${activeTab === 'worst' ? 'active' : ''}`} onClick={() => setActiveTab('worst')}>
          Worst Values
        </button>
      </div>

      <div className={`tab-content ${activeTab === 'mean' ? 'active' : ''}`}>
        {renderSliders('mean')}
      </div>
      <div className={`tab-content ${activeTab === 'se' ? 'active' : ''}`}>
        {renderSliders('se')}
      </div>
      <div className={`tab-content ${activeTab === 'worst' ? 'active' : ''}`}>
        {renderSliders('worst')}
      </div>

      <button type="submit">Get Prediction</button>
    </form>
  );
}

export default PredictionForm;