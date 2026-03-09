import streamlit as st
import google.generativeai as genai

# --- Page Config ---
st.set_page_config(
    page_title="Fake News Detector",
    page_icon="🗞️",
    layout="centered"
)

# --- Header ---
st.title("🗞️ Fake News Detector")
st.caption("Powered by Google Gemini (Free) — Paste a headline or article to analyze it.")

# --- API Key Input ---
api_key = st.sidebar.text_input(
    "🔑 Gemini API Key",
    type="password",
    placeholder="AIza...",
    help="Get your free key at aistudio.google.com"
)
st.sidebar.markdown("[🔗 Get a free API key](https://aistudio.google.com/app/apikey)")

# --- Input ---
st.markdown("### Paste your news content below")
input_type = st.radio("What are you analyzing?", ["Headline only", "Full article"], horizontal=True)
user_input = st.text_area(
    "News content",
    placeholder="e.g. 'Scientists discover that chocolate cures all diseases'",
    height=200 if input_type == "Full article" else 80
)

analyze_btn = st.button("🔍 Analyze", use_container_width=True, type="primary")

# --- Analysis ---
if analyze_btn:
    if not api_key:
        st.error("Please enter your Gemini API key in the sidebar. It's free at aistudio.google.com!")
    elif not user_input.strip():
        st.warning("Please paste some news content to analyze.")
    else:
        with st.spinner("Analyzing..."):
            try:
                genai.configure(api_key=api_key)
                model = genai.GenerativeModel("gemini-2.0-flash")

                prompt = f"""You are a professional fact-checker and media literacy expert. Analyze the following {"headline" if input_type == "Headline only" else "article"} for signs of fake news, misinformation, or clickbait.

Content to analyze:
\"\"\"{user_input}\"\"\"

Provide your analysis in this exact format:

VERDICT: [LIKELY REAL / LIKELY FAKE / CLICKBAIT / NEEDS VERIFICATION]

CONFIDENCE: [Low / Medium / High]

CREDIBILITY SCORE: [0-100]

RED FLAGS:
- List any red flags you spotted (or "None detected")

REASONING:
A clear 2-3 sentence explanation of your verdict.

ADVICE:
One actionable tip for the reader on how to verify this themselves."""

                response = model.generate_content(prompt)
                result = response.text

                # Parse and display results
                st.markdown("---")
                st.markdown("## 📊 Analysis Result")

                verdict_color = {
                    "LIKELY REAL": "🟢",
                    "LIKELY FAKE": "🔴",
                    "CLICKBAIT": "🟡",
                    "NEEDS VERIFICATION": "🟠"
                }

                lines = result.strip().split("\n")
                for line in lines:
                    if line.startswith("VERDICT:"):
                        verdict = line.replace("VERDICT:", "").strip()
                        emoji = next((v for k, v in verdict_color.items() if k in verdict.upper()), "⚪")
                        st.markdown(f"### {emoji} Verdict: **{verdict}**")
                    elif line.startswith("CONFIDENCE:"):
                        st.markdown(f"**{line}**")
                    elif line.startswith("CREDIBILITY SCORE:"):
                        score_text = line.replace("CREDIBILITY SCORE:", "").strip()
                        try:
                            score = int(score_text.split("/")[0].strip())
                            st.progress(score / 100, text=f"Credibility Score: {score}/100")
                        except:
                            st.markdown(f"**{line}**")
                    elif line.startswith("RED FLAGS:"):
                        st.markdown("#### 🚩 Red Flags")
                    elif line.startswith("REASONING:"):
                        st.markdown("#### 🧠 Reasoning")
                    elif line.startswith("ADVICE:"):
                        st.markdown("#### 💡 How to Verify")
                    elif line.strip():
                        st.markdown(line)

            except Exception as e:
                st.error(f"Error: {str(e)}\n\nMake sure your API key is correct!")

# --- Footer ---
st.markdown("---")
st.caption("Built for hackathon demo purposes. Always verify news from multiple trusted sources.")
