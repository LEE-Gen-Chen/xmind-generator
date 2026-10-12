#!/usr/bin/env python3
"""
xmindgen.core — Pure-Python XMind 8 file generator

No external dependencies. Works on Python 3.8+.
Tested with XMind 8, XMind 2025 (ZEN mode).
"""

import zipfile
import os
import time
import re
import uuid

# ─── XML Helpers ──────────────────────────────────────────────────────────────

def _nid():
    """Generate a unique XMind topic ID."""
    return f"id-{int(time.time())}-{uuid.uuid4().hex[:8]}"

def _xml_esc(s):
    """Escape special XML characters."""
    return (str(s)
        .replace("&", "&amp;")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
        .replace('"', "&quot;")
        .replace("'", "&apos;"))

def _topic_xml(id_, title, children_xml="", notes="", props_xml=""):
    """Render a single <topic> element (no styling)."""
    r = f'<topic id="{id_}">'
    r += f"<title>{_xml_esc(title)}</title>"
    if notes:
        r += f"<notes><plain-text>{_xml_esc(notes)}</plain-text></notes>"
    if props_xml:
        r += f"<topic-props>{props_xml}</topic-props>"
    if children_xml:
        r += "<children><topics type=\"attached\">"
        r += children_xml
        r += "</topics></children>"
    r += "</topic>"
    return r

def _leaf(title, notes=""):
    """Create a leaf topic dict."""
    return {"id": _nid(), "title": title, "notes": notes}

def _build_children(children):
    """Recursively build children XML from a list of topic dicts."""
    xml_parts = []
    for child in children:
        xml_parts.append(_topic_dict_to_xml(child))
    return "".join(xml_parts)

def _topic_dict_to_xml(topic_dict):
    """Convert a topic dict (or Topic object) to <topic> XML string."""
    if hasattr(topic_dict, "to_dict"):
        topic_dict = topic_dict.to_dict()

    tid = topic_dict.get("id") or _nid()
    title = topic_dict.get("title", "")
    notes = topic_dict.get("notes", "")
    children = topic_dict.get("children", [])
    rels = topic_dict.get("_rels", [])

    children_xml = _build_children(children)
    return _topic_xml(tid, title, children_xml, notes)


# ─── Topic Class ──────────────────────────────────────────────────────────────

class Topic:
    """
    Programmatic topic builder.

    Usage:
        root = Topic("Root")
        child = root.add_child("My Branch")
        child.add_child("Leaf A")
        child.add_child("Leaf B")

        root.save("map.xmind")
    """

    def __init__(self, title, notes="", topic_id=None):
        self.id = topic_id or _nid()
        self.title = title
        self.notes = notes
        self._children = []
        self._relationships = []  # list of (other_topic_id, label)

    def add_child(self, title, notes=""):
        """Add a child topic and return it for chaining."""
        child = Topic(title, notes)
        self._children.append(child)
        return child

    def add_relationship(self, other_topic_id, label=""):
        """Add a bidirectional relationship (cross-reference) to another topic."""
        self._relationships.append((other_topic_id, label))
        return self

    def to_dict(self):
        """Serialize to a plain dict (compatible with dict-based API)."""
        return {
            "id": self.id,
            "title": self.title,
            "notes": self.notes,
            "children": [c.to_dict() for c in self._children],
            "_rels": self._relationships,
        }

    def save(self, path, styles=None):
        """Save this topic tree as an XMind file."""
        save(path, self, styles=styles)


# ─── Dict-based Tree Builder ──────────────────────────────────────────────────

def build_tree(title, *children, notes="", **kwargs):
    """
    Build a topic tree using dicts (no Topic class needed).

    Usage:
        tree = build_tree(
            "Root",
            {"title": "Branch 1", "children": [
                {"title": "Leaf 1a"},
            ]},
            {"title": "Branch 2"},
        )
    """
    node = {"id": _nid(), "title": title, "notes": notes}
    if children:
        node["children"] = [c if isinstance(c, dict) else {"title": str(c)} for c in children]
    return node


# ─── XMind ZIP Packager ───────────────────────────────────────────────────────

def _make_content_xml(tree, title=None, timestamp=None):
    """Generate the XMind content.xml from a tree dict or Topic."""
    if hasattr(tree, "to_dict"):
        tree = tree.to_dict()

    ts = timestamp or int(time.time())
    root_title = title or tree.get("title", "Mind Map")
    root_id = tree.get("id") or _nid()

    # Recursively render all topics (collects all relationship pairs)
    root_xml = _topic_dict_to_xml(tree)
    rels_xml = _build_relationships_xml(tree)

    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<xmap-content xmlns:xmap="http://www.xmind.org/xmap" '
        'xmlns:fo="http://www.w3.org/1999/XSL/Format">\n'
        f'  <sheet id="{_nid()}" timestamp="{ts}" version="2.0">\n'
        f"    <title>{_xml_esc(root_title)}</title>\n"
        f"    <root-topic>{root_xml}</root-topic>\n"
        f"  </sheet>\n"
        f"  <relationships>{rels_xml}</relationships>\n"
        "</xmap-content>"
    )

