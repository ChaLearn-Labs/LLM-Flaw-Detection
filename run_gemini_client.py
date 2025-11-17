import os
from gemini_client import GeminiClient
from prompt import prompt_1 as PROMPT
from config import (
    GEMINI_MODEL,
    HTML_DIRECTORY, 
    HTML_FILE_NAME,
    JSON_DIRECTORY,
    JSON_FILE_NAME
)
from utils import (
    read_html_file,
    fill_paper_in_prompt,
    save_json_to_file,
    convert_json_string_to_json
)
from dotenv import load_dotenv
load_dotenv()
API_KEY = os.getenv("GEMINI_API_KEY")


if __name__ == "__main__":

    gemini = GeminiClient(api_key=API_KEY, model=GEMINI_MODEL)
    html_content = read_html_file(directory=HTML_DIRECTORY, filename=HTML_FILE_NAME)
    prompt = fill_paper_in_prompt(prompt=PROMPT, html_content=html_content)
    llm_response = gemini.generate_text(prompt)
    cleaned_llm_response = convert_json_string_to_json(llm_response)
    save_json_to_file(data=cleaned_llm_response, directory=JSON_DIRECTORY, filename=JSON_FILE_NAME)
