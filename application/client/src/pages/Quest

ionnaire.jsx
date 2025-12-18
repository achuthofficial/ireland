import { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { assessQuestionnaire } from '../services/api';

function Questionnaire() {
  const navigate = useNavigate();
  const [step, setStep] = useState(0);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [responses, setResponses] = useState({
    vendor_name: '',
    software_type: '',
    contract_value: '',
    business_criticality: '',
    data_export: '',
    data_format: '',
    api_access: '',
    post_termination_access: '',
    price_lock: '',
    price_increase: '',
    price_increase_cap: '',
    price_notice: '',
    support_sla: '',
    support_hours: '',
    feature_changes: '',
    termination_flexibility: '',
    termination_fee: '',
    auto_renewal: '',
    renewal_notice: '',
    sla_exists: '',
    uptime_percentage: '',
    sla_credits: '',
    liability_cap: ''
  });

  const questions = [
    // Basic Information
    {
      section: 'Basic Information',
      questions: [
        { key: 'vendor_name', label: 'Vendor Name', type: 'text' },
        { key: 'software_type', label: 'Software Type', type: 'select', options: ['Cloud', 'SaaS', 'Enterprise'] },
        { key: 'contract_value', label: 'Annual Contract Value (USD)', type: 'text' },
        { key: 'business_criticality', label: 'Business Criticality', type: 'select', options: ['Critical', 'Important', 'Nice-to-have'] }
      ]
    },
    // Data Portability
    {
      section: 'Data Portability',
      questions: [
        { key: 'data_export', label: 'Does the contract explicitly grant data export rights?', type: 'select', options: ['Yes', 'No', 'Unclear'] },
        { key: 'data_format', label: 'Are standard export formats (CSV/JSON/XML) mentioned?', type: 'select', options: ['Yes', 'No', 'Unclear'] },
        { key: 'api_access', label: 'Is API access for data export guaranteed?', type: 'select', options: ['Yes', 'No', 'Unclear'] },
        { key: 'post_termination_access', label: 'Can you retrieve data after termination?', type: 'select', options: ['Yes', 'No', 'Unclear'] }
      ]
    },
    // Pricing Terms
    {
      section: 'Pricing Terms',
      questions: [
        { key: 'price_lock', label: 'Is pricing locked for the contract term?', type: 'select', options: ['Yes', 'No', 'Unclear'] },
        { key: 'price_increase', label: 'Can vendor increase prices unilaterally?', type: 'select', options: ['Yes', 'No', 'Unclear'] },
        { key: 'price_increase_cap', label: 'Is there a cap on price increases?', type: 'select', options: ['Yes', 'No', 'Unclear'], conditional: 'price_increase', conditionalValue: 'yes' },
        { key: 'price_notice', label: 'Advance notice for price changes (days)', type: 'number', conditional: 'price_increase', conditionalValue: 'yes' }
      ]
    },
    // Support Obligations
    {
      section: 'Support Obligations',
      questions: [
        { key: 'support_sla', label: 'Are support response times specified?', type: 'select', options: ['Yes', 'No', 'Unclear'] },
        { key: 'support_hours', label: 'Support Availability', type: 'select', options: ['24x7', 'Business-hours', 'Best-effort'] },
        { key: 'feature_changes', label: 'Can vendor discontinue features without notice?', type: 'select', options: ['Yes', 'No', 'Unclear'] }
      ]
    },
    // Termination & Exit
    {
      section: 'Termination and Exit',
      questions: [
        { key: 'termination_flexibility', label: 'Can you terminate before contract end?', type: 'select', options: ['Yes', 'No', 'Only-for-cause'] },
        { key: 'termination_fee', label: 'Are there early termination fees?', type: 'select', options: ['Yes', 'No', 'Unclear'] },
        { key: 'auto_renewal', label: 'Does contract auto-renew?', type: 'select', options: ['Yes', 'No', 'Unclear'] },
        { key: 'renewal_notice', label: 'Notice period to prevent renewal (days)', type: 'number', conditional: 'auto_renewal', conditionalValue: 'yes' }
      ]
    },
    // Service Level
    {
      section: 'Service Level Agreements',
      questions: [
        { key: 'sla_exists', label: 'Does contract include uptime SLA?', type: 'select', options: ['Yes', 'No', 'Unclear'] },
        { key: 'uptime_percentage', label: 'Guaranteed uptime percentage (e.g., 99.9)', type: 'number', conditional: 'sla_exists', conditionalValue: 'yes' },
        { key: 'sla_credits', label: 'Are service credits provided for SLA failures?', type: 'select', options: ['Yes', 'No', 'Unclear'], conditional: 'sla_exists', conditionalValue: 'yes' },
        { key: 'liability_cap', label: 'Does vendor cap liability for outages?', type: 'select', options: ['Yes', 'No', 'Unclear'] }
      ]
    }
  ];

  const currentSection = questions[step];

  const handleInputChange = (key, value) => {
    setResponses({ ...responses, [key]: value });
  };

  const handleNext = () => {
    if (step < questions.length - 1) {
      setStep(step + 1);
    }
  };

  const handlePrevious = () => {
    if (step > 0) {
      setStep(step - 1);
    }
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    setError('');

    try {
      const data = await assessQuestionnaire(responses);

      if (data.success) {
        navigate('/results', { state: { assessment: data.assessment, recommendations: data.recommendations } });
      } else {
        setError(data.error || 'Failed to assess contract');
      }
    } catch (err) {
      setError(err.response?.data?.error || 'Error processing questionnaire. Please try again.');
      console.error('Questionnaire error:', err);
    } finally {
      setLoading(false);
    }
  };

  const shouldShowQuestion = (question) => {
    if (!question.conditional) return true;
    return responses[question.conditional]?.toLowerCase() === question.conditionalValue;
  };

  const filteredQuestions = currentSection.questions.filter(shouldShowQuestion);

  return (
    <div className="questionnaire-page">
      <h1 className="page-title">Contract Assessment Questionnaire</h1>
      <p className="page-subtitle">
        Answer questions about your contract to receive a risk assessment
      </p>

      <div className="card">
        <div style={{ marginBottom: '2rem' }}>
          <h2>Section {step + 1} of {questions.length}: {currentSection.section}</h2>
          <div style={{ background: '#e9ecef', height: '10px', borderRadius: '5px', marginTop: '1rem' }}>
            <div
              style={{
                background: '#007bff',
                height: '100%',
                borderRadius: '5px',
                width: `${((step + 1) / questions.length) * 100}%`,
                transition: 'width 0.3s'
              }}
            ></div>
          </div>
        </div>

        <form onSubmit={step === questions.length - 1 ? handleSubmit : (e) => { e.preventDefault(); handleNext(); }}>
          {filteredQuestions.map((q) => (
            <div key={q.key} className="form-group">
              <label className="form-label">{q.label}</label>
              {q.type === 'text' || q.type === 'number' ? (
                <input
                  type={q.type}
                  className="form-input"
                  value={responses[q.key]}
                  onChange={(e) => handleInputChange(q.key, e.target.value)}
                  required
                />
              ) : (
                <select
                  className="form-select"
                  value={responses[q.key]}
                  onChange={(e) => handleInputChange(q.key, e.target.value)}
                  required
                >
                  <option value="">Select an option...</option>
                  {q.options.map((opt) => (
                    <option key={opt} value={opt}>{opt}</option>
                  ))}
                </select>
              )}
            </div>
          ))}

          {error && (
            <div className="error" style={{ marginTop: '1rem' }}>
              {error}
            </div>
          )}

          <div style={{ display: 'flex', gap: '1rem', marginTop: '2rem' }}>
            {step > 0 && (
              <button
                type="button"
                className="btn btn-secondary"
                onClick={handlePrevious}
                style={{ flex: 1 }}
              >
                Previous
              </button>
            )}
            <button
              type="submit"
              className="btn btn-primary"
              disabled={loading}
              style={{ flex: 1 }}
            >
              {loading ? 'Processing...' : step === questions.length - 1 ? 'Get Results' : 'Next'}
            </button>
          </div>
        </form>

        {loading && (
          <div className="loading" style={{ marginTop: '2rem' }}>
            <div className="spinner"></div>
            <p style={{ marginTop: '1rem', color: '#666' }}>
              Calculating risk assessment...
            </p>
          </div>
        )}
      </div>
    </div>
  );
}

export default Questionnaire;
