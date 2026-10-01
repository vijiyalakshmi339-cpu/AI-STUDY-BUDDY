import os
import streamlit as st
from google import genai

# If you get a "model not found" error, change this name
MODEL = "gemini-2.5-flash"

st.set_page_config(page_title="AI Study Buddy", page_icon="📚")
st.title("📚 AI Study Buddy")
st.caption("Your AI-powered personal learning assistant")

# API key: from Streamlit secrets, env variable, or sidebar box (never hard-code it)
api_key = os.getenv("GEMINI_API_KEY", "")
try:
    api_key = st.secrets.get("GEMINI_API_KEY", api_key)
except Exception:
    pass
if not api_key:
    api_key = st.sidebar.text_input("Enter Gemini API Key", type="password")

level = st.sidebar.selectbox("Explain like I am in", ["School", "College", "Beginner"])


def ask_ai(prompt):
    if not api_key:
        return "Please enter your Gemini API key in the sidebar."
    try:
        client = genai.Client(api_key=api_key)
        response = client.models.generate_content(model=MODEL, contents=prompt)
        return response.text
    except Exception as e:
        return f"Error: {e}"


tab1, tab2, tab3 = st.tabs(["❓ Ask Doubt", "📝 Summarize Notes", "🧠 Quiz"])

with tab1:
    q = st.text_area("Type your doubt")
    if st.button("Get Answer"):
        if q.strip():
            with st.spinner("Thinking..."):
                st.write(ask_ai(f"Explain in simple words for a {level} student with an example:\n{q}"))
        else:
            st.warning("Please type a question.")

with tab2:
    notes = st.text_area("Paste your notes here", height=200)
    if st.button("Summarize"):
        if notes.strip():
            with st.spinner("Summarizing..."):
                st.write(ask_ai(f"Summarize these notes in short bullet points for a {level} student:\n{notes}"))
        else:
            st.warning("Please paste some notes.")

with tab3:
    topic = st.text_input("Enter a topic")
    n = st.slider("Number of questions", 3, 10, 5)
    if st.button("Generate Quiz"):
        if topic.strip():
            with st.spinner("Creating quiz..."):
                st.write(ask_ai(
                    f"Create {n} multiple-choice questions on '{topic}' for a {level} student. "
                    "Give 4 options each, then the answers at the end."
                ))
        else:
            st.warning("Please enter a topic.")
