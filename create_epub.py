#!/usr/bin/env python3
"""
create_epub.py — Generates an EPUB file from a JSON book definition.

Usage:
    python create_epub.py --input book.json --output output.epub

The JSON input must contain:
    - title (str): Book title
    - author (str): Author name
    - language (str): Language code (e.g., "en", "pt-BR", "ja")
    - chapters (list): Each with title, filename, and content_html

Dependencies:
    pip install ebooklib --break-system-packages
"""

import argparse
import json
import sys
import uuid

try:
    from ebooklib import epub
except ImportError:
    print("ERROR: ebooklib is not installed.", file=sys.stderr)
    print("Run: pip install ebooklib --break-system-packages", file=sys.stderr)
    sys.exit(1)


DEFAULT_CSS = """
body {
    font-family: Georgia, "Times New Roman", serif;
    line-height: 1.6;
    margin: 1em;
    color: #1a1a1a;
}
h1 {
    font-size: 1.8em;
    margin-top: 1.5em;
    margin-bottom: 0.5em;
    color: #2c2c2c;
}
h2 {
    font-size: 1.4em;
    margin-top: 1.2em;
    margin-bottom: 0.4em;
    color: #333;
}
h3 {
    font-size: 1.15em;
    margin-top: 1em;
    margin-bottom: 0.3em;
    color: #444;
}
p {
    margin-bottom: 0.8em;
    text-align: justify;
}
ul, ol {
    margin-bottom: 0.8em;
    padding-left: 1.5em;
}
li {
    margin-bottom: 0.3em;
}
code {
    font-family: Menlo, Courier, monospace;
    font-size: 0.85em;
    background-color: #f4f4f4;
    padding: 0.1em 0.3em;
    border-radius: 3px;
}
pre {
    background-color: #f4f4f4;
    padding: 0.8em;
    border-radius: 5px;
    overflow-x: auto;
    font-size: 0.82em;
    line-height: 1.4;
    margin-bottom: 1em;
}
pre code {
    background: none;
    padding: 0;
}
table {
    width: 100%;
    border-collapse: collapse;
    margin-bottom: 1em;
    font-size: 0.9em;
}
th, td {
    border: 1px solid #ccc;
    padding: 0.5em;
    text-align: left;
}
th {
    background-color: #f0f0f0;
    font-weight: bold;
}
blockquote {
    border-left: 3px solid #4a90d9;
    margin: 1em 0;
    padding: 0.5em 1em;
    background-color: #f0f7ff;
    font-style: italic;
}
.tip {
    background-color: #f0f7ff;
    border-left: 3px solid #4a90d9;
    padding: 0.8em;
    margin: 1em 0;
}
.chapter-title {
    font-size: 2em;
    text-align: center;
    margin-top: 3em;
    margin-bottom: 1em;
}
.cover-title {
    font-size: 2.2em;
    text-align: center;
    margin-top: 40%;
    color: #2c2c2c;
    line-height: 1.3;
}
"""


def create_epub_from_json(data: dict, output_path: str) -> None:
    """Create an EPUB file from a book definition dictionary."""
    book = epub.EpubBook()

    # Metadata
    book.set_identifier(str(uuid.uuid4()))
    book.set_title(data["title"])
    book.set_language(data.get("language", "en"))
    book.add_author(data.get("author", "Unknown"))

    # Stylesheet
    css_content = data.get("css", DEFAULT_CSS)
    css_item = epub.EpubItem(
        uid="style",
        file_name="style/default.css",
        media_type="text/css",
        content=css_content,
    )
    book.add_item(css_item)

    # Build chapters
    chapters = []
    for ch_def in data["chapters"]:
        chapter = epub.EpubHtml(
            title=ch_def["title"],
            file_name=ch_def["filename"],
            lang=data.get("language", "en"),
        )
        chapter.content = ch_def["content_html"]
        chapter.add_item(css_item)
        book.add_item(chapter)
        chapters.append(chapter)

    # Table of contents and spine
    book.toc = chapters
    book.spine = ["nav"] + chapters

    # Navigation files
    book.add_item(epub.EpubNcx())
    book.add_item(epub.EpubNav())

    # Write
    epub.write_epub(output_path, book)
    print(f"EPUB created: {output_path}")


def main():
    parser = argparse.ArgumentParser(
        description="Generate an EPUB from a JSON book definition."
    )
    parser.add_argument(
        "--input", required=True, help="Path to the JSON book definition file."
    )
    parser.add_argument(
        "--output", required=True, help="Path for the output EPUB file."
    )
    args = parser.parse_args()

    with open(args.input, "r", encoding="utf-8") as f:
        data = json.load(f)

    # Validate required fields
    if "title" not in data:
        print("ERROR: JSON must contain a 'title' field.", file=sys.stderr)
        sys.exit(1)
    if "chapters" not in data or not data["chapters"]:
        print("ERROR: JSON must contain a non-empty 'chapters' array.", file=sys.stderr)
        sys.exit(1)
    for i, ch in enumerate(data["chapters"]):
        for field in ("title", "filename", "content_html"):
            if field not in ch:
                print(
                    f"ERROR: Chapter {i} is missing required field '{field}'.",
                    file=sys.stderr,
                )
                sys.exit(1)

    create_epub_from_json(data, args.output)


if __name__ == "__main__":
    main()
