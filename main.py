"""
ReaderScraper: Web Scraping and Summarization Tool
--------------------------------------------------
ReaderScraper is designed to facilitate the extraction of web content via the Jina AI Reader service (https://jina.ai/reader/).
It automates the handling of a list of URLs for parsing and can optionally aggregate the content of all processed pages into a single file.
This single file is particularly useful for bulk upload into Large Language Models (LLMs) for further processing or analysis.

Usage:
1. Create or ensure 'url.txt' exists in the same directory as this script with web URLs listed line by line.
2. Run the script. Use `--summarize` option if you want to aggregate all output content into a single file.

Example:
  python ReaderScraper.py --summarize

Author: Maxim Borzov
GitHub Profile: https://github.com/borzov
"""

import os
import sys
import argparse

def check_and_install_packages():
    """Check and install required packages"""
    required_packages = ['requests', 'tqdm']
    missing_packages = []
    for package in required_packages:
        try:
            __import__(package)
        except ImportError:
            missing_packages.append(package)
    if missing_packages:
        print("The following packages are required but not installed:")
        print(", ".join(missing_packages))
        print("Please install them using the command:")
        print("pip install " + " ".join(missing_packages))
        sys.exit(1)

def prepare_urls_file(filename):
    """Ensure that URL file exists or create it with instructions"""
    if not os.path.exists(filename):
        print(f"No URL file found. Creating a sample file: {filename}")
        with open(filename, 'w') as file:
            file.write("# Enter each URL on a new line followed by a newline.\n")
        print(f"Please populate the {filename} file with URLs.")
        sys.exit(1)

def process_url(reader_url, site_url):
    """Fetch processed content from Reader for a given site URL"""
    import requests  # Import locally to allow package check before import
    response = requests.get(f'{reader_url}{site_url}')
    if response.status_code == 200:
        return response.text
    else:
        return None

def extract_title(content):
    """Extract title from content"""
    first_line = content.split('\n')[0]
    if first_line.startswith('Title: '):
        return first_line[7:]
    return "Unknown Title"

def summarize_contents(output_dir):
    """Generate a summary file of all contents"""
    summary_file_path = os.path.join(output_dir, "!summarized.txt")
    with open(summary_file_path, 'w') as summary_file:
        summary_file.write("The following blocks contain web page content, organized separately. Do not use <content> tags in your responses.\n\n")

        for file_name in os.listdir(output_dir):
            if file_name.endswith(".txt") and not file_name.startswith("!"):
                with open(os.path.join(output_dir, file_name), 'r') as content_file:
                    file_content = content_file.read()
                    summary_file.write(f"{file_name} content is:\n<content>{file_content}</content>\n\n")

def main():
    """Main function to orchestrate the crawling process with optional content summarization"""
    parser = argparse.ArgumentParser(description="Web scraper and content aggregator for use with Jina AI Reader service")
    parser.add_argument("--summarize", help="Create a summary file for all contents", action="store_true")
    args = parser.parse_args()

    check_and_install_packages()

    reader_url = "https://r.jina.ai/"
    urls_filename = "url.txt"
    output_dir = "scrape"
    
    prepare_urls_file(urls_filename)

    import requests
    from tqdm import tqdm

    if not os.path.exists(output_dir):
        os.makedirs(output_dir)

    with open(urls_filename, 'r') as file:
        urls = [line.strip() for line in file if not line.strip().startswith("#") and line.strip()]

    for index, url in enumerate(tqdm(urls, desc="Processing URLs")):
        if url:
            content = process_url(reader_url, url)
            if content:
                title = extract_title(content)
                filename = f"{index + 1} - {title}.txt"
                file_path = os.path.join(output_dir, filename)
                with open(file_path, 'w') as output_file:
                    output_file.write(content)
            else:
                print(f"Failed to retrieve content for URL: {url}")

    if args.summarize:
        summarize_contents(output_dir)

if __name__ == "__main__":
    main()
