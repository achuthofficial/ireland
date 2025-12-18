#!/usr/bin/env python3
"""
Phase 3: Extended Validation Testing
Tests framework on 10+ reserved validation contracts
"""

import sys
import json
from pathlib import Path
from datetime import datetime
import csv

sys.path.append(str(Path(__file__).parent.parent.parent / "phase2_framework"))

from risk_assessor import RiskAssessmentEngine
from report_generator import ReportGenerator


class ExtendedValidation:
    """Extended validation testing on reserved contracts."""

    def __init__(self):
        self.engine = RiskAssessmentEngine()
        self.report_gen = ReportGenerator()
        self.results = []

    def select_validation_contracts(self):
        """Select 10 contracts for validation from downloaded contracts."""
        import random

        contracts_dir = Path("/workspaces/ireland/contracts")
        all_contracts = list(contracts_dir.glob("*.html"))

        # Select 10 random contracts for validation
        validation_contracts = random.sample(all_contracts, min(10, len(all_contracts)))

        return [str(c) for c in validation_contracts]

    def run_validation(self):
        """Run validation on all selected contracts."""

        print("=" * 80)
        print("PHASE 3: EXTENDED VALIDATION TESTING")
        print("=" * 80)
        print()

        contracts = self.select_validation_contracts()

        print(f"Testing framework on {len(contracts)} validation contracts...\n")

        successful = 0
        failed = 0

        for idx, contract_path in enumerate(contracts, 1):
            try:
                vendor_name = Path(contract_path).stem
                print(f"[{idx}/{len(contracts)}] Assessing: {vendor_name}")

                # Run assessment
                assessment = self.engine.assess_contract_file(contract_path)

                if 'error' in assessment:
                    print(f"  ⚠️  Warning: {assessment['error']}")
                    failed += 1
                    self.results.append({
                        'contract_path': contract_path,
                        'vendor_name': vendor_name,
                        'status': 'failed',
                        'error': assessment['error']
                    })
                    print()
                    continue

                # Display results
                print(f"  ✓ Risk Score: {assessment['total_score']}/100")
                print(f"  ✓ Risk Level: {assessment['risk_level']}")
                print(f"  ✓ Clauses: {assessment.get('total_clauses', 0)}")
                print()

                successful += 1
                self.results.append({
                    'contract_path': contract_path,
                    'vendor_name': assessment.get('vendor_name'),
                    'status': 'success',
                    'total_score': assessment['total_score'],
                    'risk_level': assessment['risk_level'],
                    'total_clauses': assessment.get('total_clauses', 0),
                    'category_scores': assessment.get('category_scores', {}),
                    'critical_issues': len(assessment.get('critical_issues', [])),
                    'assessment': assessment
                })

            except Exception as e:
                print(f"  ❌ Error: {e}\n")
                failed += 1
                self.results.append({
                    'contract_path': contract_path,
                    'vendor_name': Path(contract_path).stem,
                    'status': 'error',
                    'error': str(e)
                })

        print("=" * 80)
        print("VALIDATION COMPLETE")
        print("=" * 80)
        print(f"\nSuccessful: {successful}/{len(contracts)} ({successful/len(contracts)*100:.1f}%)")
        print(f"Failed: {failed}/{len(contracts)}")

        return self.results

    def generate_validation_statistics(self):
        """Generate comprehensive validation statistics."""

        successful_results = [r for r in self.results if r['status'] == 'success']

        if not successful_results:
            return {}

        scores = [r['total_score'] for r in successful_results]
        clauses = [r['total_clauses'] for r in successful_results]

        # Risk level distribution
        risk_distribution = {
            'LOW': sum(1 for r in successful_results if r['risk_level'] == 'LOW'),
            'MEDIUM': sum(1 for r in successful_results if r['risk_level'] == 'MEDIUM'),
            'HIGH': sum(1 for r in successful_results if r['risk_level'] == 'HIGH')
        }

        # Category statistics
        category_stats = {}
        for category in ['service_level', 'pricing_terms', 'termination_exit', 'data_portability', 'support_obligations']:
            category_scores = [r['category_scores'].get(category, 0) for r in successful_results if 'category_scores' in r]
            if category_scores:
                category_stats[category] = {
                    'mean': sum(category_scores) / len(category_scores),
                    'min': min(category_scores),
                    'max': max(category_scores),
                    'std_dev': self._calculate_std_dev(category_scores)
                }

        stats = {
            'total_contracts_tested': len(self.results),
            'successful_assessments': len(successful_results),
            'failed_assessments': len(self.results) - len(successful_results),
            'success_rate': len(successful_results) / len(self.results) * 100,

            'risk_scores': {
                'mean': sum(scores) / len(scores),
                'median': sorted(scores)[len(scores)//2],
                'min': min(scores),
                'max': max(scores),
                'std_dev': self._calculate_std_dev(scores)
            },

            'risk_distribution': risk_distribution,
            'risk_percentages': {
                'low': risk_distribution['LOW'] / len(successful_results) * 100,
                'medium': risk_distribution['MEDIUM'] / len(successful_results) * 100,
                'high': risk_distribution['HIGH'] / len(successful_results) * 100
            },

            'clause_statistics': {
                'mean': sum(clauses) / len(clauses),
                'min': min(clauses),
                'max': max(clauses),
                'total': sum(clauses)
            },

            'category_statistics': category_stats,

            'critical_issues': {
                'mean': sum(r['critical_issues'] for r in successful_results) / len(successful_results),
                'total': sum(r['critical_issues'] for r in successful_results)
            }
        }

        return stats

    def _calculate_std_dev(self, values):
        """Calculate standard deviation."""
        if len(values) < 2:
            return 0
        mean = sum(values) / len(values)
        variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
        return variance ** 0.5

    def save_results(self, output_dir):
        """Save validation results."""

        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        # Save detailed results
        results_file = output_path / "validation_results.json"
        with open(results_file, 'w') as f:
            json.dump({
                'validation_date': datetime.now().isoformat(),
                'results': self.results,
                'statistics': self.generate_validation_statistics()
            }, f, indent=2)

        print(f"\n✓ Results saved to: {results_file}")

        # Save CSV summary
        csv_file = output_path / "validation_summary.csv"
        successful_results = [r for r in self.results if r['status'] == 'success']

        with open(csv_file, 'w', newline='') as f:
            if successful_results:
                writer = csv.DictWriter(f, fieldnames=[
                    'vendor_name', 'total_score', 'risk_level', 'total_clauses', 'critical_issues'
                ])
                writer.writeheader()
                for r in successful_results:
                    writer.writerow({
                        'vendor_name': r['vendor_name'],
                        'total_score': r['total_score'],
                        'risk_level': r['risk_level'],
                        'total_clauses': r['total_clauses'],
                        'critical_issues': r['critical_issues']
                    })

        print(f"✓ CSV summary saved to: {csv_file}")

        # Generate sample reports for top 3
        print(f"\nGenerating sample HTML reports...")
        for idx, result in enumerate(successful_results[:3], 1):
            if result['status'] == 'success':
                vendor_name = result['vendor_name'].replace(' ', '_')
                report_file = output_path / f"validation_report_{vendor_name}.html"
                self.report_gen.generate_html_report(result['assessment'], str(report_file))
                print(f"  ✓ Report {idx}: {report_file.name}")

    def print_statistics(self):
        """Print validation statistics."""

        stats = self.generate_validation_statistics()

        print("\n" + "=" * 80)
        print("VALIDATION STATISTICS")
        print("=" * 80)

        print(f"\nOverall Performance:")
        print(f"  Contracts Tested: {stats['total_contracts_tested']}")
        print(f"  Successful: {stats['successful_assessments']}")
        print(f"  Success Rate: {stats['success_rate']:.1f}%")

        print(f"\nRisk Score Distribution:")
        print(f"  Mean: {stats['risk_scores']['mean']:.2f}/100")
        print(f"  Median: {stats['risk_scores']['median']:.2f}/100")
        print(f"  Range: {stats['risk_scores']['min']:.2f} - {stats['risk_scores']['max']:.2f}")
        print(f"  Std Dev: {stats['risk_scores']['std_dev']:.2f}")

        print(f"\nRisk Level Distribution:")
        print(f"  Low Risk: {stats['risk_distribution']['LOW']} ({stats['risk_percentages']['low']:.1f}%)")
        print(f"  Medium Risk: {stats['risk_distribution']['MEDIUM']} ({stats['risk_percentages']['medium']:.1f}%)")
        print(f"  High Risk: {stats['risk_distribution']['HIGH']} ({stats['risk_percentages']['high']:.1f}%)")

        print(f"\nClause Analysis:")
        print(f"  Mean Clauses per Contract: {stats['clause_statistics']['mean']:.1f}")
        print(f"  Total Clauses Analyzed: {stats['clause_statistics']['total']}")

        print(f"\nCategory Performance (Mean Scores):")
        for category, cat_stats in stats['category_statistics'].items():
            print(f"  {category.replace('_', ' ').title()}: {cat_stats['mean']:.2f}")

        print(f"\nCritical Issues:")
        print(f"  Mean per Contract: {stats['critical_issues']['mean']:.1f}")
        print(f"  Total Identified: {stats['critical_issues']['total']}")


def main():
    """Main validation function."""

    validator = ExtendedValidation()

    # Run validation
    results = validator.run_validation()

    # Print statistics
    validator.print_statistics()

    # Save results
    output_dir = Path(__file__).parent.parent / "data"
    validator.save_results(output_dir)

    print("\n" + "=" * 80)
    print("Extended validation complete!")
    print("=" * 80 + "\n")


if __name__ == "__main__":
    main()
