import { useLocation, useNavigate } from 'react-router-dom';
import { useState } from 'react';
import { generateReport } from '../services/api';

function Results() {
  const location = useLocation();
  const navigate = useNavigate();
  const [downloading, setDownloading] = useState(false);

  const { assessment, recommendations, comparison, assessments, isComparison } = location.state || {};

  if (!assessment && !isComparison) {
    return (
      <div className="card">
        <h2>No Results Available</h2>
        <p>Please complete an assessment first.</p>
        <button className="btn btn-primary" onClick={() => navigate('/')}>
          Go Home
        </button>
      </div>
    );
  }

  const handleDownloadReport = async () => {
    if (!assessment) return;

    setDownloading(true);
    try {
      const blob = await generateReport(assessment);
      const url = window.URL.createObjectURL(blob);
      const a = document.createElement('a');
      a.href = url;
      a.download = `risk_report_${assessment.vendor_name}.html`;
      document.body.appendChild(a);
      a.click();
      window.URL.revokeObjectURL(url);
      document.body.removeChild(a);
    } catch (error) {
      console.error('Error downloading report:', error);
      alert('Failed to download report. Please try again.');
    } finally {
      setDownloading(false);
    }
  };

  const getRiskColor = (level) => {
    const colors = {
      'LOW': { bg: '#d4edda', text: '#155724' },
      'MEDIUM': { bg: '#fff3cd', text: '#856404' },
      'HIGH': { bg: '#f8d7da', text: '#721c24' }
    };
    return colors[level] || colors['MEDIUM'];
  };

  const getCategoryName = (category) => {
    const names = {
      'service_level': 'Service Level Agreements',
      'pricing_terms': 'Pricing Terms',
      'termination_exit': 'Termination & Exit',
      'data_portability': 'Data Portability',
      'support_obligations': 'Support Obligations'
    };
    return names[category] || category;
  };

  if (isComparison && comparison) {
    return (
      <div className="results-page">
        <h1 className="page-title">Vendor Comparison Results</h1>

        <div className="card">
          <h2>Comparison Summary</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem', marginTop: '1.5rem' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#007bff' }}>
                {comparison.total_vendors}
              </div>
              <div>Vendors Compared</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#007bff' }}>
                {comparison.average_score.toFixed(1)}/100
              </div>
              <div>Average Risk Score</div>
            </div>
          </div>

          <div style={{ marginTop: '2rem' }}>
            <h3>Risk Distribution</h3>
            <div style={{ display: 'flex', gap: '1rem', marginTop: '1rem' }}>
              <div style={{ flex: 1, textAlign: 'center', padding: '1rem', background: '#d4edda', borderRadius: '5px' }}>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{comparison.risk_distribution.LOW}</div>
                <div>Low Risk</div>
              </div>
              <div style={{ flex: 1, textAlign: 'center', padding: '1rem', background: '#fff3cd', borderRadius: '5px' }}>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{comparison.risk_distribution.MEDIUM}</div>
                <div>Medium Risk</div>
              </div>
              <div style={{ flex: 1, textAlign: 'center', padding: '1rem', background: '#f8d7da', borderRadius: '5px' }}>
                <div style={{ fontSize: '1.5rem', fontWeight: 'bold' }}>{comparison.risk_distribution.HIGH}</div>
                <div>High Risk</div>
              </div>
            </div>
          </div>
        </div>

        <div className="card">
          <h2>Best Vendors (Lowest Risk)</h2>
          <table style={{ width: '100%', marginTop: '1rem' }}>
            <thead>
              <tr>
                <th style={{ textAlign: 'left', padding: '0.75rem' }}>Rank</th>
                <th style={{ textAlign: 'left', padding: '0.75rem' }}>Vendor</th>
                <th style={{ textAlign: 'center', padding: '0.75rem' }}>Risk Score</th>
                <th style={{ textAlign: 'center', padding: '0.75rem' }}>Risk Level</th>
              </tr>
            </thead>
            <tbody>
              {comparison.best_vendors.map((vendor, idx) => (
                <tr key={idx} style={{ borderBottom: '1px solid #dee2e6' }}>
                  <td style={{ padding: '0.75rem' }}>{idx + 1}</td>
                  <td style={{ padding: '0.75rem', fontWeight: 'bold' }}>{vendor.vendor_name}</td>
                  <td style={{ padding: '0.75rem', textAlign: 'center' }}>{vendor.total_score}/100</td>
                  <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                    <span className={`risk-badge ${vendor.risk_level.toLowerCase()}`}>
                      {vendor.risk_level}
                    </span>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        </div>

        {comparison.worst_vendors.length > 0 && (
          <div className="card">
            <h2>Highest Risk Vendors</h2>
            <table style={{ width: '100%', marginTop: '1rem' }}>
              <thead>
                <tr>
                  <th style={{ textAlign: 'left', padding: '0.75rem' }}>Rank</th>
                  <th style={{ textAlign: 'left', padding: '0.75rem' }}>Vendor</th>
                  <th style={{ textAlign: 'center', padding: '0.75rem' }}>Risk Score</th>
                  <th style={{ textAlign: 'center', padding: '0.75rem' }}>Risk Level</th>
                </tr>
              </thead>
              <tbody>
                {comparison.worst_vendors.map((vendor, idx) => (
                  <tr key={idx} style={{ borderBottom: '1px solid #dee2e6' }}>
                    <td style={{ padding: '0.75rem' }}>{idx + 1}</td>
                    <td style={{ padding: '0.75rem', fontWeight: 'bold' }}>{vendor.vendor_name}</td>
                    <td style={{ padding: '0.75rem', textAlign: 'center' }}>{vendor.total_score}/100</td>
                    <td style={{ padding: '0.75rem', textAlign: 'center' }}>
                      <span className={`risk-badge ${vendor.risk_level.toLowerCase()}`}>
                        {vendor.risk_level}
                      </span>
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}

        <div style={{ marginTop: '2rem', textAlign: 'center' }}>
          <button className="btn btn-primary" onClick={() => navigate('/')}>
            New Assessment
          </button>
        </div>
      </div>
    );
  }

  // Single assessment results
  const riskColors = getRiskColor(assessment.risk_level);

  return (
    <div className="results-page">
      <h1 className="page-title">Risk Assessment Results</h1>

      <div className="card" style={{ background: riskColors.bg, borderLeft: `5px solid ${riskColors.text}` }}>
        <h2 style={{ color: riskColors.text }}>{assessment.vendor_name}</h2>
        <div style={{ fontSize: '3rem', fontWeight: 'bold', color: riskColors.text, margin: '1rem 0' }}>
          {assessment.total_score}/100
        </div>
        <span className={`risk-badge ${assessment.risk_level.toLowerCase()}`}>
          {assessment.risk_level} RISK
        </span>
        <p style={{ marginTop: '1rem', color: riskColors.text }}>
          {assessment.risk_level === 'HIGH' && 'WARNING: This contract presents significant vendor lock-in risk.'}
          {assessment.risk_level === 'MEDIUM' && 'This contract presents moderate lock-in risk.'}
          {assessment.risk_level === 'LOW' && 'This contract presents relatively low lock-in risk.'}
        </p>
      </div>

      <div className="card">
        <h2>Category Breakdown</h2>
        {Object.entries(assessment.category_scores || {}).map(([category, score]) => {
          const details = assessment.category_details?.[category] || {};
          const maxPoints = details.max_points || 25;
          const percentage = (score / maxPoints * 100);

          return (
            <div key={category} style={{ marginBottom: '1.5rem' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                <strong>{getCategoryName(category)}</strong>
                <span>{score}/{maxPoints}</span>
              </div>
              <div style={{ background: '#e9ecef', height: '25px', borderRadius: '5px', overflow: 'hidden' }}>
                <div
                  style={{
                    height: '100%',
                    background: percentage >= 70 ? '#dc3545' : percentage >= 40 ? '#ffc107' : '#28a745',
                    width: `${percentage}%`,
                    transition: 'width 0.3s',
                    display: 'flex',
                    alignItems: 'center',
                    justifyContent: 'center',
                    color: 'white',
                    fontWeight: 'bold'
                  }}
                >
                  {percentage.toFixed(0)}%
                </div>
              </div>
              {details.clause_count > 0 && (
                <div style={{ fontSize: '0.9rem', color: '#666', marginTop: '0.25rem' }}>
                  {details.clause_count} clauses • {details.high_risk_count} high-risk
                </div>
              )}
            </div>
          );
        })}
      </div>

      {recommendations?.priority_issues && recommendations.priority_issues.length > 0 && (
        <div className="card">
          <h2>Priority Issues</h2>
          {recommendations.priority_issues.slice(0, 5).map((issue, idx) => (
            <div key={idx} style={{ marginBottom: '1rem', padding: '1rem', background: '#f8f9fa', borderRadius: '5px' }}>
              <div style={{ display: 'flex', justifyContent: 'space-between', marginBottom: '0.5rem' }}>
                <strong>{idx + 1}. {issue.issue}</strong>
                <span className={`risk-badge ${issue.priority.toLowerCase()}`}>{issue.priority}</span>
              </div>
              {issue.negotiation_points && issue.negotiation_points.length > 0 && (
                <ul style={{ paddingLeft: '1.5rem', marginTop: '0.5rem' }}>
                  {issue.negotiation_points.slice(0, 3).map((point, pidx) => (
                    <li key={pidx} style={{ fontSize: '0.9rem' }}>{point}</li>
                  ))}
                </ul>
              )}
            </div>
          ))}
        </div>
      )}

      {recommendations?.negotiation_strategy && recommendations.negotiation_strategy.length > 0 && (
        <div className="card">
          <h2>Recommended Actions</h2>
          <ol style={{ paddingLeft: '1.5rem' }}>
            {recommendations.negotiation_strategy.map((strategy, idx) => (
              <li key={idx} style={{ marginBottom: '0.5rem' }}>{strategy}</li>
            ))}
          </ol>
        </div>
      )}

      <div style={{ display: 'flex', gap: '1rem', marginTop: '2rem' }}>
        <button
          className="btn btn-primary"
          onClick={handleDownloadReport}
          disabled={downloading}
          style={{ flex: 1 }}
        >
          {downloading ? 'Generating...' : 'Download Full Report'}
        </button>
        <button
          className="btn btn-secondary"
          onClick={() => navigate('/')}
          style={{ flex: 1 }}
        >
          New Assessment
        </button>
      </div>
    </div>
  );
}

export default Results;
