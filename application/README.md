# Contract Risk Assessment Web Application

A full-stack web application for automated vendor contract risk assessment. Built with React (Vite) frontend and Flask backend.

## Features

- **Upload Contract**: Upload HTML contract files for instant automated analysis
- **Questionnaire Mode**: Answer guided questions if you don't have the contract file
- **Vendor Comparison**: Compare multiple contracts side-by-side
- **Risk Scoring**: Get objective 0-100 risk scores based on 5 critical categories
- **Negotiation Templates**: Receive actionable recommendations and alternative contract language
- **Professional Reports**: Download comprehensive HTML reports

## Tech Stack

### Frontend
- React 19 with Vite
- React Router for navigation
- Axios for API calls
- Responsive CSS design

### Backend
- Flask (Python 3)
- Flask-CORS for cross-origin support
- BeautifulSoup4 for HTML parsing
- scikit-learn for ML models

## Quick Start

### Prerequisites
- Python 3.8 or higher
- Node.js 18 or higher
- npm

### 1. Install Backend Dependencies

```bash
cd server
pip install -r requirements.txt
```

### 2. Install Frontend Dependencies

```bash
cd ../client
npm install
```

### 3. Start Backend Server

```bash
cd ../server
python app.py
```

Backend will run on: http://localhost:5000

### 4. Start Frontend (in a new terminal)

```bash
cd client
npm run dev
```

Frontend will run on: http://localhost:5173

### 5. Open Browser

Navigate to: http://localhost:5173

## Project Structure

```
application/
├── client/                 # React frontend
│   ├── src/
│   │   ├── pages/         # Page components
│   │   │   ├── Home.jsx
│   │   │   ├── FileUpload.jsx
│   │   │   ├── Questionnaire.jsx
│   │   │   ├── Compare.jsx
│   │   │   └── Results.jsx
│   │   ├── services/      # API service layer
│   │   │   └── api.js
│   │   ├── App.jsx        # Main app component
│   │   └── App.css        # Global styles
│   ├── package.json
│   └── vite.config.js
│
└── server/                # Flask backend
    ├── app.py            # Main Flask application
    └── requirements.txt
```

## API Endpoints

### Health Check
- `GET /api/health` - Check API status

### Assessment
- `POST /api/assess/upload` - Upload and assess contract file
- `POST /api/assess/questionnaire` - Assess based on questionnaire responses

### Comparison
- `POST /api/compare` - Compare multiple contracts

### Reports
- `POST /api/report/generate` - Generate downloadable HTML report

### Data
- `GET /api/stats/overview` - Get overall statistics
- `GET /api/vendors/list` - Get list of analyzed vendors
- `GET /api/templates/all` - Get all negotiation templates

## Usage Examples

### 1. Upload and Analyze a Contract

1. Go to "Upload Contract"
2. Drag and drop or select an HTML contract file
3. Click "Analyze Contract"
4. View results with risk score and recommendations

### 2. Questionnaire Assessment

1. Go to "Questionnaire"
2. Answer 6 sections of questions about your contract
3. Submit to get instant risk assessment
4. Review results and download report

### 3. Compare Multiple Vendors

1. Go to "Compare Vendors"
2. Upload 2 or more HTML contract files
3. View side-by-side comparison
4. Identify best and worst vendors

## Development

### Frontend Development

```bash
cd client
npm run dev     # Start dev server
npm run build   # Build for production
npm run preview # Preview production build
```

### Backend Development

```bash
cd server
python app.py   # Runs in debug mode
```

## Environment Variables

### Frontend (.env)
```
VITE_API_URL=http://localhost:5000/api
```

## Production Deployment

### Frontend Build

```bash
cd client
npm run build
# Build output in client/dist/
```

### Backend Production

Use a production WSGI server like Gunicorn:

```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

## Important Notes

⚠️ **Legal Disclaimer**: This tool provides automated analysis and does not constitute legal advice. Always consult with qualified legal counsel before signing contracts.

## Research Foundation

This tool is based on comprehensive research:
- **53 real vendor contracts** analyzed
- **213 lock-in clauses** extracted and categorized
- **100% validation success rate** on test set
- **99.9% time savings** vs. manual review
- **5-phase research methodology** (Analysis, Framework, Validation, Testing, ML)

## License

This is a research project. See main project documentation for licensing details.

## Support

For issues or questions:
1. Check existing documentation in `/results/` folder
2. Review Phase 1-5 research reports
3. Open an issue in the repository

## Contributing

This is a research project. Contributions should maintain the integrity of the validated framework and research methodology.
