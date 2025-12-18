#!/usr/bin/env python3
"""
Phase 2: Automated Risk Assessment Engine
Automated Vendor Contract Risk Assessment Tool

This module provides automated contract analysis and risk assessment.
"""

import sys
import os
from pathlib import Path
from bs4 import BeautifulSoup
import csv
import json
from typing import Dict, List, Tuple

# Import scoring algorithm from same directory
from scoring_algorithm import ContractScorer


class ContractAnalyzer:
    """Automated contract analysis and clause extraction."""

    # Clause detection rules based on Phase 1 validated patterns
    CLAUSE_CATEGORIES = {
        "data_portability": {
            "keywords": [
                "data export", "data portability", "data migration", "export data",
                "data transfer", "download data", "retrieve data", "data extraction",
                "data backup", "api access", "bulk export", "data ownership",
                "portable format", "standard format", "data retrieval"
            ],
            "negative_keywords": [
                "no obligation to provide", "may not export", "cannot export",
                "prohibit export", "restrict export", "no portability",
                "proprietary format only", "no api access", "limited export"
            ],
            "required_phrases": [
                "export", "portability", "migration", "api", "retrieval"
            ]
        },
        "pricing_terms": {
            "keywords": [
                "pricing", "fees", "payment", "cost", "subscription", "charges",
                "price increase", "rate change", "fee change", "pricing change",
                "billing", "invoice", "payment terms", "price adjustment",
                "renewal fee", "price lock", "pricing guarantee", "price modification"
            ],
            "negative_keywords": [
                "increase prices", "raise fees", "modify pricing", "change fees",
                "at our discretion", "sole discretion", "without notice",
                "unilateral", "at any time", "right to change", "may increase"
            ],
            "required_phrases": [
                "pric", "fee", "cost", "payment", "subscription"
            ]
        },
        "support_obligations": {
            "keywords": [
                "support", "technical support", "customer support", "assistance",
                "help desk", "support hours", "support availability", "support level",
                "maintenance", "updates", "patches", "bug fixes", "response time",
                "support tier", "support plan", "customer service", "service availability"
            ],
            "negative_keywords": [
                "no support", "no obligation to support", "may discontinue support",
                "at our discretion", "no guarantee", "best effort", "as is",
                "no commitment", "may suspend", "right to discontinue"
            ],
            "required_phrases": [
                "support", "maintenance", "assistance", "service"
            ]
        },
        "termination_exit": {
            "keywords": [
                "termination", "terminate", "cancel", "cancellation", "exit",
                "end of term", "contract end", "notice period", "termination fee",
                "early termination", "wind down", "transition", "off-boarding",
                "data deletion", "account closure", "suspension", "renewal"
            ],
            "negative_keywords": [
                "termination fee", "penalty", "early termination fee", "cannot terminate",
                "must continue", "auto-renew", "automatic renewal", "no refund",
                "immediately delete", "forfeit", "early cancellation fee"
            ],
            "required_phrases": [
                "terminat", "cancel", "exit", "renewal", "end"
            ]
        },
        "service_level": {
            "keywords": [
                "sla", "service level", "uptime", "availability", "performance",
                "guarantee", "commitment", "downtime", "credits", "compensation",
                "reliability", "service credit", "remedies", "service performance",
                "service guarantee", "warranty", "service quality"
            ],
            "negative_keywords": [
                "no sla", "no guarantee", "best effort", "as is", "no warranty",
                "sole remedy", "exclusive remedy", "no liability", "no compensation",
                "service credits only", "as available", "without warranty"
            ],
            "required_phrases": [
                "sla", "uptime", "availability", "guarantee", "service level"
            ]
        }
    }

    # Lock-in mechanism detection patterns
    LOCK_IN_PATTERNS = {
        "data_portability": {
            "data_restriction": ["proprietary format", "no export", "cannot export", "restrict"],
            "no_api_access": ["no api", "limited api", "no programmatic access"],
            "export_restriction": ["export restriction", "limited export", "no bulk export"]
        },
        "pricing_terms": {
            "price_increase_risk": ["increase", "raise", "adjust", "modify"],
            "unilateral_pricing": ["sole discretion", "unilateral", "at our discretion", "right to change"],
            "no_notice_changes": ["without notice", "immediate effect", "no advance notice"],
            "automatic_renewal": ["auto-renew", "automatic renewal", "automatically renew"]
        },
        "support_obligations": {
            "no_support_guarantee": ["no support", "no obligation", "no guarantee"],
            "discontinuation_risk": ["may discontinue", "right to discontinue", "suspend"],
            "no_commitment": ["best effort", "no commitment", "as is"]
        },
        "termination_exit": {
            "exit_fees": ["termination fee", "early termination", "cancellation fee"],
            "cancellation_penalty": ["penalty", "forfeit", "early cancellation"],
            "automatic_renewal": ["auto-renew", "automatic renewal", "automatically renew"]
        },
        "service_level": {
            "no_sla": ["no sla", "no service level"],
            "no_compensation": ["no compensation", "no liability", "sole remedy"],
            "no_guarantee": ["no guarantee", "best effort", "as is", "without warranty"],
            "limited_remedies": ["sole remedy", "exclusive remedy", "only remedy", "service credits only"]
        }
    }

    def __init__(self):
        self.clause_categories = self.CLAUSE_CATEGORIES
        self.lock_in_patterns = self.LOCK_IN_PATTERNS

    def extract_text_from_html(self, file_path: str) -> str:
        """Extract clean text from HTML contract file."""
        try:
            with open(file_path, 'r', encoding='utf-8', errors='ignore') as f:
                soup = BeautifulSoup(f.read(), 'html.parser')

                # Remove script and style elements
                for script in soup(["script", "style", "nav", "footer", "header"]):
                    script.decompose()

                text = soup.get_text()
                lines = (line.strip() for line in text.splitlines())
                chunks = (phrase.strip() for line in lines for phrase in line.split("  "))
                text = ' '.join(chunk for chunk in chunks if chunk)

                return text
        except Exception as e:
            print(f"Error reading {file_path}: {e}")
            return ""

    def find_clauses(self, text: str, vendor_name: str, file_name: str) -> List[Dict]:
        """Find and categorize clauses in contract text."""
        clauses = []
        clause_id = 0

        # Split into meaningful sections
        sections = self._split_into_sections(text)

        for category, config in self.clause_categories.items():
            for section in sections:
                if len(section) < 100:  # Skip very short sections
                    continue

                section_lower = section.lower()

                # Check for required phrases (at least one must be present)
                has_required = any(phrase in section_lower for phrase in config['required_phrases'])
                if not has_required:
                    continue

                # Count keyword matches
                keyword_matches = sum(1 for kw in config['keywords'] if kw in section_lower)

                if keyword_matches >= 2:  # Require at least 2 keyword matches
                    clause_id += 1

                    # Determine risk level
                    has_negative = any(nkw in section_lower for nkw in config['negative_keywords'])
                    risk_level = "High" if has_negative else "Medium"

                    # Identify specific lock-in mechanism
                    lock_in_type = self._identify_lock_in_mechanism(section_lower, category)

                    clauses.append({
                        'clause_id': f"{vendor_name}_{clause_id}",
                        'vendor_name': vendor_name,
                        'contract_file': file_name,
                        'clause_category': category,
                        'clause_text': section[:500],  # Limit length
                        'risk_level': risk_level,
                        'lock_in_mechanism': lock_in_type,
                        'keyword_matches': keyword_matches
                    })

        return clauses

    def _split_into_sections(self, text: str) -> List[str]:
        """Split text into meaningful sections for analysis."""
        # Split by common section markers
        import re

        # Try to split by numbered sections, headings, or double newlines
        sections = re.split(r'\n\n+|\n[0-9]+\.|\n[A-Z][A-Z\s]+\n', text)

        # Filter out very short sections
        sections = [s.strip() for s in sections if len(s.strip()) > 100]

        # If we don't have good sections, split by paragraphs
        if len(sections) < 5:
            sections = [p for p in text.split('\n') if len(p) > 100]

        return sections

    def _identify_lock_in_mechanism(self, text: str, category: str) -> str:
        """Identify specific lock-in mechanisms in text."""
        if category not in self.lock_in_patterns:
            return "standard"

        for mechanism, patterns in self.lock_in_patterns[category].items():
            for pattern in patterns:
                if pattern in text:
                    return mechanism

        return "standard"

    def analyze_contract_file(self, file_path: str) -> List[Dict]:
        """Analyze a single contract file and extract clauses."""
        vendor_name = Path(file_path).stem.replace('_tos', '').replace('_terms', '').replace('_', ' ').title()
        file_name = Path(file_path).name

        print(f"Analyzing: {vendor_name}")

        text = self.extract_text_from_html(file_path)

        if not text or len(text) < 1000:
            print(f"  Warning: Contract too short or empty ({len(text)} chars)")
            return []

        clauses = self.find_clauses(text, vendor_name, file_name)
        print(f"  Found {len(clauses)} clauses")

        return clauses


