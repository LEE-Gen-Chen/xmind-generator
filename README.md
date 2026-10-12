# xmind-generator

> **Pure-Python XMind 8 file generator — no SDK, no dependencies**

[![Python 3.8+](https://img.shields.io/badge/python-3.8+-blue.svg)](https://www.python.org/)
[![MIT License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)

## Why this exists

All official XMind SDKs have critical bugs that make them unusable for programmatic generation:

| SDK | Problem |
|-----|---------|
| `npm xmind` | `createSheet()` **overwrites** the root sheet — your first branch vanishes |
| `xmind-mcp-server` | ZEN JSON format causes **parse errors** in XMind 2025 |
| `python-xmind` (PyPI) | Old lib; incompatible with XMind 8 ZIP spec |

**xmindgen** bypasses all SDKs by generating `.xmind` files directly:
- Pure Python stdlib (`zipfile` + string templates)
- Zero external dependencies
- Zero npm/Node.js required
- Tested with XMind 8 and XMind 2025

## Quick start

```bash
pip install xmindgen
```

```python
from xmindgen import save, Topic

# Method 1: Topic class (recommended)
root = Topic("My Mind Map")
root.add_child("Branch A", notes="Details here")
b = root.add_child("Branch B")
b.add_child("Leaf B1").add_child("Deep leaf")
b.add_child("Leaf B2")

# Style each branch with a distinct color
root.save("demo.xmind", styles={
    b.id: ("#7B2D8B", "#FFFFFF"),
})

# Method 2: Dict-based (no class needed)
from xmindgen import build_tree, save

tree = build_tree(
    "Root Title",
    {"title": "Branch 1", "children": [
        {"title": "Leaf 1a"},
        {"title": "Leaf 1b"},
    ]},
    {"title": "Branch 2"},
)
save("demo2.xmind", tree)
```

Open `demo.xmind` in XMind 8 or XMind 2025. Done.

## API Reference

### `save(path, tree, title=None, styles=None, relationships=None)`

| Param | Type | Description |
|-------|------|-------------|
| `path` | `str` | Output `.xmind` file path |
| `tree` | `dict` or `Topic` | Root topic |
| `title` | `str` | Sheet title (default: root title) |
| `styles` | `dict` | `{topic_id: (bg_hex, text_hex)}` |
| `relationships` | `list` | `[(id1, id2, label), ...]` |

### `Topic(title, notes="", topic_id=None)`

```python
t = Topic("Node Title", notes="Optional note")
t.add_child("Child 1")           # returns child for chaining
t.add_child("Child 2", notes="With note")
t.add_relationship(other_id, "A↔B cross-ref")
t.to_dict()                       # serialize to plain dict
t.save("out.xmind")               # save directly
```

### `build_tree(title, *children, notes="", **kwargs)`

Dict-based tree builder. Children can be dicts or plain strings.

## Relationships (Cross-References)

Topics can link to each other bidirectionally:

```python
from xmindgen import Topic

root = Topic("Root")
a = root.add_child("Concept A")
b = root.add_child("Concept B")
a.add_relationship(b.id, "related to")

root.save("linked.xmind")
```

This creates a `<relationship>` element in `content.xml`. XMind renders these as dotted lines between topics.

## Branch Styling

Pass a `styles` dict to color-code branches:

```python
root.save("styled.xmind", styles={
    branch_a.id: ("#1A6B5C", "#FFFFFF"),  # teal
    branch_b.id: ("#7B2D8B", "#FFFFFF"),  # purple
})
```

Color format: standard hex RGB (`#RRGGBB`). Both `bg` and `text` are required.

## File Format

`.xmind` files are ZIP archives with this structure:

```
example.xmind/
├── content.xml          ← XMind 8 xmap XML (required)
└── META-INF/
    ├── manifest.xml     ← ZIP member manifest (required)
    └── styles.xml       ← Branch colors (optional)
```

Generated with `zipfile.ZIP_DEFLATED`. Compatible with XMind 8.2+ and XMind 2025 (ZEN).

## Advanced: Low-level XML

```python
from xmindgen import to_content_xml, to_styles_xml, manifest_xml

content = to_content_xml(tree_dict)
styles  = to_styles_xml({topic_id: ("#1A6B5C", "#FFFFFF")})
meta    = manifest_xml()
```

## Install from source

```bash
git clone https://github.com/LEE-Gen-Chen/xmind-generator.git
cd xmind-generator
pip install -e .
```

Or copy `xmindgen/` directly into your project — it's a single-file module.

## Limitations

- No image attachments
- No integrated markers/labels (XMind Pro feature)
- Relationships are cross-references only (not hierarchical)
- Numbered priority markers not supported in free version

## License

MIT License. See [LICENSE](LICENSE).
