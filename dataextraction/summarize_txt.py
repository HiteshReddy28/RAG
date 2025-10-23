import os
import json
from typing import Dict, List
import os
import sys

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(THIS_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)
from utils.format import generate_summary_from_html

def process_file(file_path: str, doc_id: int) -> Dict:
    """Process a single text file and return a structured dict with document ID.
    
    Args:
        file_path: Path to the text file
        doc_id: Unique document identifier
    """
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()

    # Get relative path and convert to URL path
    rel_path = os.path.relpath(
        file_path, 
        "uscis_extracted_text"
    )
    # Replace .txt with .html in the path and construct URL path
    url_path = "/" + os.path.splitext(rel_path)[0].replace("\\", "/") + ".html"
    
    # Get the formatted document from generate_summary_from_html
    doc = generate_summary_from_html(url=url_path, html_content=content)
    
    # Add document ID to the document
    doc['document_id'] = f"doc_{doc_id}"
    
    return doc

def main():
    input_dir = "uscis_extracted_text"
    output_file = "uscis_summary.json"
    
    if not os.path.isdir(input_dir):
        print(f"Error: Directory '{input_dir}' not found")
        return

    # Collect all .txt files
    all_files = []
    for root, _, files in os.walk(input_dir):
        for file in files:
            if not file.endswith(".txt"):
                continue
            all_files.append(os.path.join(root, file))

    total = len(all_files)
    if total == 0:
        print(f"No .txt files found in '{input_dir}'")
        return

    print(f"Found {total} text files, processing...")

    # Process all files
    documents = []
    for idx, file_path in enumerate(all_files, 1):
        try:
            # Pass both file path and document ID (using idx as the ID)
            doc = process_file(file_path, idx)
            documents.append(doc)
            print(f"[{idx}/{total}] Processed: {file_path} (ID: {doc['document_id']})")
        except Exception as e:
            print(f"[{idx}/{total}] Error processing {file_path}: {e}")

    # Save to JSON
    with open(output_file, "w", encoding="utf-8") as f:
        json.dump(
            {
                "total_documents": len(documents),
                "documents": documents
            },
            f,
            indent=2,
            ensure_ascii=False
        )

    print(f"\nDone! Saved {len(documents)} documents to {output_file}")

if __name__ == "__main__":
    main()