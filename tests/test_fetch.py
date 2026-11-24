import hashlib
import json

import pytest

from dexhand_description import mesh_cache

MESH = b"solid cube\nendsolid cube\n"


@pytest.fixture
def setup(tmp_path, monkeypatch):
    share = tmp_path / "share"
    hand = share / "toy_hand"
    hand.mkdir(parents=True)
    (hand / "toy_hand_right.urdf").write_text('<robot name="toy"><link name="a"/></robot>')
    upstream = tmp_path / "upstream" / "owner" / "repo" / "abc123"
    (upstream / "dir with space").mkdir(parents=True)
    (upstream / "dir with space" / "part #1.stl").write_bytes(MESH)
    entry = {
        "path": "meshes/part.stl",
        "source": "dir with space/part #1.stl",
        "sha256": hashlib.sha256(MESH).hexdigest(),
        "size": len(MESH),
    }
    manifest = {"repo": "owner/repo", "commit": "abc123", "files": [entry]}
    (hand / "meshes.json").write_text(json.dumps(manifest))
    monkeypatch.setattr(mesh_cache, "get_share", lambda: str(share))
    monkeypatch.setattr(mesh_cache, "RAW_URL", (tmp_path / "upstream").as_uri() + "/{repo}/{commit}/{path}")
    monkeypatch.setenv("XDG_CACHE_HOME", str(tmp_path / "cache"))
    return hand, manifest


def leftovers(root):
    return [p for p in root.rglob("*.part")]


def test_fetch_downloads_verifies_and_skips(setup, tmp_path):
    result = mesh_cache.fetch("toy_hand")
    assert result.ok and result.downloaded == 1
    assert (result.path / "meshes/part.stl").read_bytes() == MESH
    assert (result.path / "toy_hand_right.urdf").is_file()
    again = mesh_cache.fetch("toy_hand")
    assert again.ok and again.downloaded == 0 and again.present == 1
    assert mesh_cache.hand_dir("toy_hand") == result.path
    assert mesh_cache.list_hands() == ["toy_hand"]


def test_hand_dir_without_download_is_none_until_fetched(setup):
    assert mesh_cache.hand_dir("toy_hand", download=False) is None
    assert not (mesh_cache.cache_root() / "toy_hand").exists()
    assert mesh_cache.hand_dir("toy_hand") is not None
    assert mesh_cache.hand_dir("toy_hand", download=False) is not None


def test_missing_upstream_file_fails_without_partial_files(setup, tmp_path):
    hand, manifest = setup
    manifest["files"][0]["source"] = "missing.stl"
    (hand / "meshes.json").write_text(json.dumps(manifest))
    result = mesh_cache.fetch("toy_hand")
    assert not result.ok and result.path is None
    assert result.failed[0][1].startswith("curl exit")
    assert not leftovers(tmp_path / "cache")
    assert not (mesh_cache.cache_root() / "toy_hand/meshes/part.stl").exists()


def test_hash_mismatch_fails_without_partial_files(setup, tmp_path):
    hand, manifest = setup
    manifest["files"][0]["sha256"] = "0" * 64
    (hand / "meshes.json").write_text(json.dumps(manifest))
    result = mesh_cache.fetch("toy_hand")
    assert result.failed == [("meshes/part.stl", "sha256 or size mismatch")]
    assert not leftovers(tmp_path / "cache")
    assert not (mesh_cache.cache_root() / "toy_hand/meshes/part.stl").exists()


def test_corrupted_cache_file_is_replaced(setup):
    path = mesh_cache.hand_dir("toy_hand") / "meshes/part.stl"
    path.write_bytes(b"broken")
    result = mesh_cache.fetch("toy_hand")
    assert result.ok and result.downloaded == 1
    assert path.read_bytes() == MESH


def test_unknown_hand_and_cli(setup, capsys):
    assert not mesh_cache.fetch("nope").ok
    assert mesh_cache.main(["--list"]) == 0
    assert "toy_hand\t1 files" in capsys.readouterr().out
    assert mesh_cache.main(["toy_hand"]) == 0
    assert mesh_cache.main(["nope"]) == 1
    assert mesh_cache.main([]) == 2


def test_not_redistributable_meshes_warn_but_download(setup, capsys):
    hand, manifest = setup
    manifest["redistribute"] = False
    (hand / "meshes.json").write_text(json.dumps(manifest))
    with pytest.warns(UserWarning, match="MESHES-LICENSE"):
        result = mesh_cache.fetch("toy_hand")
    assert result.ok and result.notice
    assert mesh_cache.main(["toy_hand"]) == 0
    assert "MESHES-LICENSE" in capsys.readouterr().err
    assert mesh_cache.main(["--list"]) == 0
    assert "not redistributable" in capsys.readouterr().out
