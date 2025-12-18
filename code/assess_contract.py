#!/usr/bin/env python3
"""
Main Entry Point: Automated Contract Risk Assessment
Quick access to framework functionality
"""

import sys
import argparse
from pathlib import Path

# Add current directory to path
sys.path.append(str(Path(__file__).parent))

from risk_assessor import RiskAssessmentEngine
from report_generator import ReportGenerator
from interactive_assessment import InteractiveAssessment


def print_banner():
    """Print welcome banner."""
    print("=" * 70)
    print("  AUTOMATED VENDOR CONTRACT RISK ASSESSMENT TOOL")
    print("  Phase 2: Framework Implementation")
    print("=" * 70)
    print()


def main():
    """Main entry point with user-friendly interface."""

    parser = argparse.ArgumentParser(
        description='Automated Vendor Contract Risk Assessment',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Assess a single contract
  python3 assess_contract.py --file vendor_contract.html

  # Interactive questionnaire
  python3 assess_contract.py --interactive

  # Compare multiple vendors
  python3 assess_contract.py --directory contracts_folder/

  # Custom output location
  python3 assess_contract.py --file contract.html --output my_report.html

For more information, see README.md or docs/USER_GUIDE.md
        """
    )

    parser.add_argument(
        '--file',
        type=str,
        help='Path to vendor contract file (HTML format)'
    )

    parser.add_argument(
        '--directory',
        type=str,
        help='Directory containing multiple contract files for comparison'
    )

    parser.add_argument(
        '--interactive',
        action='store_true',
        help='Launch interactive questionnaire mode'
    )

    parser.add_argument(
        '--output',
        type=str,
        default='risk_assessment_report.html',
        help='Output file path for report (default: risk_assessment_report.html)'
    )

    parser.add_argument(
        '--format',
        type=str,
        choices=['html', 'markdown', 'both'],
        default='html',
        help='Report format: html, markdown, or both (default: html)'
    )

    args = parser.parse_args()

    print_banner()

    # Interactive mode
    if args.interactive:
        print("Launching interactive questionnaire...\n")
        assessment = InteractiveAssessment()
        assessment.run_complete_assessment()
        return

    # File mode
    if args.file:
        if not Path(args.file).exists():
            print(f"❌ Error: File not found: {args.file}")
            return

        print(f"Analyzing contract: {args.file}\n")

        engine = RiskAssessmentEngine()
        assessment_result = engine.assess_contract_file(args.file)

        if 'error' in assessment_result:
            print(f"❌ Error: {assessment_result['error']}")
            print("\nTry using --interactive mode instead")
            return

        # Display quick results
        print(f"✓ Analysis complete!")
        print(f"  Vendor: {assessment_result.get('vendor_name', 'Unknown')}")
        print(f"  Risk Score: {assessment_result.get('total_score', 0)}/100")
        print(f"  Risk Level: {assessment_result.get('risk_level', 'Unknown')}")
        print(f"  Clauses Analyzed: {assessment_result.get('total_clauses', 0)}\n")

        # Generate report
        print(f"Generating report...")
        report_gen = ReportGenerator()

        if args.format in ['html', 'both']:
            html_file = args.output if args.output.endswith('.html') else args.output + '.html'
            report_gen.generate_html_report(assessment_result, html_file)
            print(f"  ✓ HTML report: {html_file}")

        if args.format in ['markdown', 'both']:
            md_file = args.output.replace('.html', '.md') if '.html' in args.output else args.output + '.md'
            report_gen.generate_markdown_report(assessment_result, md_file)
            print(f"  ✓ Markdown report: {md_file}")

        print(f"\n{'=' * 70}")
        print("Assessment complete! Open the report in your browser.")
        print("=" * 70 + "\n")
        return

    # Directory mode
    if args.directory:
        if not Path(args.directory).exists():
            print(f"❌ Error: Directory not found: {args.directory}")
            return

        print(f"Analyzing all contracts in: {args.directory}\n")

        engine = RiskAssessmentEngine()
        contract_files = list(Path(args.directory).glob("*.html"))

        if not contract_files:
            print(f"❌ No HTML files found in {args.directory}")
            return

        print(f"Found {len(contract_files)} contracts\n")

        assessments = engine.assess_multiple_contracts([str(f) for f in contract_files])
        comparison = engine.generate_comparison_report(assessments)

        # Display summary
        print(f"\n{'=' * 70}")
        print("COMPARISON SUMMARY")
        print("=" * 70)
        print(f"Vendors Assessed: {comparison.get('total_vendors', 0)}")
        print(f"Average Risk Score: {comparison.get('average_score', 0):.2f}/100")
        print(f"\nRisk Distribution:")
        dist = comparison.get('risk_distribution', {})
        print(f"  Low Risk: {dist.get('LOW', 0)}")
        print(f"  Medium Risk: {dist.get('MEDIUM', 0)}")
        print(f"  High Risk: {dist.get('HIGH', 0)}")

        print(f"\nBest Vendors (Lowest Risk):")
        for idx, vendor in enumerate(comparison.get('best_vendors', [])[:5], 1):
            print(f"  {idx}. {vendor.get('vendor_name')}: {vendor.get('total_score')}/100")

        print(f"\nHighest Risk Vendors:")
        for idx, vendor in enumerate(comparison.get('worst_vendors', [])[:5], 1):
            print(f"  {idx}. {vendor.get('vendor_name')}: {vendor.get('total_score')}/100")

        # Save comparison report
        import json
        output_file = args.output.replace('.html', '.json') if '.html' in args.output else args.output + '.json'
        with open(output_file, 'w') as f:
            json.dump({
                'assessments': assessments,
                'comparison': comparison
            }, f, indent=2)

        print(f"\n{'=' * 70}")
        print(f"Comparison data saved to: {output_file}")
        print("=" * 70 + "\n")
        return

    # No mode specified
    print("Please specify an assessment mode:\n")
    print("  --file <contract.html>       Assess a single contract")
    print("  --directory <folder>         Compare multiple contracts")
    print("  --interactive                Use guided questionnaire")
    print("\nFor help: python3 assess_contract.py --help")
    print()


if __name__ == "__main__":
    main()