def _collect_relationships(topic_dict, collected=None):
    """Recursively collect all (id1, id2, label) triples from topic dicts."""
    if collected is None:
        collected = []
    if hasattr(topic_dict, "to_dict"):
        topic_dict = topic_dict.to_dict()
    for rel in topic_dict.get("_rels", []):
        collected.append((topic_dict["id"], rel[0], rel[1]))
    for child in topic_dict.get("children", []):
        _collect_relationships(child, collected)
    return collected

def _build_relationships_xml(tree):
    """Build <relationship> XML elements from all relationship pairs."""
    rels = _collect_relationships(tree)
    parts = []
    for end1, end2, label in rels:
        parts.append(
            f'<relationship id="{_nid()}" type="generalization" '
            f'end1="{end1}" end2="{end2}">'
            f"<title>{_xml_esc(label)}</title>"
            f"</relationship>"
        )
    return "".join(parts)

def _make_styles_xml(styles_dict):
    """
    Generate the XMind styles.xml.

    styles_dict = {
        topic_id: (background_hex, title_hex),  e.g. ("#1A6B5C", "#FFFFFF")
        ...
    }
    """
    if not styles_dict:
        return ""

    parts = ['<?xml version="1.0" encoding="UTF-8"?>\n',
             '<style-sheet xmlns:fo="http://www.w3.org/1999/XSL/Format">\n',
             '  <styles>\n']

    for topic_id, (bg, fg) in styles_dict.items():
        parts.append(
            f'    <topic id="{topic_id}">\n'
            f'      <title-color>{fg}</title-color>\n'
            f'      <background-color>{bg}</background-color>\n'
            f'    </topic>\n'
        )

    parts.extend(['  </styles>\n', '</style-sheet>'])
    return "".join(parts)

def _manifest_xml():
    """Return the XMind META-INF/manifest.xml."""
    return (
        '<?xml version="1.0" encoding="UTF-8"?>\n'
        '<manifest>\n'
        '  <file-list>\n'
        '    <file path="content.xml" />\n'
        '    <file path="META-INF/styles.xml" />\n'
        '  </file-list>\n'
        '</manifest>'
    )


# ─── Public API ───────────────────────────────────────────────────────────────

def save(path, tree, title=None, styles=None, relationships=None):
    """
    Save a mind-map tree as a .xmind file.

    Parameters
    ----------
    path : str
        Output .xmind file path.
    tree : dict or Topic
        Root topic dict or Topic instance.
        Dict format: {"title": str, "notes": str, "children": [dict, ...], ...}
        Topic objects have .to_dict() called automatically.
    title : str, optional
        Sheet title override. Defaults to root topic's title.
    styles : dict, optional
        {topic_id: (bg_hex, text_hex)}. Example: {"branch1": ("#1A6B5C", "#FFFFFF")}
    relationships : list of (id1, id2, label), optional
        Cross-reference relationships. (deprecated: use Topic.add_relationship instead)

    Example
    -------
        from xmindgen import save, Topic

        root = Topic("My Map")
        a = root.add_child("Branch A")
        a.add_child("Leaf 1", notes="Details here")
        b = root.add_child("Branch B")
        b.add_child("Leaf 2")

        # Add cross-reference relationship
        a.add_relationship(b.id, "A↔B link")

        # Style branches with distinct colors
        root.save("out.xmind", styles={
            a.id: ("#1A6B5C", "#FFFFFF"),
            b.id: ("#7B2D8B", "#FFFFFF"),
        })
    """
    os.makedirs(os.path.dirname(path) or ".", exist_ok=True)

    # Handle relationships parameter (backward compat)
    if relationships:
        if hasattr(tree, "to_dict"):
            tree = tree.to_dict()
        # Inject relationships into root dict
        existing_rels = tree.get("_rels", [])
        tree["_rels"] = existing_rels + list(relationships)

    content = _make_content_xml(tree, title=title)
    styles_content = _make_styles_xml(styles) if styles else ""

    with zipfile.ZipFile(path, "w", zipfile.ZIP_DEFLATED) as zout:
        zout.writestr("content.xml", content)
        if styles_content:
            zout.writestr("META-INF/styles.xml", styles_content)
        zout.writestr("META-INF/manifest.xml", _manifest_xml())

    return path


# ─── Low-level XML generators (public) ──────────────────────────────────────

def to_content_xml(tree, timestamp=None):
    """Return the content.xml XML string for a tree."""
    return _make_content_xml(tree, timestamp=timestamp)

def to_styles_xml(styles_dict):
    """Return the styles.xml XML string for a styles dict."""
    return _make_styles_xml(styles_dict)

def manifest_xml():
    """Return the META-INF/manifest.xml XML string."""
    return _manifest_xml()
