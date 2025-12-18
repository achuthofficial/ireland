#!/usr/bin/env python3
"""
Phase 2: Weighted Scoring Algorithm
Automated Vendor Contract Risk Assessment Tool

This module implements the 100-point weighted scoring system based on Phase 1 findings.
"""

import json
from typing import Dict, List, Tuple

# Category weights based on Phase 1 empirical findings
CATEGORY_WEIGHTS = {
    "service_level": 25,        # 81.1% high-risk in Phase 1
    "pricing_terms": 25,        # 66.1% high-risk in Phase 1
    "termination_exit": 20,     # 41.3% high-risk in Phase 1
    "data_portability": 15,     # 29.2% high-risk, critically under-addressed
    "support_obligations": 15   # 25.0% high-risk in Phase 1
}

# Risk multipliers for lock-in mechanisms
LOCK_IN_MULTIPLIERS = {
    # High severity (1.0x - full penalty)
    "no_compensation": 1.0,
    "price_increase_risk": 1.0,
    "data_restriction": 1.0,
    "unilateral_pricing": 1.0,
    "no_sla": 1.0,

    # Medium severity (0.7x)
    "discontinuation_risk": 0.7,
    "automatic_renewal": 0.7,
    "limited_remedies": 0.7,
    "no_commitment": 0.7,
    "no_guarantee": 0.7,

    # Lower severity (0.5x)
    "cancellation_penalty": 0.5,
    "no_support_guarantee": 0.5,
    "exit_fees": 0.5,
    "no_notice_changes": 0.5,

    # Standard (0.3x)
    "standard": 0.3
}

# Risk thresholds
RISK_THRESHOLDS = {
    "low": (0, 33),      # 0-33 points
    "medium": (34, 66),  # 34-66 points
    "high": (67, 100)    # 67-100 points
}


