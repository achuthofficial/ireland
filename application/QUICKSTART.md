# Quick Start Guide

Get the Contract Risk Assessment application running in under 5 minutes!

## Prerequisites

- Python 3.8+
- Node.js 18+
- npm

## Starting the Application

### Option 1: Using Startup Scripts (Recommended)

**Terminal 1 - Backend:**
```bash
cd /workspaces/ireland/application
./start-backend.sh
```

**Terminal 2 - Frontend:**
```bash
cd /workspaces/ireland/application
./start-frontend.sh
```

### Option 2: Manual Start

**Terminal 1 - Backend:**
```bash
cd /workspaces/ireland/application/server
pip install -r requirements.txt
python3 app.py
```

**Terminal 2 - Frontend:**
```bash
cd /workspaces/ireland/application/client
npm install
npm run dev
```

## Access the Application

Once both servers are running:

1. **Frontend**: http://localhost:5173
2. **Backend API**: http://localhost:5000/api/health

## First Steps

1. **Home Page**: View research overview and statistics
2. **Upload Contract**: Try uploading one of the sample contracts from `/workspaces/ireland/contracts/`
3. **Questionnaire**: Answer guided questions for assessment without a file
4. **Compare**: Upload 2-3 contracts to see comparison

## Sample Contracts

Test the app with real vendor contracts:

```bash
# Available in:
/workspaces/ireland/contracts/

# Examples:
- aws.html
- google_cloud.html
- stripe_tos.html
- github.html
```

## Troubleshooting

### Backend won't start
- Check Python version: `python3 --version` (need 3.8+)
- Install dependencies manually: `cd server && pip install -r requirements.txt`
- Check port 5000 is available: `lsof -i :5000`

### Frontend won't start
- Check Node version: `node --version` (need 18+)
- Clear and reinstall: `cd client && rm -rf node_modules && npm install`
- Check port 5173 is available: `lsof -i :5173`

### API Connection Error
- Make sure backend is running on port 5000
- Check `.env` file in `/client/` directory
- Verify CORS is enabled in Flask

## Testing the API

```bash
# Health check
curl http://localhost:5000/api/health

# Get statistics
curl http://localhost:5000/api/stats/overview

# Get vendor list
curl http://localhost:5000/api/vendors/list
```

## Next Steps

- See README.md for full documentation
- Review Phase 1-5 research reports in `/results/`
- Explore API endpoints in `/server/app.py`
- Customize frontend styling in `/client/src/App.css`

## Support

Issues? Check:
1. Both servers are running
2. No port conflicts
3. Dependencies installed correctly
4. Browser console for frontend errors
5. Terminal output for backend errors
