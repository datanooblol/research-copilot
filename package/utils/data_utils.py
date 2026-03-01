import requests
import re

def arxiv_to_pdf(url, filename="paper.pdf"):
    response = requests.get(url)
    with open(filename, "wb") as f:
        f.write(response.content)

def sanitize_filename(title, replace_with="_"):
    # Remove invalid characters: / \ : * ? " < > |
    return re.sub(r'[/\\:*?"<>|]', replace_with, title).lower()
