import re
from pathlib import Path


SKIP_DIRS = {".git", "__pycache__", "node_modules", "dist", "build", ".venv", "venv"}
SKIP_SUFFIXES = {".png", ".jpg", ".jpeg", ".gif", ".svg", ".ico", ".db", ".sqlite3", ".pyc"}
PATTERNS = {
    "aws_access_key": re.compile(r"AKIA[0-9A-Z]{16}"),
    "private_key": re.compile(r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----"),
    "generic_token": re.compile(r"(?i)(api[_-]?key|secret|token)\s*=\s*['\"][^'\"]{12,}['\"]"),
}


def iter_files():
    for path in Path(".").rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.suffix.lower() in SKIP_SUFFIXES:
            continue
        yield path


def main():
    findings = []
    for path in iter_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        for name, pattern in PATTERNS.items():
            if pattern.search(text):
                findings.append(f"{path}: {name}")

    if findings:
        raise SystemExit("Potential secrets found:\n" + "\n".join(findings))

    print("secret scan passed")


if __name__ == "__main__":
    main()
