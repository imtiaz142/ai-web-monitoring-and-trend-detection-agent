import re
from bs4 import BeautifulSoup


def strip_html(html_content: str) -> str:
    if not html_content:
        return ""
    # Use html.parser (not lxml) to avoid mangling plain text
    soup = BeautifulSoup(html_content, "html.parser")
    for tag in soup(["script", "iframe", "style"]):
        tag.decompose()
    text = soup.get_text(separator=" ")
    text = re.sub(r"\s+", " ", text).strip()
    return text


def clean_title(title: str) -> str:
    """Clean an RSS title. Titles are usually plain text, so only strip HTML if tags present."""
    if not title:
        return ""
    title = title.strip()
    # Only parse as HTML if it actually contains tags
    if "<" in title and ">" in title:
        return strip_html(title)
    # Otherwise just clean whitespace and decode entities
    return re.sub(r"\s+", " ", title).strip()
