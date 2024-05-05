"""
ReaderScraper: Automated Domain-wise Content Aggregation from Web URLs
-----------------------------------------------------------------------
Author: Maxim Borzov

Description:
This script automates fetching web content using the Jina AI Reader API. It processes URLs from a file, saves contents into domain-specific folders,
and generates a summarizing file in each folder. This script supports optional command to summarize content across domains.

Usage:
-    To process URLs from 'url.txt' and save to domain-specific folders:
  $ python3 main.py

-    To create a summary file for all contents in a specific folder:
  $ python3 main.py --summarize [optional: folder name]
"""

import os
import sys
import argparse
import time
from urllib.parse import urlparse
from tqdm import tqdm


def check_and_install_packages():
    """Ensure all required packages are installed."""
    try:
        __import__('requests')
        __import__('tqdm')
    except ImportError as e:
        print(f"Missing required package: {e.name}")
        sys.exit("Please install it using the command: pip install " + e.name)


def process_url(reader_url, site_url):
    """Fetch content from Reader API for a given site URL."""
    import requests
    response = requests.get(f'{reader_url}{site_url}')
    return response.text if response.status_code == 200 else None


def extract_title(content):
    """Extract title from content based on its first line."""
    first_line = content.split('\n')[0]
    return first_line[7:].strip() if first_line.startswith('Title: ') else "Unknown Title"


def summarize_contents(output_dir, domain):
    """Create a domain summary file in the specific output directory."""
    if not os.path.exists(output_dir):
        os.makedirs(output_dir, exist_ok=True)
    
    summary_file_name = f"!{domain}_summarize.txt"
    summary_file_path = os.path.join(output_dir, summary_file_name)
    with open(summary_file_path, 'w') as summary_file:
        summary_file.write(f"Content summaries for {domain} are provided below:\n\n")
        for filename in sorted(os.listdir(output_dir)):
            if filename.endswith(".txt") and not filename.startswith("!"):
                path = os.path.join(output_dir, filename)
                with open(path, 'r') as content_file:
                    content = content_file.read()
                summary_file.write(f"{filename} content is:\n<content>{content}</content>\n\n")


def main():
    parser = argparse.ArgumentParser(description="Web content fetcher and summarizer with domain-specific organization.")
    parser.add_argument('--summarize', action='store_true', help="Create a summary file for all contents in a specified folder.")
    args = parser.parse_args()

    check_and_install_packages()

    reader_url = "https://r.jina.ai/"
    urls_filename = "url.txt"
    base_path = "scrape"
    processed_domains = set()
    start_time = time.time()

    if not os.path.exists(urls_filename):
        print(f"URL list file '{urls_filename}' not found.")
        return

    with open(urls_filename, 'r') as file:
        urls = [line.strip() for line in file if line.strip() and not line.strip().startswith('#')]

    successful_requests = 0
    failed_requests = 0
    total_content_length = 0

    for url in tqdm(urls, desc="Processing URLs"):
        parsed_url = urlparse(url)
        domain = parsed_url.netloc
        domain_path = os.path.join(base_path, domain)
        if not os.path.exists(domain_path):
            os.makedirs(domain_path)
            print(f"Created directory `{domain_path}` for domain {domain}.")

        content = process_url(reader_url, url)
        if content:
            successful_requests += 1
            title = extract_title(content)
            timestamp = int(time.time())
            filename = f"{timestamp}_{title}.txt"
            filepath = os.path.join(domain_path, filename)
            with open(filepath, 'w') as f:
                f.write(content)
            total_content_length += len(content)
        else:
            failed_requests += 1

        processed_domains.add(domain)

    for domain in processed_domains:
        domain_path = os.path.join(base_path, domain)
        summarize_contents(domain_path, domain)

    time_elapsed = time.time() - start_time
    print(f"\nProcessed {len(urls)} URLs in {time_elapsed:.2f} seconds.")
    print(f"Successful requests: {successful_requests}, Failed requests: {failed_requests}")
    print(f"Total content length: {total_content_length} characters")

if __name__ == "__main__":
    main()