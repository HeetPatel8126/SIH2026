"""
scrape_bis.py — Tech 2 ingestion: pulls text from confirmed BIS source pages,
strips navigation/footer junk, saves clean .txt files + a metadata index.

USAGE:
    pip install requests beautifulsoup4
    python ingestion/scrape_bis.py

Output:
    data/raw/<capability>_<number>.txt   (one file per source page)
    data/raw/_index.csv                  (filename -> url, capability, title)
"""

import os
import re
import csv
import time
import requests
from bs4 import BeautifulSoup

# --- Confirmed sources, organized by capability (from corpus_sources_final.md) ---
SOURCES = [
    ("standards_qa", "https://www.bis.gov.in/know-your-standard/?lang=en"),
    ("standards_qa", "https://www.bis.gov.in/product-certification/products-under-compulsory-certification/?lang=en"),
    ("certification_schemes", "https://www.bis.gov.in/product-certification/product-certification-overivews/?lang=en"),
    ("certification_schemes", "https://www.bis.gov.in/product-certification/products-under-compulsory-certification/scheme-i-mark-scheme/?lang=en"),
    ("certification_schemes", "https://www.services.bis.gov.in/php/BIS_2.0/BISBlog/product-certification-scheme/"),
    ("process_explainer", "https://www.bis.gov.in/product-certification/product-certification-process/"),
    ("consumer_queries", "https://www.bis.gov.in/system-certification-overview/public-grievance/complaints/?lang=en"),
    ("hallmarking", "https://www.bis.gov.in/hallmarking-overview/hallmarking-faqs/hallmarking-faq/?lang=en"),
    ("hallmarking", "https://www.bis.gov.in/hallmarking-jewellers/?lang=en"),
    ("hallmarking", "https://www.bis.gov.in/hallmarking-overview/consumer-protection/?lang=en"),
    ("hallmarking", "https://www.bis.gov.in/hallmarking-overview/?lang=en"),
    ("lab_suggestion", "https://www.bis.gov.in/laboratorys/list-of-laboratories/"),
    ("lab_suggestion", "https://www.bis.gov.in/laboratorys/list-of-bis-recognized-lab/"),
    ("lab_suggestion", "https://www.bis.gov.in/directory/laboratory/?lang=en"),
]

# Lines that are clearly repeating site navigation/footer junk (seen across
# multiple BIS pages) — anything matching these gets dropped.
JUNK_PATTERNS = [
    r"^Complaints\s*·",
    r"^Appeals\s*·",
    r"FMCS\s*·\s*Overview",
    r"^Registration Scheme\s*·",
    r"^Scheme-X Certification",
    r"^Laboratory Services",
    r"^Ministry login",
]

OUTPUT_DIR = "data/raw"
MIN_LINE_WORDS = 6  # drop very short lines (usually nav labels, not real content)


def is_junk_line(line: str) -> bool:
    for pattern in JUNK_PATTERNS:
        if re.search(pattern, line):
            return True
    if len(line.split()) < MIN_LINE_WORDS:
        return True
    return False


def scrape_page(url: str) -> tuple[str, str]:
    """Returns (title, cleaned_text) for one URL."""
    headers = {"User-Agent": "Mozilla/5.0 (compatible; BIS-Assistant-Ingestion/1.0)"}
    resp = requests.get(url, headers=headers, timeout=20)
    resp.raise_for_status()
    resp.encoding = "utf-8"  # force correct decoding — fixes mojibake like "â€“" instead of "–"

    soup = BeautifulSoup(resp.text, "html.parser")

    # Remove obviously non-content tags entirely
    for tag in soup(["script", "style", "nav", "header", "footer", "aside", "form"]):
        tag.decompose()

    title = soup.title.string.strip() if soup.title and soup.title.string else url

    # Pull all paragraph-like text
    raw_lines = []
    for el in soup.find_all(["p", "li", "h1", "h2", "h3"]):
        text = el.get_text(separator=" ", strip=True)
        if text:
            raw_lines.append(text)

    # Filter out junk/nav lines
    clean_lines = [line for line in raw_lines if not is_junk_line(line)]

    cleaned_text = "\n\n".join(clean_lines)
    return title, cleaned_text


def main():
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    index_rows = []
    counters = {}

    for capability, url in SOURCES:
        counters[capability] = counters.get(capability, 0) + 1
        n = counters[capability]
        filename = f"{capability}_{n}.txt"
        filepath = os.path.join(OUTPUT_DIR, filename)

        print(f"Scraping [{capability}] {url} ...")
        try:
            title, text = scrape_page(url)
        except Exception as e:
            print(f"  FAILED: {e}")
            continue

        if len(text.split()) < 30:
            print(f"  WARNING: very little content extracted ({len(text.split())} words) — check manually.")

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(f"SOURCE URL: {url}\nTITLE: {title}\n\n{text}")

        index_rows.append({
            "filename": filename,
            "capability": capability,
            "title": title,
            "url": url,
            "word_count": len(text.split()),
        })
        print(f"  Saved: {filename} ({len(text.split())} words)")
        time.sleep(1)  # be polite to the server

    index_path = os.path.join(OUTPUT_DIR, "_index.csv")
    with open(index_path, "w", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=["filename", "capability", "title", "url", "word_count"])
        writer.writeheader()
        writer.writerows(index_rows)

    print(f"\nDone. {len(index_rows)} documents saved to {OUTPUT_DIR}/")
    print(f"Index saved to {index_path}")


if __name__ == "__main__":
    main()