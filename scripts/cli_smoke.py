import json
import subprocess
import sys


SAMPLE = (
    "SOS: 52 people near Lake Road School need drinking water, food, blankets "
    "and medical help. Contact +91 90000 11111."
)


def main():
    completed = subprocess.run(
        [sys.executable, "cli.py", "--text", SAMPLE, "--no-save"],
        check=True,
        capture_output=True,
        text=True,
    )
    payload = json.loads(completed.stdout)

    if payload["urgency"] != "critical":
        raise SystemExit("CLI did not classify SOS request as critical")
    if payload["peopleAffected"] != 52:
        raise SystemExit("CLI did not extract people affected")
    if "water" not in payload["needs"]:
        raise SystemExit("CLI did not extract water need")
    if not payload["contact"]["phone"]:
        raise SystemExit("CLI did not extract phone contact")

    print("cli smoke passed")


if __name__ == "__main__":
    main()
