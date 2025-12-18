#!/usr/bin/env python3
"""
Comprehensive Report Generator
Creates professional HTML and Markdown reports for risk assessments
"""

import json
from datetime import datetime
from pathlib import Path
from typing import Dict, List
import sys

sys.path.append(str(Path(__file__).parent.parent))

from template_generator import NegotiationTemplateGenerator


class ReportGenerator:
    """Generate comprehensive risk assessment reports."""

    def __init__(self):
        self.template_gen = NegotiationTemplateGenerator()

    def generate_html_report(self, assessment: Dict, output_file: str = "risk_report.html"):
        """Generate comprehensive HTML report."""

        # Get negotiation recommendations
        recommendations = self.template_gen.generate_recommendations(assessment)

        html = self._generate_html_content(assessment, recommendations)

        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(html)

        return output_file

    def _generate_html_content(self, assessment: Dict, recommendations: Dict) -> str:
        """Generate HTML content for the report."""

        vendor_name = assessment.get('vendor_name', 'Unknown Vendor')
        risk_score = assessment.get('total_score', 0)
        risk_level = assessment.get('risk_level', 'UNKNOWN')
        category_scores = assessment.get('category_scores', {})
        category_details = assessment.get('category_details', {})

        # Determine color scheme based on risk level
        risk_colors = {
            'LOW': {'bg': '#d4edda', 'border': '#28a745', 'text': '#155724'},
            'MEDIUM': {'bg': '#fff3cd', 'border': '#ffc107', 'text': '#856404'},
            'HIGH': {'bg': '#f8d7da', 'border': '#dc3545', 'text': '#721c24'}
        }

        colors = risk_colors.get(risk_level, risk_colors['MEDIUM'])

        html = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Risk Assessment Report - {vendor_name}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}

        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            line-height: 1.6;
            color: #333;
            background-color: #f5f5f5;
            padding: 20px;
        }}

        .container {{
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 40px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
            border-radius: 8px;
        }}

        .header {{
            border-bottom: 3px solid #007bff;
            padding-bottom: 20px;
            margin-bottom: 30px;
        }}

        .header h1 {{
            color: #007bff;
            font-size: 2.5em;
            margin-bottom: 10px;
        }}

        .header .subtitle {{
            color: #666;
            font-size: 1.1em;
        }}

        .risk-summary {{
            background: {colors['bg']};
            border-left: 5px solid {colors['border']};
            padding: 25px;
            margin: 30px 0;
            border-radius: 5px;
        }}

        .risk-summary h2 {{
            color: {colors['text']};
            font-size: 1.8em;
            margin-bottom: 15px;
        }}

        .risk-score {{
            font-size: 3em;
            font-weight: bold;
            color: {colors['border']};
            margin: 15px 0;
        }}

        .risk-level {{
            display: inline-block;
            padding: 8px 20px;
            background: {colors['border']};
            color: white;
            border-radius: 20px;
            font-weight: bold;
            font-size: 1.2em;
        }}

        .section {{
            margin: 40px 0;
        }}

        .section h2 {{
            color: #007bff;
            font-size: 1.8em;
            margin-bottom: 20px;
            padding-bottom: 10px;
            border-bottom: 2px solid #e0e0e0;
        }}

        .section h3 {{
            color: #495057;
            font-size: 1.4em;
            margin: 25px 0 15px 0;
        }}

        .category-card {{
            background: #f8f9fa;
            border: 1px solid #dee2e6;
            border-radius: 8px;
            padding: 20px;
            margin: 15px 0;
        }}

        .category-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }}

        .category-name {{
            font-size: 1.3em;
            font-weight: bold;
            color: #495057;
        }}

        .category-score {{
            font-size: 1.5em;
            font-weight: bold;
        }}

        .progress-bar {{
            width: 100%;
            height: 30px;
            background: #e9ecef;
            border-radius: 15px;
            overflow: hidden;
            margin: 10px 0;
        }}

        .progress-fill {{
            height: 100%;
            background: linear-gradient(90deg, #28a745, #ffc107, #dc3545);
            transition: width 0.3s ease;
            display: flex;
            align-items: center;
            justify-content: center;
            color: white;
            font-weight: bold;
        }}

        .issue-card {{
            background: white;
            border: 1px solid #dee2e6;
            border-left: 4px solid #dc3545;
            padding: 20px;
            margin: 15px 0;
            border-radius: 5px;
        }}

        .issue-card.high {{
            border-left-color: #dc3545;
        }}

        .issue-card.medium {{
            border-left-color: #ffc107;
        }}

        .issue-card.low {{
            border-left-color: #28a745;
        }}

        .issue-title {{
            font-size: 1.2em;
            font-weight: bold;
            color: #212529;
            margin-bottom: 10px;
        }}

        .issue-description {{
            color: #666;
            margin: 10px 0;
        }}

        .negotiation-points {{
            margin: 15px 0;
        }}

        .negotiation-points ul {{
            list-style: none;
            padding-left: 0;
        }}

        .negotiation-points li {{
            padding: 8px 0;
            padding-left: 25px;
            position: relative;
        }}

        .negotiation-points li:before {{
            content: "→";
            position: absolute;
            left: 0;
            color: #007bff;
            font-weight: bold;
        }}

        .template-box {{
            background: #f8f9fa;
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            font-family: 'Courier New', monospace;
            font-size: 0.9em;
        }}

        .template-label {{
            font-weight: bold;
            color: #007bff;
            margin-bottom: 8px;
        }}

        .recommendation-list {{
            background: #e7f3ff;
            border-left: 4px solid #007bff;
            padding: 20px;
            margin: 20px 0;
        }}

        .recommendation-list li {{
            margin: 10px 0;
            padding-left: 10px;
        }}

        .priority-badge {{
            display: inline-block;
            padding: 4px 12px;
            border-radius: 12px;
            font-size: 0.85em;
            font-weight: bold;
            margin-left: 10px;
        }}

        .priority-badge.high {{
            background: #dc3545;
            color: white;
        }}

        .priority-badge.medium {{
            background: #ffc107;
            color: #333;
        }}

        .priority-badge.low {{
            background: #28a745;
            color: white;
        }}

        table {{
            width: 100%;
            border-collapse: collapse;
            margin: 20px 0;
        }}

        th, td {{
            padding: 12px;
            text-align: left;
            border-bottom: 1px solid #dee2e6;
        }}

        th {{
            background: #007bff;
            color: white;
            font-weight: bold;
        }}

        tr:hover {{
            background: #f8f9fa;
        }}

        .footer {{
            margin-top: 50px;
            padding-top: 20px;
            border-top: 2px solid #dee2e6;
            text-align: center;
            color: #666;
            font-size: 0.9em;
        }}

        @media print {{
            body {{
                background: white;
                padding: 0;
            }}
            .container {{
                box-shadow: none;
                padding: 20px;
            }}
        }}
    </style>
</head>
<body>
    <div class="container">
        <div class="header">
            <h1>Vendor Contract Risk Assessment Report</h1>
            <div class="subtitle">
                Automated Lock-In Risk Analysis for IT Practitioners
            </div>
            <div class="subtitle" style="margin-top: 10px;">
                Generated: {datetime.now().strftime('%B %d, %Y at %I:%M %p')}
            </div>
        </div>

        <div class="risk-summary">
            <h2>{vendor_name}</h2>
            <div class="risk-score">{risk_score}/100</div>
            <div class="risk-level">{risk_level} RISK</div>
            <p style="margin-top: 15px; color: {colors['text']}; font-size: 1.1em;">
                {self._get_risk_interpretation(risk_score, risk_level)}
            </p>
        </div>

        <div class="section">
            <h2>Executive Summary</h2>
            <p style="font-size: 1.1em; line-height: 1.8;">
                This automated risk assessment analyzed the vendor contract across five critical categories
                that impact vendor lock-in and switching costs. The analysis uses a 100-point weighted scoring
                system based on empirical research of 61 major vendor contracts.
            </p>
        </div>

        <div class="section">
            <h2>Risk Breakdown by Category</h2>
            {self._generate_category_breakdown_html(category_scores, category_details)}
        </div>

        <div class="section">
            <h2>Critical Issues Identified</h2>
            {self._generate_critical_issues_html(recommendations)}
        </div>

        <div class="section">
            <h2>Negotiation Recommendations</h2>
            <div class="recommendation-list">
                <h3>Recommended Actions (Priority Order):</h3>
                <ol>
                    {self._generate_recommendations_list_html(recommendations)}
                </ol>
            </div>
        </div>

        <div class="section">
            <h2>Alternative Contract Language</h2>
            <p style="margin-bottom: 20px;">
                The following sections provide recommended contract language to address identified risks.
                Work with your procurement and legal teams to propose these modifications to the vendor.
            </p>
            {self._generate_template_language_html(recommendations)}
        </div>

        <div class="section">
            <h2>Negotiation Strategy</h2>
            <div class="recommendation-list">
                <ul>
                    {self._generate_strategy_list_html(recommendations)}
                </ul>
            </div>
        </div>

        <div class="section">
            <h2>About This Assessment</h2>
            <h3>Methodology</h3>
            <p>
                This assessment uses a validated framework based on systematic content analysis of 61
                vendor contracts from major software providers. The 100-point weighted scoring system
                prioritizes categories based on empirical risk data:
            </p>
            <ul style="margin: 15px 0 15px 30px; line-height: 2;">
                <li><strong>Service Level Agreements (25 points)</strong> - Highest risk category (81.1% of SLA clauses were high-risk)</li>
                <li><strong>Pricing Terms (25 points)</strong> - Second highest risk (66.1% high-risk)</li>
                <li><strong>Termination/Exit (20 points)</strong> - Moderate risk (41.3% high-risk)</li>
                <li><strong>Data Portability (15 points)</strong> - Often under-addressed</li>
                <li><strong>Support Obligations (15 points)</strong> - Lower average risk (25.0% high-risk)</li>
            </ul>

            <h3>Limitations</h3>
            <p>
                This automated assessment identifies common lock-in mechanisms but cannot replace
                professional legal review. Always consult with qualified legal counsel before signing
                contracts, especially for high-value or business-critical services.
            </p>
        </div>

        <div class="footer">
            <p><strong>Automated Vendor Contract Risk Assessment Tool</strong></p>
            <p>Phase 2 Framework - Research Project</p>
            <p>For IT practitioners evaluating vendor lock-in risks</p>
            <p style="margin-top: 10px; font-size: 0.85em;">
                This report is for informational purposes only and does not constitute legal advice.
            </p>
        </div>
    </div>
</body>
</html>"""

        return html

    def _get_risk_interpretation(self, score: float, level: str) -> str:
        """Get interpretation text for risk score."""
        if level == "HIGH":
            return f"This contract presents significant vendor lock-in risk. We strongly recommend extensive negotiation or consideration of alternative vendors before signing."
        elif level == "MEDIUM":
            return f"This contract presents moderate lock-in risk. Several areas need improvement through negotiation, particularly in the high-scoring categories below."
        else:
            return f"This contract presents relatively low lock-in risk compared to industry averages. However, review the recommendations below to address any remaining concerns."

    def _generate_category_breakdown_html(self, category_scores: Dict, category_details: Dict) -> str:
        """Generate HTML for category breakdown section."""
        html = ""

        category_info = {
            'service_level': {'name': 'Service Level Agreements', 'max': 25},
            'pricing_terms': {'name': 'Pricing Terms', 'max': 25},
            'termination_exit': {'name': 'Termination & Exit', 'max': 20},
            'data_portability': {'name': 'Data Portability', 'max': 15},
            'support_obligations': {'name': 'Support Obligations', 'max': 15}
        }

        for category, score in category_scores.items():
            info = category_info.get(category, {'name': category, 'max': 25})
            max_score = info['max']
            percentage = (score / max_score * 100) if max_score > 0 else 0

            details = category_details.get(category, {})
            clause_count = details.get('clause_count', 0)
            high_risk_count = details.get('high_risk_count', 0)
            high_risk_pct = details.get('high_risk_percentage', 0)

            # Determine color
            if percentage >= 70:
                color = '#dc3545'
            elif percentage >= 40:
                color = '#ffc107'
            else:
                color = '#28a745'

            html += f"""
            <div class="category-card">
                <div class="category-header">
                    <div class="category-name">{info['name']}</div>
                    <div class="category-score" style="color: {color};">{score}/{max_score}</div>
                </div>
                <div class="progress-bar">
                    <div class="progress-fill" style="width: {percentage}%; background: {color};">
                        {percentage:.0f}%
                    </div>
                </div>
                <div style="margin-top: 10px; color: #666; font-size: 0.95em;">
                    {clause_count} clauses analyzed • {high_risk_count} high-risk ({high_risk_pct:.0f}%)
                </div>
            </div>
            """

        return html

    def _generate_critical_issues_html(self, recommendations: Dict) -> str:
        """Generate HTML for critical issues section."""
        priority_issues = recommendations.get('priority_issues', [])

        if not priority_issues:
            return "<p>No critical issues identified.</p>"

        html = ""
        for idx, issue in enumerate(priority_issues[:10], 1):  # Top 10 issues
            priority = issue.get('priority', 'MEDIUM').lower()
            category = issue.get('category', '').replace('_', ' ').title()
            issue_desc = issue.get('issue', '')
            neg_points = issue.get('negotiation_points', [])

            html += f"""
            <div class="issue-card {priority}">
                <div class="issue-title">
                    {idx}. {issue_desc}
                    <span class="priority-badge {priority}">{priority.upper()}</span>
                </div>
                <div class="issue-description">
                    <strong>Category:</strong> {category}
                </div>
                <div class="negotiation-points">
                    <strong>Key Negotiation Points:</strong>
                    <ul>
                        {''.join(f'<li>{point}</li>' for point in neg_points[:5])}
                    </ul>
                </div>
            </div>
            """

        return html

    def _generate_recommendations_list_html(self, recommendations: Dict) -> str:
        """Generate HTML list of recommendations."""
        strategy = recommendations.get('negotiation_strategy', [])

        html = ""
        for rec in strategy:
            html += f"<li>{rec}</li>\n"

        return html

    def _generate_template_language_html(self, recommendations: Dict) -> str:
        """Generate HTML for template language section."""
        templates = recommendations.get('template_language', {})

        if not templates:
            return "<p>No specific template language available.</p>"

        html = ""
        for idx, (key, template) in enumerate(list(templates.items())[:5], 1):
            parts = key.split('_', 1)
            category = parts[0].replace('_', ' ').title()
            issue = parts[1] if len(parts) > 1 else ''

            html += f"""
            <h3>{idx}. {issue.replace('_', ' ').title()} ({category})</h3>
            <div class="template-label">❌ Problematic Language:</div>
            <div class="template-box" style="border-left: 3px solid #dc3545;">
                {template.get('problematic', 'N/A')}
            </div>
            <div class="template-label" style="margin-top: 15px;">✅ Recommended Language:</div>
            <div class="template-box" style="border-left: 3px solid #28a745;">
                {template.get('recommended', 'N/A')}
            </div>
            """

        return html

    def _generate_strategy_list_html(self, recommendations: Dict) -> str:
        """Generate HTML for general strategies."""
        strategies = recommendations.get('general_strategies', [])

        html = ""
        for strategy in strategies[:8]:
            html += f"<li>{strategy}</li>\n"

        return html

    def generate_markdown_report(self, assessment: Dict, output_file: str = "risk_report.md") -> str:
        """Generate markdown version of the report."""

        recommendations = self.template_gen.generate_recommendations(assessment)
        redline_doc = self.template_gen.generate_redline_document(recommendations)

        # Add assessment summary to redline
        summary = f"""# VENDOR CONTRACT RISK ASSESSMENT REPORT

**Vendor**: {assessment.get('vendor_name')}
**Date**: {datetime.now().strftime('%B %d, %Y')}
**Risk Score**: {assessment.get('total_score')}/100
**Risk Level**: {assessment.get('risk_level')}

---

## ASSESSMENT SUMMARY

Total Score: **{assessment.get('total_score')}/100**
Risk Classification: **{assessment.get('risk_level')} RISK**

### Category Scores

"""

        for category, score in assessment.get('category_scores', {}).items():
            summary += f"- **{category.replace('_', ' ').title()}**: {score} points\n"

        summary += "\n---\n\n"

        full_report = summary + redline_doc

        # Save to file
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(full_report)

        return output_file


def main():
    """Example usage."""
    generator = ReportGenerator()

    # Example assessment
    example = {
        'vendor_name': 'Example Vendor Inc.',
        'total_score': 68.5,
        'risk_level': 'HIGH',
        'category_scores': {
            'service_level': 20,
            'pricing_terms': 18,
            'termination_exit': 15,
            'data_portability': 10,
            'support_obligations': 5.5
        },
        'category_details': {
            'service_level': {'score': 20, 'max_points': 25, 'clause_count': 5, 'high_risk_count': 4, 'high_risk_percentage': 80},
            'pricing_terms': {'score': 18, 'max_points': 25, 'clause_count': 4, 'high_risk_count': 3, 'high_risk_percentage': 75}
        }
    }

    # Generate HTML report
    html_file = generator.generate_html_report(example, "example_report.html")
    print(f"HTML report generated: {html_file}")

    # Generate markdown report
    md_file = generator.generate_markdown_report(example, "example_report.md")
    print(f"Markdown report generated: {md_file}")


if __name__ == "__main__":
    main()
