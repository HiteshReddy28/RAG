import os
import sys
from bs4 import BeautifulSoup

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(THIS_DIR, os.pardir))
if PROJECT_ROOT not in sys.path:
    sys.path.insert(0, PROJECT_ROOT)

from utils.extract import uscis_extract

input_root = "uscis_body_html"
output_root = "uscis_extracted_text"

# Supported file extensions (quick include)
EXTS = (".html", ".htm")

# Heuristic: if a file doesn't have an HTML extension, inspect its first
# few KB for HTML markers like '<html' or '<!doctype html' (case-insensitive).
def looks_like_html(path: str, sniff_bytes: int = 4096) -> bool:
    try:
        with open(path, "rb") as f:
            start = f.read(sniff_bytes).lower()
        return b"<html" in start or b"<!doctype html" in start
    except Exception:
        return False

# Collect all files under input_root (user confirmed every file contains HTML)
targets = []
for root, _, files in os.walk(input_root):
    for file in files:
        targets.append(os.path.join(root, file))

total = len(targets)
if total == 0:
    print(f"No HTML files found under '{input_root}'")
else:
    print(f"Found {total} HTML files under '{input_root}', starting extraction...")

for idx, input_path in enumerate(targets, start=1):
    try:
        relative_path = os.path.relpath(input_path, input_root)
        output_path = os.path.join(output_root, os.path.splitext(relative_path)[0] + ".txt")

        os.makedirs(os.path.dirname(output_path), exist_ok=True)

        # read defensively to avoid decode errors
        with open(input_path, "r", encoding="utf-8", errors="replace") as f:
            html_content = f.read()

        extracted_text = uscis_extract(html_content)

        with open(output_path, "w", encoding="utf-8") as f:
            f.write(extracted_text)

        print(f"[{idx}/{total}] Extracted: {input_path} → {output_path}")
    except Exception as e:
        print(f"[{idx}/{total}] ERROR processing {input_path}: {e}")
        # continue with next file
