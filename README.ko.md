<p align="center"><img src="banner.jpg" alt="WHATs LAB" width="100%"></p>

<p align="center"><a href="README.md">English</a> | <b>한국어</b></p>

# dexterous-hand-urdf

[whatslab](https://github.com/whats-lab/whatslab-sdk) 텔레오퍼레이션 스택
([whatslab-ros2](https://github.com/whats-lab/whatslab-ros2))에서 사용하는, 다관절
로봇 손 URDF 모델 모음입니다.

포함된 모델은 모두 상업 호환 라이선스(BSD / MIT / Apache-2.0)를 따릅니다.

---

## 포함 모델

| 디렉토리 | 손 | 제조사 | 라이선스 | 출처 |
|-----------|------|--------------|---------|--------|
| `base_hand/` | Base Hand | WHATsLAB | Proprietary | Internal |
| `orca_hand/` | Orca Hand | ETH Zurich SRL | MIT | [orcahand_description](https://github.com/orcahand/orcahand_description) |
| `robotis_hx5_d20/` | ROBOTIS Hand 2 HX5 | ROBOTIS | Apache-2.0 | [robotis_hand](https://github.com/ROBOTIS-GIT/robotis_hand) |
| `allegro_hand/` | Allegro Hand | Wonik Robotics | BSD | [dex-urdf](https://github.com/dexsuite/dex-urdf) |
| `leap_hand/` | LEAP Hand | CMU | MIT | [dex-urdf](https://github.com/dexsuite/dex-urdf) |
| `schunk_hand/` | SCHUNK SVH | SCHUNK | Apache-2.0 | [dex-urdf](https://github.com/dexsuite/dex-urdf) |
| `tesollo_dg5f/` | DG5F | Tesollo | BSD-3-Clause | [dg5f_ros2](https://github.com/tesollodelto/dg5f_ros2) |

---

## 디렉토리 구조

**dex-urdf** 계열 모델은 원본 구조를 유지합니다(URDF 루트, `meshes/` 병렬):

```
{hand}/
├── {hand}_{side}.urdf
└── meshes/
    └── visual/
```

**내부 모델**(base_hand, orca_hand, robotis_hx5_d20)은 `urdf/` 하위 디렉토리를 씁니다:

```
{hand}/
├── urdf/
│   ├── left.urdf
│   └── right.urdf
└── meshes/
```

---

## 저작자 표시 (Attribution)

### Allegro Hand
Copyright © Wonik Robotics  
License: BSD  
Changes: none (original from dex-urdf)

### LEAP Hand
Copyright © Carnegie Mellon University  
License: MIT  
Changes: none (original from dex-urdf)

### SCHUNK SVH
Copyright © SCHUNK GmbH  
License: Apache-2.0  
Changes: none (original from dex-urdf)

### ROBOTIS Hand 2 (HX5)
Copyright © ROBOTIS Co., Ltd.  
License: Apache-2.0  
Changes: URDF path adjustments and physics parameter tuning for ROS 2.

### Orca Hand
Copyright © Soft Robotics Lab, ETH Zurich  
License: MIT  
Changes: Added fixed joints at fingertip positions.

### Tesollo DG5F
Copyright © Tesollo  
License: BSD-3-Clause  
Changes: Converted `package://` mesh paths to relative paths.

### Base Hand

base hand 모델은 **BodyParts3D**의 해부학 3D 메쉬 데이터를 사용합니다.

Copyright © The Database Center for Life Science (DBCLS)  
License: Creative Commons Attribution 4.0 International (CC BY 4.0)  
Changes: Mesh scale adjustment, coordinate axis conversion, and URDF rigging for ROS 2 simulation and FK computation.

The overall base_hand package is © WHATsLAB. All rights reserved.

---

## 라이선스

이 저장소는 **서드파티 손 모델을 각자의 upstream 라이선스 아래 모아 놓은 것**입니다
([저작자 표시](#저작자-표시-attribution) 참고 — BSD / MIT / Apache-2.0 / CC BY 4.0).
모음 전체에 단일 라이선스를 부과하지 않으며, 번들된 각 모델은 원래의 라이선스와
저작권을 그대로 유지합니다. WHATs LAB 자체 기여분(패키징·리깅·`base_hand`)은
© WHATs LAB Corp.
