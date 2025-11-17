import re
from utils import (
    read_json_file,
    read_html_file,
    save_html_to_file
)
from jinja2 import Environment, FileSystemLoader


class HTMLAnnotator:
    def __init__(self, template_directory, template_file):
        """
        Initialize the annotator with an optional template path.
        """
        self.template_directory = template_directory
        self.template_file = template_file
        self.html_paper = ""
        self.flaws = []
        self.annotated_html = ""

    def load_html(self, html_directory, html_file):
        """
        Load the HTML paper into memory.
        """
        self.html_paper = read_html_file(directory=html_directory, filename=html_file)
        print("[+] Loaded HTML from file")

    def load_flaws(self, json_directory, json_file):
        """
        Load the flaws JSON file into memory.
        """
        self.flaws = read_json_file(directory=json_directory, filename=json_file)
        print("[+] Loaded Flaws from file")

    def _map_flaw_category_to_template(self, cat_str: str) -> str:
        """
        Map a flaw_category string like '1a', '3b', '4c' to template class 'cat1'–'cat5'.
        """
        match = re.match(r"(\d)", str(cat_str))
        if match:
            num = match.group(1)
            return f"cat{num}"
        return "cat1"  # default fallback

    def _get_flaw_count(self) -> dict:
        """
        Count the number of flaws per category (cat1–cat5) and return as a dict.
        """
        counts = {f"cat{i}": 0 for i in range(1, 6)}

        for flaw in self.flaws:
            cat_key = flaw.get("flaw_category", "")
            if cat_key:
                # Map the first digit of flaw_category to cat1–cat5
                match = re.match(r"(\d)", str(cat_key))
                if match:
                    num = match.group(1)
                    cat_class = f"cat{num}"
                    if cat_class in counts:
                        counts[cat_class] += 1
        return counts

    def annotate_html(self) -> None:
        """
        Function to annotate html with flaws
        Wrap flaw text in <span> with category and confidence classes.
        Uses 'start_of_flaw' and 'end_of_flaw' to locate the exact text.
        """

        html_content = self.html_paper

        for flaw in self.flaws:
            start_text = flaw.get("start_of_flaw")
            end_text = flaw.get("end_of_flaw")
            category_key = flaw.get("flaw_category")
            severity = flaw.get("flaw_severity", "N/A")
            confidence = flaw.get("flaw_confidence", 3)
            description = flaw.get("flaw_description", "")

            if not start_text or not end_text or not category_key:
                continue  # skip invalid flaw entry

            # Map category to template class
            category_class = self._map_flaw_category_to_template(category_key)

            # Determine confidence class
            conf_class = f"conf{confidence}"

            # Regex to find the text between start and end (non-greedy)
            pattern = re.escape(start_text) + r"(.*?)" + re.escape(end_text)
            if not re.search(pattern, html_content, flags=re.DOTALL):
                print(f"  ❌ Could not find in HTML! -- {category_class}")
                print(start_text)

            def replacer(match):
                full_text = match.group(0)
                # return f"<span class='flaw {category_class} {conf_class}'>{full_text}</span>"
                return f"<span class='flaw {category_class} {conf_class}' " \
                    f"data-category='{category_key}' " \
                    f"data-severity='{severity}' " \
                    f"data-confidence='{confidence}' " \
                    f"data-description='{description}'>{full_text}</span>"

            # Replace only the first match
            html_content = re.sub(pattern, replacer, html_content, count=1, flags=re.DOTALL)

        # Inject into template
        env = Environment(loader=FileSystemLoader(str(self.template_directory)))
        template = env.get_template(self.template_file)
        self.annotated_html = template.render(
            annotated_content=html_content,
            flaw_counts=self._get_flaw_count(),
            title="Flaw-Annotated Document"
        )
        print("[+] Annotated HTML file")

    def save_annotated_html(self, html_directory, html_file):
        """
        Save the annotated HTML to a file.
        """
        if not self.annotated_html:
            raise ValueError("[-] Annotated HTML not generated. Please call annotate_html() first.")
        saved_path = save_html_to_file(html_content=self.annotated_html, directory=html_directory, filename=html_file)
        print(f"[+] Saved annotated HTML to {saved_path}")