class RiskAssessmentEngine:
    """Complete automated risk assessment system."""

    def __init__(self):
        self.analyzer = ContractAnalyzer()
        self.scorer = ContractScorer()

    def assess_contract_file(self, file_path: str) -> Dict:
        """
        Perform complete risk assessment on a contract file.

        Args:
            file_path: Path to contract HTML file

        Returns:
            Complete risk assessment report
        """
        # Extract clauses
        clauses = self.analyzer.analyze_contract_file(file_path)

        if not clauses:
            return {
                'error': 'No clauses could be extracted from contract',
                'file_path': file_path,
                'vendor_name': Path(file_path).stem
            }

        # Score the contract
        assessment = self.scorer.score_contract(clauses)

        # Add metadata
        assessment['vendor_name'] = clauses[0]['vendor_name']
        assessment['contract_file'] = Path(file_path).name
        assessment['total_clauses'] = len(clauses)
        assessment['clauses'] = clauses

        return assessment

    def assess_multiple_contracts(self, contract_files: List[str]) -> List[Dict]:
        """
        Assess multiple contracts.

        Args:
            contract_files: List of contract file paths

        Returns:
            List of assessment reports
        """
        assessments = []

        print(f"\n{'=' * 60}")
        print("AUTOMATED RISK ASSESSMENT")
        print(f"{'=' * 60}\n")

        for file_path in contract_files:
            try:
                assessment = self.assess_contract_file(file_path)
                assessments.append(assessment)
            except Exception as e:
                print(f"Error assessing {file_path}: {e}")

        return assessments

    def generate_comparison_report(self, assessments: List[Dict]) -> Dict:
        """Generate comparative analysis across multiple vendors."""

        if not assessments:
            return {}

        valid_assessments = [a for a in assessments if 'error' not in a]

        comparison = {
            'total_vendors': len(valid_assessments),
            'average_score': sum(a['total_score'] for a in valid_assessments) / len(valid_assessments) if valid_assessments else 0,
            'risk_distribution': {
                'LOW': len([a for a in valid_assessments if a['risk_level'] == 'LOW']),
                'MEDIUM': len([a for a in valid_assessments if a['risk_level'] == 'MEDIUM']),
                'HIGH': len([a for a in valid_assessments if a['risk_level'] == 'HIGH'])
            },
            'best_vendors': sorted(valid_assessments, key=lambda x: x['total_score'])[:5],
            'worst_vendors': sorted(valid_assessments, key=lambda x: x['total_score'], reverse=True)[:5],
            'category_averages': self._calculate_category_averages(valid_assessments)
        }

        return comparison

    def _calculate_category_averages(self, assessments: List[Dict]) -> Dict:
        """Calculate average scores by category across vendors."""
        from collections import defaultdict

        category_totals = defaultdict(list)

        for assessment in assessments:
            for category, score in assessment.get('category_scores', {}).items():
                category_totals[category].append(score)

        return {
            category: round(sum(scores) / len(scores), 2)
            for category, scores in category_totals.items()
        }


