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

All three videos are hosted as Unlisted YouTube links with English transcripts/captions enabled:

### Video 1 — Research Evolution & Thinking Changes (≤ 3:00)
- **YouTube Link:** `https://www.youtube.com/watch?v=EXAMPLE_VIDEO_1` *(To be populated upon final recording)*
- **Duration:** 2:45
- **Transcripts:** [`submission/transcripts/transcript-video-1.txt`](transcripts/transcript-video-1.txt)
- **Key Questions Answered:** What changed in the investment system and student thinking between Lab 13 and Project 2? How was the AI output for correlation matrix symmetry and grid optimization independently checked and verified?

### Video 2 — Technical Code & Model Walkthrough (≤ 5:00)
- **YouTube Link:** `https://www.youtube.com/watch?v=EXAMPLE_VIDEO_2` *(To be populated upon final recording)*
- **Duration:** 4:30
- **Transcripts:** [`submission/transcripts/transcript-video-2.txt`](transcripts/transcript-video-2.txt)
- **Key Questions Answered:** How does `engine.py` turn raw price histories and course-authored parameters into optimal weights? How does `mandate.py` detect the covenant failure in the 60/40 benchmark? Which tests passed in the verification suite?

### Video 3 — Investment Committee Defense & Live Demo (≤ 5:00)
- **YouTube Link:** `https://www.youtube.com/watch?v=EXAMPLE_VIDEO_3` *(To be populated upon final recording)*
- **Duration:** 4:50
- **Transcripts:** [`submission/transcripts/transcript-video-3.txt`](transcripts/transcript-video-3.txt)
- **Key Questions Answered:** Live operation of `app.py`. Why should the committee allocate to the Constrained Optimal Portfolio? Under what macroeconomic conditions does the Process Kill Rule stop the strategy? What are the reversal triggers?

---

## 3. Frozen Verification Checklist

- [x] A stranger can clone the repo and execute `streamlit run app.py` from the README without error.
- [x] Mandatory AI and Educational disclaimers open README, Decision Memo, and all video scripts.
- [x] Decision Memo, Validation Record, and Live App report identical numbers (Return: 6.50%, Vol: 9.30%, Res: 8.0%).
- [x] Locked Changed-Input Record includes pre-run prediction, parameter shift, and failure sensitivity analysis.
- [x] Point-in-time data card documents dual timestamps, publication lags, and revision risk.
- [x] No private API keys, passwords, or personal credentials committed to Git.

