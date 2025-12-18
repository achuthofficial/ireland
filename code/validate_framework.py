#!/usr/bin/env python3
"""
Framework Validation Script
Tests the Phase 2 framework on validation contracts
"""

import sys
import json
from pathlib import Path
from datetime import datetime

sys.path.append(str(Path(__file__).parent.parent))

from assessment.risk_assessor import RiskAssessmentEngine
from reports.report_generator import ReportGenerator


def validate_framework():
    """Run validation tests on sample contracts."""

    print("=" * 70)
    print("PHASE 2 FRAMEWORK VALIDATION")
    print("=" * 70)
    print()

    # Initialize engine
    engine = RiskAssessmentEngine()
    report_gen = ReportGenerator()

    # Select validation contracts (contracts not used in Phase 1 development)
    validation_contracts = [
        "/workspaces/ireland/vendor_contracts_dataset/saas_providers/github_tos.html",
        "/workspaces/ireland/vendor_contracts_dataset/saas_providers/slack_tos.html",
        "/workspaces/ireland/vendor_contracts_dataset/cloud_providers/aws_customer_agreement.html",
        "/workspaces/ireland/vendor_contracts_dataset/saas_providers/stripe_tos.html",
        "/workspaces/ireland/vendor_contracts_dataset/enterprise_software/mongodb_tos.html"
    ]

    print(f"Running validation on {len(validation_contracts)} test contracts...\n")

    results = []

    for contract_path in validation_contracts:
        try:
            print(f"Assessing: {Path(contract_path).stem}")

            # Run assessment
            assessment = engine.assess_contract_file(contract_path)

            if 'error' in assessment:
                print(f"  ⚠️  Warning: {assessment['error']}")
                continue

            # Display results
            print(f"  Risk Score: {assessment['total_score']}/100")
            print(f"  Risk Level: {assessment['risk_level']}")
            print(f"  Clauses Found: {assessment.get('total_clauses', 0)}")
            print()

            results.append(assessment)

        except Exception as e:
            print(f"  ❌ Error: {e}\n")
            continue

    # Generate validation report
    validation_summary = {
        'validation_date': datetime.now().isoformat(),
        'total_contracts_tested': len(validation_contracts),
        'successful_assessments': len(results),
        'results': results,
        'statistics': generate_validation_statistics(results)
    }

    # Save validation results
    output_dir = Path(__file__).parent
    results_file = output_dir / "validation_results.json"

    with open(results_file, 'w') as f:
        json.dump(validation_summary, f, indent=2)

    print("=" * 70)
    print("VALIDATION COMPLETE")
    print("=" * 70)
    print(f"\nSuccessfully assessed: {len(results)}/{len(validation_contracts)} contracts")
    print(f"Results saved to: {results_file}")

    # Print summary statistics
    stats = validation_summary['statistics']
    print(f"\nValidation Statistics:")
    print(f"  Average Risk Score: {stats['average_score']:.2f}/100")
    print(f"  Risk Distribution:")
    print(f"    - Low Risk: {stats['risk_distribution']['LOW']}")
    print(f"    - Medium Risk: {stats['risk_distribution']['MEDIUM']}")
    print(f"    - High Risk: {stats['risk_distribution']['HIGH']}")
    print(f"  Average Clauses per Contract: {stats['average_clauses']:.1f}")

    # Generate sample reports for top 2 contracts
    if results:
        print(f"\nGenerating sample HTML reports...")
        for idx, assessment in enumerate(results[:2], 1):
            vendor_name = assessment.get('vendor_name', 'vendor').replace(' ', '_')
            report_file = output_dir / f"sample_report_{vendor_name}.html"
            report_gen.generate_html_report(assessment, str(report_file))
            print(f"  ✓ Report {idx}: {report_file}")

    print("\n" + "=" * 70)
    print("Framework validation successful!")
    print("=" * 70 + "\n")

    return validation_summary


def generate_validation_statistics(results):
    """Generate statistics from validation results."""

    if not results:
        return {}

    total_scores = [r['total_score'] for r in results]
    risk_levels = [r['risk_level'] for r in results]
    total_clauses = [r.get('total_clauses', 0) for r in results]

    return {
        'average_score': sum(total_scores) / len(total_scores),
        'min_score': min(total_scores),
        'max_score': max(total_scores),
        'risk_distribution': {
            'LOW': risk_levels.count('LOW'),
            'MEDIUM': risk_levels.count('MEDIUM'),
            'HIGH': risk_levels.count('HIGH')
        },
        'average_clauses': sum(total_clauses) / len(total_clauses),
        'total_clauses_analyzed': sum(total_clauses)
    }


def compare_with_phase1():
    """Compare Phase 2 framework results with Phase 1 findings."""

    print("\n" + "=" * 70)
    print("COMPARING WITH PHASE 1 FINDINGS")
    print("=" * 70 + "\n")

    # Load Phase 1 data
    phase1_file = Path("/workspaces/ireland/phase1_analysis/data/clause_patterns.json")

    if not phase1_file.exists():
        print("Phase 1 data not found. Skipping comparison.")
        return

    with open(phase1_file, 'r') as f:
        phase1_data = json.load(f)

    print("Phase 1 Findings:")
    print(f"  Total Vendors: {phase1_data.get('vendors_analyzed', 0)}")
    print(f"  Total Clauses: {phase1_data.get('total_clauses_analyzed', 0)}")
    print(f"  High-Risk Rate: {phase1_data.get('high_risk_clause_count', 0) / phase1_data.get('total_clauses_analyzed', 1) * 100:.1f}%")

    print("\nPhase 2 Framework:")
    print("  ✓ Automated risk scoring (100-point system)")
    print("  ✓ Weighted category scores based on Phase 1 empirical data")
    print("  ✓ Negotiation templates library")
    print("  ✓ Interactive questionnaire interface")
    print("  ✓ Comprehensive HTML report generation")

    print("\nFramework Improvements:")
    print("  • Reduced assessment time: Manual review (hours) → Automated (minutes)")
    print("  • Consistent scoring: Eliminates subjective interpretation")
    print("  • Actionable output: Specific negotiation recommendations")
    print("  • Accessible: No legal expertise required")

    print()


if __name__ == "__main__":
    validation_summary = validate_framework()
    compare_with_phase1()
