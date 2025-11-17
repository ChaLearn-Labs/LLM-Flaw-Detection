import os
import re
import requests
from bs4 import BeautifulSoup
from utils import save_html_to_file


class HTML_Downloader:

    def __init__(self, html_url, html_file_name, output_dir=None):
        self.html_url = html_url
        self.output_dir = output_dir
        self.html_file_name = html_file_name

        self._create_output_dir()

    def _create_output_dir(self):
        if self.output_dir is None:
            self.output_dir = self.url.split("/")[-1].replace(".", "_")

        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def _clean_html(self, soup):
        print("[*] Cleaning HTML")

        # Remove unwanted sections
        for tag in soup(["script", "style", "link", "noscript", "svg", "iframe"]):
            tag.decompose()

        # Remove navigation and headers/footers
        for tag in soup.find_all(["nav", "header", "footer"]):
            tag.decompose()

        # Keep only the <article> content if present
        article = soup.find("article")
        if article:
            soup = article

        # Clean attributes
        for tag in soup.find_all(True):
            # Always remove these attributes if they exist
            for attr in list(tag.attrs):
                if (
                    attr == "class"
                    or attr == "style"
                    or attr == "onclick"
                    or attr == "lang"
                    or attr == "height"
                    or attr == "width"
                    or attr == "alt"
                    or attr.startswith("data-")
                ):
                    del tag.attrs[attr]

        # Remove spans (or any tag) that contain only "{strip}" or similar placeholder text
        for tag in soup.find_all(True):
            if tag.get_text(strip=True) in ["{strip}", "{strip/}", "{strip }"]:
                tag.decompose()

        # Unwrap redundant nested <span> tags
        # If a <span> contains only another <span>, unwrap it repeatedly
        changed = True
        while changed:
            changed = False
            for span in soup.find_all("span"):
                children = [c for c in span.children if c.name or str(c).strip()]
                # If it has exactly one child which is also a <span>
                if len(children) == 1 and getattr(children[0], "name", None) == "span":
                    span.unwrap()
                    changed = True
                    break  # restart to avoid modifying during iteration

        # Repeatedly remove empty <div> and <figure> until none remain
        changed = True
        while changed:
            changed = False

            for tag in soup.find_all(["div", "figure"]):
                # Determine if this tag is empty or only whitespace
                has_text = bool(tag.get_text(strip=True))
                has_content = tag.find(["img", "table", "p", "figcaption", "figure", "div"])

                # If it's completely empty (no text, no content)
                if not has_text and not has_content:
                    tag.decompose()
                    changed = True
                    break  # Restart loop after modifying DOM

        # Unwrap <span> tags that don't contribute anything (only text)
        for span in soup.find_all("span"):
            if len(span.attrs) == 0:
                span.unwrap()

        # Convert soup to string for post-processing
        html_str = str(soup)

        # Remove multiple empty lines (2 or more → 1)
        html_str = re.sub(r'\n\s*\n+', '\n', html_str)

        # Trim leading/trailing whitespace
        html_str = html_str.strip()

        # Re-parse cleaned HTML back into BeautifulSoup
        return BeautifulSoup(html_str, "html.parser")

    # def _rewrite_image_src(self, soup):
    #     for img_tag in soup.find_all('img'):
    #         src = img_tag.get('src')
    #         if src:
    #             img_filename = src.split('/')[-1]
    #             img_tag['src'] = img_filename
    #     return soup

    def _remove_images(self, soup):

        for img_tag in soup.find_all("img"):
            img_tag.decompose()
        return soup

    def _remove_figure_captions(self, soup):

        for figcaption in soup.find_all("figcaption"):
            text = figcaption.get_text(strip=True)
            if text.lower().startswith("figure"):
                figcaption.decompose()
        return soup

    def _rewrite_citation_links(self, soup):

        for a_tag in soup.find_all("a", href=True):
            href = a_tag["href"]
            if href.startswith("https://arxiv.org/") and "#" in href:
                # Keep only the fragment part after '#'
                fragment = href.split("#", 1)[1]
                a_tag["href"] = f"#{fragment}"

        return soup

    def download_html(self):
        try:
            print("[*] Downloading HTML")
            response = requests.get(self.html_url)
            soup = BeautifulSoup(response.text, 'html.parser')

            # Remove all img tags
            soup = self._remove_images(soup)
            # Remove all figure captions
            soup = self._remove_figure_captions(soup)

            # Rewrite citation links
            soup = self._rewrite_citation_links(soup)

            # Clean HTML
            soup = self._clean_html(soup)

            # Rewrite image src attributes
            # soup = self._rewrite_image_src(soup)

            # Save html
            save_html_to_file(html_content=str(soup), directory=self.output_dir, filename=self.html_file_name)

            print("[+]")
        except Exception as e:
            print(f"[-] Error: {e}")

    # def download_images(self):
    #     try:
    #         print("[*] Downloading Images")
    #         # Send a GET request to the webpage
    #         headers = {
    #             'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
    #         }
    #         response = requests.get(self.url, headers=headers)
    #         response.raise_for_status()  # Raise an exception for HTTP errors (4xx or 5xx)

    #         # Parse the HTML content
    #         soup = BeautifulSoup(response.content, 'html.parser')

    #         # Find all <img> tags
    #         img_tags = soup.find_all('img')

    #         if not img_tags:
    #             print(f"No <img> tags found on {self.url}")
    #             return

    #         print(f"Found {len(img_tags)} image tags. Attempting to download...")

    #         for img_tag in img_tags:
    #             img_url = img_tag.get('src')
    #             if not img_url:
    #                 # Sometimes the actual URL is in 'data-src' or other attributes
    #                 img_url = img_tag.get('data-src')

    #             if img_url:
    #                 # Make sure the URL is absolute
    #                 img_url = self.url + '/' + img_url
    #                 try:
    #                     # Get the image content
    #                     img_response = requests.get(img_url, headers=headers, stream=True)
    #                     img_response.raise_for_status()

    #                     # Extract image name from URL
    #                     img_name = os.path.join(self.output_dir, img_url.split('/')[-1].split('?')[0]) # Basic name cleaning

    #                     # Ensure the image name has an extension, default to .png if not obvious
    #                     if not os.path.splitext(img_name)[1]:
    #                         content_type = img_response.headers.get('content-type')
    #                         if content_type and 'image' in content_type:
    #                             extension = content_type.split('/')[-1]
    #                             img_name += f".{extension}"
    #                         else:
    #                             img_name += ".png" # Default extension

    #                     # Save the image
    #                     with open(img_name, 'wb') as f:
    #                         for chunk in img_response.iter_content(1024):
    #                             f.write(chunk)
    #                     print(f"Successfully downloaded: {img_name}")

    #                 except requests.exceptions.RequestException as e:
    #                     print(f"Could not download {img_url}. Error: {e}")
    #                 except Exception as e:
    #                     print(f"An error occurred for {img_url}. Error: {e}")
    #             else:
    #                 print("Found an img tag without a 'src' or 'data-src' attribute.")
    #         print("[+]")
    #     except Exception as e:
    #         print(f"[-] Error: {e}")