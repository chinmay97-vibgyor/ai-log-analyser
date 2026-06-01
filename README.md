# AI Log Analyzer (V1)

A GenAI-powered log analysis tool that reads log files, chunks them, and uses an LLM to extract errors, warnings, and summaries based on user questions.

## Features
- Upload any `.log` or `.txt` file
- Ask natural language questions about your logs
- Get structured output — errors, warnings, and summary per chunk
- Built with LangChain and Groq (free tier)

## Tech Stack
- Python
- LangChain
- Groq API (llama-3.3-70b-versatile)
- Streamlit
- python-dotenv

## Project Structure
ai_log_analyser/
├── logs/                  # Sample log files
├── src/
│   ├── loader.py          # Load and chunk log files
│   ├── chain.py           # LLMChain setup
│   └── output_parser.py   # Structured output parser
├── prompts/
│   └── log_prompt.py      # PromptTemplate
├── vectorstore/           # For V2 (RAG)
├── main.py                # Streamlit app entry point
├── requirements.txt
└── README.md

## How to Run

**1. Clone the repo:**
git clone https://github.com/your-username/ai-log-analyser.git
cd ai-log-analyser

**2. Create and activate virtual environment:**
python -m venv venv
venv\Scripts\activate

**3. Install dependencies:**
pip install -r requirements.txt

**4. Add your Groq API key:**

Create a `.env` file in the root folder:
GROQ_API_KEY=your_groq_api_key_here

**5. Run the app:**
streamlit run main.py

## Usage
1. Upload a `.log` or `.txt` file
2. Type your question (e.g. "What errors occurred?")
3. Click **Analyze**
4. Get structured results — errors, warnings, and summary