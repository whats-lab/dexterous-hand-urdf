import os
import sys
import sysconfig

_NAME = "dexhand_description"
_PKG = os.path.dirname(os.path.abspath(__file__))


def get_share() -> str:
    candidates = [
        os.path.join(os.path.dirname(os.path.realpath(_PKG)), "robots", "hands"),
        os.path.join(_PKG, os.pardir, os.pardir, os.pardir, os.pardir, "share", _NAME),
        os.path.join(sysconfig.get_path("data"), "share", _NAME),
        os.path.join(sys.prefix, "share", _NAME),
    ]
    for path in candidates:
        if os.path.isdir(path):
            return os.path.normpath(path)
    raise FileNotFoundError(f"{_NAME} share directory not found; tried: {candidates}")


from dexhand_description.mesh_cache import FetchResult, fetch, hand_dir, list_hands  # noqa: E402

__all__ = ["FetchResult", "fetch", "get_share", "hand_dir", "list_hands"]
