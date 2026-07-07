# import streamlit as st
# from src.loader import load_log_file_streamlit, chunk_lines
# from src.chain import analyze_logs

# st.title("AI Log Analyzer")

# uploaded_file = st.file_uploader("Upload a log file", type=["log", "txt"])
# question = st.text_input("Enter your question:")

# if st.button("Analyze"):
#     if uploaded_file and question:
#         lines = load_log_file_streamlit(uploaded_file)
#         chunks = chunk_lines(lines, chunk_size=5)
#         for chunk in chunks:
#             logs = ''.join(chunk)
#             result = analyze_logs(logs, question)
#             st.write(result)
#     else:
#         st.warning("Please upload a file and enter a question.")

# import streamlit as st
# from vectorstore.vec_store import build_documents, create_vector_store
# from src.chain import analyze_logs_rag

# st.title("AI Log Analyzer")

# uploaded_file = st.file_uploader("Upload a log file", type=["log", "txt"])
# question = st.text_input("Enter your question:")

# if st.button("Analyze"):
#     if uploaded_file and question:
#         # save uploaded file temporarily so build_documents can read it
#         temp_path = f"logs/{uploaded_file.name}"
#         with open(temp_path, "wb") as f:
#             f.write(uploaded_file.getbuffer())

#         docs, ids = build_documents(temp_path)
#         vs = create_vector_store(docs, ids)

#         result = analyze_logs_rag(question, vs)
#         st.write(result)
#     else:
#         st.warning("Please upload a file and enter a question.")

import streamlit as st
from vectorstore.vec_store import build_documents, create_vector_store
from src.chain import analyze_logs_rag

st.title("AI Log Analyzer")

st.caption(
    "💡 Asking about a specific time range? Use this format: "
    "`errors between 2024-03-15 03:00:00 and 2024-03-15 06:00:00` "
    "— both a date and time are required for accurate filtering."
)

uploaded_file = st.file_uploader("Upload a log file", type=["log", "txt"])
question = st.text_input("Enter your question:")

if st.button("Analyze"):
    if uploaded_file and question:
        temp_path = f"logs/{uploaded_file.name}"
        with open(temp_path, "wb") as f:
            f.write(uploaded_file.getbuffer())

        docs, ids = build_documents(temp_path)
        vs = create_vector_store(docs, ids)

        result = analyze_logs_rag(question, vs)
        st.write(result)
    else:
        st.warning("Please upload a file and enter a question.")