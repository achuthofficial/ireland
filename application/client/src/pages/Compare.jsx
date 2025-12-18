import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { compareContracts } from '../services/api';

function Compare() {
  const navigate = useNavigate();
  const [files, setFiles] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileSelect = (e) => {
    const selectedFiles = Array.from(e.target.files);
    const htmlFiles = selectedFiles.filter(f => f.name.endsWith('.html') || f.name.endsWith('.htm'));

    if (htmlFiles.length !== selectedFiles.length) {
      setError('Some files were skipped. Only HTML files are accepted.');
    } else {
      setError('');
    }

    setFiles([...files, ...htmlFiles]);
  };

  const removeFile = (index) => {
    setFiles(files.filter((_, i) => i !== index));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (files.length < 2) {
      setError('Please select at least 2 contracts to compare');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const data = await compareContracts(files);

      if (data.success) {
        navigate('/results', {
          state: {
            comparison: data.comparison,
            assessments: data.assessments,
            isComparison: true
          }
        });
      } else {
        setError(data.error || 'Failed to compare contracts');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Error comparing contracts. Please try again.');
      console.error('Comparison error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="compare-page">
      <h1 className="page-title">Compare Vendor Contracts</h1>
      <p className="page-subtitle">
        Upload multiple contracts to compare vendors objectively
      </p>

      <div className="card">
        <form onSubmit={handleSubmit}>
          <div className="form-group">
            <label className="form-label">Select Contracts (HTML files)</label>
            <input
              type="file"
              accept=".html,.htm"
              multiple
              onChange={handleFileSelect}
              className="form-input"
            />
            <p style={{ marginTop: '0.5rem', fontSize: '0.9rem', color: '#666' }}>
              Select at least 2 contracts to compare
            </p>
          </div>

          {files.length > 0 && (
            <div style={{ marginTop: '1.5rem' }}>
              <h3>Selected Contracts ({files.length})</h3>
              <div style={{ marginTop: '1rem' }}>
                {files.map((file, index) => (
                  <div
                    key={index}
                    style={{
                      display: 'flex',
                      justifyContent: 'space-between',
                      alignItems: 'center',
                      padding: '1rem',
                      background: '#f8f9fa',
                      borderRadius: '5px',
                      marginBottom: '0.5rem'
                    }}
                  >
                    <div>
                      <div style={{ fontWeight: 'bold' }}>{file.name}</div>
                      <div style={{ fontSize: '0.9rem', color: '#666' }}>
                        {(file.size / 1024).toFixed(2)} KB
                      </div>
                    </div>
                    <button
                      type="button"
                      onClick={() => removeFile(index)}
                      style={{
                        background: '#dc3545',
                        color: 'white',
                        border: 'none',
                        padding: '0.5rem 1rem',
                        borderRadius: '5px',
                        cursor: 'pointer'
                      }}
                    >
                      Remove
                    </button>
                  </div>
                ))}
              </div>
            </div>
          )}

          {error && (
            <div className="error" style={{ marginTop: '1rem' }}>
              {error}
            </div>
          )}

          <button
            type="submit"
            className="btn btn-primary"
            disabled={files.length < 2 || loading}
            style={{ marginTop: '1.5rem', width: '100%', fontSize: '1.1rem', padding: '1rem' }}
          >
            {loading ? 'Comparing Contracts...' : `Compare ${files.length} Contracts`}
          </button>
        </form>

        {loading && (
          <div className="loading" style={{ marginTop: '2rem' }}>
            <div className="spinner"></div>
            <p style={{ marginTop: '1rem', color: '#666' }}>
              Analyzing and comparing contracts... This may take a moment.
            </p>
          </div>
        )}
      </div>

      <div className="card">
        <h3>What You'll Get</h3>
        <ul style={{ paddingLeft: '1.5rem' }}>
          <li style={{ marginBottom: '0.5rem' }}>Side-by-side risk score comparison</li>
          <li style={{ marginBottom: '0.5rem' }}>Best and worst vendors identified</li>
          <li style={{ marginBottom: '0.5rem' }}>Category-level comparison across all vendors</li>
          <li style={{ marginBottom: '0.5rem' }}>Risk distribution summary</li>
          <li style={{ marginBottom: '0.5rem' }}>Detailed breakdown for each vendor</li>
        </ul>
      </div>

      <div className="card" style={{ background: '#e7f3ff', borderLeft: '4px solid #007bff' }}>
        <h3>💡 Comparison Tips</h3>
        <ul style={{ paddingLeft: '1.5rem' }}>
          <li>Compare similar service types (e.g., all cloud providers)</li>
          <li>Use contracts of similar complexity for best results</li>
          <li>Look for significant differences in category scores</li>
          <li>Pay attention to vendors with missing coverage</li>
          <li>Use results as negotiation leverage with higher-risk vendors</li>
        </ul>
      </div>
    </div>
  );
}

export default Compare;
