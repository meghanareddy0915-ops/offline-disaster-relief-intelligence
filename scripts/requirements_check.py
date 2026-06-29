from pathlib import Path


def main():
    requirements = Path("requirements.txt").read_text(encoding="utf-8").splitlines()
    cleaned = [
        line.strip()
        for line in requirements
        if line.strip() and not line.startswith("#")
    ]

    if not any(line.startswith("streamlit") for line in cleaned):
        raise SystemExit("requirements.txt must include streamlit")

    for line in cleaned:
        if "==" not in line and ">=" not in line and "~=" not in line:
            raise SystemExit(f"Requirement should include a version constraint: {line}")

    print("requirements check passed")


if __name__ == "__main__":
    main()
