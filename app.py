import streamlit as st
from utils import analyze_code

# ---------------- Page Config ---------------- #

st.set_page_config(
    page_title="NeuronCode AI",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
<style>

/* App Background */
.stApp{
    background-color: #0E1117;
}

/* Text Color */
h1, h2, h3, h4, h5, h6, p, label, span, div{
    color: white !important;
}

/* Buttons */
.stButton > button {
    background: linear-gradient(90deg, #2563EB, #3B82F6);
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px;
    font-weight: bold;
    width: 100%;
}

.stButton > button:hover {
    background: linear-gradient(90deg, #1D4ED8, #2563EB);
    color: white;
}

</style>
""", unsafe_allow_html=True)

st.markdown("""
<style>

.stApp {
    background-color: #0E1117;
    color: white;
}

</style>
""", unsafe_allow_html=True)

# ---------------- Session State ---------------- #

if "history" not in st.session_state:
    st.session_state.history = []

if "user_code" not in st.session_state:
    st.session_state.user_code = ""

# ---------------- Sidebar ---------------- #

st.sidebar.title("🤖 NeuronCode AI")

st.sidebar.success("🟢 Gemini AI Connected")

st.sidebar.markdown("---")

st.sidebar.caption("Version 1.0")

st.sidebar.markdown("""
### Features

✅ AI Code Review
✅ Bug Detection
✅ Code Optimization
✅ Explain Code
✅ Multi-Language Support
""")

st.sidebar.markdown("---")

st.sidebar.info(
    "Built with using Streamlit & Google Gemini AI."
)

st.sidebar.markdown("---")
st.sidebar.subheader("📜 Recent Analyses")

if len(st.session_state.history) == 0:
    st.sidebar.write("No analysis yet.")
else:
    for item in reversed(st.session_state.history[-5:]):
        st.sidebar.write(
            f"• {item['language']} | {item['mode']}"
        )

# ---------------- Main Page ---------------- #

a, b, c = st.columns([2,1,2])
with b:
    st.image("logo.png", width=150)


st.markdown("""
<h1 style='text-align:center; color:#3B82F6;'>
🤖 NeuronCode AI
</h1>

<h3 style='text-align:center; color:white;'>
Your AI Pair Programming Assistant 🚀
</h3>

<p style='text-align:center; color:lightgray; font-size:18px;'>
Analyze • Debug • Optimize • Explain Code using Google Gemini AI
</p>

<hr>
""", unsafe_allow_html=True)

left_col, right_col = st.columns(2)

# ===================================================
# LEFT COLUMN
# ===================================================

with left_col:

    st.subheader("💻 Code Editor")

    language = st.selectbox(
        "💻 Select Programming Language",
        [
            "Python",
            "Java",
            "C++",
            "JavaScript"
        ]
    )

    mode = st.selectbox(
        "🤖 AI Mode",
        [
            "Code Review",
            "Find Bugs",
            "Optimize Code",
            "Explain Code"
        ]
    )

    uploaded_file = st.file_uploader(
        "📂 Upload Code File",
        type=["py", "java", "cpp", "js"]
    )

    if uploaded_file is not None:
        st.session_state.user_code = uploaded_file.read().decode("utf-8")

    user_code = st.text_area(
        "Paste your code here:",
        key="user_code",
        height=320,
        placeholder="def hello():\n    print('Hello World')"
    )

    col1, col2 = st.columns(2)

    with col1:
        analyze_button = st.button(
            "🚀 Analyze Code",
            use_container_width=True
        )

    with col2:
        clear_button = st.button(
            "🗑️ Clear Code",
            use_container_width=True
        )

    if clear_button:
        st.session_state.user_code = ""
        st.rerun()

        # ===================================================
# RIGHT COLUMN
# ===================================================

with right_col:

    st.subheader("🤖 AI Analysis")

    score1, score2, score3 = st.columns(3)
    st.markdown("<br>", unsafe_allow_html=True)

    with score1:
        st.metric("⭐ Score", "--")

    with score2:
        st.metric("🐞 Bugs", "--")

    with score3:
        st.metric("💡 Tips", "--")

    st.markdown("---")

    if analyze_button:

        if user_code.strip() == "":
            st.warning("Please enter some code.")

        else:

            with st.spinner("🤖 AI is analyzing your code..."):
                result = analyze_code(
                    user_code,
                    language,
                    mode
                )

            analysis = result["analysis"]
            score = result["score"]

            score1.metric("⭐ Score", score)

            st.session_state.history.append({
                "language": language,
                "mode": mode,
                "result": analysis
            })

            st.markdown(analysis)

            st.download_button(
                label="📥 Download Analysis",
                data=analysis,
                file_name="analysis.md",
                mime="text/markdown"
            )

    else:
        st.info("AI response will appear here.")

# ---------------- Footer ---------------- #

st.markdown("---")

st.markdown(
    """
<div style='text-align:center;color:gray;'>
🤖 NeuronCode AI | Built with using Streamlit & Google Gemini AI
</div>
""",
    unsafe_allow_html=True
)