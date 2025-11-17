# LLM-Flaw-Detection

This repository provides code that can be used to download an arxiv html paper, clean it, run it through an LLM (Gemini) to detect flaws and annotate the flaws in an html

To run the pipeline follow the steps below

### Step 1: Configure `.env`
Copy the `.env_sample` as `.env` and place your Gemini API Key at the right place in this file
```
cp .env_sample .env
```

### Step 2: Configure `config.py`
Configure the `config.py` file for naming the result files, arxiv paper html link, gemini model name etc.

### Step 3: Execute `run_html_downloader.py`
Execute the script `run_html_downloader.py` to download an arxiv html, clean the html and save the cleaned version.  

⚠️ NOTE: This step uses configuration from `config.py`

### Step 4: Execute `run_gemini_client.py`
Execute the script `run_gemini_client.py` to process the cleaned html and detect flaws in the paper and save the flaws in a json file.  

⚠️ NOTE: This step uses configuration from `config.py`

### Step 5: Execute `run_html_annotator.py`
Execute the script `run_html_annotator.py` to use the detected flaws and the cleaned html to produce an annotated html that visualizes the flaws.

⚠️ NOTE: This step uses configuration from `config.py`
