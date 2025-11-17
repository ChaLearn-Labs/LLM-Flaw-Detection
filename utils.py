import os
import json
import re


def read_html_file(directory: str, filename: str) -> str:
    """
    Reads an HTML file and returns its content as a string.

    Args:
        directory (str): Path to the directory containing the HTML file.
        filename (str): Name of the HTML file (e.g., 'paper.html').

    Returns:
        str: The content of the HTML file.
    """
    filepath = os.path.join(directory, filename)

    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"[-] File not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as file:
        content = file.read()

    return content


def read_json_file(directory: str, filename: str):
    """
    Reads a JSON file and returns its parsed content as a Python object.

    Args:
        directory (str): Path to the directory containing the JSON file.
        filename (str): Name of the JSON file (e.g., 'flaws.json').

    Returns:
        dict or list: Parsed JSON data from the file.
    """
    filepath = os.path.join(directory, filename)

    if not os.path.isfile(filepath):
        raise FileNotFoundError(f"[-] File not found: {filepath}")

    with open(filepath, "r", encoding="utf-8") as file:
        try:
            data = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"[-] Invalid JSON format in {filepath}: {e}")

    return data


def fill_paper_in_prompt(prompt: str, html_content: str) -> str:
    """
    Replaces the '{paper}' placeholder in the prompt with the HTML content.

    Args:
        prompt (str): The prompt template containing the placeholder '{paper}'.
        html_content (str): The HTML content of the paper.

    Returns:
        str: The prompt with the HTML content inserted.
    """
    if "{paper}" not in prompt:
        raise ValueError("[-] The prompt does not contain the '{paper}' placeholder.")

    return prompt.replace("{paper}", html_content)


def save_html_to_file(html_content: str, directory: str, filename: str) -> str:
    """
    Saves HTML content to a file.

    Args:
        html_content (str): The HTML content to save.
        directory (str): Path to the directory where the file will be saved.
        filename (str): Name of the HTML file (e.g., 'annotated.html').

    Returns:
        str: Full path to the saved HTML file.
    """
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    filepath = os.path.join(directory, filename)

    # Write the HTML content to the file
    with open(filepath, "w", encoding="utf-8") as f:
        f.write(html_content)

    return filepath


def save_json_to_file(data, directory: str, filename: str) -> str:
    """
    Saves a Python object (dict or list) as a JSON file.

    Args:
        data (dict or list): The data to save as JSON.
        directory (str): Path to the directory where the file will be saved.
        filename (str): Name of the JSON file (e.g., 'flaws.json').

    Returns:
        str: Full path to the saved JSON file.
    """
    # Ensure the directory exists
    os.makedirs(directory, exist_ok=True)

    filepath = os.path.join(directory, filename)

    # Write the JSON data to the file with pretty formatting
    with open(filepath, "w", encoding="utf-8") as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

    return filepath


def convert_json_string_to_json(json_string: str):
    """
    Converts a JSON string (possibly wrapped in markdown code blocks) into a Python JSON object.

    Args:
        json_string (str): The JSON string, possibly including markdown ```json ... ``` markers.

    Returns:
        dict or list: Parsed JSON object.
    """
    # Remove ```json ... ``` or ``` ... ``` markers
    cleaned_string = re.sub(r"^```(?:json)?\s*|\s*```$", "", json_string.strip(), flags=re.MULTILINE)

    # Convert to JSON object
    try:
        json_obj = json.loads(cleaned_string)
        return json_obj
    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON string provided. Error: {e}")
