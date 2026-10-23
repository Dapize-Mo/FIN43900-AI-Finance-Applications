# Existing-artifact audit — Project 1

**Analyst:** Oladapo Olaniyan  
**Review date:** October 6, 2026

## Starting point

The target is PEP, continuing the prior course work. Brightspace confirms the Edition A checkpoint is a distinct, individual no-grade assignment and records submission `22599005` (`Project_1_Edition_A_Baseline_PEP.pdf`, September 1, 2026, 2:30 PM). The receipt-linked download and local copy at `labs/lab-03/Project_1_Edition_A_Baseline_PEP.pdf` are byte-identical (SHA-256 `F745E7EA27A1445830573029A77D28967A1E4F5E53A9BA9A794079373F35464F`), but each contains a one-page Edge “File not found” error rather than the baseline report. Preserve both unchanged. The submission event is verified; the expected report contents are unresolved. Get instructor/TA recovery guidance before packaging Edition A, and do not reconstruct or silently replace the baseline.

## Reuse review

| Existing artifact | Useful contribution | Required treatment before Project 1 use |
|---|---|---|
| `labs/lab-03/edition-a-baseline.md` and PDF | Frozen initial thesis, intended user, valuation plan, prior claims and AI-off attestation | Keep the PDF unchanged. Validate the displayed FY2024 numbers and broken/missing digit strings in the Markdown/PDF against the actual filing; document corrections in a dated addendum or Edition B. |
| `labs/lab-04/pep_evidence_ledger_lab04.csv` | Initial source-ledger structure and FY2024/normalization questions | Re-source all material inputs to FY2025 10-K/latest 10-Q; verify exact locators and arithmetic. FY2024-only facts are historical context. |
| `labs/lab-05/dcf.py` and training case | Reusable FCFF DCF mechanics and synthetic known-answer fixture | Retain only after wiring it to the new linked forecast and checking the exact training-case fixture. |
| `labs/lab-06/pep_dcf_model_lab06.py` | Existing FCFF scenarios, sensitivity, reverse-DCF mechanics | It starts from a hard-coded normalized FCFF and market close dated February 2025. Replace those stale inputs and connect the DCF to the five-year pro-forma; audit all output logic. |
| `labs/lab-10/pep_proforma_lab10.py` | Five-year statement-linkage and balance-sheet balancing concepts | Do not adopt its valuation as the project result: it discounts FCFE at cost of equity, has hard-coded FY2024 opening figures/assumptions, and its cash/shareholder-return treatment needs reconciliation. Rebuild or adapt with a documented FCFF/WACC convention, current audited base year, tested statement articulation, and sourced assumptions. |
| `labs/lab-11/credit_stress_lab11.py` | General stress-test vocabulary and propagation ideas | Do not treat its target-company stress figures or thresholds as verified PEP facts. The assignment requires a project-specific downside scenario, supported by sourced starting values and a causal path through the pro-forma to cash flow/value/action. |
| `labs/lab-12/project2_audit.py` and project 2 template | Possible mechanical manifest-audit pattern | Do not repurpose as the Project 1 manifest without checking assignment-specific rows/fields. |

## Key open issues

1. The prior company work is anchored on FY2024. The Edition B historical base must be rebuilt from the FY2025 10-K and updated with the latest available interim data as of the declared valuation date.
2. Lab 10 computes FCFE and discounts it at a cost-of-equity input; the Project 1 assignment specifies FCFF discounted at WACC, with the linked forecast driving DCF.
3. The old DCF uses a February 4, 2025 price. A new, dated market price and consistent security/share basis are needed.
4. Prior worksheets contain some blank/garbled reported digits (e.g., in copied Markdown); use actual filings as authority rather than repairing from memory.
5. No peer policy, updated peer data, verified current valuation, locked changed-input result, cold-run record, memo, video, transcript, or final manifest is approved yet.

## First modeling gate

Before using forecast assumptions, produce a FY2023–FY2025 historical statement bridge to the filing, annotate one-time items and changes in accounting/presentation, and reconcile the FY2025 base-year FCFF. Do not write or execute the Project 1 locked changed-input run until the analyst has supplied and frozen the human prediction required by Brightspace.

## Initial verified filing observations (research leads, not conclusions)

- The FY2025 Form 10-K reports net revenue of **$93,925 million**, operating profit of **$11,498 million**, and an intangible-asset impairment line of **$1,993 million**. It reports D&A of **$3,451 million** and total segment/corporate capital spending of **$4,415 million**. The capital-spending footnote is not automatically interchangeable with cash PP&E purchases.
- FY2025 year-end reported cash was **$9,159 million**, short-term investments **$371 million**, short-term debt **$6,861 million**, and long-term debt **$42,321 million**. Keep the components separate until the bridge's cash/debt-like policy is settled.
- The 10-K reports intangible impairments in more than one of the three displayed years (**$1,993 million in 2025, $33 million in 2024, and $927 million in 2023**). This is evidence against reflexively classifying the line as a nonrecurring add-back; investigate the underlying brands, segments, triggers, and future exposure.
- The latest interim filing identified as available by October 6 is Q2 2026 (24 weeks ended June 13). It reports YTD net revenue of **$43,624 million** and operating profit of **$7,236 million**, versus **$40,645 million** and **$4,372 million** for the comparable 2025 period. The comparative period included **$1,860 million** of intangible impairment, so the headline EBIT increase needs normalization before interpretation.
- Q2 2026 balance-sheet cash/short-term investments were **$10,251 million / $465 million**, short-term/long-term debt **$10,602 million / $42,612 million**. These are interim balance-sheet facts, not annual forecast values.

Primary source locators are recorded in `source-register.csv`; the numbers above were read from the SEC FY2025 10-K statements/Note 15 and the SEC Q2 2026 10-Q statements. These observations guide the next research questions; they do not select a forecast, valuation range, or action.