def main():
    """Main assessment function."""
    import argparse

    parser = argparse.ArgumentParser(description='Automated Contract Risk Assessment')
    parser.add_argument('--file', type=str, help='Single contract file to assess')
    parser.add_argument('--directory', type=str, help='Directory of contracts to assess')
    parser.add_argument('--output', type=str, default='assessment_report.json', help='Output file path')

    args = parser.parse_args()

    engine = RiskAssessmentEngine()

    if args.file:
        # Assess single file
        assessment = engine.assess_contract_file(args.file)

        # Save report
        with open(args.output, 'w') as f:
            json.dump(assessment, f, indent=2)

        print(f"\nAssessment saved to: {args.output}")
        print(f"Risk Score: {assessment.get('total_score', 'N/A')}/100")
        print(f"Risk Level: {assessment.get('risk_level', 'N/A')}")

    elif args.directory:
        # Assess all contracts in directory
        contract_files = list(Path(args.directory).glob("*.html"))
        assessments = engine.assess_multiple_contracts(contract_files)

        # Generate comparison
        comparison = engine.generate_comparison_report(assessments)

        report = {
            'individual_assessments': assessments,
            'comparative_analysis': comparison
        }

        # Save report
        with open(args.output, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"\n{'=' * 60}")
        print(f"Assessment complete!")
        print(f"  Vendors assessed: {len(assessments)}")
        print(f"  Average risk score: {comparison.get('average_score', 0):.2f}/100")
        print(f"  Report saved to: {args.output}")
        print(f"{'=' * 60}")


if __name__ == "__main__":
    main()
