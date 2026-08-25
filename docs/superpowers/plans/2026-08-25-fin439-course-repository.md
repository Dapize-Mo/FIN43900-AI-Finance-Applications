# FIN 439 Course Repository Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Create and publish a safe private GitHub repository for FIN 439 course planning, labs, and supporting materials.

**Architecture:** The existing FIN 439 workspace becomes the repository root. A small README and defensive `.gitignore` establish course conventions and credential safety; existing files remain intact. GitHub CLI creates the private remote and pushes the initial `main` branch.

**Tech Stack:** Git, GitHub CLI, Markdown, PowerShell

**Spec:** `docs/superpowers/specs/2026-08-25-fin439-course-repository-design.md`

## Global Constraints

- GitHub name: `FIN43900-AI-Finance-Applications`.
- Visibility: private.
- Local home: the existing FIN 439 workspace.
- Existing syllabus, `TASKS.md`, and dashboard remain intact.
- Secrets, API keys, tokens, passwords, credentials, and private data must never be committed.
- Empty organizational folders are not created until they have real content.
- Major projects remain here initially and may move only when Brightspace instructions require or materially favor separate repositories.

---

### Task 1: Establish the Local Course Repository

**Files:**
- Create: `.gitignore`
- Create: `README.md`
- Preserve: `TASKS.md`
- Preserve: `dashboard.html`
- Preserve: `WL-Fall-2026-FIN-(WL)-43900-001-AI-Finance-Applications.pdf`
- Preserve: `docs/superpowers/specs/2026-08-25-fin439-course-repository-design.md`
- Preserve: `docs/superpowers/plans/2026-08-25-fin439-course-repository.md`

**Interfaces:**
- Consumes: the current workspace and approved repository design.
- Produces: a local Git repository on `main` with one clean, reviewable initial commit.

- [ ] **Step 1: Confirm the workspace is not already a Git repository**

Run: `git status --short --branch`

Expected: failure stating that the folder is not a Git repository.

- [ ] **Step 2: Create the safety-focused `.gitignore`**

Include Python virtual environments and caches, `.env` variants except `.env.example`, credentials and key files, editor files, OS clutter, build outputs, and temporary files. Do not ignore the syllabus, Markdown planning files, or dashboard.

- [ ] **Step 3: Create the repository README**

Document the course purpose, current organization, local-first/GitHub workflow, Brightspace authority, Edition A boundary, AI disclosure and validation responsibility, and credential rules.

- [ ] **Step 4: Initialize Git on `main`**

Run: `git init -b main`

Expected: a new repository with `main` as the current branch.

- [ ] **Step 5: Audit files before staging**

Run: `git status --short --ignored`

Expected: intended course files are untracked, while any local secrets, environments, caches, and temporary files are ignored.

- [ ] **Step 6: Scan candidate files for likely secrets**

Review tracked candidates for private keys, credential filenames, and common token or password assignments. If a likely secret is found, stop before staging and remove it from the candidate set.

- [ ] **Step 7: Create the initial commit**

Run: `git add .`

Run: `git diff --cached --check`

Run: `git commit -m "chore: initialize FIN 439 course workspace"`

Expected: one commit containing the preserved course files, README, `.gitignore`, specification, and plan.

- [ ] **Step 8: Verify the local repository**

Run: `git status --short --branch`

Expected: `## main` with no uncommitted changes.

### Task 2: Publish and Verify the Private GitHub Repository

**Files:**
- Modify: `.git/config` through GitHub CLI remote setup

**Interfaces:**
- Consumes: the clean local `main` branch from Task 1 and an authenticated GitHub CLI session.
- Produces: a private GitHub repository named `FIN43900-AI-Finance-Applications`, an `origin` remote, and a pushed `main` branch.

- [ ] **Step 1: Verify GitHub CLI availability and authentication**

Run: `gh --version`

Run: `gh auth status`

Expected: GitHub CLI is installed and authenticated to the intended GitHub account. If authentication is missing, stop for the user-controlled sign-in flow.

- [ ] **Step 2: Check for a pre-existing repository with the target name**

Run: `gh repo view FIN43900-AI-Finance-Applications --json name,visibility,url`

Expected: repository not found. If it exists, inspect it and stop rather than overwrite or repoint anything.

- [ ] **Step 3: Create and push the private repository**

Run: `gh repo create FIN43900-AI-Finance-Applications --private --source . --remote origin --push`

Expected: the private repository is created, `origin` is configured, and `main` is pushed.

- [ ] **Step 4: Verify privacy and remote configuration**

Run: `gh repo view FIN43900-AI-Finance-Applications --json name,visibility,url,defaultBranchRef`

Expected: visibility is `PRIVATE` and the default branch is `main`.

Run: `git remote -v`

Expected: fetch and push URLs for `origin` point to the new FIN 439 repository.

- [ ] **Step 5: Verify synchronization and cleanliness**

Run: `git status --short --branch`

Expected: local `main` tracks `origin/main` with no uncommitted changes.

