# 🧙 Static Site Generator

A from-scratch static site generator written in pure Python — no external libraries, no frameworks. Takes a directory of Markdown files and produces a fully-rendered, styled website ready to serve.

Built as part of the [Boot.dev](https://www.boot.dev) curriculum.

---

## ✨ Features

- **Full Markdown parsing** — headings, bold, italic, code, blockquotes, ordered/unordered lists, links, and images
- **Recursive content generation** — mirrors your `content/` directory structure into `public/`
- **HTML templating** — a single `template.html` is used for every page, with `{{ Title }}` and `{{ Content }}` placeholders
- **Static asset copying** — CSS, images, and any other static files are copied verbatim into `public/`
- **Zero dependencies** — stdlib only (`os`, `shutil`, `re`, `pathlib`, `enum`, `unittest`)
- **Test suite** — unit tests for every layer of the parsing pipeline

---

## 📁 Project Structure

```
Static_Site_Generator/
├── content/                  # Your Markdown source files (mirrors to public/)
│   ├── index.md
│   ├── blog/
│   │   ├── glorfindel/
│   │   ├── majesty/
│   │   └── tom/
│   └── contact/
│       └── index.md
├── static/                   # Static assets copied verbatim to public/
│   ├── index.css
│   └── images/
├── public/                   # ⚙️ Generated output — do not edit (git-ignored)
├── src/                      # All Python source code
│   ├── main.py               # Entry point — orchestrates build
│   ├── copystatic.py         # Recursively copies static/ → public/
│   ├── generate_page.py      # Renders .md files → .html using the template
│   ├── extract_title.py      # Pulls the h1 title out of a markdown doc
│   ├── markdown_to_html.py   # Top-level MD → HTMLNode conversion
│   ├── block_markdown.py     # Splits MD into blocks; classifies block types
│   ├── inline_markdown.py    # Parses inline elements (bold, links, images…)
│   ├── htmlnode.py           # Base HTMLNode class
│   ├── leafnode.py           # HTMLNode subclass for elements with no children
│   ├── parentnode.py         # HTMLNode subclass for elements with children
│   ├── textnode.py           # Intermediate TextNode + TextType enum
│   └── test_*.py             # Unit tests for every module
├── template.html             # HTML page template
├── main.sh                   # Build + serve script
└── test.sh                   # Run the test suite
```

---

## 🏗️ Architecture

The build pipeline has three stages that run in sequence:

```
content/*.md  ──┐
                ├──► [Parser] ──► HTMLNode tree ──► [Template] ──► public/*.html
template.html ──┘
static/       ──────────────────────────────────────────────────► public/ (copied)
```

### Stage 1 — Static Asset Copy

`copystatic.copy_files_recursive(src, dest)` walks the `static/` directory and mirrors its entire tree into `public/`, using `shutil.copy` for files and recursing into subdirectories.

### Stage 2 — Markdown → HTMLNode Tree

This is the core of the project. Every Markdown file goes through a two-pass parsing pipeline:

**Pass 1 — Block-level parsing** (`block_markdown.py`)
1. `markdown_to_blocks(md)` — splits the raw string on blank lines (`\n\n`) and strips whitespace, yielding a list of raw block strings.
2. `block_to_block_type(block)` — classifies each block as one of six `BlockType` enum values: `PARAGRAPH`, `HEADING`, `CODE`, `QUOTE`, `ULIST`, `OLIST`.

**Pass 2 — Inline parsing** (`inline_markdown.py`)
Each block's text content is run through `text_to_textnodes(text)`, which applies a series of transforms using the `split_nodes_*` family of functions:
1. Delimiter-based splits for `` ` `` (code), `**` (bold), `*` / `_` (italic)
2. Regex-based splits for `![alt](url)` images and `[text](url)` links

This produces a flat list of `TextNode` objects, each carrying a `TextType` enum value.

### Stage 3 — HTMLNode → HTML String

`markdown_to_html.py` bridges both levels:
- `block_to_html_node(block)` dispatches to a specific converter (`heading_to_html_node`, `code_to_html_node`, etc.)
- `text_to_children(text)` converts a list of `TextNode`s → `LeafNode`s via `text_node_to_html_node`
- The resulting tree is rooted in a `ParentNode("div", [...])` and serialized with `.to_html()`

### Stage 4 — Page Assembly

`generate_page.py` reads a `.md` file, converts it to HTML, extracts the `# H1` title, injects both into `template.html` by replacing `{{ Title }}` and `{{ Content }}`, then writes the output `.html` file (creating any needed directories).

`generate_pages_recursive` mirrors this for entire directory trees, mapping `content/foo/index.md` → `public/foo/index.html`.

---

## 🧩 Class Design

### `HTMLNode` (base class)
```
HTMLNode(tag, value, children, props)
```
Abstract base. All four fields are optional (`None` by default). Defines:
- `to_html()` — abstract, raises `NotImplementedError`
- `props_to_html()` — renders the `props` dict as HTML attribute strings (e.g. `href="..."`)

### `LeafNode(HTMLNode)`
A node with **no children** — represents self-contained elements like `<b>`, `<a>`, `<img>`, or plain text.
- Requires a `value`; tag is optional (bare text when `tag=None`)
- `to_html()` renders as `<tag props>value</tag>`

### `ParentNode(HTMLNode)`
A node that has **only children**, no direct value.
- `to_html()` recursively calls `.to_html()` on each child, making the tree serialization naturally recursive

### `TextNode`
An intermediate representation sitting **between raw Markdown text and HTML nodes**. Holds `(text, TextType, url?)` and is converted to a `LeafNode` by `text_node_to_html_node`.

### `TextType` (Enum)
```python
TEXT | BOLD | ITALIC | CODE | LINK | IMAGE
```

### `BlockType` (Enum)
```python
PARAGRAPH | HEADING | CODE | QUOTE | ULIST | OLIST
```

---

## ⚙️ Local Setup

**Requirements:** Python 3.10+ (uses `match`/`case` syntax)

```bash
# 1. Clone the repo
git clone https://github.com/<your-username>/Static_Site_Generator.git
cd Static_Site_Generator

# 2. Build the site and serve it
bash main.sh
```

The generator runs, writes everything to `public/`, then starts Python's built-in HTTP server on port 3000. Open [http://localhost:3000](http://localhost:3000) in your browser.

To **just build** without serving:
```bash
python3 src/main.py
```

To **run the test suite**:
```bash
bash test.sh
# equivalent to:
python3 -m unittest discover -s src
```

---

## 📝 Serving Your Own Markdown Files

The content directory structure maps directly to URL paths:

| File | URL |
|------|-----|
| `content/index.md` | `/` |
| `content/blog/my-post/index.md` | `/blog/my-post/` |
| `content/about.md` | `/about` |

**Steps:**

1. **Add your Markdown files** to the `content/` directory. Each file must have at least one `# H1 heading` — this becomes the page `<title>`.

2. **(Optional) Add static assets** to `static/` — images, fonts, extra CSS files. They'll be copied to `public/` as-is.

3. **(Optional) Customize the template** — edit `template.html`. It uses two placeholders:
   - `{{ Title }}` — replaced with the extracted `# H1` text
   - `{{ Content }}` — replaced with the fully rendered HTML body

4. **Build and serve:**
   ```bash
   bash main.sh
   ```

### Supported Markdown Syntax

| Syntax | Output |
|--------|--------|
| `# H1` through `###### H6` | `<h1>` – `<h6>` |
| `**bold**` | `<b>` |
| `*italic*` or `_italic_` | `<i>` |
| `` `code` `` | `<code>` |
| ` ``` ... ``` ` (fenced block) | `<pre><code>` |
| `> quote` | `<blockquote>` |
| `- item` | `<ul><li>` |
| `1. item` | `<ol><li>` |
| `[text](url)` | `<a href="url">` |
| `![alt](url)` | `<img src="url" alt="alt">` |

---

## 🧪 Test Coverage

Each module has a corresponding test file:

| Test file | What it covers |
|-----------|----------------|
| `test_htmlnode.py` | `HTMLNode.props_to_html()` |
| `test_leafnode.py` | `LeafNode.to_html()` edge cases |
| `test_parentnode.py` | Recursive `ParentNode.to_html()` |
| `test_textnode.py` | `TextNode.__eq__` and `text_node_to_html_node` |
| `test_inline_markdown.py` | `split_nodes_*`, `extract_markdown_*`, `text_to_textnodes` |
| `test_block_markdown.py` | `markdown_to_blocks`, `block_to_block_type` |
| `test_generate_page.py` | `generate_page` end-to-end |

---

## 🗒️ Notes

- The `public/` directory is **deleted and fully rebuilt** on every run — never store anything there manually.
- macOS `.DS_Store` files in `content/` are safely ignored by the recursive generator (uses `os.path.isdir()` guard).
- The project uses only Python's standard library — no `pip install` needed.
