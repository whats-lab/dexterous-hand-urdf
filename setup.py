import os

from setuptools import setup

package_name = "dexhand_description"
hands_dir = os.path.join("robots", "hands")
share_dir = os.path.join("share", package_name)


def hand_data_files():
    data_files = [
        ("share/ament_index/resource_index/packages", ["resource/" + package_name]),
        (share_dir, ["package.xml"]),
    ]
    for root, _dirs, files in sorted(os.walk(hands_dir)):
        if files:
            target = os.path.normpath(os.path.join(share_dir, os.path.relpath(root, hands_dir)))
            data_files.append((target, [os.path.join(root, f) for f in sorted(files)]))
    return data_files


setup(
    name=package_name,
    version="1.0.0",
    packages=[package_name],
    data_files=hand_data_files(),
    install_requires=["setuptools"],
    zip_safe=False,
    entry_points={"console_scripts": ["dexhand-fetch = dexhand_description.mesh_cache:main"]},
    maintainer="WHATs LAB",
    maintainer_email="minjun.park@whatslab.co.kr",
    description="Dexterous robot hand URDF models (dex-urdf hands plus hands added by WHATs LAB; see README).",
    url="https://github.com/whats-lab/dexterous-hand-urdf",
    license=(
        "Per-model, see robots/hands/<hand>/LICENSE* and README: "
        "BSD-2-Clause, BSD-3-Clause, MIT, Apache-2.0, GPL-3.0, CC-BY-NC-SA-4.0, "
        "no license text for some hands (see LICENSE_STATUS.txt), "
        "repository code MIT"
    ),
)
