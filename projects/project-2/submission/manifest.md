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

> **1. AI Tool Disclosure:** Anthropic Claude and Google Antigravity were utilized in designing analytical scripts, unit testing architecture, visualization ergonomics, and formatting optimization. All mathematical derivations, input validations, fiduciary constraints, and investment decisions were directed, verified, and finalized independently by the student analyst.  
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
| **Point-in-Time Vintage Dataset** | `projects/project-2/data/pit_macro.csv` | CPI vintage snapshot (60-month revision window; 13 revisions detected across 31 rows) | [pit_macro.csv on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/projects/project-2/data/pit_macro.csv) |
| **Dependency Specification** | `projects/project-2/requirements.txt` | Complete execution dependencies for local and cloud environments | [requirements.txt on GitHub](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/projects/project-2/requirements.txt) |

---

## 2. Video Submissions (YouTube Links & Transcripts)

All three videos are Unlisted YouTube links with captions enabled. **Status: All three videos uploaded (unlisted)** - Links and durations below are as shown by YouTube.

| Video | Limit | YouTube link | Actual duration | Transcript |
| :--- | :---: | :--- | :---: | :--- |
| 1 - Research evolution & thinking changes | 3:00 | [https://youtu.be/C-fHpIHxUow](https://youtu.be/C-fHpIHxUow) (unlisted) | 2:42 (per YouTube) | [transcript-video-1.txt](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/projects/project-2/submission/transcripts/transcript-video-1.txt) |
| 2 - Technical code & model walkthrough | 5:00 | [https://youtu.be/mBZEseHDXXk](https://youtu.be/mBZEseHDXXk) (unlisted) | 4:40 (per YouTube) | [transcript-video-2.txt](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/projects/project-2/submission/transcripts/transcript-video-2.txt) |
| 3 - Committee defense & live demo (opens with live app) | 5:00 | [https://youtu.be/qsCibfoSNPY](https://youtu.be/qsCibfoSNPY) (unlisted) | 3:52 (per YouTube) | [transcript-video-3.txt](https://github.com/Dapize-Mo/FIN43900-AI-Finance-Applications/blob/main/projects/project-2/submission/transcripts/transcript-video-3.txt) |

### Timestamp index (approximate, taken from the prepared scripts; use YouTube captions for exact positions)

| Video | Time | Content |
| :--- | :---: | :--- |
| 1 | 0:00 | Two required statements (AI use; ownership) |
| 1 | ~0:25 | What changed from Lab 13 to Project 2 |
| 1 | ~1:15 | How AI output was independently checked |
| 2 | 0:00 | Two required statements; repository tour |
| 2 | ~0:45 | `mandate.py` and `engine.py`: mandate checks, covariance, optimizer |
| 2 | ~1:30 | Stress engine: drivers and stop condition |
| 2 | ~2:20 | `point_in_time.py`: ALFRED snapshot and data card |
| 2 | ~3:20 | Tests (9/9), run live in the terminal |
| 3 | 0:00 | Live app shown first; two required statements |
| 3 | ~0:25 | Three-portfolio comparison and recommendation |
| 3 | ~1:10 | Point-in-time data card |
| 3 | ~1:35 | Stress tab and -100 bps kill rule (12.70% vol) |
| 3 | ~2:10 | Locked Changed-Input Record |
| 3 | ~2:45 | Reversal triggers and committee ask |

### Access confirmation

- [x] GitHub repository is public (verified).
- [x] Each video opened logged out / incognito and played (checked Nov 19, 2026).
- [ ] Same `.md` files attached to Brightspace.

---

## 3. Frozen Verification Checklist

- [x] A stranger can clone the repo and execute `streamlit run app.py` from the README without error.
- [x] Mandatory AI and Educational disclaimers open README, Decision Memo, and all video scripts.
- [x] Decision Memo, Validation Record, and Live App report identical numbers (Return: 6.50%, Vol: 9.30%, Res: 8.0%).
- [ ] Locked Changed-Input Record with AI-off prediction committed to Git before the run (LCIR-001 and LCIR-002; LCIR-002 prediction committed before the run).
- [x] Point-in-time data card documents dual timestamps, publication lags, and revision risk.
- [x] No private API keys, passwords, or personal credentials committed to Git.

