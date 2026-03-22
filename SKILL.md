---
name: pdf-to-epub
description: >
  Converts PDF documents into reflowable EPUB files optimized for e-readers
  and mobile reading apps (Apple Books, Kindle, Kobo, etc.). Use when the user
  wants to read a PDF on their phone, tablet, or e-reader, asks to convert a
  PDF to EPUB, wants a document in a format compatible with Apple Books or
  Kindle, asks for a "readable" or "mobile-friendly" version of a PDF, or
  mentions converting documents for iPhone, iPad, or e-reader. Also handles
  translation of the EPUB content into any language when requested. Covers
  scenarios like "make this PDF readable on my phone", "convert to ebook",
  "I want to read this on my Kindle", "turn this into an EPUB", or
  "translate this PDF to Portuguese and make it an ebook".
---

# PDF to EPUB Converter

Converts PDF documents into well-structured, reflowable EPUB files suitable
for e-readers and mobile reading apps. Optionally translates content into
any target language.

## Why EPUB?

PDFs are fixed-layout: they look great on desktop but are painful to read on
phones and e-readers because the text doesn't reflow. EPUB is the native
format for Apple Books, Kobo, and most e-readers. It adapts to any screen
size, lets users adjust font size and spacing, and supports navigable tables
of contents.

## Core workflow

1. **Extract content from the PDF.** Read the uploaded PDF and identify its
   structure: title, chapters, sections, code blocks, lists, tables, and
   other elements.

2. **Plan the EPUB structure.** Map the PDF's logical structure to EPUB
   chapters. Each major section or chapter becomes a separate XHTML file
   inside the EPUB. Decide on a table of contents based on headings.

3. **Translate if requested.** If the user asks for translation, translate
   all body text into the target language. Keep code snippets, technical
   terms (like `SKILL.md`, `kebab-case`, `frontmatter`), CLI commands, and
   file paths in their original form since they must be used exactly as-is.

4. **Generate the EPUB using the bundled script.** Run
   `python scripts/create_epub.py` with a JSON structure describing the book.
   See the Script Interface section below.

5. **Present the file.** Copy the output EPUB to `/mnt/user-data/outputs/`
   and use `present_files` to share it with the user.

## Script interface

The script `scripts/create_epub.py` reads a JSON file and produces an EPUB.

```bash
python scripts/create_epub.py --input book.json --output /mnt/user-data/outputs/Book.epub
```

The JSON file must follow this structure:

```json
{
  "title": "Book Title",
  "author": "Author Name",
  "language": "en",
  "chapters": [
    {
      "title": "Chapter Title",
      "filename": "ch01.xhtml",
      "content_html": "<h1>Chapter Title</h1><p>Body text in XHTML...</p>"
    }
  ]
}
```

Each chapter's `content_html` is a fragment of valid XHTML that will be
wrapped in a full XHTML document by the script. Use semantic HTML: `<h1>`
through `<h3>` for headings, `<p>` for paragraphs, `<ul>`/`<ol>` for lists,
`<pre><code>` for code blocks, `<table>` for tables.

The script bundles a default CSS stylesheet that provides clean typography,
responsive code blocks, and styled tables. You do not need to include CSS
in the chapter HTML.

## Content guidelines

When converting PDF content to EPUB chapters, follow these principles:

- **Preserve the full content.** Do not summarize or skip sections. The user
  wants the complete document in a more readable format.
- **Respect the original structure.** Map PDF headings to HTML headings at
  the same level. Keep lists as lists, tables as tables, code as code blocks.
- **Split at natural boundaries.** Each chapter in the EPUB should correspond
  to a major section of the PDF (e.g., a chapter, a titled section, or a
  logical grouping of content). Avoid chapters that are too short (a single
  paragraph) or too long (the entire document in one file).
- **Clean up artifacts.** Remove page numbers, headers/footers, and other
  PDF layout artifacts that don't belong in reflowing text.
- **Handle code blocks carefully.** Preserve indentation and formatting in
  code examples. Use `<pre><code>` tags. If the code is very long, keep it
  intact rather than splitting it across chapters.

## Translation guidelines

When translating content for the EPUB:

- Translate all prose, headings, list items, and table content.
- Do NOT translate: code snippets, terminal commands, file paths, variable
  names, technical identifiers (like `kebab-case`, `YAML`, `MCP`), or
  proper nouns that are product/tool names (like `Claude`, `Linear`, `Figma`).
- Maintain the same document structure and emphasis after translation.
- Use natural, fluent language in the target locale rather than stiff
  literal translation.

## Troubleshooting

**EPUB won't open in Apple Books:** Make sure the file extension is `.epub`
(not `.zip`). The script produces a valid EPUB 3 file. If the user has issues,
suggest they AirDrop the file to their device or open it directly from the
Files app.

**Characters look wrong after translation:** Ensure the `language` field in
the JSON matches the target language (e.g., `pt-BR`, `ja`, `zh-CN`). The
EPUB uses UTF-8 encoding which supports all languages.

**Large PDFs produce huge EPUBs:** The EPUB format is text-based and
compresses well. If the PDF has many embedded images, note that this skill
converts text content only. Mention this to the user if the source PDF is
image-heavy.

**Script not found:** Run `pip install ebooklib --break-system-packages`
before executing the script. This is the only external dependency.
