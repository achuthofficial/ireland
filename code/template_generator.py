#!/usr/bin/env python3
"""
Negotiation Template Generator
Provides recommended language and negotiation strategies based on risk assessment.
"""

import json
from pathlib import Path
from typing import Dict, List


class NegotiationTemplateGenerator:
    """Generate negotiation recommendations based on contract assessment."""

    def __init__(self):
        # Load templates
        template_path = Path(__file__).parent / "negotiation_templates.json"
        with open(template_path, 'r') as f:
            self.templates = json.load(f)

    def generate_recommendations(self, assessment: Dict) -> Dict:
        """
        Generate negotiation recommendations based on risk assessment.

        Args:
            assessment: Risk assessment dictionary from RiskAssessmentEngine

        Returns:
            Dictionary with prioritized recommendations and templates
        """
        recommendations = {
            'vendor_name': assessment.get('vendor_name'),
            'risk_score': assessment.get('total_score'),
            'risk_level': assessment.get('risk_level'),
            'priority_issues': [],
            'recommended_changes': [],
            'negotiation_strategy': [],
            'template_language': {}
        }

        # Analyze critical issues
        critical_issues = assessment.get('critical_issues', [])
        category_details = assessment.get('category_details', {})

        # Generate recommendations by category
        for category, details in category_details.items():
            if category not in self.templates:
                continue

            category_templates = self.templates[category]['templates']

            # High-risk categories get priority
            if details.get('high_risk_percentage', 0) >= 60 or details.get('missing_coverage'):
                priority = 'HIGH'
            elif details.get('score', 0) >= details.get('max_points', 100) * 0.5:
                priority = 'MEDIUM'
            else:
                priority = 'LOW'

            # Add category recommendations
            for template in category_templates:
                if template['priority'] == 'HIGH' and priority in ['HIGH', 'MEDIUM']:
                    recommendations['priority_issues'].append({
                        'category': category,
                        'issue': template['issue'],
                        'priority': priority,
                        'negotiation_points': template['negotiation_points']
                    })

                    recommendations['template_language'][f"{category}_{template['issue']}"] = {
                        'problematic': template['problematic_language'],
                        'recommended': template['recommended_language']
                    }

        # Add general strategies
        if assessment.get('risk_level') == 'HIGH':
            recommendations['negotiation_strategy'] = [
                "CRITICAL: This contract presents significant lock-in risk. Strongly consider alternative vendors or extensive negotiation.",
                "Prepare to walk away if critical issues cannot be resolved.",
                "Focus on the top 3-5 highest priority issues first.",
                "Request executive-level review on vendor side."
            ]
        elif assessment.get('risk_level') == 'MEDIUM':
            recommendations['negotiation_strategy'] = [
                "This contract has moderate risk. Negotiation is recommended to improve terms.",
                "Focus on high-risk categories identified in the assessment.",
                "Use comparison data from other vendors as leverage.",
                "Consider requesting shorter initial term with option to renew."
            ]
        else:
            recommendations['negotiation_strategy'] = [
                "This contract presents relatively low risk overall.",
                "Review and negotiate any remaining high-risk clauses.",
                "Ensure all negotiated terms are reflected in final contract.",
                "Consider requesting additional service level commitments."
            ]

        # Add general strategies from templates
        general_strategies = self.templates.get('general_negotiation_strategies', {}).get('strategies', [])
        recommendations['general_strategies'] = [
            f"{s['strategy']}: {s['guidance']}" for s in general_strategies
        ]

        return recommendations

    def generate_redline_document(self, recommendations: Dict) -> str:
        """
        Generate a redline document with proposed contract changes.

        Args:
            recommendations: Recommendations dictionary

        Returns:
            Formatted markdown redline document
        """
        doc = f"""# CONTRACT REDLINE RECOMMENDATIONS

**Vendor**: {recommendations['vendor_name']}
**Risk Score**: {recommendations['risk_score']}/100
**Risk Level**: {recommendations['risk_level']}

---

## EXECUTIVE SUMMARY

This document provides recommended contract modifications to reduce vendor lock-in risk and improve terms. Issues are prioritized based on business impact.

**Total Priority Issues Identified**: {len(recommendations['priority_issues'])}

---

## PRIORITY ISSUES AND RECOMMENDED CHANGES

"""

        # Group by priority
        high_priority = [i for i in recommendations['priority_issues'] if i['priority'] == 'HIGH']
        medium_priority = [i for i in recommendations['priority_issues'] if i['priority'] == 'MEDIUM']

        if high_priority:
            doc += "### HIGH PRIORITY (Must Address)\n\n"
            for idx, issue in enumerate(high_priority, 1):
                doc += f"#### {idx}. {issue['issue']} ({issue['category'].replace('_', ' ').title()})\n\n"
                doc += "**Negotiation Points**:\n"
                for point in issue['negotiation_points'][:5]:
                    doc += f"- {point}\n"
                doc += "\n"

                # Add template language if available
                template_key = f"{issue['category']}_{issue['issue']}"
                if template_key in recommendations['template_language']:
                    template = recommendations['template_language'][template_key]
                    doc += "**Current Problematic Language**:\n"
                    doc += f"> {template['problematic']}\n\n"
                    doc += "**Recommended Language**:\n"
                    doc += f"> {template['recommended']}\n\n"
                doc += "---\n\n"

        if medium_priority:
            doc += "### MEDIUM PRIORITY (Should Address)\n\n"
            for idx, issue in enumerate(medium_priority, 1):
                doc += f"#### {idx}. {issue['issue']} ({issue['category'].replace('_', ' ').title()})\n\n"
                doc += "**Key Negotiation Points**:\n"
                for point in issue['negotiation_points'][:3]:
                    doc += f"- {point}\n"
                doc += "\n---\n\n"

        # Add negotiation strategy
        doc += "## NEGOTIATION STRATEGY\n\n"
        for strategy in recommendations['negotiation_strategy']:
            doc += f"- {strategy}\n"

        doc += "\n---\n\n"

        # Add general guidance
        doc += "## GENERAL GUIDANCE\n\n"
        for guidance in recommendations.get('general_strategies', [])[:5]:
            doc += f"- {guidance}\n"

        doc += "\n---\n\n"
        doc += "*This redline document was generated by the Automated Vendor Contract Risk Assessment Tool*\n"

        return doc

    def get_category_templates(self, category: str) -> List[Dict]:
        """Get all templates for a specific category."""
        if category in self.templates:
            return self.templates[category].get('templates', [])
        return []

    def get_template_for_issue(self, category: str, issue: str) -> Dict:
        """Get a specific template by category and issue."""
        templates = self.get_category_templates(category)
        for template in templates:
            if template['issue'].lower() == issue.lower():
                return template
        return {}


def main():
    """Example usage."""
    generator = NegotiationTemplateGenerator()

    # Example assessment
    example_assessment = {
        'vendor_name': 'Example Vendor',
        'total_score': 72.5,
        'risk_level': 'HIGH',
        'category_details': {
            'service_level': {
                'score': 20,
                'max_points': 25,
                'high_risk_percentage': 80,
                'clause_count': 5
            },
            'pricing_terms': {
                'score': 18,
                'max_points': 25,
                'high_risk_percentage': 70,
                'clause_count': 4
            }
        },
        'critical_issues': [
            {'category': 'service_level', 'severity': 'HIGH', 'issue': 'No SLA provisions'},
            {'category': 'pricing_terms', 'severity': 'HIGH', 'issue': 'Unilateral price increases'}
        ]
    }

    recommendations = generator.generate_recommendations(example_assessment)
    redline_doc = generator.generate_redline_document(recommendations)

    print(redline_doc)


if __name__ == "__main__":
    main()
