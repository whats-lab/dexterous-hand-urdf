import os

from setuptools import setup

package_name = 'dexhand_description'


def _share_data_files():
    """dexhand_description/**(비 .py) → share/dexhand_description/** (ament/ROS 해석용)."""
    result = [
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ]
    for root, _dirs, files in os.walk(package_name):
        if '__pycache__' in root:
            continue
        fl = [os.path.join(root, f) for f in files if not f.endswith('.py')]
        if fl:
            # root = dexhand_description/orca_hand/meshes → share/dexhand_description/orca_hand/meshes
            result.append((os.path.join('share', root), fl))
    return result


setup(
    name=package_name,
    version='0.1.0',
    packages=[package_name],
    # pip: 패키지 하위 자산(urdf/mesh/rviz/LICENSE)을 wheel 에 동봉
    package_data={package_name: ['**/*']},
    exclude_package_data={package_name: ['**/__pycache__/**', '**/*.py[cod]']},
    include_package_data=True,
    # ROS(colcon ament_python): share 트리 설치
    data_files=_share_data_files(),
    install_requires=['setuptools'],
    zip_safe=False,
    maintainer='WHATs LAB',
    maintainer_email='minjun.park@whatslab.co.kr',
    description='WHATs LAB dexterous hand + arm robot description (URDF / meshes / rviz).',
    license='per-model LICENSE (BSD / MIT / Apache-2.0); base_hand: WHATs LAB',
)
