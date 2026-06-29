from pathlib import Path

REQUIRED_FILES = [
    "README.md",
    "LICENSE",
    "CONTRIBUTING.md",
    "CHANGELOG.md",
    "SPEC.md",
    "app.py",
    "cli.py",
    "requirements.txt",
    ".gitignore",
]

README_TERMS = [
    "Streamlit",
    "CPU",
    "SQLite",
    "cloud",
    "app.py",
]


def main():
    missing = [path for path in REQUIRED_FILES if not Path(path).exists()]
    if missing:
        raise SystemExit(
            f"Missing required metadata/project files: {', '.join(missing)}"
        )

    readme = Path("README.md").read_text(encoding="utf-8")
    missing_terms = [
        term for term in README_TERMS if term.lower() not in readme.lower()
    ]
    if missing_terms:
        raise SystemExit(
            f"README is missing required terms: {', '.join(missing_terms)}"
        )

    license_text = Path("LICENSE").read_text(encoding="utf-8", errors="ignore")
    strong_copyleft = [
        "GNU GENERAL PUBLIC LICENSE",
        "GNU AFFERO GENERAL PUBLIC LICENSE",
    ]
    if not any(name in license_text for name in strong_copyleft):
        raise SystemExit("LICENSE must be a strong copyleft GPL/AGPL license")

    print("metadata audit passed")


if __name__ == "__main__":
    main()
