# dexterous-hand-urdf

Curated URDF models for dexterous robot hands, used by [atlas_hand_ROS2](https://github.com/whats-lab/atlas_hand_ROS2).

All included models carry commercially-compatible licenses (BSD / MIT / Apache-2.0).

---

## Included Models

| Directory | Hand | Manufacturer | License | Source |
|-----------|------|--------------|---------|--------|
| `base_hand/` | Base Hand | WHATsLAB | Proprietary | Internal |
| `orca_hand/` | Orca Hand | ETH Zurich SRL | MIT | [orcahand_description](https://github.com/orcahand/orcahand_description) |
| `robotis_hx5_d20/` | ROBOTIS Hand 2 HX5 | ROBOTIS | Apache-2.0 | [robotis_hand](https://github.com/ROBOTIS-GIT/robotis_hand) |
| `allegro_hand/` | Allegro Hand | Wonik Robotics | BSD | [dex-urdf](https://github.com/dexsuite/dex-urdf) |
| `leap_hand/` | LEAP Hand | CMU | MIT | [dex-urdf](https://github.com/dexsuite/dex-urdf) |
| `schunk_hand/` | SCHUNK SVH | SCHUNK | Apache-2.0 | [dex-urdf](https://github.com/dexsuite/dex-urdf) |
| `tesollo_dg5f/` | DG5F | Tesollo | BSD-3-Clause | [dg5f_ros2](https://github.com/tesollodelto/dg5f_ros2) |

---

## Directory Layout

Models from **dex-urdf** keep the original layout (URDF at root, `meshes/` alongside):

```
{hand}/
├── {hand}_{side}.urdf
└── meshes/
    └── visual/
```

**Internal models** (base_hand, orca_hand, robotis_hx5_d20) use a `urdf/` subdirectory:

```
{hand}/
├── urdf/
│   ├── left.urdf
│   └── right.urdf
└── meshes/
```

---

## Attribution

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

The base hand model uses anatomical 3D mesh data from **BodyParts3D**.

Copyright © The Database Center for Life Science (DBCLS)  
License: Creative Commons Attribution 4.0 International (CC BY 4.0)  
Changes: Mesh scale adjustment, coordinate axis conversion, and URDF rigging for ROS 2 simulation and FK computation.

The overall base_hand package is © WHATsLAB. All rights reserved.
