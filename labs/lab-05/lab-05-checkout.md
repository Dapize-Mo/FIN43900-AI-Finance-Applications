# Lab 05 Brightspace Submission Package

Student Analyst: Oladapo Olaniyan
Teammate: kogbuef@purdue.edu
Course: FIN 43900 — AI Finance Applications, Purdue University
Lab Date: September 8, 2026

================================================================================
QUESTION 1 (0 points): Team Information
================================================================================

kogbuef@purdue.edu


================================================================================
QUESTION 2 (25 points): Individual Checkout Headings
================================================================================

DISCOVER — What was uncertain or unknown at the start? What evidence, test, result, or discussion made it clearer?
At the start, it was uncertain whether terminal-value concentration (~72.4% of EV in synthetic case) indicated a flawed model or a standard financial reality for going-concern valuations. Examining the discounting formula and present value of explicit cash flows ($448.44M) versus terminal value ($1,176.43M) made it clear that terminal value concentration is economically expected, meaning defending a valuation primarily requires defending WACC and long-run perpetual growth (g).

DEFINE — State the problem or question as you now understand it. Identify one boundary, assumption, or success criterion that matters.
The problem is to build an audited FCFF DCF model that passes all 12 synthetic known-answer checkpoints within tolerance, enforces boundary constraints (g < WACC), and transfers to PepsiCo (PEP) using FY2024 SEC Form 10-K evidence. A critical boundary parameter is that perpetual terminal growth (g = 2.50%) must remain strictly less than WACC (7.00%) to avoid division-by-zero or negative enterprise values.

GOOD QUESTION — Write one question worth pursuing next and explain why it matters.
How should PepsiCo's $44.3B multi-tranche debt structure be weighted for WACC when interest rates fluctuate, and should market value of debt replace book value during rate shifts? This matters because WACC is the dominant denominator in terminal value discounting, and a 50 bps shift in WACC alters PepsiCo's equity value by over $20 per share.

MY CONTRIBUTION — What did you personally do? Be specific enough to distinguish your work from your teammates' work.
Working alongside my partner (kogbuef@purdue.edu), I drew the 5-step DCF architecture from memory, hand-calculated Year 1 FCFF ($108.00M) and its PV ($98.18M at 10% WACC), implemented the four STUDENT_WORK functions in dcf_starter.py (project_fcff, value_dcf, sensitivity_table, reverse_dcf_for_growth), added boundary validation for g >= WACC, transferred our sourced PepsiCo FY2024 SEC Form 10-K inputs ($9,688.59M normalized core FCFF, $35,801M net debt, 1,378M diluted shares) yielding a $140.73/share Base Case (0.98x market price), and documented our cost of debt assumption.

TEST / CHECK / RESULT — What did you test, verify, compare, challenge, or change, and what happened? For a case discussion, identify the claim or evidence you examined.
- Verified Checkpoints: Tested dcf_starter.py against dcf_expected_output.csv; all 12 synthetic checkpoints passed within tolerance ($27.50/share equity value, $1,624.87M EV, 72.40% TV share).
- Boundary Check: Verified that setting terminal growth g = 10% >= WACC = 10% correctly threw a ValueError.
- Failure Corrected: Initial terminal value calculation returned $1,839.46M instead of $1,894.65M because the Gordon Growth numerator used raw Year 5 FCFF ($128.76M) without multiplying by (1 + g). I updated the numerator to FCFF5 * (1 + g) = $132.63M, which re-tested successfully at $1,894.65M and restored per-share value to $27.50.

OPTIONAL ARTIFACT LINK — Add a GitHub, app, notebook, document, or other link if one exists. Write N/A if no artifact was produced.
https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/tree/main/labs/lab-05

ATTESTATION — Type exactly: I completed this work in today's class with the teammate(s) listed above, and this checkout is truthful.
I completed this work in today's class with the teammate(s) listed above, and this checkout is truthful.
