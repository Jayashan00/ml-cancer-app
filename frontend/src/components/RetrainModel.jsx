// src/components/RetrainModel.jsx
import React, { useState } from 'react';

function RetrainModel() {
  const [file, setFile] = useState(null);
  const [retraining, setRetraining] = useState(false);
  const [message, setMessage] = useState('');
  const [metrics, setMetrics] = useState(null);

  const handleFileChange = (e) => {
    setFile(e.target.files[0]);
  };

  const handleRetrain = async () => {
    if (!file) {
      setMessage('Please select a CSV file first');
      return;
    }

    setRetraining(true);
    setMessage('');
    setMetrics(null);

    const formData = new FormData();
    formData.append('file', file);

    try {
      const response = await fetch('http://127.0.0.1:8000/retrain-model', {
        method: 'POST',
        body: formData
      });

      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();

      if (data.error) {
        setMessage(`Error: ${data.error}`);
      } else {
        setMessage(`Model retrained successfully with ${data.samples_used} samples`);
        setMetrics({
          accuracy: data.accuracy,
          precision: data.precision,
          recall: data.recall
        });
        setFile(null);
        // Reset file input
        document.getElementById('csv-file-input').value = '';
      }
    } catch (error) {
      console.error('Error retraining model:', error);
      setMessage(`Failed to retrain model: ${error.message}`);
    } finally {
      setRetraining(false);
    }
  };

  return (
    <div className="retrain-card">
      <h3>Retrain Model with New Data</h3>
      <p className="retrain-info">
        Upload a CSV file with 30 features and a 'diagnosis' column (M or B)
      </p>
      
      <div className="file-input-group">
        <input
          id="csv-file-input"
          type="file"
          accept=".csv"
          onChange={handleFileChange}
          disabled={retraining}
          className="file-input"
        />
        <button
          onClick={handleRetrain}
          disabled={!file || retraining}
          className="retrain-btn"
        >
          {retraining ? 'Retraining...' : 'Retrain Model'}
        </button>
      </div>

      {message && (
        <p className={`retrain-message ${message.includes('Error') ? 'error' : 'success'}`}>
          {message}
        </p>
      )}

      {metrics && (
        <div className="retrain-metrics">
          <h4>New Model Metrics</h4>
          <div className="metrics-grid">
            <div className="metric-item">
              <span className="metric-label">Accuracy</span>
              <span className="metric-value">{(metrics.accuracy * 100).toFixed(2)}%</span>
            </div>
            <div className="metric-item">
              <span className="metric-label">Precision</span>
              <span className="metric-value">{(metrics.precision * 100).toFixed(2)}%</span>
            </div>
            <div className="metric-item">
              <span className="metric-label">Recall</span>
              <span className="metric-value">{(metrics.recall * 100).toFixed(2)}%</span>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}

export default RetrainModel;
