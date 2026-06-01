def load_log_file(file_path):
    with open(file_path, 'r') as file:
        lines = file.readlines()
    return lines

def load_log_file_streamlit(uploaded_file):
    lines = uploaded_file.read().decode("utf-8").splitlines(keepends=True)
    return lines

def chunk_lines(lines, chunk_size=5):
    chunks = [lines[i:i+chunk_size] for i in range(0, len(lines), chunk_size)]
    return chunks