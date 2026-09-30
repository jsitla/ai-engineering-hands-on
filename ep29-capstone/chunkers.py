"""Three ways to cut a document into chunks."""
import re


def fixed(text, size=300):
    """Every `size` characters, no matter where words or sentences end."""
    return [text[i:i + size] for i in range(0, len(text), size)]


def fixed_overlap(text, size=300, overlap=100):
    """Like fixed, but each chunk repeats the end of the previous one."""
    step = size - overlap
    return [text[i:i + size] for i in range(0, len(text), step)]


def by_section(text):
    """Split on headings and paragraphs, and keep the section title on every piece."""
    chunks = []
    title = ""
    for block in re.split(r"\n\s*\n", text):
        block = block.strip()
        if not block:
            continue
        if block.startswith("#"):
            title = block.lstrip("# ").strip()
            continue
        chunks.append(f"{title}: {block}")
    return chunks
