import argparse
import filecmp
import hashlib
import json
import os
import shutil
import subprocess
import sys
import warnings
from concurrent.futures import ThreadPoolExecutor
from dataclasses import dataclass, field
from pathlib import Path
from urllib.parse import quote

from dexhand_description import get_share

VERSION = "1.0.0"
MANIFEST = "meshes.json"
RAW_URL = "https://raw.githubusercontent.com/{repo}/{commit}/{path}"
WORKERS = 8


@dataclass
class FetchResult:
    hand: str
    path: Path | None = None
    downloaded: int = 0
    present: int = 0
    failed: list[tuple[str, str]] = field(default_factory=list)
    notice: str | None = None

    @property
    def ok(self) -> bool:
        return self.path is not None and not self.failed


def hands_root() -> Path:
    return Path(get_share())


def cache_root() -> Path:
    base = os.environ.get("XDG_CACHE_HOME") or os.path.join(os.path.expanduser("~"), ".cache")
    return Path(base) / "dexhand_description" / VERSION


def list_hands() -> list[str]:
    return sorted(p.name for p in hands_root().iterdir() if p.is_dir() and any(p.rglob("*.urdf")))


def load_manifest(hand: str) -> dict:
    path = hands_root() / hand / MANIFEST
    if not path.is_file():
        return {"files": []}
    return json.loads(path.read_text())


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as stream:
        for chunk in iter(lambda: stream.read(1 << 20), b""):
            digest.update(chunk)
    return digest.hexdigest()


def is_valid(path: Path, entry: dict) -> bool:
    return path.is_file() and path.stat().st_size == entry["size"] and sha256(path) == entry["sha256"]


def source_url(manifest: dict, entry: dict) -> str:
    return RAW_URL.format(repo=manifest["repo"], commit=manifest["commit"], path=quote(entry["source"], safe="/"))


def download_file(url: str, target: Path, entry: dict) -> str | None:
    target.parent.mkdir(parents=True, exist_ok=True)
    part = target.with_name(f".{target.name}.{os.getpid()}.part")
    proc = subprocess.run(
        ["curl", "-fsSL", "--retry", "3", "--connect-timeout", "20", "-o", str(part), url],
        capture_output=True,
        text=True,
    )
    if proc.returncode != 0:
        part.unlink(missing_ok=True)
        return f"curl exit {proc.returncode}: {proc.stderr.strip()}"
    if not is_valid(part, entry):
        part.unlink(missing_ok=True)
        return "sha256 or size mismatch"
    os.replace(part, target)
    return None


def sync_files(src: Path, dst: Path, skip: set[str]) -> None:
    for path in sorted(src.rglob("*")):
        rel = path.relative_to(src)
        if not path.is_file() or rel.as_posix() in skip or rel.name == MANIFEST:
            continue
        target = dst / rel
        if target.is_file() and filecmp.cmp(path, target, shallow=False):
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        part = target.with_name(f".{target.name}.{os.getpid()}.part")
        shutil.copyfile(path, part)
        os.replace(part, target)


def fetch(hand: str, download: bool = True) -> FetchResult:
    result = FetchResult(hand)
    src = hands_root() / hand
    if hand not in list_hands():
        result.failed.append((hand, "unknown hand"))
        return result
    dst = cache_root() / hand
    manifest = load_manifest(hand)
    if manifest.get("redistribute") is False:
        result.notice = (
            f"{hand}: the meshes are not redistributable; see {src / 'MESHES-LICENSE'}. "
            "Use them only under that license and do not rehost them."
        )
    todo = []
    for entry in manifest["files"]:
        if is_valid(dst / entry["path"], entry):
            result.present += 1
        elif download:
            todo.append(entry)
        else:
            result.failed.append((entry["path"], "missing"))
    if todo and shutil.which("curl") is None:
        result.failed.extend((e["path"], "curl not found") for e in todo)
        return result
    if todo and result.notice:
        warnings.warn(result.notice, stacklevel=2)
    with ThreadPoolExecutor(WORKERS) as pool:
        errors = pool.map(lambda e: download_file(source_url(manifest, e), dst / e["path"], e), todo)
        for entry, error in zip(todo, errors):
            if error is None:
                result.downloaded += 1
            else:
                result.failed.append((entry["path"], error))
    if not result.failed:
        sync_files(src, dst, {e["path"] for e in manifest["files"]})
        result.path = dst
    return result


def hand_dir(hand: str, download: bool = True) -> Path | None:
    return fetch(hand, download).path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(
        prog="dexhand-fetch",
        description="Download the upstream meshes of dexterous hands into the user cache and verify their sha256.",
    )
    parser.add_argument("hands", nargs="*")
    parser.add_argument("--all", action="store_true")
    parser.add_argument("--list", action="store_true")
    args = parser.parse_args(argv)
    if args.list:
        for hand in list_hands():
            manifest = load_manifest(hand)
            size = sum(e["size"] for e in manifest["files"]) / 1e6
            flag = "\tnot redistributable" if manifest.get("redistribute") is False else ""
            print(f"{hand}\t{len(manifest['files'])} files\t{size:.1f} MB\t{manifest.get('repo', '-')}{flag}")
        return 0
    hands = list_hands() if args.all else args.hands
    if not hands:
        parser.print_usage(sys.stderr)
        return 2
    status = 0
    for hand in hands:
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            result = fetch(hand)
        if result.notice:
            print(f"warning: {result.notice}", file=sys.stderr)
        if result.ok:
            print(f"{hand}: {result.path} ({result.downloaded} downloaded, {result.present} cached)")
            continue
        status = 1
        print(f"{hand}: FAILED ({len(result.failed)} files)", file=sys.stderr)
        for path, reason in result.failed[:10]:
            print(f"  {path}: {reason}", file=sys.stderr)
    return status


if __name__ == "__main__":
    sys.exit(main())
