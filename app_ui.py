import streamlit as st
import requests

st.set_page_config(page_title="CodeReviewer AI", page_icon="🔍", layout="wide")

BACKEND_URL = "http://localhost:8000/analyze"

TRANSLATIONS = {
    "English": {
        "lang_code": "en",
        "title": "🔍 CodeReviewer AI",
        "subtitle": "Smart & Friendly Python Code Analysis",
        "input_header": "📝 Input Python Code",
        "input_label": "Paste your code here:",
        "upload_label": "Or upload a .py file:",
        "btn_analyze": "🚀 Analyze Code",
        "output_header": "📊 Analysis Summary",
        "score_label": "Code Health Score",
        "metric_lines": "Lines of Code",
        "metric_funcs": "Functions",
        "metric_classes": "Classes",
        "issues_header": "⚠️ Things to Look At:",
        "suggestions_header": "💡 Quick Tips for Improvement:",
        "empty_warning": "Please enter some Python code first!",
        "syntax_error": "Oops! There is a syntax error in your code.",
        "server_error": "Could not connect to the server: ",
        "default_code": '''def calculate_total(items):
    total = 0
    for item in items:
        total += item
    return total

def very_long_function_example():
    print("Line 1")
    print("Line 2")
    print("Line 3")
    print("Line 4")
    print("Line 5")
    print("Line 6")
    print("Line 7")
    print("Line 8")
    print("Line 9")
    print("Line 10")
    print("Line 11")
    print("Line 12")
    print("Line 13")
    print("Line 14")
    print("Line 15")
    print("Line 16")
'''
    },
    "فارسی": {
        "lang_code": "fa",
        "title": "🔍 CodeReviewer AI",
        "subtitle": "تحلیل هوشمند و دوستانه کدهای پایتون",
        "input_header": "📝 کد پایتون ورودی",
        "input_label": "کدت رو اینجا بنویس یا پیست کن:",
        "upload_label": "یا یک فایل .py آپلود کن:",
        "btn_analyze": "🚀 بررسی کیفیت کد",
        "output_header": "📊 خلاصه وضعیت کد",
        "score_label": "امتیاز سلامت کد",
        "metric_lines": "تعداد خط‌ها",
        "metric_funcs": "توابع",
        "metric_classes": "کلاس‌ها",
        "issues_header": "⚠️ مواردی که بهتره بررسی بشه:",
        "suggestions_header": "💡 پیشنهادهای خفن برای بهبود کد:",
        "empty_warning": "لطفاً اول یک قطعه کد وارد کن!",
        "syntax_error": "اوپس! یک خطای سینتکسی توی کدت وجود داره.",
        "server_error": "خطا در ارتباط با سرور: ",
        "default_code": '''def calculate_total(items):
    total = 0
    for item in items:
        total += item
    return total

def very_long_function_example():
    print("Line 1")
    print("Line 2")
    print("Line 3")
    print("Line 4")
    print("Line 5")
    print("Line 6")
    print("Line 7")
    print("Line 8")
    print("Line 9")
    print("Line 10")
    print("Line 11")
    print("Line 12")
    print("Line 13")
    print("Line 14")
    print("Line 15")
    print("Line 16")
'''
    }
}

with st.sidebar:
    st.header("⚙️ Settings / تنظیمات")
    language = st.radio("Language / زبان", ["English", "فارسی"])

t = TRANSLATIONS[language]
lang_code = t["lang_code"]

st.title(t["title"])
st.subheader(t["subtitle"])

col1, col2 = st.columns([1, 1])

with col1:
    st.markdown(f"### {t['input_header']}")
    code_input = st.text_area(t["input_label"], value=t["default_code"], height=350)
    
    uploaded_file = st.file_uploader(t["upload_label"], type=["py"])
    if uploaded_file is not None:
        code_input = uploaded_file.read().decode("utf-8")

    analyze_btn = st.button(t["btn_analyze"], type="primary", use_container_width=True)

with col2:
    st.markdown(f"### {t['output_header']}")
    
    if analyze_btn:
        if not code_input.strip():
            st.warning(t["empty_warning"])
        else:
            with st.spinner("Analyzing code... / در حال بررسی..."):
                try:
                    response = requests.post(BACKEND_URL, json={"code": code_input})
                    if response.status_code == 200:
                        data = response.json()
                        
                        if not data["valid_syntax"]:
                            st.error(f"{t['syntax_error']}\n\n`{data.get('error_message', '')}`")
                        else:
                            score = data["score"]
                            st.metric(label=t["score_label"], value=f"{score} / 100")
                            
                            metrics = data["metrics"]
                            m_col1, m_col2, m_col3 = st.columns(3)
                            m_col1.metric(t["metric_lines"], metrics["total_lines"])
                            m_col2.metric(t["metric_funcs"], metrics["functions_count"])
                            m_col3.metric(t["metric_classes"], metrics["classes_count"])
                            
                            st.divider()
                            
                            st.markdown(f"#### {t['issues_header']}")
                            for issue in data["issues"]:
                                text = issue.get(lang_code, issue.get("en"))
                                st.write(f"- {text}")
                                
                            st.markdown(f"#### {t['suggestions_header']}")
                            for sug in data["suggestions"]:
                                text = sug.get(lang_code, sug.get("en"))
                                st.write(f"- {text}")
                                
                except Exception as e:
                    st.error(f"{t['server_error']}{e}")