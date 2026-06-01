import os
from langchain_groq import ChatGroq
from langchain_core.prompts import PromptTemplate
from dotenv import load_dotenv
from src.output_parser import parser

load_dotenv()

template = PromptTemplate(
    input_variables=["logs", "question"],
    partial_variables={"format_instruction": parser.get_format_instructions()},
    template="""
You are a log file analyzer. Your task is to analyze the provided log file and extract relevant information based on the user's query.
The log file is provided in chunks, and you should analyze each chunk to find the relevant information. The log file contains various entries, including timestamps, log levels (e.g., INFO, ERROR), and messages.
When analyzing the log file, consider the following:
1. Identify the log level of each entry (e.g., INFO, ERROR).
2. Extract the timestamp of each entry.
3. Summarize the message content of each entry.
4. Look for any patterns or anomalies in the log entries that may be relevant to the user's query.
5. Provide a concise summary of the relevant information extracted from the log file based on the user's query.
When responding to the user's query, ensure that your answer is clear, concise, and directly addresses the user's question based on the information extracted from the log file. If you find any relevant patterns or anomalies, include them in your response to provide a comprehensive analysis of the log file.

Log Data:
{logs}

User Question:
{question}

{format_instruction}

Provide a clear and concise answer based on the log data above.
"""
)

