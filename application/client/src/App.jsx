import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import Home from './pages/Home';
import FileUpload from './pages/FileUpload';
import Questionnaire from './pages/Questionnaire';
import Compare from './pages/Compare';
import Results from './pages/Results';
import './App.css';

function App() {
  return (
    <Router>
      <div className="app">
        <nav className="navbar">
          <div className="nav-container">
            <Link to="/" className="nav-logo">
              📋 Contract Risk Assessment
            </Link>
            <ul className="nav-menu">
              <li className="nav-item">
                <Link to="/" className="nav-link">Home</Link>
              </li>
              <li className="nav-item">
                <Link to="/upload" className="nav-link">Upload Contract</Link>
              </li>
              <li className="nav-item">
                <Link to="/questionnaire" className="nav-link">Questionnaire</Link>
              </li>
              <li className="nav-item">
                <Link to="/compare" className="nav-link">Compare Vendors</Link>
              </li>
            </ul>
          </div>
        </nav>

        <main className="main-content">
          <Routes>
            <Route path="/" element={<Home />} />
            <Route path="/upload" element={<FileUpload />} />
            <Route path="/questionnaire" element={<Questionnaire />} />
            <Route path="/compare" element={<Compare />} />
            <Route path="/results" element={<Results />} />
          </Routes>
        </main>

        <footer className="footer">
          <div className="footer-content">
            <p>Automated Vendor Contract Risk Assessment Tool</p>
            <p className="disclaimer">
              This tool provides automated analysis and does not constitute legal advice.
              Always consult with qualified legal counsel before signing contracts.
            </p>
          </div>
        </footer>
      </div>
    </Router>
  );
}

export default App;
