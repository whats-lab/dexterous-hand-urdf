import argparse
import hashlib
import json
import os
import re
import subprocess
import sys
from pathlib import Path

PACKAGE_PREFIX = "package://dexhand_description/"


def mesh_refs(hand_dir):
    refs = set()
    for urdf in sorted(hand_dir.rglob("*.urdf")):
        for name in re.findall(r'<mesh[^>]*\sfilename="([^"]+)"', urdf.read_text()):
            if name.startswith(PACKAGE_PREFIX):
                path = hand_dir.parent / name[len(PACKAGE_PREFIX) :]
            else:
                path = urdf.parent / name
            refs.add(Path(os.path.normpath(path)).relative_to(hand_dir).as_posix())
    return refs


def companions(rel, originals):
    path = originals / rel
    if path.suffix.lower() != ".obj" or not path.is_file():
        return set()
    names = re.findall(rb"^mtllib\s+(\S+)", path.read_bytes(), re.M)
    return {(Path(rel).parent / n.decode()).as_posix() for n in names if (path.parent / n.decode()).is_file()}


def upstream_blobs(clone, commit):
    tree = subprocess.run(
        ["git", "-C", str(clone), "ls-tree", "-r", commit], capture_output=True, text=True, check=True
    ).stdout
    blobs = {}
    for line in tree.splitlines():
        meta, path = line.split("\t", 1)
        blobs.setdefault(meta.split()[2], []).append(path)
    return blobs


def best_source(rel, candidates, prefix):
    def score(path):
        return (
            path.startswith(prefix),
            Path(path).name == Path(rel).name,
            len(os.path.commonprefix([path[::-1], rel[::-1]])),
        )

    return max(candidates, key=score)


def main(argv=None):
    parser = argparse.ArgumentParser(description="Write <hand>/meshes.json mapping URDF meshes to upstream files.")
    parser.add_argument("hand_dir", type=Path)
    parser.add_argument("--repo", required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--clone", required=True, type=Path)
    parser.add_argument("--originals", type=Path)
    parser.add_argument("--prefer", default="")
    parser.add_argument("--note")
    args = parser.parse_args(argv)
    originals = args.originals or args.hand_dir
    refs = mesh_refs(args.hand_dir)
    for rel in sorted(refs):
        refs |= companions(rel, originals)
    blobs = upstream_blobs(args.clone, args.commit)
    files, missing = [], []
    for rel in sorted(refs):
        path = originals / rel
        if not path.is_file():
            missing.append(f"{rel}: no original file")
            continue
        data = path.read_bytes()
        blob = hashlib.sha1(b"blob %d\0" % len(data) + data).hexdigest()
        if blob not in blobs:
            missing.append(f"{rel}: not in {args.repo}@{args.commit[:7]}")
            continue
        files.append(
            {
                "path": rel,
                "source": best_source(rel, blobs[blob], args.prefer),
                "sha256": hashlib.sha256(data).hexdigest(),
                "size": len(data),
            }
        )
    if missing:
        print("\n".join(missing), file=sys.stderr)
        return 1
    manifest = {"repo": args.repo, "commit": args.commit}
    if args.note:
        manifest["note"] = args.note
    manifest["files"] = files
    (args.hand_dir / "meshes.json").write_text(json.dumps(manifest, indent=1) + "\n")
    print(f"{args.hand_dir.name}: {len(files)} files, {sum(f['size'] for f in files)} bytes")
    return 0


if __name__ == "__main__":
    sys.exit(main())
