from pathlib import Path


CHECK_SUFFIXES = {".py", ".md", ".txt", ".yml", ".yaml"}
SKIP_DIRS = {".git", "__pycache__", "node_modules", "dist", "build", ".venv", "venv"}
CHECK_ROOT_FILES = {
    ".gitlab-ci.yml",
    ".pre-commit-config.yaml",
    "README.md",
    "CHANGELOG.md",
    "CONTRIBUTING.md",
    "SPEC.md",
    "requirements.txt",
    "app.py",
    "cli.py",
}
CHECK_DIRS = {"scripts", "tests"}


def iter_files():
    for path in Path(".").rglob("*"):
        if not path.is_file():
            continue
        if any(part in SKIP_DIRS for part in path.parts):
            continue
        if path.parts[0] not in CHECK_DIRS and str(path) not in CHECK_ROOT_FILES:
            continue
        if path.suffix.lower() in CHECK_SUFFIXES:
            yield path


def main():
    failures = []
    for path in iter_files():
        text = path.read_text(encoding="utf-8", errors="ignore")
        if text == "":
            continue
        if "\t" in text:
            failures.append(f"{path}: contains tab characters")
        if not text.endswith("\n"):
            failures.append(f"{path}: missing final newline")
        for number, line in enumerate(text.splitlines(), start=1):
            if line.rstrip() != line:
                failures.append(f"{path}:{number}: trailing whitespace")
            if path.suffix == ".py" and len(line) > 120:
                failures.append(f"{path}:{number}: Python line exceeds 120 characters")

    if failures:
        raise SystemExit("Formatting check failed:\n" + "\n".join(failures))

    print("format check passed")


if __name__ == "__main__":
    main()
