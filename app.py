import streamlit as st
import google.generativeai as genai

# Page config
st.set_page_config(
    page_title="TruthLens AI",
    page_icon="🗞️",
    layout="centered"
)

st.title("🗞️ TruthLens AI")
st.caption("AI-powered misinformation analyzer using Google Gemini")

# --- API KEY ---
api_key = None

# Try Streamlit secrets first
if "GEMINI_API_KEY" in st.secrets:
    api_key = st.secrets["GEMINI_API_KEY"]
else:
    api_key = st.sidebar.text_input(
        "🔑 Gemini API Key",
        type="password",
        help="Get one free at https://aistudio.google.com/app/apikey"
    )

# Sidebar info
st.sidebar.markdown("[🔗 Get a free Gemini API key](https://aistudio.google.com/app/apikey)")

# --- Input ---
st.markdown("### Paste news content below")

input_type = st.radio(
    "What are you analyzing?",
    ["Headline only", "Full article"],
    horizontal=True
)

user_input = st.text_area(
    "News content",
    placeholder="Scientists discover chocolate cures all diseases",
    height=200 if input_type == "Full article" else 80
)

analyze_btn = st.button("🔍 Analyze", use_container_width=True)

# --- Analysis ---
if analyze_btn:

    if not api_key:
        st.error("Please enter your Gemini API key.")
        st.stop()

    if not user_input.strip():
        st.warning("Please paste some news content.")
        st.stop()

    try:
        genai.configure(api_key=api_key)
        model = genai.GenerativeModel("gemini-1.5-flash")

        prompt = f"""
You are a professional fact-checker.

Analyze the following {"headline" if input_type=="Headline only" else "news article"}.

CONTENT:
{user_input}

Respond EXACTLY in this format:

VERDICT: [LIKELY REAL / LIKELY FAKE / CLICKBAIT / NEEDS VERIFICATION]

CONFIDENCE: [Low / Medium / High]

CREDIBILITY SCORE: [0-100]

RED FLAGS:
- bullet points

REASONING:
2 sentence explanation.

ADVICE:
One tip to verify this claim.
"""

        with st.spinner("Analyzing..."):
            response = model.generate_content(prompt)

        result = ""

        if response and hasattr(response, "text"):
            result = response.text
        else:
            result = "Model returned no response."

        st.markdown("---")
        st.markdown("## 📊 Analysis Result")

        st.markdown(result)

    except Exception as e:
        st.error(f"Error: {str(e)}")

# Footer
st.markdown("---")
st.caption("Demo project. Always verify information with trusted sources.")
