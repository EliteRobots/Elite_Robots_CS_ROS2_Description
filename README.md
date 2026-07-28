# Elite Robots CS ROS 2 Description

English | [中文](README_CN.md)

This repository provides the ROS 2 description package for Elite Robots CS and
LS series robots. The package is named `elite_robots_description` and includes
Xacro/URDF models, joint limits, kinematic and physical parameters, visual and
collision meshes, and a launch file for viewing the robots in RViz2.

## Supported Robots

| Series | Models |
| --- | --- |
| CS | `cs63`, `cs66`, `cs66a`, `cs68`, `cs612`, `cs616`, `cs618f`, `cs620`, `cs625`, `cs520h` |
| LS | `ls65` |

The `cs520h` is a five-axis model. The launch file automatically selects its
description from the `urdf_5f` directory.

## Requirements

- ROS 2
- `colcon`
- `rosdep`
- RViz2, Xacro, Robot State Publisher, and Joint State Publisher GUI

Use `rosdep` to install the dependencies declared in `package.xml`.

## Installation and Build

Clone this repository into the `src` directory of a ROS 2 workspace:

```bash
mkdir -p ~/elite_ros_ws/src
cd ~/elite_ros_ws/src
git clone <repository-url> Elite_Robots_CS_ROS2_Description

cd ~/elite_ros_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install --packages-select elite_robots_description
source install/setup.bash
```

If the repository is already in a workspace, run the final three commands from
the workspace root.

## View a Robot in RViz2

The `cs_type` argument is required. For example, to view a CS63:

```bash
ros2 launch elite_robots_description view_cs.launch.py cs_type:=cs63
```

Replace the model argument to view another supported robot:

```bash
ros2 launch elite_robots_description view_cs.launch.py cs_type:=cs620
ros2 launch elite_robots_description view_cs.launch.py cs_type:=cs520h
```

After launching, use the Joint State Publisher GUI to adjust the joint
positions and inspect the model and TF tree in RViz2.

### Common Launch Arguments

| Argument | Default | Description |
| --- | --- | --- |
| `cs_type` | None | Robot model; required |
| `safety_limits` | `true` | Enables safety soft limits |
| `safety_pos_margin` | `0.15` | Safety margin from the lower and upper joint limits |
| `safety_k_position` | `20` | Position gain used by the safety controller |
| `tf_prefix` | Empty | Prefix for TF frames and joint names in multi-robot setups |
| `description_package` | `elite_robots_description` | ROS 2 package containing the description |
| `description_file` | `cs.urdf.xacro` | Description file to load |

For example, to use a TF prefix and disable safety soft limits:

```bash
ros2 launch elite_robots_description view_cs.launch.py \
  cs_type:=cs66 \
  tf_prefix:=robot1_ \
  safety_limits:=false
```

## Generate a URDF

After building and sourcing the workspace, expand the Xacro file directly:

```bash
xacro "$(ros2 pkg prefix elite_robots_description)/share/elite_robots_description/urdf/cs.urdf.xacro" \
  cs_type:=cs63 \
  name:=cs63 \
  > /tmp/cs63.urdf
```

Use the five-axis entry point for `cs520h`:

```bash
xacro "$(ros2 pkg prefix elite_robots_description)/share/elite_robots_description/urdf_5f/cs.urdf.xacro" \
  cs_type:=cs520h \
  name:=cs520h \
  > /tmp/cs520h.urdf
```

The main Xacro also accepts parameters for real hardware, fake hardware,
Gazebo/Ignition simulation, tool serial communication, and initial joint
positions. Pass these parameters as needed when integrating the description
with a driver or simulator.

## Configuration Files

Each robot has the following files under `config/<model>/`:

- `joint_limits.yaml`: joint position, velocity, and related limits
- `default_kinematics.yaml`: default kinematic parameters
- `physical_parameters.yaml`: link mass, inertia, and other physical parameters
- `visual_parameters.yaml`: mesh and appearance parameters

Initial joint positions for simulation are stored in
`config/initial_positions*.yaml`.

## Repository Structure

```text
.
├── config/          # Model parameters and initial simulation positions
├── launch/          # RViz2 visualization launch files
├── meshes/          # Visual and collision meshes
├── rviz/            # RViz2 configuration
├── test/            # Xacro/URDF and launch tests
├── urdf/            # Standard six-axis robot descriptions
└── urdf_5f/         # Five-axis robot descriptions
```

## Testing

Run the tests from the workspace root:

```bash
colcon test --packages-select elite_robots_description
colcon test-result --verbose
```

The tests verify that the Xacro files expand to valid URDF and check the RViz
description launch file.

## License

This project is licensed under the [Apache License 2.0](LICENSE).
