#!/usr/bin/env python3
"""
Phase 1: Analyze all 53 vendor contracts
Extract lock-in clauses and generate statistics
"""

import os
import json
import csv
from pathlib import Path
from bs4 import BeautifulSoup

# Import our existing risk assessor
import sys
sys.path.insert(0, '/workspaces/ireland/code')
from risk_assessor import ContractAnalyzer


def analyze_all_contracts():
    """Analyze all contracts in /contracts folder."""

    contracts_dir = Path("/workspaces/ireland/contracts")
    analyzer = ContractAnalyzer()

    all_results = []
    all_clauses = []
    vendor_stats = {}

    # Get all HTML files
    contract_files = sorted(contracts_dir.glob("*.html"))

    print(f"Found {len(contract_files)} contracts to analyze")
    print("=" * 80)

    for idx, contract_file in enumerate(contract_files, 1):
        vendor_name = contract_file.stem.replace('_', ' ').replace('2', '').title()

        print(f"\n[{idx}/{len(contract_files)}] Analyzing: {vendor_name}")

        try:
            # Read contract
            with open(contract_file, 'r', encoding='utf-8', errors='ignore') as f:
                html_content = f.read()

            # Parse with BeautifulSoup
            soup = BeautifulSoup(html_content, 'html.parser')
            text = soup.get_text(separator=' ', strip=True)

            # Find clauses
            clauses = analyzer.find_clauses(text, vendor_name, str(contract_file.name))

            print(f"  Found {len(clauses)} lock-in clauses")

            # Count risk levels (case insensitive)
            high_risk = sum(1 for c in clauses if c.get('risk_level', '').upper() == 'HIGH')
            medium_risk = sum(1 for c in clauses if c.get('risk_level', '').upper() == 'MEDIUM')

            # Add to all clauses list
            for clause in clauses:
                # Normalize keys for consistency
                normalized_clause = {
                    'vendor': vendor_name,
                    'contract_file': str(contract_file.name),
                    'category': clause.get('clause_category', 'unknown'),
                    'risk_level': clause.get('risk_level', 'MEDIUM'),
                    'lock_in_mechanisms': [clause.get('lock_in_mechanism', '')],  # Make it a list
                    'text': clause.get('clause_text', ''),
                    'keywords_found': [str(clause.get('keyword_matches', 0))]  # Store count as list
                }
                all_clauses.append(normalized_clause)

            # Store vendor stats
            vendor_stats[vendor_name] = {
                'total_clauses': len(clauses),
                'high_risk': high_risk,
                'medium_risk': medium_risk,
                'high_risk_percentage': (high_risk / len(clauses) * 100) if len(clauses) > 0 else 0,
                'contract_file': contract_file.name
            }

            all_results.append({
                'vendor': vendor_name,
                'clauses_found': len(clauses),
                'high_risk': high_risk,
                'medium_risk': medium_risk,
                'status': 'success'
            })

        except Exception as e:
            print(f"  ERROR: {str(e)}")
            all_results.append({
                'vendor': vendor_name,
                'clauses_found': 0,
                'high_risk': 0,
                'medium_risk': 0,
                'status': f'failed: {str(e)}'
            })

    return all_results, all_clauses, vendor_stats


