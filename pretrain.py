import os
import time
import requests
from urllib.parse import urlparse
from webscraper import scrape_website
from documentsaver import save_scraped_text
from vector_store import store_in_vector_db

PDF_EXT = (".pdf",)
CSV_EXT = (".csv",)
TXT_EXT = (".txt", ".text")
DATA_DIR = "data/scraped_docs"

def download_file(url, save_dir=DATA_DIR):
    os.makedirs(save_dir, exist_ok=True)
    local_filename = os.path.join(save_dir, os.path.basename(urlparse(url).path))
    try:
        with requests.get(url, stream=True) as r:
            r.raise_for_status()
            with open(local_filename, 'wb') as f:
                for chunk in r.iter_content(chunk_size=8192):
                    f.write(chunk)
        print(f"Downloaded file: {local_filename}")
        return local_filename
    except Exception as e:
        print(f"Download failed for {url}: {e}")
        return None

def pretrain_from_urls(file_path="urls.txt"):
    with open(file_path, "r") as f:
        urls = [line.strip() for line in f if line.strip()]

    for url in urls:
        lower_url = url.lower()
        if lower_url.endswith(PDF_EXT) or ".pdf" in lower_url:
            print(f"Detected PDF: {url}")
            download_file(url)

        elif lower_url.endswith(CSV_EXT) or ".csv" in lower_url:
            print(f"Detected CSV: {url}")
            download_file(url)

        elif lower_url.endswith(TXT_EXT):
            print(f"Detected Text File: {url}")
            download_file(url)

        else:
            print(f"Scraping web page: {url}")
            content = scrape_website(url)
            if "Error" not in content and len(content) > 100:
                save_scraped_text(content)
                print(f"Scraped and saved: {url}")
            else:
                print(f"Failed to scrape or empty content: {url}")

        time.sleep(1) 

    print("\nStarting vector DB creation...")
    store_in_vector_db()
    print("Knowledge base pretrained successfully.")

if __name__ == "__main__":
    pretrain_from_urls()
