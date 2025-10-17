#!/usr/bin/env python3
from pathlib import Path
import re, sys
# Add a new path (for example: "/my/custom/modules")
script_file = Path(__file__).resolve()
sys.path.append(str(script_file.parents))
from config import REPO_PATH

SRC = REPO_PATH / "notes/README.template.md"
OUT = REPO_PATH / "README.md"                # built file to render (e.g., README.md)
INCLUDE_RE = re.compile(r"<!--\s*include:(.*?)\s*-->")

def expand_includes(text, base=Path(".")):
    def repl(m):
        rel = m.group(1).strip()
        p = (base / rel).resolve()
        if not p.exists():
            return f"<!-- missing: {rel} -->"
        return p.read_text(encoding="utf-8")
    return INCLUDE_RE.sub(repl, text)

def main():
    src = SRC.read_text(encoding="utf-8")
    out = expand_includes(src)
    OUT.write_text(out, encoding="utf-8")

if __name__ == "__main__":
    sys.exit(main())