def save_results(all_results, all_clauses, vendor_stats):
    """Save analysis results to files."""

    data_dir = Path("/workspaces/ireland/data")
    data_dir.mkdir(exist_ok=True)

    # 1. Save clauses to CSV
    csv_file = data_dir / "phase1_extracted_clauses.csv"

    if all_clauses:
        with open(csv_file, 'w', newline='', encoding='utf-8') as f:
            writer = csv.DictWriter(f, fieldnames=[
                'vendor', 'contract_file', 'category', 'risk_level',
                'lock_in_mechanism', 'clause_text', 'keywords_found'
            ])
            writer.writeheader()

            for clause in all_clauses:
                writer.writerow({
                    'vendor': clause.get('vendor', ''),
                    'contract_file': clause.get('contract_file', ''),
                    'category': clause.get('category', ''),
                    'risk_level': clause.get('risk_level', ''),
                    'lock_in_mechanism': ', '.join(clause.get('lock_in_mechanisms', [])),
                    'clause_text': clause.get('text', '')[:500],  # Truncate long text
                    'keywords_found': ', '.join(clause.get('keywords_found', []))
                })

    print(f"\n✓ Saved {len(all_clauses)} clauses to {csv_file}")

    # 2. Save patterns to JSON
    json_file = data_dir / "phase1_clause_patterns.json"

    # Calculate overall statistics
    total_clauses = len(all_clauses)
    high_risk_clauses = sum(1 for c in all_clauses if c.get('risk_level', '').upper() == 'HIGH')
    medium_risk_clauses = sum(1 for c in all_clauses if c.get('risk_level', '').upper() == 'MEDIUM')

    # Category statistics
    category_stats = {}
    for clause in all_clauses:
        cat = clause.get('category', 'unknown')
        if cat not in category_stats:
            category_stats[cat] = {'total': 0, 'high_risk': 0, 'medium_risk': 0}

        category_stats[cat]['total'] += 1
        risk = clause.get('risk_level', '').upper()
        if risk == 'HIGH':
            category_stats[cat]['high_risk'] += 1
        elif risk == 'MEDIUM':
            category_stats[cat]['medium_risk'] += 1

    # Lock-in mechanism counts
    mechanism_counts = {}
    for clause in all_clauses:
        for mech in clause.get('lock_in_mechanisms', []):
            mechanism_counts[mech] = mechanism_counts.get(mech, 0) + 1

    patterns_data = {
        'analysis_date': '2025-12-17',
        'contracts_analyzed': len(all_results),
        'successful_analyses': sum(1 for r in all_results if r['status'] == 'success'),
        'total_clauses': total_clauses,
        'high_risk_clauses': high_risk_clauses,
        'medium_risk_clauses': medium_risk_clauses,
        'high_risk_percentage': (high_risk_clauses / total_clauses * 100) if total_clauses > 0 else 0,
        'category_statistics': category_stats,
        'lock_in_mechanism_counts': mechanism_counts,
        'vendor_statistics': vendor_stats
    }

    with open(json_file, 'w', encoding='utf-8') as f:
        json.dump(patterns_data, f, indent=2)

    print(f"✓ Saved patterns to {json_file}")

    return patterns_data


def print_summary(patterns_data):
    """Print analysis summary."""

    print("\n" + "=" * 80)
    print("PHASE 1 ANALYSIS COMPLETE")
    print("=" * 80)

    print(f"\nContracts Analyzed: {patterns_data['contracts_analyzed']}")
    print(f"Successful: {patterns_data['successful_analyses']}")
    print(f"Total Clauses Extracted: {patterns_data['total_clauses']}")
    print(f"High Risk: {patterns_data['high_risk_clauses']} ({patterns_data['high_risk_percentage']:.1f}%)")
    print(f"Medium Risk: {patterns_data['medium_risk_clauses']}")

    print(f"\nCategory Breakdown:")
    for cat, stats in patterns_data['category_statistics'].items():
        print(f"  {cat}: {stats['total']} clauses ({stats['high_risk']} high-risk)")

    print(f"\nTop Lock-in Mechanisms:")
    sorted_mechs = sorted(patterns_data['lock_in_mechanism_counts'].items(),
                         key=lambda x: x[1], reverse=True)
    for mech, count in sorted_mechs[:10]:
        print(f"  {mech}: {count}")

    print("\n" + "=" * 80)


def main():
    """Main analysis function."""

    print("=" * 80)
    print("PHASE 1: VENDOR CONTRACT ANALYSIS")
    print("=" * 80)

    # Analyze all contracts
    all_results, all_clauses, vendor_stats = analyze_all_contracts()

    # Save results
    patterns_data = save_results(all_results, all_clauses, vendor_stats)

    # Print summary
    print_summary(patterns_data)


if __name__ == "__main__":
    main()
