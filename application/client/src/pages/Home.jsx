import { Link } from 'react-router-dom';
import { useEffect, useState } from 'react';
import { getOverviewStats } from '../services/api';

function Home() {
  const [stats, setStats] = useState(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadStats();
  }, []);

  const loadStats = async () => {
    try {
      const data = await getOverviewStats();
      setStats(data.stats);
    } catch (error) {
      console.error('Error loading stats:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="home">
      <h1 className="page-title">Automated Vendor Contract Risk Assessment</h1>
      <p className="page-subtitle">
        Analyze vendor contracts for lock-in risks in minutes, without legal expertise.
      </p>

      <div className="card">
        <h2>What is this tool?</h2>
        <p>
          This framework helps IT practitioners evaluate vendor contract lock-in risks quickly and objectively.
          Based on analysis of <strong>53 real vendor contracts</strong> and <strong>213 lock-in clauses</strong>,
          it provides automated risk scoring and actionable negotiation recommendations.
        </p>
      </div>

      {!loading && stats && (
        <div className="card">
          <h2>Research Foundation</h2>
          <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(200px, 1fr))', gap: '1.5rem', marginTop: '1rem' }}>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#007bff' }}>
                {stats.contracts_analyzed}
              </div>
              <div>Contracts Analyzed</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#007bff' }}>
                {stats.total_clauses}
              </div>
              <div>Lock-in Clauses Found</div>
            </div>
            <div style={{ textAlign: 'center' }}>
              <div style={{ fontSize: '2.5rem', fontWeight: 'bold', color: '#dc3545' }}>
                {stats.high_risk_percentage.toFixed(1)}%
              </div>
              <div>High Risk Rate</div>
            </div>
          </div>
        </div>
      )}

      <div className="card">
        <h2>How to Use</h2>
        <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '2rem', marginTop: '1.5rem' }}>
          <div>
            <h3>📁 Upload Contract</h3>
            <p>Upload an HTML contract file for instant automated analysis</p>
            <Link to="/upload" className="btn btn-primary" style={{ marginTop: '1rem' }}>
              Upload Contract
            </Link>
          </div>
          <div>
            <h3>📝 Questionnaire</h3>
            <p>Answer guided questions about your contract if you don't have the file</p>
            <Link to="/questionnaire" className="btn btn-primary" style={{ marginTop: '1rem' }}>
              Start Questionnaire
            </Link>
          </div>
          <div>
            <h3>⚖️ Compare Vendors</h3>
            <p>Upload multiple contracts to compare vendors objectively</p>
            <Link to="/compare" className="btn btn-primary" style={{ marginTop: '1rem' }}>
              Compare Vendors
            </Link>
          </div>
        </div>
      </div>

      <div className="card">
        <h2>What You'll Get</h2>
        <ul style={{ listStyle: 'none', padding: 0 }}>
          <li style={{ padding: '0.5rem 0', display: 'flex', alignItems: 'start', gap: '0.5rem' }}>
            <span>✓</span>
            <span><strong>Risk Score (0-100):</strong> Objective quantitative assessment</span>
          </li>
          <li style={{ padding: '0.5rem 0', display: 'flex', alignItems: 'start', gap: '0.5rem' }}>
            <span>✓</span>
            <span><strong>Category Breakdown:</strong> Scores across 5 critical areas</span>
          </li>
          <li style={{ padding: '0.5rem 0', display: 'flex', alignItems: 'start', gap: '0.5rem' }}>
            <span>✓</span>
            <span><strong>Critical Issues:</strong> Prioritized list of concerning clauses</span>
          </li>
          <li style={{ padding: '0.5rem 0', display: 'flex', alignItems: 'start', gap: '0.5rem' }}>
            <span>✓</span>
            <span><strong>Negotiation Templates:</strong> Recommended alternative language</span>
          </li>
          <li style={{ padding: '0.5rem 0', display: 'flex', alignItems: 'start', gap: '0.5rem' }}>
            <span>✓</span>
            <span><strong>Professional Report:</strong> Downloadable HTML report</span>
          </li>
        </ul>
      </div>

      <div className="card" style={{ background: '#fff3cd', borderLeft: '4px solid #ffc107' }}>
        <h3>⚠️ Important Disclaimer</h3>
        <p>
          This tool provides automated analysis based on pattern matching and does not constitute legal advice.
          It is designed for initial vendor screening and negotiation preparation.
          <strong> Always consult with qualified legal counsel before signing contracts</strong>, especially for:
        </p>
        <ul>
          <li>Contracts over $500K/year</li>
          <li>Mission-critical services</li>
          <li>Regulated industries</li>
          <li>Complex negotiations</li>
        </ul>
      </div>
    </div>
  );
}

export default Home;
