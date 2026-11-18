# Project 2 Submission Manifest & Artifact Index

**Student / Author:** **Oladapo Olaniyan** (`oolaniy@purdue.edu`)  
**Course:** FIN 43900 — AI Finance Applications, Fall 2026  
**Institution:** Mitchell E. Daniels, Jr. School of Business, Purdue University  
**Project Title:** Project 2 — Investment Management Application  
**Client / Case:** Meridian Foundation Reserve ($100 Million Reserve Fund)  
**Submission As-Of Date:** November 10, 2026  
**GitHub Repository:** [Dapize-Mo/FIN43900-AI-Finance-Applications](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications)  
**Streamlit Live Application:** [Project 2 Investment Management System](https://dapize-mo-fin43900-ai-finance-appli-projectsproject-2app-kxfhnr.streamlit.app/) *(or local run via `streamlit run app.py`)*

---

### Mandatory Fiduciary Disclosures

> **1. AI Tool Disclosure:** Anthropic Claude (Claude 3.5 Sonnet / Claude Opus 5.5) and Google Antigravity were utilized in designing analytical scripts, unit testing architecture, visualization ergonomics, and formatting optimization. All mathematical derivations, input validations, fiduciary constraints, and investment decisions were directed, verified, and finalized independently by the student analyst.  
> **2. Ownership & Academic Notice:** The analysis, models, interpretations, and committee recommendations presented herein are solely the author's work; this package is an educational simulation developed for academic demonstration in FIN 43900 at Purdue University, not personalized investment advice.

---

## 1. Primary Artifacts & Repository Links

Every written deliverable is maintained in GitHub-versioned Markdown in compliance with the updated course architecture ruling (November 10, 2026).

| Artifact / Deliverable | Exact File Path in Repo | Description & Fiduciary Scope | Direct GitHub Link |
| :--- | :--- | :--- | :--- |
| **Project 2 Readme** | `projects/project-2/README.md` | Single-command cold-run guide, repo architecture map, and disclaimers | [README.md on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/projects/project-2/README.md) |
| **Decision Memorandum** | `projects/project-2/docs/decision-memo.md` | Formal investment committee memo recommending Constrained Optimal mix | [decision-memo.md on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/projects/project-2/docs/decision-memo.md) |
| **Validation & AI-Use Record** | `projects/project-2/docs/validation-and-ai-use.md` | SR 26-2 model audit, test ledger, AI disposition, and Locked Changed-Input Record | [validation-and-ai-use.md on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/projects/project-2/docs/validation-and-ai-use.md) |
| **Streamlit Web Application** | `projects/project-2/app.py` | Standalone interactive fiduciary allocation, mandate check & stress app | [app.py on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/projects/project-2/app.py) |
| **Analytical Engine** | `projects/project-2/src/engine.py` | Covariance math, optimization search, stress testing, and Stop Condition | [engine.py on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/projects/project-2/src/engine.py) |
| **Mandate Verification** | `projects/project-2/src/mandate.py` | Algorithmic covenant checks across all Meridian S1–S10 constraints | [mandate.py on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/projects/project-2/src/mandate.py) |
| **Point-in-Time Signal** | `projects/project-2/src/point_in_time.py` | Dual timestamp engine ($t_{\text{event}}, t_{\text{pub}}$) and official Data Card | [point_in_time.py on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/projects/project-2/src/point_in_time.py) |
| **Historical Price Dataset** | `projects/project-2/data/prices.csv` | 5-Year monthly adjusted close prices across ETF universe (BIL, IEF, LQD, VT) | [prices.csv on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/projects/project-2/data/prices.csv) |
| **Point-in-Time Vintage Dataset** | `projects/project-2/data/pit_macro.csv` | Historical CPI vintages proving 60-month seasonal factor restatements | [pit_macro.csv on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/projects/project-2/data/pit_macro.csv) |
| **Dependency Specification** | `projects/project-2/requirements.txt` | Complete execution dependencies for local and cloud environments | [requirements.txt on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/projects/project-2/requirements.txt) |

---

## 2. Video Submissions (YouTube Links & Transcripts)

All three videos are Unlisted YouTube links with captions enabled. **Status: Video 1 uploaded (unlisted); Videos 2 and 3 PENDING recording** - link, duration and timestamps below are filled in after upload; none is claimed until then.

| Video | Limit | YouTube link | Actual duration | Transcript |
| :--- | :---: | :--- | :---: | :--- |
| 1 - Research evolution & thinking changes | 3:00 | [https://youtu.be/C-fHpIHxUow](https://youtu.be/C-fHpIHxUow) (unlisted) | 2:42 (per YouTube) | [transcript-video-1.txt](transcripts/transcript-video-1.txt) |
| 2 - Technical code & model walkthrough | 5:00 | PENDING | PENDING | [transcript-video-2.txt](transcripts/transcript-video-2.txt) |
| 3 - Committee defense & live demo (opens with live app) | 5:00 | PENDING | PENDING | [transcript-video-3.txt](transcripts/transcript-video-3.txt) |

### Timestamp index (to be confirmed against final recordings)

| Video | Time | Content |
| :--- | :---: | :--- |
| 1 | 0:00 | Two required statements (AI use; ownership) |
| 1 | PENDING | What changed from Lab 13 to Project 2 |
| 1 | PENDING | How AI output was independently checked |
| 2 | 0:00 | Two required statements |
| 2 | PENDING | `engine.py`: covariance, optimizer, stress drivers |
| 2 | PENDING | `mandate.py`: 60/40 covenant failure |
| 2 | PENDING | Tests (9/9) and LCIR |
| 3 | 0:00 | Live app shown first; two required statements |
| 3 | PENDING | Three-portfolio comparison and recommendation |
| 3 | PENDING | Stress tab and -100 bps kill rule (12.70% vol) |
| 3 | PENDING | Reversal triggers and committee ask |

### Access confirmation

- [x] GitHub repository is public (verified).
- [ ] Each video opened logged out / incognito with transcript visible (do after upload).
- [ ] Same `.md` files attached to Brightspace.

---

## 3. Frozen Verification Checklist

- [x] A stranger can clone the repo and execute `streamlit run app.py` from the README without error.
- [x] Mandatory AI and Educational disclaimers open README, Decision Memo, and all video scripts.
- [x] Decision Memo, Validation Record, and Live App report identical numbers (Return: 6.50%, Vol: 9.30%, Res: 8.0%).
- [ ] Locked Changed-Input Record with AI-off prediction committed to Git before the run (LCIR-002 pending the analyst's own prediction).
- [x] Point-in-time data card documents dual timestamps, publication lags, and revision risk.
- [x] No private API keys, passwords, or personal credentials committed to Git.

