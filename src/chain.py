import os
import re
from datetime import datetime
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from src.output_parser import parser
from prompts.log_prompt import template

load_dotenv()

llm = ChatGroq(
    model="llama-3.3-70b-versatile",
    api_key=os.getenv("GROQ_API_KEY"),
    temperature=0.0,
)

chain = template | llm | parser

def analyze_logs(logs, question):
    return chain.invoke({"logs": logs, "question": question})


# --- time-range detection ---
FULL_DATETIME_RANGE = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})\s*(?:and|to|-)\s*(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"
SINGLE_DATE = r"(\d{4}-\d{2}-\d{2})"
TIME_ONLY_RANGE = r"(\d{2}:\d{2}:\d{2})\s*(?:and|to|-)\s*(\d{2}:\d{2}:\d{2})"


def detect_time_range(question):
    match = re.search(FULL_DATETIME_RANGE, question)
    if match:
        start_dt = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
        end_dt = datetime.strptime(match.group(2), "%Y-%m-%d %H:%M:%S")
        return start_dt.timestamp(), end_dt.timestamp()

    time_match = re.search(TIME_ONLY_RANGE, question)
    if time_match:
        date_match = re.search(SINGLE_DATE, question)
        if date_match:
            log_date = date_match.group(1)
            start_dt = datetime.strptime(f"{log_date} {time_match.group(1)}", "%Y-%m-%d %H:%M:%S")
            end_dt = datetime.strptime(f"{log_date} {time_match.group(2)}", "%Y-%m-%d %H:%M:%S")
            return start_dt.timestamp(), end_dt.timestamp()

        return "AMBIGUOUS"

    return None


# --- exhaustive query detection ---
EXHAUSTIVE_KEYWORDS = ["all", "every", "entire", "complete", "full list", "each"]

def is_exhaustive_query(question):
    question_lower = question.lower()
    return any(keyword in question_lower for keyword in EXHAUSTIVE_KEYWORDS)


# --- RAG-based analysis ---
def analyze_logs_rag(question, vector_store, k=3):
    time_range = detect_time_range(question)

    if time_range == "AMBIGUOUS":
        return {
            "errors": "N/A",
            "warnings": "Please specify a date in the question (format: YYYY-MM-DD) so I can filter logs correctly for the given time range.",
            "summary": "Could not process time-based query — a specific date is required alongside the time range."
        }

    if time_range:
        start_epoch, end_epoch = time_range
        relevant_docs = vector_store.similarity_search(
            question, k=20,
            filter={
                "$and": [
                    {"timestamp_epoch": {"$gte": start_epoch}},
                    {"timestamp_epoch": {"$lte": end_epoch}}
                ]
            }
        )
        context = "\n".join([doc.page_content for doc in relevant_docs])
        return chain.invoke({"logs": context, "question": question})

    if is_exhaustive_query(question):
        all_data = vector_store.get()
        context = "\n".join(all_data["documents"])
        return chain.invoke({"logs": context, "question": question})

    relevant_docs = vector_store.similarity_search(question, k=k)
    context = "\n".join([doc.page_content for doc in relevant_docs])
    return chain.invoke({"logs": context, "question": question})