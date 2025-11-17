from html_downloader import HTML_Downloader
from config import HTML_URL, HTML_FILE_NAME, HTML_DIRECTORY

if __name__ == "__main__":

    html_download = HTML_Downloader(
        html_url=HTML_URL,
        html_file_name=HTML_FILE_NAME,
        output_dir=HTML_DIRECTORY
    )
    html_download.download_html()
