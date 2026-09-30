"""Copy the llm.py template into every episode folder.
Episodes 1-20 get tools/llm_template.py (as shown in those videos).
Episodes 21+ get tools/llm_template_v2.py: one reused client, and 127.0.0.1 (see episode 21)."""
from pathlib import Path

root = Path(__file__).resolve().parent.parent
v1 = (root / "tools" / "llm_template.py").read_text(encoding="utf-8")
v2 = (root / "tools" / "llm_template_v2.py").read_text(encoding="utf-8")
for folder in sorted(root.glob("ep[0-9][0-9]-*")):
    if folder.name.startswith("ep02") or any(folder.glob("*.py")):
        (folder / "llm.py").write_text(v2 if int(folder.name[2:4]) >= 21 else v1, encoding="utf-8")
        print("updated", folder.name)
