from html_annotator import HTMLAnnotator
from config import (
    HTML_FILE_NAME,
    HTML_DIRECTORY,
    HTML_TEMPLATE_DIRECTORY,
    HTML_TEMPLATE_FILE_NAME,
    JSON_DIRECTORY,
    JSON_FILE_NAME,
    ANNOTATED_HTML_FILE,
    ANNOTATED_HTML_DIRECTORY
)

# Example usage
if __name__ == "__main__":
    annotator = HTMLAnnotator(
        template_directory=HTML_TEMPLATE_DIRECTORY,
        template_file=HTML_TEMPLATE_FILE_NAME,
    )
    annotator.load_html(html_directory=HTML_DIRECTORY, html_file=HTML_FILE_NAME)
    annotator.load_flaws(json_directory=JSON_DIRECTORY, json_file=JSON_FILE_NAME)
    annotator.annotate_html()
    annotator.save_annotated_html(html_directory=ANNOTATED_HTML_DIRECTORY, html_file=ANNOTATED_HTML_FILE)