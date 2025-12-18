#!/usr/bin/env python3
"""
Interactive Contract Risk Assessment Questionnaire
User-friendly interface for IT practitioners without legal background
"""

import sys
import os
from pathlib import Path
import json

# Add parent directory to path
sys.path.append(str(Path(__file__).parent.parent))

from risk_assessor import RiskAssessmentEngine
from template_generator import NegotiationTemplateGenerator
from report_generator import ReportGenerator


class InteractiveAssessment:
    """Interactive questionnaire for contract risk assessment."""

    def __init__(self):
        self.engine = RiskAssessmentEngine()
        self.template_gen = NegotiationTemplateGenerator()
        self.responses = {}

    def clear_screen(self):
        """Clear terminal screen."""
        os.system('clear' if os.name != 'nt' else 'cls')

    def print_header(self, title: str):
        """Print formatted section header."""
        print("\n" + "=" * 70)
        print(f"  {title}")
        print("=" * 70 + "\n")

    def print_section(self, title: str):
        """Print formatted subsection."""
        print(f"\n--- {title} ---\n")

    def get_input(self, prompt: str, valid_options: list = None) -> str:
        """Get user input with validation."""
        while True:
            response = input(f"{prompt}: ").strip()

            if valid_options:
                if response.lower() in [opt.lower() for opt in valid_options]:
                    return response
                else:
                    print(f"Invalid input. Please choose from: {', '.join(valid_options)}")
            else:
                if response:
                    return response
                else:
                    print("Please provide a response.")

    def run_assessment_questionnaire(self) -> dict:
        """Run the complete interactive assessment questionnaire."""

        self.clear_screen()
        self.print_header("AUTOMATED VENDOR CONTRACT RISK ASSESSMENT")

        print("Welcome! This tool helps IT practitioners evaluate vendor lock-in risks")
        print("in software contracts without requiring legal expertise.\n")

        print("We'll guide you through a series of questions about the vendor contract.")
        print("Based on your responses, we'll provide a risk score and recommendations.\n")

        input("Press Enter to begin...")

        # Section 1: Basic Information
        self.clear_screen()
        self.print_header("SECTION 1: Basic Information")

        self.responses['vendor_name'] = self.get_input("Vendor name")
        self.responses['software_type'] = self.get_input(
            "Software type (Cloud/SaaS/Enterprise)",
            ['Cloud', 'SaaS', 'Enterprise']
        )
        self.responses['contract_value'] = self.get_input("Annual contract value (USD)")
        self.responses['business_criticality'] = self.get_input(
            "How critical is this software? (Critical/Important/Nice-to-have)",
            ['Critical', 'Important', 'Nice-to-have']
        )

        # Section 2: Data Portability
        self.clear_screen()
        self.print_header("SECTION 2: Data Portability")

        print("Questions about your ability to export and migrate data:\n")

        self.responses['data_export'] = self.get_input(
            "Does the contract explicitly grant data export rights? (Yes/No/Unclear)",
            ['Yes', 'No', 'Unclear']
        )

        self.responses['data_format'] = self.get_input(
            "Are standard export formats (CSV/JSON/XML) mentioned? (Yes/No/Unclear)",
            ['Yes', 'No', 'Unclear']
        )

        self.responses['api_access'] = self.get_input(
            "Is API access for data export guaranteed? (Yes/No/Unclear)",
            ['Yes', 'No', 'Unclear']
        )

        self.responses['post_termination_access'] = self.get_input(
            "Can you retrieve data after termination? (Yes/No/Unclear)",
            ['Yes', 'No', 'Unclear']
        )

        # Section 3: Pricing Terms
        self.clear_screen()
        self.print_header("SECTION 3: Pricing Terms")

        print("Questions about pricing changes and increases:\n")

        self.responses['price_lock'] = self.get_input(
            "Is pricing locked for the contract term? (Yes/No/Unclear)",
            ['Yes', 'No', 'Unclear']
        )

        self.responses['price_increase'] = self.get_input(
            "Can vendor increase prices unilaterally? (Yes/No/Unclear)",
            ['Yes', 'No', 'Unclear']
        )

        if self.responses['price_increase'].lower() == 'yes':
            self.responses['price_increase_cap'] = self.get_input(
                "Is there a cap on price increases? (Yes/No/Unclear)",
                ['Yes', 'No', 'Unclear']
            )

            self.responses['price_notice'] = self.get_input(
                "How much advance notice for price changes? (days)"
            )

        # Section 4: Support Obligations
        self.clear_screen()
        self.print_header("SECTION 4: Support Obligations")

        print("Questions about vendor support commitments:\n")

        self.responses['support_sla'] = self.get_input(
            "Are support response times specified? (Yes/No/Unclear)",
            ['Yes', 'No', 'Unclear']
        )

        self.responses['support_hours'] = self.get_input(
            "Support availability (24x7/Business-hours/Best-effort)",
            ['24x7', 'Business-hours', 'Best-effort']
        )

        self.responses['feature_changes'] = self.get_input(
            "Can vendor discontinue features without notice? (Yes/No/Unclear)",
            ['Yes', 'No', 'Unclear']
        )

        # Section 5: Termination and Exit
        self.clear_screen()
        self.print_header("SECTION 5: Termination and Exit")

        print("Questions about ending the contract:\n")

        self.responses['termination_flexibility'] = self.get_input(
            "Can you terminate before contract end? (Yes/No/Only-for-cause)",
            ['Yes', 'No', 'Only-for-cause']
        )

        self.responses['termination_fee'] = self.get_input(
            "Are there early termination fees? (Yes/No/Unclear)",
            ['Yes', 'No', 'Unclear']
        )

        self.responses['auto_renewal'] = self.get_input(
            "Does contract auto-renew? (Yes/No/Unclear)",
            ['Yes', 'No', 'Unclear']
        )

        if self.responses['auto_renewal'].lower() == 'yes':
            self.responses['renewal_notice'] = self.get_input(
                "Notice period to prevent renewal (days)"
            )

        # Section 6: Service Level Agreements
        self.clear_screen()
        self.print_header("SECTION 6: Service Level Agreements")

        print("Questions about uptime and service guarantees:\n")

        self.responses['sla_exists'] = self.get_input(
            "Does contract include uptime SLA? (Yes/No/Unclear)",
            ['Yes', 'No', 'Unclear']
        )

        if self.responses['sla_exists'].lower() == 'yes':
            self.responses['uptime_percentage'] = self.get_input(
                "Guaranteed uptime percentage (e.g., 99.9)"
            )

            self.responses['sla_credits'] = self.get_input(
                "Are service credits provided for SLA failures? (Yes/No/Unclear)",
                ['Yes', 'No', 'Unclear']
            )

        self.responses['liability_cap'] = self.get_input(
            "Does vendor cap liability for outages? (Yes/No/Unclear)",
            ['Yes', 'No', 'Unclear']
        )

        # Calculate risk score
        self.clear_screen()
        self.print_header("CALCULATING RISK ASSESSMENT...")

        print("Analyzing your responses...\n")

        risk_analysis = self.calculate_risk_from_responses()

        return risk_analysis

    def calculate_risk_from_responses(self) -> dict:
        """Calculate risk score based on questionnaire responses."""

        # Initialize category scores
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
        if self.responses.get('data_export', '').lower() in ['no', 'unclear']:
            category_scores['data_portability'] += 5
        if self.responses.get('data_format', '').lower() in ['no', 'unclear']:
            category_scores['data_portability'] += 4
        if self.responses.get('api_access', '').lower() in ['no', 'unclear']:
            category_scores['data_portability'] += 3
        if self.responses.get('post_termination_access', '').lower() in ['no', 'unclear']:
            category_scores['data_portability'] += 3

        # Pricing Terms scoring
        if self.responses.get('price_lock', '').lower() in ['no', 'unclear']:
            category_scores['pricing_terms'] += 8
        if self.responses.get('price_increase', '').lower() == 'yes':
            category_scores['pricing_terms'] += 10
            if self.responses.get('price_increase_cap', '').lower() in ['no', 'unclear']:
                category_scores['pricing_terms'] += 5
            try:
                notice_days = int(self.responses.get('price_notice', '0'))
                if notice_days < 30:
                    category_scores['pricing_terms'] += 2
            except:
                pass

        # Support Obligations scoring
        if self.responses.get('support_sla', '').lower() in ['no', 'unclear']:
            category_scores['support_obligations'] += 6
        if self.responses.get('support_hours', '').lower() == 'best-effort':
            category_scores['support_obligations'] += 5
        if self.responses.get('feature_changes', '').lower() == 'yes':
            category_scores['support_obligations'] += 4

        # Termination/Exit scoring
        if self.responses.get('termination_flexibility', '').lower() in ['no', 'only-for-cause']:
            category_scores['termination_exit'] += 8
        if self.responses.get('termination_fee', '').lower() == 'yes':
            category_scores['termination_exit'] += 7
        if self.responses.get('auto_renewal', '').lower() == 'yes':
            try:
                renewal_notice = int(self.responses.get('renewal_notice', '0'))
                if renewal_notice > 60:
                    category_scores['termination_exit'] += 5
                elif renewal_notice > 30:
                    category_scores['termination_exit'] += 3
            except:
                category_scores['termination_exit'] += 4

        # Service Level scoring
        if self.responses.get('sla_exists', '').lower() in ['no', 'unclear']:
            category_scores['service_level'] += 15
        else:
            try:
                uptime = float(self.responses.get('uptime_percentage', '0'))
                if uptime < 99.0:
                    category_scores['service_level'] += 8
                elif uptime < 99.5:
                    category_scores['service_level'] += 5
                elif uptime < 99.9:
                    category_scores['service_level'] += 3
            except:
                category_scores['service_level'] += 10

            if self.responses.get('sla_credits', '').lower() in ['no', 'unclear']:
                category_scores['service_level'] += 5

        if self.responses.get('liability_cap', '').lower() == 'yes':
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

        return {
            'vendor_name': self.responses.get('vendor_name'),
            'total_score': round(total_score, 2),
            'risk_level': risk_level,
            'category_scores': category_scores,
            'max_points': max_points,
            'business_criticality': self.responses.get('business_criticality'),
            'questionnaire_responses': self.responses
        }

    def display_results(self, risk_analysis: dict):
        """Display assessment results to user."""

        self.clear_screen()
        self.print_header("RISK ASSESSMENT RESULTS")

        print(f"Vendor: {risk_analysis['vendor_name']}")
        print(f"Risk Score: {risk_analysis['total_score']}/100")
        print(f"Risk Level: {risk_analysis['risk_level']}")
        print(f"Business Criticality: {risk_analysis['business_criticality']}\n")

        # Risk interpretation
        if risk_analysis['risk_level'] == 'HIGH':
            print("⚠️  WARNING: HIGH RISK CONTRACT")
            print("This contract presents significant vendor lock-in risk.")
            print("Strong recommendation: Negotiate better terms or consider alternatives.\n")
        elif risk_analysis['risk_level'] == 'MEDIUM':
            print("⚡ MEDIUM RISK CONTRACT")
            print("This contract has moderate lock-in risk.")
            print("Recommendation: Negotiate improvements in high-risk areas.\n")
        else:
            print("✓ LOW RISK CONTRACT")
            print("This contract presents relatively low lock-in risk.")
            print("Recommendation: Review and address any remaining concerns.\n")

        # Category breakdown
        self.print_section("Risk by Category")

        for category, score in risk_analysis['category_scores'].items():
            max_score = risk_analysis['max_points'][category]
            percentage = (score / max_score * 100) if max_score > 0 else 0

            category_name = category.replace('_', ' ').title()
            bar_length = int(percentage / 5)
            bar = '█' * bar_length + '░' * (20 - bar_length)

            print(f"{category_name:.<30} {score}/{max_score} points  {bar} {percentage:.0f}%")

        print()

        # Top recommendations
        self.print_section("Top 5 Recommendations")

        recommendations = self.generate_quick_recommendations(risk_analysis)
        for idx, rec in enumerate(recommendations[:5], 1):
            print(f"{idx}. {rec}")

        print("\n" + "=" * 70)
        print("Full detailed report with negotiation templates available")
        print("=" * 70 + "\n")

    def generate_quick_recommendations(self, risk_analysis: dict) -> list:
        """Generate quick actionable recommendations."""

        recs = []

        # Data portability
        if risk_analysis['category_scores']['data_portability'] >= 8:
            recs.append("❗ Request explicit data export rights in standard formats (CSV/JSON)")

        # Pricing
        if risk_analysis['category_scores']['pricing_terms'] >= 15:
            recs.append("❗ Negotiate price lock or cap on annual increases (e.g., 5% max)")

        # Support
        if risk_analysis['category_scores']['support_obligations'] >= 8:
            recs.append("⚠️  Request written support SLA with response time commitments")

        # Termination
        if risk_analysis['category_scores']['termination_exit'] >= 12:
            recs.append("⚠️  Reduce early termination fees and auto-renewal notice period")

        # Service level
        if risk_analysis['category_scores']['service_level'] >= 15:
            recs.append("❗ Require uptime SLA (minimum 99.5%) with service credits")

        # Additional recommendations
        if len(recs) < 5:
            recs.append("📋 Document all verbal commitments in contract amendments")
            recs.append("🔍 Compare terms with alternative vendors before signing")
            recs.append("✅ Have legal counsel review negotiated changes")

        return recs

    def run_complete_assessment(self):
        """Run complete interactive assessment with report generation."""

        # Run questionnaire
        risk_analysis = self.run_assessment_questionnaire()

        # Display results
        self.display_results(risk_analysis)

        # Offer to generate full report
        generate_report = self.get_input(
            "\nGenerate full detailed report with negotiation templates? (Yes/No)",
            ['Yes', 'No']
        )

        if generate_report.lower() == 'yes':
            output_file = self.get_input(
                "Output filename (default: risk_report.html)",
            )
            if not output_file:
                output_file = "risk_report.html"

            print(f"\nGenerating comprehensive report...")

            # Generate and save report
            try:
                report_gen = ReportGenerator()
                report_gen.generate_html_report(risk_analysis, output_file)
                print(f"✓ Report saved to: {output_file}")
            except Exception as e:
                print(f"Error generating report: {e}")

        print("\nThank you for using the Automated Contract Risk Assessment Tool!")
        print("=" * 70 + "\n")


def main():
    """Main entry point for interactive assessment."""
    assessment = InteractiveAssessment()
    assessment.run_complete_assessment()


if __name__ == "__main__":
    main()
