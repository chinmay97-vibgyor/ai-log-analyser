# from langchain_huggingface import HuggingFaceEmbeddings
# from langchain_chroma import Chroma
# from langchain_core.documents import Document
# from src.loader import load_log_file, chunk_lines
# from langchain_text_splitters import RecursiveCharacterTextSplitter

# def build_documents(file_path, chunk_size=500, chunk_overlap=100):
#     lines = load_log_file(file_path)
#     full_text = ''.join(lines)   # join all lines into one text block

#     splitter = RecursiveCharacterTextSplitter(
#         chunk_size=chunk_size,       # characters, not lines
#         chunk_overlap=chunk_overlap, # overlap preserves continuity across boundaries
#         separators=["\n\n", "\n", " ", ""]  # tries paragraph, then line, then word splits
#     )

#     text_chunks = splitter.split_text(full_text)

#     documents = []
#     ids = []
#     for i, chunk_text in enumerate(text_chunks):
#         doc = Document(
#             page_content=chunk_text,
#             metadata={
#                 "source": file_path,
#                 "chunk_index": i
#             }
#         )
#         documents.append(doc)
#         ids.append(f"{file_path}::chunk_{i}")

#     return documents, ids

# def create_vector_store(documents, ids, persist_directory="chroma_db_ailogs"):
#     embeddings = HuggingFaceEmbeddings(
#         model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
#     )
#     vector_store = Chroma.from_documents(
#         documents=documents,
#         embedding=embeddings,
#         ids=ids,                          # <-- this is what makes Option B work
#         persist_directory=persist_directory
#     )
#     return vector_store

import re
from datetime import datetime
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_text_splitters import RecursiveCharacterTextSplitter
from src.loader import load_log_file

TIMESTAMP_PATTERN = r"(\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2})"


def extract_timestamp_epoch(text):
    match = re.search(TIMESTAMP_PATTERN, text)
    if match:
        dt = datetime.strptime(match.group(1), "%Y-%m-%d %H:%M:%S")
        return dt.timestamp()
    return None


def build_documents(file_path, chunk_size=500, chunk_overlap=100):
    lines = load_log_file(file_path)
    full_text = ''.join(lines)

    splitter = RecursiveCharacterTextSplitter(
        chunk_size=chunk_size,
        chunk_overlap=chunk_overlap,
        separators=["\n\n", "\n", " ", ""]
    )
    text_chunks = splitter.split_text(full_text)

    documents = []
    ids = []
    for i, chunk_text in enumerate(text_chunks):
        timestamp_epoch = extract_timestamp_epoch(chunk_text)
        metadata = {
            "source": file_path,
            "chunk_index": i
        }
        if timestamp_epoch is not None:
            metadata["timestamp_epoch"] = timestamp_epoch

        doc = Document(page_content=chunk_text, metadata=metadata)
        documents.append(doc)
        ids.append(f"{file_path}::chunk_{i}")

    return documents, ids


def create_vector_store(documents, ids, persist_directory="chroma_db_ailogs"):
    embeddings = HuggingFaceEmbeddings(
        model_name="sentence-transformers/paraphrase-multilingual-mpnet-base-v2"
    )
    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embeddings,
        ids=ids,
        persist_directory=persist_directory
    )
    return vector_store