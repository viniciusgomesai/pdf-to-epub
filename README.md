# pdf-to-epub

> **[Leia em português](README.pt-BR.md)**

A skill for Claude that converts PDF documents into reflowable EPUB files optimized for e-readers and mobile reading apps like Apple Books, Kindle, and Kobo.

## The problem

PDFs have fixed layout. They look fine on desktop, but reading a 30-page PDF on an iPhone means constant pinching, zooming, and horizontal scrolling. EPUB is the native format for e-readers: text reflows to fit any screen, users control font size and spacing, and chapter navigation works out of the box.

This skill teaches Claude to take any PDF and produce a clean, well-structured EPUB that you can read comfortably on your phone, tablet, or e-reader.

## What it does

- Extracts content from uploaded PDFs, preserving the original structure (chapters, headings, code blocks, tables, lists)
- Generates valid EPUB 3 files with embedded CSS, navigable table of contents, and UTF-8 support
- Translates content into any language when requested, keeping code snippets and technical terms intact
- Produces files compatible with Apple Books, Kindle (via Send to Kindle), Kobo, and any EPUB-compatible reader

## Installation

### Claude.ai

1. Download the [latest release](../../releases/latest) (.zip file)
1. Go to **Settings > Capabilities > Skills**
1. Click **Upload skill** and select the .zip file
1. Toggle the skill on

### Claude Code

```bash
git clone https://github.com/viniciusgomesai/pdf-to-epub.git ~/.claude/skills/pdf-to-epub
```

## Usage

Upload a PDF to Claude and ask for a conversion:

- “Convert this PDF to EPUB so I can read it on my iPhone”
- “Turn this document into an ebook for Apple Books”
- “Make this PDF readable on my Kindle”
- “Convert this PDF to EPUB and translate it to Portuguese”

The skill triggers automatically when Claude detects you want to convert a PDF for mobile or e-reader use.

## How it works

|File                    |Purpose                                                                                                                                                           |
|------------------------|------------------------------------------------------------------------------------------------------------------------------------------------------------------|
|`SKILL.md`              |Instructions that teach Claude the full conversion workflow: how to extract PDF structure, map it to EPUB chapters, handle translation, and produce the final file|
|`scripts/create_epub.py`|Reusable Python script that takes a JSON book definition and generates a valid EPUB 3 file with embedded typography and navigation                                |

Claude reads the PDF, plans the chapter structure, builds a JSON definition, and passes it to the script. The result is a ready-to-read EPUB file.

## Requirements

- Python 3.8+
- `ebooklib` (installed automatically by the skill when needed)

## File structure

```
pdf-to-epub/
├── SKILL.md              # Skill instructions (for Claude)
├── scripts/
│   └── create_epub.py    # EPUB generation script
├── README.md             # This file (for humans)
├── README.pt-BR.md       # Portuguese version
└── LICENSE
```

## Tips

- **Apple Books**: AirDrop the EPUB to your iPhone/iPad, or open it from the Files app. It will open directly in Books.
- **Kindle**: Use Amazon’s [Send to Kindle](https://www.amazon.com/sendtokindle) service to email the EPUB to your Kindle device.
- **Translation**: When asking for translation, Claude preserves code snippets, terminal commands, file paths, and technical identifiers in their original language since they need to be used exactly as written.

## License

MIT
