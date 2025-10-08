import os
import json
from openai import OpenAI

client = OpenAI()

MEMORY_DIR = "memory"

def store_summary(file_path, summary):
    """Store summarized info about a file in the memory directory."""
    os.makedirs(MEMORY_DIR, exist_ok=True)
    file_name = os.path.basename(file_path)
    memory_file = os.path.join(MEMORY_DIR, f"{file_name}.json")

    data = {"file": file_name, "summary": summary}
    with open(memory_file, "w") as f:
        json.dump(data, f)

def get_all_summaries():
    """Retrieve all saved file summaries."""
    summaries = []
    if not os.path.exists(MEMORY_DIR):
        return summaries

    for file in os.listdir(MEMORY_DIR):
        if file.endswith(".json"):
            with open(os.path.join(MEMORY_DIR, file)) as f:
                summaries.append(json.load(f))
    return summaries

def summarize_code(code):
    """Use OpenAI to summarize a given code snippet."""
    prompt = f"Summarize this code in one short paragraph:\n\n{code}"
    response = client.responses.create(
        model="gpt-4o-mini",
        input=prompt
    )
    return response.output[0].content[0].text

def process_file_for_memory(file_path):
    """Read a code file, summarize it, and store its memory."""
    with open(file_path, "r") as f:
        code = f.read()

    summary = summarize_code(code)
    store_summary(file_path, summary)
    print(f"✅ Memory stored for: {file_path}")
