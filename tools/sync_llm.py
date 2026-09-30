"""Copy tools/llm_template.py into every episode folder as llm.py."""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
template = (root / "tools" / "llm_template.py").read_text(encoding="utf-8")
for folder in sorted(root.glob("ep[0-9][0-9]-*")):
    if folder.name.startswith("ep02") or any(folder.glob("*.py")):
        (folder / "llm.py").write_text(template, encoding="utf-8")
        print("updated", folder.name)
