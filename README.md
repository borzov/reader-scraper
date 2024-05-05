# ReaderScraper: Enhanced Web Content Aggregation Tool

### Introduction
ReaderScraper is a powerful Python script designed to simplify and automate the extraction of web content through the Jina AI Reader API. This tool processes URLs from a provided text file and efficiently organizes content into domain-specific folders. Moreover, it automatically generates a summarizing file for each domain, highlighting the script's ability to manage and compile information seamlessly.

### Features
-  **Domain-Specific Organization:** Automatically saves content into respective domain-named folders.
-  **Automatic Summary File Creation:** Generates a summary text file within each domain folder to aggregate content details.
-  **Timestamp Naming Convention:** Enhances file management by prefixing filenames with a timestamp, ensuring uniqueness across executions.
-  **Batch Processing with Virtual Environment:** Includes a bash script (`run.sh`) to handle virtual environment setup, script execution, and environment teardown, streamlining the entire operation.

### Usage
1. **Prepare URL List:**
   - Create a `url.txt` file in the project’s root directory.
   - Add URLs to the file, each on a new line.

2. **Running the Script:**
   - Directly via Python:
     ```
     python3 main.py
     ```
   - Using the provided bash script to manage virtual environments:
     ```
     ./run.sh [--summarize] [optional: folder name]
     ```
   The bash script `run.sh` helps in setting up a Python virtual environment, running the script, and then cleaning up the environment. It passes additional parameters directly to the Python script.

### Changelog for Version 0.2
-  **Domain-Specific Folders:** Content is now saved into folders named after the domains of the URLs processed.
-  **Summary Files:** Each domain folder gets a summary file named with a prefix to clearly denote it is a summarized document.
-  **Timestamp in Filenames:** Introduced a timestamp prefix in filenames to prevent overwrites and to track when content was pulled.
-  **Script Runner (`run.sh`):** Added a bash script for easy virtual environment management and script execution.

### Virtual Environment and Script Runner (run.sh)
The `run.sh` bash script facilitates a smoother operation by automating the environment setup and script execution process. Here’s how it works:
-  **Creates a virtual environment** named `env` if it doesn't exist.
-  **Activates the virtual environment**, runs the Python script with any provided command-line arguments, and then deactivates the environment.

This tool is perfect for users seeking an efficient way to handle multiple web contents for aggregation and summarization without manually managing dependencies and virtual environments.

---

Feel free to copy and use this updated `README.md` text directly for the project documentation for ReaderScraper v0.2. This version reflects both technical enhancements and usability improvements while providing comprehensive instructions and support for new users.