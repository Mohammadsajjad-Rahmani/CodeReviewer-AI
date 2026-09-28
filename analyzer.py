import ast

def analyze_python_code(code_str: str) -> dict:
    """
    Analyzes Python code string using the built-in `ast` module.
    Returns metrics, code smells, and user-friendly refactoring tips.
    """
    try:
        tree = ast.parse(code_str)
    except SyntaxError as e:
        return {
            "valid_syntax": False,
            "error_message": f"Syntax Error at line {e.lineno}: {e.msg}",
            "score": 0,
            "metrics": {},
            "issues": [],
            "suggestions": []
        }

    functions_count = 0
    classes_count = 0
    long_functions = []
    missing_docstrings = []
    issues = []
    suggestions = []

    # پیمایش ساختار درخت برای شناسایی توابع و کلاس‌ها
    for node in ast.walk(tree):
        if isinstance(node, ast.ClassDef):
            classes_count += 1

        elif isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef)):
            functions_count += 1
            
            # بررسی داشتن Docstring
            if not ast.get_docstring(node):
                missing_docstrings.append(node.name)
                
            # محاسبه طول تابع با در نظر گرفتن end_lineno (پایتون ۳.۸+)
            if hasattr(node, "end_lineno") and node.end_lineno:
                func_length = node.end_lineno - node.lineno + 1
            else:
                func_length = len(node.body)

            if func_length > 15:
                long_functions.append((node.name, func_length))

    score = 100

    if missing_docstrings:
        score -= len(missing_docstrings) * 10
        issues.append({
            "en": f"Functions missing docstrings: {', '.join(missing_docstrings)}",
            "fa": f"این توابع توضیح (Docstring) ندارند: {', '.join(missing_docstrings)}"
        })
        suggestions.append({
            "en": "Add a short docstring to your functions so others understand what they do.",
            "fa": "یک توضیح کوتاه (Docstring) به توابعت اضافه کن تا بقیه راحت‌تر کدتو بفهمن."
        })

    if long_functions:
        score -= len(long_functions) * 15
        for func_name, length in long_functions:
            issues.append({
                "en": f"Function '{func_name}' is a bit long ({length} lines).",
                "fa": f"تابع '{func_name}' یکم طولانیه ({length} خط)."
            })
        suggestions.append({
            "en": "Try breaking long functions into smaller, simpler ones.",
            "fa": "توابع طولانی رو به چند تا تابع کوچک‌تر و ساده‌تر تقسیم کن."
        })

    score = max(0, min(100, score))

    if not issues:
        issues.append({
            "en": "Great job! No major issues found.",
            "fa": "عالیه! هیچ مشکل خاصی پیدا نشد."
        })
    if not suggestions:
        suggestions.append({
            "en": "Your code looks clean and easy to read!",
            "fa": "کدت خیلی تمیز و خواناست!"
        })

    lines = [line for line in code_str.strip().split("\n") if line.strip()]

    return {
        "valid_syntax": True,
        "score": score,
        "metrics": {
            "total_lines": len(lines),
            "functions_count": functions_count,
            "classes_count": classes_count
        },
        "issues": issues,
        "suggestions": suggestions
    }