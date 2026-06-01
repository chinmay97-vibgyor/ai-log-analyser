import streamlit as st
from src.loader import load_log_file_streamlit, chunk_lines
from src.chain import analyze_logs

st.title("AI Log Analyzer")

uploaded_file = st.file_uploader("Upload a log file", type=["log", "txt"])
question = st.text_input("Enter your question:")

if st.button("Analyze"):
    if uploaded_file and question:
        lines = load_log_file_streamlit(uploaded_file)
        chunks = chunk_lines(lines, chunk_size=5)
        for chunk in chunks:
            logs = ''.join(chunk)
            result = analyze_logs(logs, question)
            st.write(result)
    else:
        st.warning("Please upload a file and enter a question.")