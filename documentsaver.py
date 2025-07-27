import os
import hashlib
import json
from uuid import uuid4

PROCESSED_LOG = "data/scraped_docs/.processed.json"

def load_processed_files():
    if os.path.exists(PROCESSED_LOG):
        with open(PROCESSED_LOG, "r") as f:
            return json.load(f)
    return {}

def save_processed_file_record(file_id, metadata):
    record = load_processed_files()
    record[file_id] = metadata
    os.makedirs(os.path.dirname(PROCESSED_LOG), exist_ok=True)
    with open(PROCESSED_LOG, "w") as f:
        json.dump(record, f, indent=2)

def get_text_hash(content: str):
    return hashlib.sha256(content.encode("utf-8")).hexdigest()

def save_scraped_text(content, output_dir="data/scraped_docs"):
    os.makedirs(output_dir, exist_ok=True)
    file_hash = get_text_hash(content)
    processed = load_processed_files()

    if file_hash in processed:
        print(f"Already processed content: {file_hash}")
        return None

    file_path = os.path.join(output_dir, f"web_doc_{uuid4().hex}.txt")
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

    save_processed_file_record(file_hash, {"source": file_path})
    return file_path
