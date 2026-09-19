# CodeReviewer AI 🔍

A clean, lightweight, and bilingual Static Code Analysis tool for Python, built to inspect code quality and health without execution risks.

---

## 🌟 What It Does

- **Safe Code Inspection**: Uses Python's native `ast` module to analyze code structures without running untrusted code.
- **Health Scoring**: Generates a dynamic score (0–100) based on code structure, docstring presence, and function length.
- **Code Smell Detection**: Identifies syntax errors, overly long functions (>15 lines), and missing docstrings.
- **Bilingual Interface**: Supports seamless toggling between English and Persian for UI and report messages.

---

## 🛠️ Tech Stack

- **Backend:** FastAPI, Pydantic
- **Frontend:** Streamlit
- **Code Engine:** Python `ast` (Abstract Syntax Tree)
- **Package Manager:** `uv`

---

## 🚀 Quick Start

### 1. Clone
git clone https://github.com/Mohammadsajjad-Rahmani/CodeReviewer-AI.git
cd codereviewer-ai

### 2. Run Backend (FastAPI)
uv run uvicorn main:app --reload

### 3. Run Frontend (Streamlit)
uv run streamlit run app_ui.py

---

## 📝 Usage Example

**Input Code:**

**def calculate_total(items):**

    total = 0

    for item in items:

        total += item

    return total

**Output Report:**
- **Code Health Score:** 90 / 100
- **Metrics:** 1 Function | 5 Total Lines
- **Issues Found:** Function `calculate_total` is missing a docstring.
- **Suggestions:** Add a short docstring to improve code readability.

---

## 💡 Engineering Challenges & Solutions

### 1. Schema Mismatch in FastAPI (`ResponseValidationError`)
- **Problem:** When adding bilingual support, `analyzer.py` was updated to return localized dictionaries (`list[dict]`) instead of plain strings (`list[str]`). This triggered a `422/500 ResponseValidationError` in FastAPI because the Pydantic response schema still expected `list[str]`.
- **Solution:** Updated the `CodeAnalysisResponse` Pydantic model in `main.py` so that `issues` and `suggestions` fields match the `list[dict]` structure.

### 2. Inspecting Untrusted Code Safely
- **Problem:** Executing user-submitted code to analyze its quality creates severe security risks like Remote Code Execution (RCE).
- **Solution:** Leveraged Python's built-in `ast.parse()` to analyze code structure purely at the syntax tree level without executing a single line of code.