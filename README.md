# AI Log Analyzer (V2)

A GenAI-powered log analysis tool that reads log files, embeds them into a vector store, and uses a RAG (Retrieval-Augmented Generation) pipeline to answer natural language questions about errors, warnings, and summaries — grounded in the actual log content.

## Features
- Upload any `.log` or `.txt` file
- Ask natural language questions about your logs
- Semantic search — retrieves only the relevant chunks for a question instead of scanning the whole file
- Time-range aware querying — e.g. "errors between 2024-03-15 03:00:00 and 2024-03-15 06:00:00"
- Exhaustive query handling — e.g. "fetch all errors" pulls the full log instead of a top-k subset
- Persistent vector store (ChromaDB) with deduplication on re-indexing
- Get structured output — errors, warnings, and summary
- Built with LangChain, ChromaDB, HuggingFace embeddings, and Groq (free tier)

## Tech Stack
- Python
- LangChain
- ChromaDB (vector store)
- HuggingFace Embeddings (`paraphrase-multilingual-mpnet-base-v2`)
- Groq API (llama-3.3-70b-versatile)
- Streamlit
- python-dotenv

## Project Structure
ai_log_analyser/
├── logs/                  # Sample and uploaded log files
├── src/
│   ├── loader.py          # Load log files
│   └── chain.py           # LLM chain, RAG retrieval, time-range & exhaustive query detection
├── vectorstore/
│   └── vec_store.py       # Chunking, embedding, vector store creation
├── prompts/
│   └── log_prompt.py      # PromptTemplate
├── src/output_parser.py   # Structured output parser
├── chroma_db_ailogs/      # Persisted vector store (generated, gitignored)
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
2. Type your question, for example:
   - `What caused the Stripe webhook error?`
   - `Fetch all the errors from the logs and summarize them`
   - `Summarize the errors between 2024-03-15 03:00:00 and 2024-03-15 06:00:00`
3. Click **Analyze**
4. Get structured results — errors, warnings, and summary

**Note on time-based questions:** include both a date and time in this format for accurate filtering:
YYYY-MM-DD HH:MM:SS to YYYY-MM-DD HH:MM:SS

If only a time is given without a date, the app will ask you to specify one instead of guessing.

## Design Decisions & Known Limitations
- **Chunking uses `RecursiveCharacterTextSplitter` with overlap** instead of fixed-line chunks — this prevents multi-line content like stack traces from being split across chunk boundaries and losing context.
- **Time-range questions bypass semantic search** and use a metadata filter on extracted timestamps instead — vector similarity search can't reliably reason about numeric date/time ranges.
- **"Fetch all" style questions bypass top-k retrieval** and pull the entire log instead — otherwise only the top 3 most "similar" chunks would be used, silently missing most of the actual errors. This works for moderately sized logs; very large log files would need a different strategy (e.g. batched summarization) to avoid hitting context window limits.
- **Re-indexing on every upload** — the app currently re-embeds the file on every "Analyze" click rather than checking if it's already indexed.

## Roadmap
- Multi-file upload and ingestion in a single session
- Persistent, incremental indexing (avoid re-embedding unchanged files)
- Source attribution in answers (which file/chunk an answer came from)
- Advanced retrievers — MultiQueryRetriever, ContextualCompressionRetriever