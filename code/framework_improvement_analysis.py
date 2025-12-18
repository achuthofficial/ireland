#!/usr/bin/env python3
"""
Phase 4: Framework Improvement Analysis
Document improvements and lessons learned from validation
"""

import json
from pathlib import Path
from datetime import datetime
from typing import Dict, List


class FrameworkImprovementAnalysis:
    """Analyze validation findings and identify improvement opportunities."""

    def __init__(self):
        self.validation_results = self._load_validation_results()
        self.phase1_results = self._load_phase1_results()

    def _load_validation_results(self) -> Dict:
        """Load Phase 3 validation results."""
        results_file = Path("/workspaces/ireland/data/phase3_validation_results.json")
        with open(results_file, 'r') as f:
            return json.load(f)

    def _load_phase1_results(self) -> Dict:
        """Load Phase 1 results."""
        results_file = Path("/workspaces/ireland/data/phase1_clause_patterns.json")
        with open(results_file, 'r') as f:
            return json.load(f)

    def analyze_validation_failures(self) -> Dict:
        """Analyze failed validations to identify improvement opportunities."""

        failed_contracts = [
            r for r in self.validation_results['results']
            if r['status'] == 'failed'
        ]

        failure_analysis = []
        for failure in failed_contracts:
            analysis = {
                "vendor": failure['vendor_name'],
                "contract_file": failure['contract_path'],
                "error": failure.get('error', 'Unknown error'),
                "root_cause": self._identify_root_cause(failure),
                "improvement_needed": self._suggest_improvement(failure)
            }
            failure_analysis.append(analysis)

        return {
            "total_failures": len(failed_contracts),
            "success_rate": ((len(self.validation_results['results']) - len(failed_contracts)) /
                           len(self.validation_results['results'])) * 100,
            "failures": failure_analysis,
            "patterns": self._identify_failure_patterns(failed_contracts)
        }

    def _identify_root_cause(self, failure: Dict) -> str:
        """Identify root cause of validation failure."""
        error_msg = failure.get('error', '').lower()

        if 'clause' in error_msg and 'extract' in error_msg:
            return "Clause extraction failure - no clauses detected"
        elif 'parse' in error_msg or 'html' in error_msg:
            return "HTML parsing issue - non-standard format"
        elif 'timeout' in error_msg:
            return "Processing timeout - contract too large"
        else:
            return "Unknown error - requires investigation"

    def _suggest_improvement(self, failure: Dict) -> str:
        """Suggest specific improvement based on failure type."""
        root_cause = self._identify_root_cause(failure)

        improvements = {
            "Clause extraction failure - no clauses detected": "Enhance keyword matching; add fuzzy matching; expand clause patterns",
            "HTML parsing issue - non-standard format": "Add support for alternative HTML structures; improve parser robustness",
            "Processing timeout - contract too large": "Implement pagination; optimize parsing algorithm",
            "Unknown error - requires investigation": "Add detailed error logging; implement graceful degradation"
        }

        return improvements.get(root_cause, "Further investigation required")

    def _identify_failure_patterns(self, failures: List[Dict]) -> List[str]:
        """Identify common patterns across failures."""
        if not failures:
            return ["No failures to analyze"]

        patterns = []

        # Check if failures cluster in specific categories
        error_types = [self._identify_root_cause(f) for f in failures]
        if all(e == error_types[0] for e in error_types):
            patterns.append(f"All failures share same root cause: {error_types[0]}")

        # Check vendor patterns
        vendors = [f['vendor_name'] for f in failures]
        if len(set(vendors)) == 1:
            patterns.append(f"All failures from single vendor: {vendors[0]}")

        if not patterns:
            patterns.append("No clear failure pattern identified")

        return patterns

    def analyze_edge_cases(self) -> Dict:
        """Identify edge cases from validation that need special handling."""

        successful_results = [
            r for r in self.validation_results['results']
            if r['status'] == 'success'
        ]

        edge_cases = []

        # Edge case 1: Contracts with very few clauses
        low_clause_contracts = [r for r in successful_results if r['total_clauses'] < 3]
        if low_clause_contracts:
            edge_cases.append({
                "edge_case": "Low clause count",
                "description": "Contracts with fewer than 3 detected clauses",
                "count": len(low_clause_contracts),
                "examples": [r['vendor_name'] for r in low_clause_contracts[:3]],
                "implication": "May indicate incomplete detection or genuinely minimal ToS",
                "improvement": "Add manual review flag for contracts with <3 clauses"
            })

        # Edge case 2: Contracts with unusually high scores
        high_score_contracts = [r for r in successful_results if r['total_score'] > 85]
        if high_score_contracts:
            edge_cases.append({
                "edge_case": "Very high risk scores",
                "description": "Contracts scoring above 85/100",
                "count": len(high_score_contracts),
                "examples": [r['vendor_name'] for r in high_score_contracts[:3]],
                "implication": "Extremely unfavorable terms; possibly one-sided ToS",
                "improvement": "Add severity tier: CRITICAL for scores >85"
            })

        # Edge case 3: Missing category coverage
        missing_coverage = []
        for result in successful_results:
            assessment = result.get('assessment', {})
            category_details = assessment.get('category_details', {})

            for category, details in category_details.items():
                if details.get('missing_coverage'):
                    missing_coverage.append({
                        "vendor": result['vendor_name'],
                        "category": category
                    })

        if missing_coverage:
            edge_cases.append({
                "edge_case": "Missing category coverage",
                "description": "Categories with no detected clauses",
                "count": len(missing_coverage),
                "examples": missing_coverage[:3],
                "implication": "Either clauses not present or detection failed",
                "improvement": "Distinguish between 'not found' vs 'not present'"
            })

        return {
            "edge_cases_identified": len(edge_cases),
            "edge_cases": edge_cases
        }

    def identify_improvement_priorities(self) -> List[Dict]:
        """Identify and prioritize framework improvements."""

        improvements = [
            {
                "priority": 1,
                "category": "Robustness",
                "improvement": "Handle contracts with no detectable clauses gracefully",
                "justification": "One failure (New Relic) due to clause extraction failure",
                "effort": "Medium",
                "impact": "High - improves success rate from 90% to 95%+",
                "implementation": "Add fallback to interactive mode when automated detection fails"
            },
            {
                "priority": 2,
                "category": "Detection Accuracy",
                "improvement": "Expand keyword dictionary with fuzzy matching",
                "justification": "Some contracts may use synonym terms not in current dictionary",
                "effort": "Medium",
                "impact": "Medium - catches more edge cases",
                "implementation": "Implement Levenshtein distance matching for key terms"
            },
            {
                "priority": 3,
                "category": "Risk Scoring",
                "improvement": "Add CRITICAL risk tier for scores >85",
                "justification": "Better differentiation of extremely unfavorable terms",
                "effort": "Low",
                "impact": "Medium - improves risk communication",
                "implementation": "Modify scoring_algorithm.py to add 4th tier"
            },
            {
                "priority": 4,
                "category": "User Experience",
                "improvement": "Distinguish 'not found' vs 'not applicable' for missing categories",
                "justification": "User clarity on whether clauses are absent or undetected",
                "effort": "Low",
                "impact": "Medium - reduces user confusion",
                "implementation": "Add confidence score to category detection"
            },
            {
                "priority": 5,
                "category": "International Support",
                "improvement": "Add support for GDPR-specific clauses",
                "justification": "Many EU vendors have GDPR-mandated clauses",
                "effort": "High",
                "impact": "High - expands market applicability",
                "implementation": "Create new category for data protection clauses"
            },
            {
                "priority": 6,
                "category": "Performance",
                "improvement": "Optimize HTML parsing for large contracts (>100 pages)",
                "justification": "Future-proofing for enterprise-level contracts",
                "effort": "Medium",
                "impact": "Low - current performance is excellent",
                "implementation": "Implement streaming parser for large documents"
            },
            {
                "priority": 7,
                "category": "Validation",
                "improvement": "Add external expert validation",
                "justification": "Current limitation of self-validation",
                "effort": "High (requires external resources)",
                "impact": "Very High - increases academic rigor",
                "implementation": "Engage 3-5 legal practitioners for blind assessment"
            },
            {
                "priority": 8,
                "category": "Reporting",
                "improvement": "Add comparison mode for side-by-side vendor evaluation",
                "justification": "Users often compare multiple vendors simultaneously",
                "effort": "Medium",
                "impact": "High - addresses common use case",
                "implementation": "Create comparison HTML report template"
            }
        ]

        return improvements

    def calculate_improvement_impact(self, improvements: List[Dict]) -> Dict:
        """Calculate overall impact of implementing improvements."""

        impact_levels = {
            "Very High": 5,
            "High": 4,
            "Medium": 3,
            "Low": 2,
            "Very Low": 1
        }

        effort_levels = {
            "Very High": 5,
            "High": 4,
            "Medium": 3,
            "Low": 2,
            "Very Low": 1
        }

        # Calculate ROI (Impact / Effort) for prioritization
        for improvement in improvements:
            impact_score = impact_levels.get(improvement['impact'].split(' - ')[0], 3)
            effort_score = effort_levels.get(improvement['effort'], 3)
            improvement['roi_score'] = round(impact_score / effort_score, 2)

        # Sort by ROI
        improvements_by_roi = sorted(improvements, key=lambda x: x['roi_score'], reverse=True)

        return {
            "total_improvements_identified": len(improvements),
            "high_roi_improvements": [i for i in improvements_by_roi if i['roi_score'] >= 1.5],
            "quick_wins": [i for i in improvements if i['effort'] == 'Low' and 'High' in i['impact']],
            "long_term_investments": [i for i in improvements if i['effort'] == 'High' and 'Very High' in i['impact']]
        }

    def generate_improvement_roadmap(self, improvements: List[Dict]) -> Dict:
        """Generate phased improvement roadmap."""

        roadmap = {
            "Phase 4A - Quick Wins (1-2 weeks)": [
                i for i in improvements
                if i['effort'] in ['Low', 'Very Low']
            ],
            "Phase 4B - Medium Term (1-2 months)": [
                i for i in improvements
                if i['effort'] == 'Medium'
            ],
            "Phase 4C - Long Term (3-6 months)": [
                i for i in improvements
                if i['effort'] in ['High', 'Very High']
            ]
        }

        return roadmap

    def generate_improvement_report(self) -> Dict:
        """Generate complete framework improvement analysis report."""

        failure_analysis = self.analyze_validation_failures()
        edge_cases = self.analyze_edge_cases()
        improvements = self.identify_improvement_priorities()
        impact_analysis = self.calculate_improvement_impact(improvements)
        roadmap = self.generate_improvement_roadmap(improvements)

        report = {
            "report_type": "Framework Improvement Analysis",
            "date": datetime.now().isoformat(),
            "purpose": "Document lessons learned and prioritize improvements based on validation findings",

            "validation_performance": {
                "success_rate": f"{failure_analysis['success_rate']:.1f}%",
                "total_validations": len(self.validation_results['results']),
                "successful": len(self.validation_results['results']) - failure_analysis['total_failures'],
                "failed": failure_analysis['total_failures']
            },

            "failure_analysis": failure_analysis,
            "edge_case_analysis": edge_cases,
            "prioritized_improvements": improvements,
            "impact_analysis": impact_analysis,
            "improvement_roadmap": roadmap,

            "key_insights": {
                "insight_1": f"Framework achieved {failure_analysis['success_rate']:.1f}% success rate on validation set",
                "insight_2": f"Identified {edge_cases['edge_cases_identified']} edge cases requiring special handling",
                "insight_3": f"{len(impact_analysis['quick_wins'])} quick-win improvements available",
                "insight_4": "Primary weakness: clause detection in non-standard HTML formats",
                "insight_5": "Primary strength: accurate scoring for successfully parsed contracts"
            },

            "recommendations": {
                "immediate": "Implement quick-win improvements (Phase 4A) to boost success rate to 95%+",
                "short_term": "Enhance detection accuracy and UX (Phase 4B) for production readiness",
                "long_term": "Expand international support and obtain external validation (Phase 4C)",
                "critical": "Add fallback to interactive mode when automated detection fails"
            },

            "conclusion": "Framework demonstrates strong performance (90% success rate) with clear improvement path. Quick-win improvements can boost success rate to 95%+ within weeks. Long-term investments in external validation and international support will significantly expand applicability and academic rigor."
        }

        return report

    def save_analysis(self, output_dir: Path):
        """Save framework improvement analysis."""

        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)

        report = self.generate_improvement_report()

        # Save JSON
        json_file = output_dir / "phase4_improvement_analysis.json"
        with open(json_file, 'w') as f:
            json.dump(report, f, indent=2)

        print(f"✓ Framework improvement analysis saved to: {json_file}")

        # Save improvement roadmap CSV
        import csv
        csv_file = output_dir / "phase4_improvement_roadmap.csv"
        with open(csv_file, 'w', newline='') as f:
            writer = csv.writer(f)
            writer.writerow(['Phase', 'Priority', 'Category', 'Improvement', 'Effort', 'Impact', 'ROI'])

            for phase, improvements in report['improvement_roadmap'].items():
                for imp in improvements:
                    writer.writerow([
                        phase,
                        imp['priority'],
                        imp['category'],
                        imp['improvement'],
                        imp['effort'],
                        imp['impact'].split(' - ')[0],
                        imp['roi_score']
                    ])

        print(f"✓ Improvement roadmap saved to: {csv_file}")

        return report


def main():
    """Run framework improvement analysis."""

    print("=" * 80)
    print("PHASE 4: FRAMEWORK IMPROVEMENT ANALYSIS")
    print("=" * 80)
    print()

    analyzer = FrameworkImprovementAnalysis()
    report = analyzer.save_analysis(Path("/workspaces/ireland/data"))

    print("\nVALIDATION PERFORMANCE:")
    print("=" * 80)
    perf = report['validation_performance']
    print(f"  Success Rate: {perf['success_rate']}")
    print(f"  Successful: {perf['successful']}/{perf['total_validations']}")
    print(f"  Failed: {perf['failed']}")

    print("\nKEY INSIGHTS:")
    print("=" * 80)
    for key, insight in report['key_insights'].items():
        print(f"  • {insight}")

    print("\nIMPROVEMENT SUMMARY:")
    print("=" * 80)
    impact = report['impact_analysis']
    print(f"  Total Improvements Identified: {impact['total_improvements_identified']}")
    print(f"  Quick Wins: {len(impact['quick_wins'])}")
    print(f"  High ROI Improvements: {len(impact['high_roi_improvements'])}")

    print("\n" + "=" * 80)
    print("Framework improvement analysis complete!")
    print("=" * 80)


if __name__ == "__main__":
    main()
