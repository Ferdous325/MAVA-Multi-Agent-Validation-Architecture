# MAVA - Multi-Agent Validation Architecture

## Reducing Hallucination in Generative AI-Based Business Analytics

MAVA is a research framework designed to reduce hallucination in
Generative AI-based business analytics through claim-level validation
and evidence-based correction.

## Research Pipeline

Dataset -> Ground Truth -> LLM Narrative -> Atomic Claims ->
Validation -> Correction -> Independent Verification -> Final MAVA Validation

## Experimental Scope

- Customer Churn
- Financial
- Walmart

Total atomic claims evaluated: 126

## Main Experimental Result

| Metric | Baseline | MAVA |
|---|---:|---:|
| Hallucination Rate | 80.36% | 16.96% |
| Absolute Reduction | - | 63.39 percentage points |
| Relative Reduction | - | 78.89% |

## Dataset Results

| Dataset | Baseline | MAVA |
|---|---:|---:|
| Customer Churn | 66.67% | 33.33% |
| Financial | 79.55% | 29.55% |
| Walmart | 86.00% | 0.00% |

## Claim-Level Evaluation

MAVA evaluates:

- NUMERIC claims
- PERCENTAGE claims
- ENTITY_VALUE claims
- COMPARISON claims

Validation statuses:

- MATCH
- MISMATCH
- UNVERIFIED

## Research Contribution

The main contribution is an auditable validation architecture that
converts free-form LLM business narratives into atomic claims and
checks those claims against deterministic evidence.

The framework therefore addresses hallucination at the claim level
rather than relying only on narrative fluency.

## Correction Verification

84 corrections were proposed.

71 corrections were independently verified.

13 corrections were rejected during verification.

## Research Integrity

- Original LLM narratives preserved
- Original atomic claims preserved
- Frozen ground truth preserved
- Baseline validation preserved
- Corrections independently verified
- No additional Gemini API calls during validation/correction

## Streamlit Demonstrator

The Streamlit application provides:

1. Research overview
2. MAVA architecture
3. Dataset explorer
4. LLM narratives
5. Claim-level validation
6. Experimental results
7. Correction verification
8. Research audit

## Author

Jannatun Ferdous

MAVA Research Project