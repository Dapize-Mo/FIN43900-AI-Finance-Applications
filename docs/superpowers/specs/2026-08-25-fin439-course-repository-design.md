# FIN 439 Course Repository Design

## Purpose

Create a private, durable home for FIN 439 course planning, weekly lab work, and supporting materials. The repository will preserve development history from the beginning while keeping major-project organization flexible until the authoritative Brightspace instructions are published.

## Repository

- GitHub name: `FIN43900-AI-Finance-Applications`
- Visibility: private
- Local home: the existing FIN 439 workspace
- Existing syllabus, `TASKS.md`, and dashboard remain intact

## Initial structure

- `weeks/` for weekly exercises and class artifacts
- `labs/` for durable lab outputs when a lab produces one
- `notes/` for course notes and planning
- `projects/` for project planning and local working areas
- `docs/` for repository-level documentation and decisions

The structure will remain intentionally small. Empty folders will not be created merely for appearance; each folder will appear when it has real content.

## Repository safeguards

- A `.gitignore` will exclude virtual environments, caches, local environment files, credentials, generated clutter, and common editor artifacts.
- Secrets, API keys, tokens, passwords, credentials, and private data will never be committed.
- A `.env.example` may later document required variable names using empty placeholder values.
- The README will explain the course purpose, working conventions, AI-disclosure responsibility, and the Edition A boundary.

## Major projects

Course-wide planning and labs will live in this repository initially. Project 1, Project 2, and the capstone may move into separate private repositories if the applicable Brightspace assignment instructions require or materially favor independent submission repositories.

## Verification

After setup:

1. Confirm the local repository is on the expected default branch.
2. Confirm the GitHub remote is private.
3. Confirm the initial push succeeds.
4. Confirm ignored credential and environment files are not tracked.
5. Confirm existing workspace files remain present.
