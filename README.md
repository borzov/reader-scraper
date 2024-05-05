# ReaderScraper
## Simplifying Web Content Acquisition

### Introduction
**ReaderScraper** is a Python script tailored to simplify and automate the extraction of web content through the Jina AI Reader service (https://jina.ai/reader/). The service is useful especially when feeding web information into Large Language Models (LLMs), where the goal is grounding. Traditional methods, such as direct webpage scraping, face challenges like blocks or the complexity arising from handling raw HTML which includes unnecessary markups and scripts. By leveraging the Reader API, the script fetches the core content from given URLs and formats it into clean, LLM-friendly text; this streamlined text is free of extraneous elements, thus ensuring high-quality input for agent and RAG systems.

### Features
-  **Automated URL Processing:** Takes a list of URLs and fetches cleaned-up content.
-  **Summarization Mode:** Optionally combines all fetched contents into a single file for easier processing or review.
-  **User-friendly Configuration:** Easy to set up with minimal requirements and straightforward usage instructions.

### How It Works
1. **Reading URLs:** URLs should be listed in the `url.txt` file line by line. The script reads these URLs sequentially.
2. **Content Fetching:** For each URL, it constructs a request to the Reader API and retrieves the processed content.
3. **Content Saving:** Each piece of content is saved individually in a structured format. Optionally, all content can be summarized in a single file `!summarized.txt`.
4. **Summarization:** If enabled, this mode compiles the contents of all processed files into one, each section demarcated clearly for easy access.

### Operating Modes
The script can be run in two modes:
-  **Default mode:** Processes URLs and saves each output into separate files.
-  **Summarization mode (`--summarize` flag):** Processes URLs and additionally, compiles all outputs into a single file.

### Running the Script
To ensure smooth operation, it is recommended to run the script in a virtual environment. Here’s a step-by-step guide:
1. **Setup Virtual Environment** (assuming you have Python installed):
    ```sh
    python -m venv reader_scraper_env
    source reader_scraper_env/bin/activate  # For Unix/macOS
    reader_scraper_env\Scripts\activate     # For Windows
    ```
2. **Install Required Packages:**
    ```sh
    pip install requests tqdm
    ```
3. **Running ReaderScraper:**
    ```sh
    python ReaderScraper.py [--summarize]
    ```

### Preparing the URL List
-  Create or ensure the presence of a `url.txt` file in the same directory as the script.
-  Enter each URL on a new line without any additional text or prefixes.
-  Ensure URLs are valid and accessible to avoid errors during processing.

### Conclusion
**ReaderScraper** stands out by handling web content fetching and simplification tasks efficiently, providing a robust tool for integrating web-derived content into LLM workflows. Whether it's for enhancing data sets for training or model feeding, ReaderScraper ensures that the content it processes complies with high-quality standards needed for advanced computational models.

### License
This script is released under the MIT License.

---

This `README.md` provides an exhaustive guide to setting up, running, and utilizing **ReaderScraper**. It clarifies the importance of the Reader API in relation to LLMs and gives users all the needed information to start leveraging web content effectively in their models or systems.