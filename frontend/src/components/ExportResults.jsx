// src/components/ExportResults.jsx
import React, { useState } from 'react';

function ExportResults() {
  const [exporting, setExporting] = useState(false);
  const [message, setMessage] = useState('');

  const handleExport = async (format) => {
    setExporting(true);
    setMessage('');

    try {
      const response = await fetch(`http://127.0.0.1:8000/export-predictions?format=${format}`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();

      if (data.error) {
        setMessage(`Error: ${data.error}`);
        return;
      }

      if (format === 'csv') {
        // Create a blob and download CSV
        const blob = new Blob([data.data], { type: 'text/csv;charset=utf-8;' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', data.filename);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        setMessage('CSV file downloaded successfully!');
      } else if (format === 'json') {
        // Download JSON
        const blob = new Blob([JSON.stringify(data.predictions, null, 2)], { type: 'application/json' });
        const link = document.createElement('a');
        const url = URL.createObjectURL(blob);
        link.setAttribute('href', url);
        link.setAttribute('download', `predictions_${new Date().getTime()}.json`);
        link.style.visibility = 'hidden';
        document.body.appendChild(link);
        link.click();
        document.body.removeChild(link);
        setMessage('JSON file downloaded successfully!');
      }
    } catch (error) {
      console.error('Error exporting predictions:', error);
      setMessage('Failed to export predictions');
    } finally {
      setExporting(false);
    }
  };

  return (
    <div className="export-card">
      <h3>Export Predictions</h3>
      <div className="export-buttons">
        <button
          onClick={() => handleExport('csv')}
          disabled={exporting}
          className="export-btn csv-btn"
        >
          {exporting ? 'Exporting...' : 'Download as CSV'}
        </button>
        <button
          onClick={() => handleExport('json')}
          disabled={exporting}
          className="export-btn json-btn"
        >
          {exporting ? 'Exporting...' : 'Download as JSON'}
        </button>
      </div>
      {message && <p className="export-message">{message}</p>}
    </div>
  );
}

export default ExportResults;
