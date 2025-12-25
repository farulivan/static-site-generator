# Static Site Generator

A lightweight, Python-based static site generator that converts Markdown content into clean, fast HTML websites. Built from scratch with zero external dependencies.

## 🎯 What It Does

This SSG transforms Markdown files into a complete static website with:

- **Markdown to HTML conversion** - Write content in Markdown, get semantic HTML
- **Directory-based routing** - File structure becomes URL structure (`content/blog/post.md` → `/blog/post/`)
- **Template system** - Single HTML template for consistent styling across all pages
- **Asset management** - Automatic copying of CSS, images, and static files
- **Clean URLs** - No `.html` extensions, just clean paths

## 🚀 Live Example

**[Dev Adventure](https://farulivan.github.io/static-site-generator/)** - An interactive choose-your-own-adventure story about a production deployment gone wrong. This demonstrates the SSG's capabilities:

- Branching narrative with multiple paths
- 8 different endings based on choices
- Professional "calm incident room" UI aesthetic
- Collapsible sections and spoiler protection
- Fully keyboard-accessible navigation

The entire adventure site is generated from Markdown files in the `content/` directory.

## ✨ Key Features

### For Content Creators
- Write in Markdown, no HTML knowledge required
- Organize content with folders (becomes navigation structure)
- Single template controls entire site appearance
- Fast builds - regenerate entire site in milliseconds

### For Developers
- **Zero dependencies** - Pure Python 3, no pip installs needed
- **Custom parser** - Hand-built Markdown parser, not a library wrapper
- **Test coverage** - 99 unit tests ensuring reliability
- **Professional architecture** - Package-based structure with clear separation of concerns
- **Modular design** - Models, parsers, converters, and generators in separate packages
- **Extensible** - Easy to add new Markdown features or HTML elements

## 🏗️ Architecture

```
static-site-generator/
├── src/
│   ├── main.py              # Entry point
│   ├── models/              # Domain models
│   │   ├── html_node.py     # HTML node base class
│   │   ├── leaf_node.py     # HTML leaf nodes (no children)
│   │   ├── parent_node.py   # HTML parent nodes (with children)
│   │   ├── text_node.py     # Text node representation
│   │   └── enums.py         # Type definitions (BlockType, TextType)
│   ├── parsers/             # Markdown parsing
│   │   ├── markdown.py      # Block-level parsing
│   │   └── inline.py        # Inline text parsing (delimiters, links, images)
│   ├── converters/          # HTML conversion
│   │   ├── text_to_html.py  # TextNode → HTMLNode conversion
│   │   └── block_to_html.py # Block → HTMLNode conversion
│   ├── generators/          # Page generation
│   │   └── page_generator.py # Page generation & routing
│   ├── utils/               # Utilities
│   │   └── file_utils.py    # File operations
│   └── tests/               # Test suite (99 unit tests)
│       ├── test_htmlnode.py
│       ├── test_leafnode.py
│       ├── test_parentnode.py
│       ├── test_textnode.py
│       ├── test_inline.py
│       ├── test_converters.py
│       └── test_file_utils.py
├── content/                 # Markdown source files
├── static/                  # CSS, images, favicon
├── template.html            # HTML template
└── docs/                    # Generated output (GitHub Pages ready)
```

## 🛠️ How It Works

1. **Parse Markdown** - Custom parser converts Markdown to intermediate representation
2. **Build HTML Nodes** - Intermediate representation becomes HTML node tree
3. **Apply Template** - Content injected into HTML template
4. **Generate Files** - HTML files written to `docs/` directory
5. **Copy Assets** - Static files (CSS, images) copied to output

### Supported Markdown Features

- Headings (`#`, `##`, `###`)
- Paragraphs and line breaks
- **Bold** and *italic* text
- `Inline code` and code blocks
- Links `[text](url)`
- Images `![alt](src)`
- Unordered and ordered lists
- Blockquotes
- Horizontal rules

### HTML Output

- Semantic HTML5 elements
- Clean, readable source code
- No inline styles (CSS in separate file)
- Accessible markup (ARIA-friendly)

## 🚦 Quick Start

### Prerequisites
- Python 3.10 or higher
- No external dependencies required

### Build the Site

```bash
# Generate site
python3 src/main.py

# Or use the build script
./build.sh
```

### Development Server

```bash
# Build and serve locally
./main.sh

# Site available at http://localhost:8888
```

### Run Tests

```bash
./test.sh
# Runs 99 unit tests
```

## 📝 Creating Content

### Basic Page

Create `content/about/index.md`:

```markdown
# About Me

I'm a developer who builds things.

## Skills

- Python
- Web Development
- System Design
```

Generates: `docs/about/index.html` → accessible at `/about/`

### Nested Pages

```
content/
├── blog/
│   ├── index.md          → /blog/
│   ├── post-1/
│   │   └── index.md      → /blog/post-1/
│   └── post-2/
│       └── index.md      → /blog/post-2/
```

### Linking Between Pages

```markdown
[Read my blog](/blog/)
[Check out this post](/blog/post-1/)
```

## 🎨 Customization

### Styling

Edit `static/index.css` to change the appearance. The Dev Adventure example uses:

- CSS custom properties for theming
- Responsive design
- Keyboard-accessible focus states
- Dark mode optimized colors

### Template

Modify `template.html` to change the HTML structure:

```html
<!doctype html>
<html lang="en">
  <head>
    <meta charset="utf-8" />
    <meta name="viewport" content="width=device-width, initial-scale=1" />
    <title>{{ Title }} | Dev Adventure</title>
    <link rel="icon" type="image/svg+xml" href="/favicon.svg" />
    <link href="/index.css" rel="stylesheet" />
    <meta name="description" content="An interactive developer adventure - your choices matter" />
  </head>

  <body>
    <article>{{ Content }}</article>
  </body>
</html>
```

## 🧪 Testing

The project includes comprehensive test coverage:

- **Markdown parsing** - Ensures correct conversion of all Markdown features
- **HTML generation** - Validates proper HTML node creation
- **File operations** - Tests recursive copying and file handling
- **Edge cases** - Empty files, special characters, nested structures

```bash
./test.sh
# Expected: Ran 99 tests in 0.006s - OK
```

## 📦 Deployment

### GitHub Pages

1. Push to GitHub
2. Enable GitHub Pages in repository settings
3. Set source to `docs/` folder
4. Site live at `https://username.github.io/repo-name/`

### Custom Domain

Add `CNAME` file to `static/` directory:

```
yourdomain.com
```

## 🎓 Learning Outcomes

This project demonstrates:

- **Parser design** - Building a Markdown parser from scratch
- **Package architecture** - Professional Python package organization with clear module boundaries
- **Object-oriented programming** - Clean class hierarchy for HTML nodes
- **Separation of concerns** - Models, parsers, converters, generators in isolated packages
- **Recursive algorithms** - Directory traversal and tree building
- **Comprehensive testing** - 99 unit tests ensuring code reliability and maintainability
- **File I/O operations** - Reading, writing, and copying files
- **Template systems** - Simple but effective content injection
- **Web fundamentals** - HTML generation, routing, static hosting

## 🔍 Code Highlights

### Package Structure

The codebase follows Python package organization:

```python
# Clean imports from organized packages
from models import HTMLNode, LeafNode, ParentNode, TextNode
from parsers import markdown_to_blocks, block_to_block_type
from converters import markdown_to_html_node
from generators import generate_pages_recursive
from utils import copy_directory_recursive
```

### Custom Markdown Parser

```python
# parsers/markdown.py - Block-level parsing
def markdown_to_html_node(markdown: str) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        children.append(block_to_html_node(block, block_type))
    return ParentNode("div", children)
```

### Recursive Page Generation

```python
# generators/page_generator.py - Generates entire directory tree
def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath='/'):
    for entry in os.listdir(dir_path_content):
        if os.path.isfile(from_path) and entry.endswith('.md'):
            generate_page(from_path, template_path, dest_path, basepath)
        elif os.path.isdir(from_path):
            generate_pages_recursive(from_path, template_path, dest_path, basepath)
```

## 🤝 Why This Matters

This isn't just another SSG - it's a demonstration of:

1. **Problem-solving** - Building complex functionality from simple primitives
2. **Code quality** - Clean, testable, maintainable code
3. **Engineering discipline** - Proper testing, documentation, version control
4. **Product thinking** - Not just code, but a complete, usable product (Dev Adventure)
5. **Attention to detail** - From UX polish to accessibility considerations

## 📊 Project Stats

- **Lines of Code**: ~1,500 (excluding tests)
- **Test Coverage**: 99 unit tests
- **Dependencies**: 0 external packages
- **Build Time**: <100ms for full site
- **Supported Markdown Features**: 12+

## 🎯 Use Cases

- **Personal portfolios** - Showcase your work
- **Documentation sites** - Technical documentation
- **Blogs** - Simple, fast blogging platform
- **Interactive stories** - Like the Dev Adventure example
- **Landing pages** - Quick marketing sites

## 📄 License

This project is open source and available for educational purposes.

## 🙋 Questions?

This SSG was built to demonstrate:
- Strong Python fundamentals
- Software engineering best practices
- Ability to build complete products from scratch
- Attention to UX and accessibility

For technical questions or to discuss the implementation, feel free to reach out!

---

**Built with Python 3 | No frameworks, no dependencies, just code**
