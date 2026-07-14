"""dexhand_description — WHATs LAB dexterous hand + arm robot description.

URDF/메쉬/rviz 자산 패키지. 설치 위치(pip site-packages 또는 ROS share)에서
자산 루트를 해석한다. URDF 의 package://dexhand_description/... URI 가 이 루트로 매핑.
"""
import os


def get_share() -> str:
    """자산 루트(디렉토리) 절대경로. pip: 이 패키지 디렉토리. ROS: share/dexhand_description."""
    return os.path.dirname(os.path.abspath(__file__))
