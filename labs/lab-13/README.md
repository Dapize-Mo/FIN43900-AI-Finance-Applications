# Lab 13 — Portfolio Mandate Defense

**Course:** FIN 43900 — AI Finance Applications, Fall 2026  
**Student / Author:** Oladapo Olaniyan  
**Brightspace item:** Lab 13 — Portfolio Mandate Defense  
**Due:** October 16, 2026, 11:59 p.m.  
**Value:** 25 points · 55-minute quiz · three attempts allowed

## Controlling instructions

Brightspace points to the course GitHub repository for the lab instructions. The current Lab 13 page is [Week 8 — Lab 13 Portfolio Mandate Defense](https://github.com/CinderZhang/FIN43900-Fall2026/blob/main/lessons/week-08/lab-13-portfolio-mandate.md). Its instruction set is newer and more specific than the older local course mirror. Brightspace governs the due date and quiz; the linked GitHub page governs the lab work.

The case is fictional **Meridian Foundation Reserve**. Use only the case and holdings/candidate tables in the Lab 13 page. Do not mix in the optional changed-case challenge or your own Project 2 client, securities, strategy, data, or code.

## Required evidence

1. In your own `.md` file, sort statements **S1–S10** as objective, hard constraint, preference, unverifiable promise, or missing, and give a one-line reason for each. The page explicitly says to do this **without AI**.
2. Use an AI partner to build and explain `mandate.py` (standard library only). The script must compute the reserve minimum and each candidate's checkable rules from editable inputs; it must label the 10% calendar-year-loss statement “requires CIO clarification,” not test it as a rule.
3. Run the script and reconcile candidates A, B, and C to the known-answer table on GitHub. Then run the required negative-weight probe for candidate A, check the output, and restore A's original inputs.
4. Ask the same AI chat for a candidate D that passes every rule the script checks but could still reasonably be rejected by the CIO. Run it, judge the objection against a named S1–S10 statement, and complete the skeptical-colleague check described in the prompt.
5. Close AI and write one CIO question that must be answered before optimization, plus the answer that would change the portfolio. Complete the investment-policy-statement mapping and reflection.
6. Push your `.md` file and `mandate.py` to **your own GitHub repository**, then paste their links into the Brightspace Lab 13 quiz. The quiz collects the links; the files are the evidence.

## Work sequence

1. Complete Section 1 of the [worksheet](lab-13-mandate-defense-worksheet.md) independently before AI.
2. Share your completed S1–S10 labels here. I can then help build `mandate.py`, explain it, and check the outputs against the published anchors.
3. Complete the probe, candidate D judgment, CIO question, IPS mapping, and reflection.
4. Publish the two files to your repository and enter their links in Brightspace before the deadline.

## Deliverables & Links

- **Checkout File:** [`checkout.md`](checkout.md)
- **Full Checkout Deliverable:** [`lab-13-checkout.md`](lab-13-checkout.md)
- **Mandate Defense Worksheet:** [`lab-13-mandate-defense-worksheet.md`](lab-13-mandate-defense-worksheet.md)
- **Standard-Library Rule Checker:** [`mandate.py`](mandate.py)
- **Direct GitHub Checkout Link:** https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-13/checkout.md
- **Direct GitHub Full Package Link:** https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-13/lab-13-checkout.md
- **Direct GitHub Worksheet Link:** https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-13/lab-13-mandate-defense-worksheet.md
- **Direct GitHub Checker Link:** https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/labs/lab-13/mandate.py

## Status

**Complete & Fully Verified.**  
- S1–S10 human-first classifications, rationales, and IPS mapping complete.
- Standard-library checker `mandate.py` fully verified against published anchors for Candidates A, B, C, D and negative-weight probe.
- Candidate D judgment, skeptical colleague check, two AI operational interpretation dispositions, CIO escalation questions, and 60-second committee defense fully articulated.
- Ready for Brightspace submission via Attempts 2 & 3.
