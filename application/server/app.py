#!/usr/bin/env python3
"""
Flask Backend for Contract Risk Assessment Application
Provides REST API endpoints for all framework functionality
"""

from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import sys
import os
import json
import tempfile
from pathlib import Path
from werkzeug.utils import secure_filename
import traceback

# Add code directory to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent / 'code'))

from risk_assessor import RiskAssessmentEngine, ContractAnalyzer
from report_generator import ReportGenerator
from template_generator import NegotiationTemplateGenerator
from scoring_algorithm import ContractScorer
from interactive_assessment import InteractiveAssessment

app = Flask(__name__)
CORS(app)  # Enable CORS for React frontend

# Configuration
UPLOAD_FOLDER = '/tmp/contract_uploads'
ALLOWED_EXTENSIONS = {'html', 'htm'}
MAX_FILE_SIZE = 10 * 1024 * 1024  # 10MB

os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize components
engine = RiskAssessmentEngine()
report_gen = ReportGenerator()
template_gen = NegotiationTemplateGenerator()


def allowed_file(filename):
    """Check if file extension is allowed."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint."""
    return jsonify({
        'status': 'healthy',
        'service': 'Contract Risk Assessment API',
        'version': '1.0.0'
    })


@app.route('/api/assess/upload', methods=['POST'])
def assess_upload():
    """
    Assess a contract from uploaded HTML file.

    Expected: multipart/form-data with 'contract' file field
    Returns: Risk assessment JSON
    """
    try:
        # Check if file is present
        if 'contract' not in request.files:
            return jsonify({'error': 'No contract file provided'}), 400

        file = request.files['contract']

        if file.filename == '':
            return jsonify({'error': 'No file selected'}), 400

        if not allowed_file(file.filename):
            return jsonify({'error': 'Only HTML files are allowed'}), 400

        # Save file temporarily
        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        # Assess contract
        assessment = engine.assess_contract_file(filepath)

        # Clean up
        os.remove(filepath)

        if 'error' in assessment:
            return jsonify({'error': assessment['error']}), 400

        # Generate recommendations
        recommendations = template_gen.generate_recommendations(assessment)

        return jsonify({
            'success': True,
            'assessment': assessment,
            'recommendations': recommendations
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/assess/questionnaire', methods=['POST'])
def assess_questionnaire():
    """
    Assess a contract from questionnaire responses.

    Expected JSON: { responses: { ... } }
    Returns: Risk assessment JSON
    """
    try:
        data = request.json
        responses = data.get('responses', {})

        if not responses:
            return jsonify({'error': 'No responses provided'}), 400

        # Calculate risk from responses
        assessment = calculate_risk_from_questionnaire(responses)

        # Generate recommendations
        recommendations = template_gen.generate_recommendations(assessment)

        return jsonify({
            'success': True,
            'assessment': assessment,
            'recommendations': recommendations
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


def calculate_risk_from_questionnaire(responses):
    """Calculate risk score from questionnaire responses."""

    category_scores = {
        'data_portability': 0,
        'pricing_terms': 0,
        'support_obligations': 0,
        'termination_exit': 0,
        'service_level': 0
    }

    max_points = {
        'data_portability': 15,
        'pricing_terms': 25,
        'support_obligations': 15,
        'termination_exit': 20,
        'service_level': 25
    }

    # Data Portability scoring
    if responses.get('data_export', '').lower() in ['no', 'unclear']:
        category_scores['data_portability'] += 5
    if responses.get('data_format', '').lower() in ['no', 'unclear']:
        category_scores['data_portability'] += 4
    if responses.get('api_access', '').lower() in ['no', 'unclear']:
        category_scores['data_portability'] += 3
    if responses.get('post_termination_access', '').lower() in ['no', 'unclear']:
        category_scores['data_portability'] += 3

    # Pricing Terms scoring
    if responses.get('price_lock', '').lower() in ['no', 'unclear']:
        category_scores['pricing_terms'] += 8
    if responses.get('price_increase', '').lower() == 'yes':
        category_scores['pricing_terms'] += 10
        if responses.get('price_increase_cap', '').lower() in ['no', 'unclear']:
            category_scores['pricing_terms'] += 5
        try:
            notice_days = int(responses.get('price_notice', '0'))
            if notice_days < 30:
                category_scores['pricing_terms'] += 2
        except:
            pass

    # Support Obligations scoring
    if responses.get('support_sla', '').lower() in ['no', 'unclear']:
        category_scores['support_obligations'] += 6
    if responses.get('support_hours', '').lower() == 'best-effort':
        category_scores['support_obligations'] += 5
    if responses.get('feature_changes', '').lower() == 'yes':
        category_scores['support_obligations'] += 4

    # Termination/Exit scoring
    if responses.get('termination_flexibility', '').lower() in ['no', 'only-for-cause']:
        category_scores['termination_exit'] += 8
    if responses.get('termination_fee', '').lower() == 'yes':
        category_scores['termination_exit'] += 7
    if responses.get('auto_renewal', '').lower() == 'yes':
        try:
            renewal_notice = int(responses.get('renewal_notice', '0'))
            if renewal_notice > 60:
                category_scores['termination_exit'] += 5
            elif renewal_notice > 30:
                category_scores['termination_exit'] += 3
        except:
            category_scores['termination_exit'] += 4

    # Service Level scoring
    if responses.get('sla_exists', '').lower() in ['no', 'unclear']:
        category_scores['service_level'] += 15
    else:
        try:
            uptime = float(responses.get('uptime_percentage', '0'))
            if uptime < 99.0:
                category_scores['service_level'] += 8
            elif uptime < 99.5:
                category_scores['service_level'] += 5
            elif uptime < 99.9:
                category_scores['service_level'] += 3
        except:
            category_scores['service_level'] += 10

        if responses.get('sla_credits', '').lower() in ['no', 'unclear']:
            category_scores['service_level'] += 5

    if responses.get('liability_cap', '').lower() == 'yes':
        category_scores['service_level'] += 5

    # Calculate total score
    total_score = sum(category_scores.values())

    # Determine risk level
    if total_score <= 33:
        risk_level = "LOW"
    elif total_score <= 66:
        risk_level = "MEDIUM"
    else:
        risk_level = "HIGH"

    # Create category details
    category_details = {}
    for category, score in category_scores.items():
        percentage = (score / max_points[category] * 100) if max_points[category] > 0 else 0
        category_details[category] = {
            'score': score,
            'max_points': max_points[category],
            'percentage': round(percentage, 1),
            'clause_count': 0,
            'high_risk_count': 0,
            'missing_coverage': False
        }

    return {
        'vendor_name': responses.get('vendor_name', 'Unknown Vendor'),
        'total_score': round(total_score, 2),
        'risk_level': risk_level,
        'category_scores': category_scores,
        'category_details': category_details,
        'total_clauses': 0,
        'questionnaire_responses': responses
    }


@app.route('/api/compare', methods=['POST'])
def compare_contracts():
    """
    Compare multiple contracts.

    Expected: multipart/form-data with multiple 'contracts[]' files
    Returns: Comparative analysis JSON
    """
    try:
        files = request.files.getlist('contracts[]')

        if not files or len(files) == 0:
            return jsonify({'error': 'No contract files provided'}), 400

        assessments = []

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                filepath = os.path.join(UPLOAD_FOLDER, filename)
                file.save(filepath)

                assessment = engine.assess_contract_file(filepath)

                if 'error' not in assessment:
                    assessments.append(assessment)

                os.remove(filepath)

        if not assessments:
            return jsonify({'error': 'No valid contracts could be assessed'}), 400

        # Generate comparison
        comparison = engine.generate_comparison_report(assessments)

        return jsonify({
            'success': True,
            'assessments': assessments,
            'comparison': comparison
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/report/generate', methods=['POST'])
def generate_report():
    """
    Generate HTML report for an assessment.

    Expected JSON: { assessment: {...} }
    Returns: HTML report file
    """
    try:
        data = request.json
        assessment = data.get('assessment')

        if not assessment:
            return jsonify({'error': 'No assessment data provided'}), 400

        # Generate HTML report
        with tempfile.NamedTemporaryFile(mode='w', suffix='.html', delete=False) as f:
            report_file = f.name

        report_gen.generate_html_report(assessment, report_file)

        return send_file(
            report_file,
            mimetype='text/html',
            as_attachment=True,
            download_name=f"risk_report_{assessment.get('vendor_name', 'contract')}.html"
        )

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/templates/all', methods=['GET'])
def get_all_templates():
    """Get all negotiation templates."""
    try:
        template_path = Path(__file__).parent.parent.parent / 'code' / 'negotiation_templates.json'
        with open(template_path, 'r') as f:
            templates = json.load(f)

        return jsonify({
            'success': True,
            'templates': templates
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/templates/category/<category>', methods=['GET'])
def get_category_templates(category):
    """Get templates for a specific category."""
    try:
        templates = template_gen.get_category_templates(category)

        return jsonify({
            'success': True,
            'category': category,
            'templates': templates
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/stats/overview', methods=['GET'])
def get_overview_stats():
    """Get overview statistics from Phase 1 analysis."""
    try:
        stats_file = Path(__file__).parent.parent.parent / 'data' / 'phase1_clause_patterns.json'

        with open(stats_file, 'r') as f:
            stats = json.load(f)

        return jsonify({
            'success': True,
            'stats': {
                'contracts_analyzed': stats.get('contracts_analyzed', 0),
                'total_clauses': stats.get('total_clauses', 0),
                'high_risk_percentage': stats.get('high_risk_percentage', 0),
                'category_statistics': stats.get('category_statistics', {}),
                'lock_in_mechanism_counts': stats.get('lock_in_mechanism_counts', {})
            }
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.route('/api/vendors/list', methods=['GET'])
def get_vendor_list():
    """Get list of analyzed vendors."""
    try:
        contracts_dir = Path(__file__).parent.parent.parent / 'contracts'
        vendors = []

        for contract_file in contracts_dir.glob('*.html'):
            vendor_name = contract_file.stem.replace('_', ' ').replace('2', '').title()
            vendors.append({
                'name': vendor_name,
                'filename': contract_file.name
            })

        return jsonify({
            'success': True,
            'vendors': sorted(vendors, key=lambda x: x['name'])
        })

    except Exception as e:
        traceback.print_exc()
        return jsonify({'error': str(e)}), 500


@app.errorhandler(413)
def too_large(e):
    """Handle file too large error."""
    return jsonify({'error': 'File too large. Maximum size is 10MB'}), 413


@app.errorhandler(404)
def not_found(e):
    """Handle 404 errors."""
    return jsonify({'error': 'Endpoint not found'}), 404


@app.errorhandler(500)
def internal_error(e):
    """Handle 500 errors."""
    return jsonify({'error': 'Internal server error'}), 500


if __name__ == '__main__':
    print("=" * 70)
    print("  CONTRACT RISK ASSESSMENT API SERVER")
    print("=" * 70)
    print()
    print("Starting Flask server...")
    print("API will be available at: http://localhost:5000")
    print()
    print("Available endpoints:")
    print("  GET  /api/health                - Health check")
    print("  POST /api/assess/upload         - Assess contract from file")
    print("  POST /api/assess/questionnaire  - Assess from questionnaire")
    print("  POST /api/compare               - Compare multiple contracts")
    print("  POST /api/report/generate       - Generate HTML report")
    print("  GET  /api/templates/all         - Get all templates")
    print("  GET  /api/stats/overview        - Get overview statistics")
    print("  GET  /api/vendors/list          - Get vendor list")
    print()
    print("=" * 70)
    print()

    app.run(host='0.0.0.0', port=5000, debug=True)
