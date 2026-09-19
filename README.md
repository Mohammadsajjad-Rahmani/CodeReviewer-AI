# CodeReviewer AI

An intelligent, bilingual Static Code Analysis and Quality Assessment tool for Python code, built with FastAPI, Streamlit, and Python native Abstract Syntax Tree (ast) module.

## Features
- Abstract Syntax Tree (AST) Parsing: Safely analyzes Python source code structure without code execution.
- Dynamic Health Scoring: Calculates a quality score (0-100) based on structural metrics and code smell checks.
- Code Smell & Anti-Pattern Detection: Highlights overly long functions, missing docstrings, and syntax errors with line precision.
- Actionable Refactoring Tips: Provides user-friendly, clean code recommendations.
- Bilingual & Friendly UI (English / Persian): Seamless toggle between English and Persian interface and report messages.
- RESTful API Architecture: Powered by FastAPI with typed Pydantic request/response schemas.

## Tech Stack
- Backend: Python 3.11+, FastAPI, Uvicorn, Pydantic
- Frontend: Streamlit
- Code Engine: Python Native ast (Abstract Syntax Tree) module
- Package Manager: uv

---

## Engineering Challenges & Solutions (Interview Prep)

### Challenge 1: Multi-Language Schema Mismatch in FastAPI (ResponseValidationError)
- Problem: When introducing bilingual support (EN/FA) for issues and suggestions, analyzer.py was updated to return localized dictionaries (list[dict]) instead of plain strings (list[str]). This caused FastAPI to throw a ResponseValidationError (422/500) because the Pydantic schema in main.py still expected list[str].
- Solution: Refactored the CodeAnalysisResponse Pydantic model in main.py to match the data payload by updating issues and suggestions fields to list[dict].
- Takeaway: Always ensure strict synchronization between domain logic data structures and API validation schemas (Pydantic).

### Challenge 2: Parsing Unsafe Code Without Execution Risk
- Problem: Running untrusted user code to check for quality is a massive security risk (RCE / Code Injection).
- Solution: Used Python built-in ast.parse() module. AST parses code into an Abstract Syntax Tree purely at the syntax/grammar level without executing a single line of Python code.

---

## Getting Started

### Prerequisites
Make sure you have uv installed.

### 1. Clone & Setup Environment
git clone https://github.com/YOUR_USERNAME/codereviewer-ai.git
cd codereviewer-ai
uv sync

### 2. Run Backend Server
uv run uvicorn main:app --reload

The API will be available at http://localhost:8000 (Swagger docs at http://localhost:8000/docs).

### 3. Run Streamlit UI
In a separate terminal, execute:
uv run streamlit run app_ui.py

## API Endpoints
- GET /: Health check endpoint.
- POST /analyze: Accepts a Python code payload and returns metrics, score, issues, and localized refactoring suggestions.