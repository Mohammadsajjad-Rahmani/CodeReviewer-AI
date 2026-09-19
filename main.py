from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from analyzer import analyze_python_code

app = FastAPI(
    title="CodeReviewer AI API",
    description="Static Code Analysis and Quality Assessment API",
    version="1.0.0"
)

class CodeRequest(BaseModel):
    code: str

# تایپ لیست‌ها از list[str] به list[dict] تغییر کرد
class CodeAnalysisResponse(BaseModel):
    valid_syntax: bool
    score: int
    metrics: dict
    issues: list[dict]
    suggestions: list[dict]
    error_message: str | None = None

@app.get("/")
def read_root():
    return {"status": "ok", "message": "CodeReviewer AI Service is running"}

@app.post("/analyze", response_model=CodeAnalysisResponse)
def analyze_code(payload: CodeRequest):
    if not payload.code.strip():
        raise HTTPException(status_code=400, detail="Code payload cannot be empty.")
    
    result = analyze_python_code(payload.code)
    return result