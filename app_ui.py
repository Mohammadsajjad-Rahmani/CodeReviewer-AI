import requests
import streamlit as st

# تنظیمات اولیه صفحه
st.set_page_config(
    page_title="CodeReviewer AI",
    page_icon="🔍",
    layout="wide",
    initial_sidebar_state="expanded",
)

BACKEND_URL = "http://localhost:8000/analyze"

# دیکشنری متون و ترجمه‌ها
TRANSLATIONS = {
    "English": {
        "lang_code": "en",
        "title": "CodeReviewer AI",
        "subtitle": "Smart & Automated Python Code Analysis",
        "input_header": "📝 Source Code Input",
        "input_label": "Paste your Python code below:",
        "upload_label": "Upload a .py file",
        "btn_analyze": "🚀 Analyze Code",
        "output_header": "📊 Analysis Dashboard",
        "score_label": "Health Score",
        "metric_lines": "Lines of Code",
        "metric_funcs": "Functions",
        "metric_classes": "Classes",
        "issues_header": "⚠️ Issues Identified",
        "suggestions_header": "💡 Refactoring Tips",
        "empty_warning": "Please enter or upload Python code to analyze.",
        "syntax_error": "Syntax Error Detected!",
        "server_error": "Server connection failed: ",
        "tab_overview": "📈 Overview",
        "tab_issues": "⚠️ Issues & Recommendations",
        "default_code": """def calculate_total(items):
    total = 0
    for item in items:
        total += item
    return total

def process_heavy_data_without_docstring():
    print("Step 1")
    print("Step 2")
    print("Step 3")
    print("Step 4")
    print("Step 5")
    print("Step 6")
    print("Step 7")
    print("Step 8")
    print("Step 9")
    print("Step 10")
    print("Step 11")
    print("Step 12")
    print("Step 13")
    print("Step 14")
    print("Step 15")
    print("Step 16")
""",
    },
    "فارسی": {
        "lang_code": "fa",
        "title": "سامانه هوشمند CodeReviewer AI",
        "subtitle": "تحلیل خودکار و بررسی کیفیت کدهای پایتون",
        "input_header": "📝 کد ورودی پایتون",
        "input_label": "کد پایتون خود را در باکس زیر وارد کنید:",
        "upload_label": "یا یک فایل py. آپلود کنید",
        "btn_analyze": "🚀 شروع بررسی کیفیت کد",
        "output_header": "📊 داشبورد تحلیل کد",
        "score_label": "امتیاز سلامت کد",
        "metric_lines": "تعداد خطوط",
        "metric_funcs": "توابع",
        "metric_classes": "کلاس‌ها",
        "issues_header": "⚠️ موارد قابل بهبود (Issues)",
        "suggestions_header": "💡 پیشنهادهای بازسازی کد (Refactoring)",
        "empty_warning": "لطفاً ابتدا کدی برای بررسی وارد کنید!",
        "syntax_error": "خطای سینتکسی در کد یافت شد!",
        "server_error": "ارتباط با سرور برقرار نشد: ",
        "tab_overview": "📈 نگاه کلی",
        "tab_issues": "⚠️ مشکلات و پیشنهادها",
        "default_code": """def calculate_total(items):
    total = 0
    for item in items:
        total += item
    return total

def process_heavy_data_without_docstring():
    print("Step 1")
    print("Step 2")
    print("Step 3")
    print("Step 4")
    print("Step 5")
    print("Step 6")
    print("Step 7")
    print("Step 8")
    print("Step 9")
    print("Step 10")
    print("Step 11")
    print("Step 12")
    print("Step 13")
    print("Step 14")
    print("Step 15")
    print("Step 16")
""",
    },
}

# --- انتخاب زبان از سایدبار ---
with st.sidebar:
    st.markdown("### ⚙️ تنظیمات / Settings")
    language = st.radio("زبان / Language", ["فارسی", "English"])
    st.divider()
    st.markdown(
        """
        <div style="font-size: 0.85rem; color: #888;">
            <b>CodeReviewer AI v1.0</b><br>
            Powered by Python AST & FastAPI
        </div>
        """,
        unsafe_allow_html=True,
    )

t = TRANSLATIONS[language]
lang_code = t["lang_code"]

