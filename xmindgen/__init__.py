"""
xmindgen — Pure-Python XMind 8 file generator (no SDK, no dependencies)

Why this exists
--------------
All official XMind SDKs (npm, Python) have critical bugs:
- npm xmind SDK: createSheet() overwrites the root sheet
- xmind-mcp-server: ZEN JSON format causes parse errors in XMind 2025

Solution: generate .xmind files directly using Python stdlib (zipfile + XML).

File format: XMind 8 ZIP (content.xml + META-INF/manifest.xml + optional styles.xml)
Compatible with: XMind 8, XMind 2025, ZEN mode

Basic usage
-----------
    from xmindgen import save

    tree = {
        "title": "My Map",
        "children": [
            {"title": "Branch A", "notes": "Details here"},
            {"title": "Branch B", "children": [
                {"title": "Leaf B1"},
                {"title": "Leaf B2"},
            ]},
        ]
    }
    save("output.xmind", tree)

Advanced: relationships, styles, notes
---------------------------------------
    from xmindgen import save, Topic

    root = Topic("Root", notes="Root note")
    root.add_child("Child 1", notes="With note")
    root.add_child("Child 2").add_child("Grandchild")

    # Relationships: bidirectional links between any two topic IDs
    root.add_relationship(end1_id, end2_id, "cross-reference label")

    # Branch styles: pass a dict of {branch_id: (bg_color, text_color)}
    root.save("out.xmind", styles={branch_id: ("#1A6B5C", "#FFFFFF")})

API Reference
-------------
    save(path, tree, title=None, styles=None, relationships=None)
        path       : output .xmind file path
        tree       : dict or Topic object (see below)
        title      : optional sheet title (defaults to root title)
        styles     : optional dict {topic_id: (bg_hex, text_hex)}
        relationships: optional list of (id1, id2, label)

    Topic(title, notes="", topic_id=None)
        .add_child(title, notes="") -> Topic
        .add_relationship(other_topic_id, label="") -> Topic
        .to_dict() -> serializable dict
        .save(path, styles=None) -> None

    build_tree(title, *children) -> dict
        Convenient dict-based tree builder (no Topic class needed)

Low-level XML
-------------
    to_content_xml(tree, timestamp=None) -> str
    to_styles_xml(styles_dict) -> str
    manifest_xml() -> str
"""

__version__ = "1.0.0"
__author__ = "Li Chuangjie"

from .core import save, build_tree, Topic, to_content_xml, to_styles_xml, manifest_xml

__all__ = [
    "save",
    "build_tree",
    "Topic",
    "to_content_xml",
    "to_styles_xml",
    "manifest_xml",
]
