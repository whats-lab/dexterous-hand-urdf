import re
import sys
from pathlib import Path

COLUMNS = ("Robot Model", "Official Website", "URDF Source", "License")
HANDS = "robots/hands/"
LINK = re.compile(r"\[([^\]]+)\]\(([^)]+)\)")


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def readme_rows(readme):
    rows = {}
    index = None
    problems = []
    for n, line in enumerate(readme.read_text().splitlines(), 1):
        if not line.lstrip().startswith("|"):
            continue
        row = cells(line)
        if row[0] == COLUMNS[0]:
            header = {c.split(" (")[0]: i for i, c in enumerate(row)}
            missing = [c for c in COLUMNS if c not in header]
            if missing:
                problems.append(f"line {n}: header lacks columns {missing}")
                index = None
            else:
                index = [header[c] for c in COLUMNS]
            continue
        if index is None or f"]({HANDS}" not in row[0]:
            continue
        if len(row) <= max(index):
            problems.append(f"line {n}: {len(row)} cells, expected at least {max(index) + 1}")
            continue
        empty = [c for c, i in zip(COLUMNS, index) if not row[i]]
        if empty:
            problems.append(f"line {n}: empty {empty}")
        link = LINK.search(row[0])
        hid = link.group(2).rstrip("/").split("/")[-1] if link else row[0]
        if hid in rows:
            problems.append(f"line {n}: duplicate row for {hid} (first on line {rows[hid]})")
        rows.setdefault(hid, n)
    if not rows and not problems:
        problems.append(f"no table with columns {list(COLUMNS)} listing {HANDS} folders")
    return rows, problems


def hand_folders(hands_root):
    return {d.name for d in hands_root.iterdir() if d.is_dir() and any(d.rglob("*.urdf"))}


def main():
    repo = Path(sys.argv[1] if len(sys.argv) > 1 else ".")
    rows, problems = readme_rows(repo / "README.md")
    folders = hand_folders(repo / HANDS)
    for hid in sorted(set(rows) - folders):
        problems.append(f"line {rows[hid]}: row {hid} has no {HANDS}{hid} folder with a URDF")
    for hid in sorted(folders - set(rows)):
        problems.append(f"folder {HANDS}{hid} has no README row")
    for p in problems:
        print(p)
    if problems:
        print(f"README table and {HANDS} disagree: {len(problems)} problem(s)")
        return 1
    print(f"README table matches {HANDS}: {len(folders)} hands")
    return 0


if __name__ == "__main__":
    sys.exit(main())
