import os
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