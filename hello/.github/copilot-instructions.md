<!-- Auto-generated for this repository. Edit only to add repository-specific guidance. -->
# Copilot / AI Agent Instructions (repository-specific)

This repository is minimal and contains a single Python script. The instructions below are focused, actionable, and tailored so an AI coding agent can be productive immediately.

- **Repository root / entry point**: `hello.py` — single-file script, no package layout.
- **Run locally**: use the user's default shell (Windows PowerShell v5.1). Example: `python hello.py` from the repository root (`c:\Users\123\hello`).
- **No virtualenv / deps file present**: there's no `requirements.txt` or `pyproject.toml` detected. If you add external packages, also add `requirements.txt` and a short README note explaining the environment.

- **Project purpose & constraints (discoverable)**:
  - Small demo or placeholder script — avoid large refactors or scaffold generation unless requested.
  - No tests, CI, or build tooling present — adding them requires an explicit user request.

- **When modifying code**:
  - Keep changes minimal and focused to the user request (single-file edits are expected).
  - If you add files or dependencies, update `README.md` (create if missing) with run instructions and list new files.
  - Preserve Windows PowerShell examples in run instructions (the user environment is Windows).

- **Committing / PR guidance for the agent**:
  - Create small, self-contained commits with descriptive messages (e.g., `fix: handle empty input in hello.py`).
  - If you create a new module or tests, include a one-paragraph note in `README.md` describing how to run them.

- **What NOT to assume**:
  - Do not assume a virtual environment manager (venv/conda) or CI configuration exists.
  - Do not rewrite repository structure (e.g., convert to package) without asking the user.

- **Useful examples from this repo**:
  - Entry: `hello.py` — use it to show runnable examples, small refactors, or to add logging.

- **Helpful small tasks you can perform autonomously**:
  - Fix a bug in `hello.py` when user shows failing output; run `python hello.py` in PowerShell to validate.
  - Add a `requirements.txt` if you introduce third-party packages, and update `README.md` accordingly.
  - Add a lightweight test file `test_hello.py` using `unittest` if asked; include run instructions (`python -m unittest`).

- **Merging guidance (if `.github/copilot-instructions.md` already exists)**:
  - Preserve any existing repository-specific bullets; append or update only items that reflect currently discoverable structure.
  - Do not remove historical notes unless they are incorrect based on current files.

If any part of the repository changes or you add more files, re-scan and update these instructions accordingly. Reply with any missing context you'd like the agent to know (CI provider, desired testing framework, packaging plans, etc.).

---
Edited by AI assistant: created initial repository-specific guidance — please review and tell me what to clarify or expand.
