import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { assessUpload } from '../services/api';

function FileUpload() {
  const navigate = useNavigate();
  const [file, setFile] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [dragging, setDragging] = useState(false);

  const handleFileSelect = (e) => {
    const selectedFile = e.target.files[0];
    if (selectedFile) {
      if (selectedFile.name.endsWith('.html') || selectedFile.name.endsWith('.htm')) {
        setFile(selectedFile);
        setError('');
      } else {
        setError('Please select an HTML file (.html or .htm)');
      }
    }
  };

  const handleDragOver = (e) => {
    e.preventDefault();
    setDragging(true);
  };

  const handleDragLeave = () => {
    setDragging(false);
  };

  const handleDrop = (e) => {
    e.preventDefault();
    setDragging(false);

    const droppedFile = e.dataTransfer.files[0];
    if (droppedFile) {
      if (droppedFile.name.endsWith('.html') || droppedFile.name.endsWith('.htm')) {
        setFile(droppedFile);
        setError('');
      } else {
        setError('Please select an HTML file (.html or .htm)');
      }
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    if (!file) {
      setError('Please select a file');
      return;
    }

    setLoading(true);
    setError('');

    try {
      const data = await assessUpload(file);

      if (data.success) {
        // Navigate to results page with data
        navigate('/results', { state: { assessment: data.assessment, recommendations: data.recommendations } });
      } else {
        setError(data.error || 'Failed to assess contract');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Error uploading file. Please try again.');
      console.error('Upload error:', err);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="file-upload-page">
      <h1 className="page-title">Upload Contract</h1>
      <p className="page-subtitle">
        Upload an HTML contract file for automated risk assessment
      </p>

      <div className="card">
        <form onSubmit={handleSubmit}>
          <div
            className={`file-upload ${dragging ? 'dragging' : ''}`}
            onDragOver={handleDragOver}
            onDragLeave={handleDragLeave}
            onDrop={handleDrop}
            onClick={() => document.getElementById('file-input').click()}
          >
            <input
              id="file-input"
              type="file"
              accept=".html,.htm"
              onChange={handleFileSelect}
              style={{ display: 'none' }}
            />

            {file ? (
              <div>
                <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📄</div>
                <p style={{ fontSize: '1.2rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>
                  {file.name}
                </p>
                <p style={{ color: '#666' }}>
                  {(file.size / 1024).toFixed(2)} KB
                </p>
                <p style={{ marginTop: '1rem', fontSize: '0.9rem', color: '#007bff' }}>
                  Click to change file or drag and drop
                </p>
              </div>
            ) : (
              <div>
                <div style={{ fontSize: '3rem', marginBottom: '1rem' }}>📁</div>
                <p style={{ fontSize: '1.2rem', fontWeight: 'bold', marginBottom: '0.5rem' }}>
                  Drag and drop your contract here
                </p>
                <p style={{ color: '#666' }}>or click to browse</p>
                <p style={{ marginTop: '1rem', fontSize: '0.9rem', color: '#007bff' }}>
                  Accepts HTML files only (.html, .htm)
                </p>
              </div>
            )}
          </div>

          {error && (
            <div className="error" style={{ marginTop: '1rem' }}>
              {error}
            </div>
          )}

          <button
            type="submit"
            className="btn btn-primary"
            disabled={!file || loading}
            style={{ marginTop: '1.5rem', width: '100%', fontSize: '1.1rem', padding: '1rem' }}
          >
            {loading ? 'Analyzing Contract...' : 'Analyze Contract'}
          </button>
        </form>

        {loading && (
          <div className="loading" style={{ marginTop: '2rem' }}>
            <div className="spinner"></div>
            <p style={{ marginTop: '1rem', color: '#666' }}>
              Analyzing contract... This may take a few seconds.
            </p>
          </div>
        )}
      </div>

      <div className="card">
        <h3>How it works</h3>
        <ol style={{ paddingLeft: '1.5rem' }}>
          <li style={{ marginBottom: '0.5rem' }}>Upload your vendor contract in HTML format</li>
          <li style={{ marginBottom: '0.5rem' }}>Our system analyzes the contract for lock-in clauses</li>
          <li style={{ marginBottom: '0.5rem' }}>Get instant risk score and category breakdown</li>
          <li style={{ marginBottom: '0.5rem' }}>Receive negotiation recommendations</li>
          <li style={{ marginBottom: '0.5rem' }}>Download comprehensive report</li>
        </ol>
      </div>

      <div className="card" style={{ background: '#e7f3ff', borderLeft: '4px solid #007bff' }}>
        <h3>💡 Tip: Where to find HTML contracts</h3>
        <ul style={{ paddingLeft: '1.5rem' }}>
          <li>Save vendor Terms of Service pages as HTML (File → Save As → Web Page, HTML Only)</li>
          <li>Most SaaS vendors provide their ToS at: vendor.com/terms or vendor.com/tos</li>
          <li>Look for "Terms of Service", "Terms and Conditions", or "Service Agreement"</li>
        </ul>
      </div>
    </div>
  );
}

export default FileUpload;