class ContractScorer:
    """Calculate risk scores for vendor contracts."""

    def __init__(self):
        self.category_weights = CATEGORY_WEIGHTS
        self.lock_in_multipliers = LOCK_IN_MULTIPLIERS
        self.risk_thresholds = RISK_THRESHOLDS

    def calculate_category_score(self, clauses: List[Dict]) -> Dict[str, float]:
        """
        Calculate risk scores for each category.

        Args:
            clauses: List of clause dictionaries from contract analysis

        Returns:
            Dictionary with category scores and details
        """
        category_scores = {}
        category_details = {}

        for category, max_points in self.category_weights.items():
            category_clauses = [c for c in clauses if c.get('clause_category') == category]

            if not category_clauses:
                # Missing category is a red flag - assign partial penalty
                category_scores[category] = max_points * 0.5
                category_details[category] = {
                    'score': max_points * 0.5,
                    'max_points': max_points,
                    'clause_count': 0,
                    'high_risk_count': 0,
                    'missing_coverage': True,
                    'penalty_reason': 'No clauses found in this category'
                }
                continue

            # Calculate weighted risk
            total_penalty = 0
            high_risk_count = 0

            for clause in category_clauses:
                risk_level = clause.get('risk_level', 'Medium')
                lock_in_type = clause.get('lock_in_mechanism', 'standard')

                if risk_level == 'High':
                    high_risk_count += 1
                    multiplier = self.lock_in_multipliers.get(lock_in_type, 0.5)
                    total_penalty += multiplier
                else:
                    # Medium risk gets 50% of the penalty
                    multiplier = self.lock_in_multipliers.get(lock_in_type, 0.3)
                    total_penalty += multiplier * 0.5

            # Average penalty across clauses, then scale to category max points
            avg_penalty = total_penalty / len(category_clauses)
            category_score = max_points * avg_penalty

            category_scores[category] = round(category_score, 2)
            category_details[category] = {
                'score': round(category_score, 2),
                'max_points': max_points,
                'clause_count': len(category_clauses),
                'high_risk_count': high_risk_count,
                'high_risk_percentage': round((high_risk_count / len(category_clauses)) * 100, 1),
                'missing_coverage': False
            }

        return category_scores, category_details

    def calculate_total_score(self, category_scores: Dict[str, float]) -> Tuple[float, str]:
        """
        Calculate total risk score and risk level.

        Args:
            category_scores: Dictionary of category scores

        Returns:
            Tuple of (total_score, risk_level)
        """
        total_score = sum(category_scores.values())
        total_score = round(total_score, 2)

        # Determine risk level
        if self.risk_thresholds["low"][0] <= total_score <= self.risk_thresholds["low"][1]:
            risk_level = "LOW"
        elif self.risk_thresholds["medium"][0] <= total_score <= self.risk_thresholds["medium"][1]:
            risk_level = "MEDIUM"
        else:
            risk_level = "HIGH"

        return total_score, risk_level

    def score_contract(self, clauses: List[Dict]) -> Dict:
        """
        Score a complete contract.

        Args:
            clauses: List of clause dictionaries

        Returns:
            Complete scoring report
        """
        category_scores, category_details = self.calculate_category_score(clauses)
        total_score, risk_level = self.calculate_total_score(category_scores)

        # Identify critical issues
        critical_issues = self._identify_critical_issues(category_details, clauses)

        # Generate recommendations
        recommendations = self._generate_recommendations(category_details, critical_issues)

        return {
            'total_score': total_score,
            'risk_level': risk_level,
            'category_scores': category_scores,
            'category_details': category_details,
            'critical_issues': critical_issues,
            'recommendations': recommendations,
            'score_interpretation': self._interpret_score(total_score, risk_level)
        }

    def _identify_critical_issues(self, category_details: Dict, clauses: List[Dict]) -> List[Dict]:
        """Identify critical risk issues in the contract."""
        issues = []

        for category, details in category_details.items():
            # Missing coverage
            if details.get('missing_coverage'):
                issues.append({
                    'category': category,
                    'severity': 'HIGH',
                    'issue': f'No {category.replace("_", " ")} clauses found',
                    'impact': 'Critical contractual gap - no protection in this area'
                })

            # High risk percentage
            elif details.get('high_risk_percentage', 0) >= 70:
                issues.append({
                    'category': category,
                    'severity': 'HIGH',
                    'issue': f'{details["high_risk_percentage"]}% of {category.replace("_", " ")} clauses are high-risk',
                    'impact': 'Significant lock-in risk in this category'
                })

            # Category score is high
            elif details['score'] >= (details['max_points'] * 0.7):
                issues.append({
                    'category': category,
                    'severity': 'MEDIUM',
                    'issue': f'Category scored {details["score"]}/{details["max_points"]} points',
                    'impact': 'Above-average risk in this area'
                })

        # Check for specific high-risk lock-in mechanisms
        high_risk_mechanisms = ['no_compensation', 'unilateral_pricing', 'data_restriction', 'no_sla']
        for clause in clauses:
            if clause.get('lock_in_mechanism') in high_risk_mechanisms:
                issues.append({
                    'category': clause.get('clause_category'),
                    'severity': 'HIGH',
                    'issue': f'Contains {clause["lock_in_mechanism"].replace("_", " ")} clause',
                    'impact': 'Critical lock-in mechanism identified'
                })

        return issues

    def _generate_recommendations(self, category_details: Dict, critical_issues: List[Dict]) -> List[str]:
        """Generate prioritized recommendations."""
        recommendations = []

        # Priority 1: Address critical issues
        high_severity_issues = [i for i in critical_issues if i['severity'] == 'HIGH']
        if high_severity_issues:
            recommendations.append("PRIORITY 1: Address the following critical issues before signing:")
            for issue in high_severity_issues[:3]:  # Top 3
                recommendations.append(f"  - {issue['issue']} in {issue['category'].replace('_', ' ')}")

        # Priority 2: Negotiate high-scoring categories
        high_score_categories = [(cat, det) for cat, det in category_details.items()
                                 if det['score'] >= det['max_points'] * 0.6]
        if high_score_categories:
            recommendations.append("\nPRIORITY 2: Negotiate improvements in these areas:")
            for cat, det in sorted(high_score_categories, key=lambda x: x[1]['score'], reverse=True):
                recommendations.append(f"  - {cat.replace('_', ' ').title()}: {det['score']}/{det['max_points']} points")

        # Priority 3: Fill coverage gaps
        missing_categories = [cat for cat, det in category_details.items() if det.get('missing_coverage')]
        if missing_categories:
            recommendations.append("\nPRIORITY 3: Request explicit provisions for:")
            for cat in missing_categories:
                recommendations.append(f"  - {cat.replace('_', ' ').title()}")

        return recommendations

    def _interpret_score(self, score: float, risk_level: str) -> str:
        """Provide interpretation of the risk score."""
        interpretations = {
            "LOW": f"Score: {score}/100 - This contract presents relatively low lock-in risk. "
                   "However, review specific clauses and negotiate improvements where possible.",

            "MEDIUM": f"Score: {score}/100 - This contract presents moderate lock-in risk. "
                      "Several areas need negotiation to improve terms. Focus on high-risk categories first.",

            "HIGH": f"Score: {score}/100 - WARNING: This contract presents significant lock-in risk. "
                    "Strongly recommend negotiating better terms or considering alternative vendors. "
                    "Multiple critical issues identified."
        }

        return interpretations.get(risk_level, f"Score: {score}/100")


def score_vendor_contract(clauses: List[Dict]) -> Dict:
    """
    Convenience function to score a contract.

    Args:
        clauses: List of clause dictionaries from contract analysis

    Returns:
        Complete scoring report
    """
    scorer = ContractScorer()
    return scorer.score_contract(clauses)


if __name__ == "__main__":
    # Example usage
    print("Weighted Scoring Algorithm - Phase 2")
    print("=" * 60)
    print("\nCategory Weights (100-point system):")
    for category, weight in CATEGORY_WEIGHTS.items():
        print(f"  {category.replace('_', ' ').title():.<30} {weight} points")
    print("\nRisk Thresholds:")
    for level, (min_score, max_score) in RISK_THRESHOLDS.items():
        print(f"  {level.upper():.<30} {min_score}-{max_score} points")