# --- اصلاح دقیق استایل‌ها بدون آسیب زدن به انیمیشن سایدبار ---
common_css = """
<style>
    .custom-card {
        background-color: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 20px;
        margin-bottom: 20px;
        box-shadow: 0 4px 12px rgba(0, 0, 0, 0.05);
    }
    div.stButton > button:first-child {
        border-radius: 8px;
        font-weight: bold;
        font-size: 1rem;
        height: 3em;
        transition: all 0.3s ease;
    }
</style>
"""

rtl_css = """
<style>
    /* اعمال RTL صرفا روی بدنه اصلی محتوا (Main Content Area) */
    section.main > div {
        direction: rtl;
        text-align: right;
    }
    
    /* تنظیمات اختصاصی سایدبار برای جلوگیری از باگ انیمیشن */
    section[data-testid="stSidebar"] {
        direction: rtl;
        text-align: right;
        overflow-x: hidden !important;
    }
    
    /* چپ‌چین نگه داشتن ناحیه ویرایشگر کد */
    textarea {
        direction: ltr !important;
        text-align: left !important;
        font-family: 'Fira Code', 'Consolas', monospace !important;
    }
</style>
"""

st.markdown(common_css, unsafe_allow_html=True)
if lang_code == "fa":
    st.markdown(rtl_css, unsafe_allow_html=True)

# --- هدر اصلی برنامه ---
st.title(t["title"])
st.caption(t["subtitle"])
st.write("---")

# --- چیدمان اصلی ---
col_input, col_output = st.columns([1.1, 0.9], gap="large")

# === ستون سمت چپ: ورودی کد ===
with col_input:
    st.markdown(f"### {t['input_header']}")

    uploaded_file = st.file_uploader(
        t["upload_label"], type=["py"], help="فایل پایتون خود را بکشید و رها کنید"
    )

    if uploaded_file is not None:
        input_text = uploaded_file.read().decode("utf-8")
    else:
        input_text = t["default_code"]

    code_input = st.text_area(
        t["input_label"], value=input_text, height=380, key="code_editor"
    )

    analyze_btn = st.button(
        t["btn_analyze"], type="primary", use_container_width=True
    )

# === ستون سمت راست: خروجی داشبورد ===
with col_output:
    st.markdown(f"### {t['output_header']}")

    if analyze_btn:
        if not code_input.strip():
            st.warning(t["empty_warning"])
        else:
            with st.spinner("در حال آنالیز ساختار کد..."):
                try:
                    response = requests.post(
                        BACKEND_URL, json={"code": code_input}, timeout=10
                    )

                    if response.status_code == 200:
                        data = response.json()

                        if not data["valid_syntax"]:
                            st.error(t["syntax_error"])
                            st.code(
                                data.get("error_message", ""), language="text"
                            )
                        else:
                            score = data["score"]
                            score_color = (
                                "#22c55e"
                                if score >= 80
                                else "#f59e0b"
                                if score >= 50
                                else "#ef4444"
                            )

                            st.markdown(
                                f"""
                                <div class="custom-card" style="text-align: center; border-left: 6px solid {score_color};">
                                    <span style="font-size: 1.1rem; color: #888;">{t['score_label']}</span>
                                    <h1 style="font-size: 3.2rem; color: {score_color}; margin: 5px 0;">{score} <span style="font-size: 1.5rem;">/ 100</span></h1>
                                </div>
                                """,
                                unsafe_allow_html=True,
                            )

                            tab_overview, tab_details = st.tabs(
                                [t["tab_overview"], t["tab_issues"]]
                            )

                            with tab_overview:
                                metrics = data["metrics"]
                                m1, m2, m3 = st.columns(3)
                                m1.metric(
                                    t["metric_lines"], metrics["total_lines"]
                                )
                                m2.metric(
                                    t["metric_funcs"], metrics["functions_count"]
                                )
                                m3.metric(
                                    t["metric_classes"], metrics["classes_count"]
                                )

                            with tab_details:
                                st.markdown(f"#### {t['issues_header']}")
                                for issue in data["issues"]:
                                    msg = issue.get(
                                        lang_code, issue.get("en", "")
                                    )
                                    st.warning(msg, icon="⚠️")

                                st.markdown(f"#### {t['suggestions_header']}")
                                for sug in data["suggestions"]:
                                    msg = sug.get(lang_code, sug.get("en", ""))
                                    st.info(msg, icon="💡")

                except Exception as e:
                    st.error(f"{t['server_error']} `{e}`")
    else:
        st.info("کد خود را در بخش سمت چپ وارد کرده و دکمه بررسی را بزنید.")