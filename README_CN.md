# Elite Robots CS ROS 2 Description

[English](README.md) | 中文

本仓库提供 Elite Robots CS/LS 系列机器人的 ROS 2 描述包，包名为
`elite_robots_description`。内容包括 Xacro/URDF 模型、关节限制、运动学与物理参数、
可视化及碰撞网格，以及用于 RViz2 预览机器人的启动文件。

## 支持的机器人

| 系列 | 型号 |
| --- | --- |
| CS | `cs63`、`cs66`、`cs66a`、`cs68`、`cs612`、`cs616`、`cs618f`、`cs620`、`cs625`、`cs520h` |
| LS | `ls65` |

其中 `cs520h` 为 5 轴机型，启动文件会自动选择 `urdf_5f` 中的模型。

## 环境要求

- ROS 2
- `colcon`
- `rosdep`
- RViz2、Xacro、Robot State Publisher 和 Joint State Publisher GUI

推荐先使用 `rosdep` 安装 `package.xml` 中声明的依赖。

## 安装与编译

将仓库放入 ROS 2 工作空间的 `src` 目录：

```bash
mkdir -p ~/elite_ros_ws/src
cd ~/elite_ros_ws/src
git clone <repository-url> Elite_Robots_CS_ROS2_Description

cd ~/elite_ros_ws
rosdep install --from-paths src --ignore-src -r -y
colcon build --symlink-install --packages-select elite_robots_description
source install/setup.bash
```

如果已经位于包含本仓库的工作空间中，只需从工作空间根目录执行最后三条命令。

## 在 RViz2 中查看模型

启动时必须通过 `cs_type` 指定机器人型号。例如查看 CS63：

```bash
ros2 launch elite_robots_description view_cs.launch.py cs_type:=cs63
```

查看其他型号时替换参数即可：

```bash
ros2 launch elite_robots_description view_cs.launch.py cs_type:=cs620
ros2 launch elite_robots_description view_cs.launch.py cs_type:=cs520h
```

启动后可使用 Joint State Publisher GUI 调整关节角度，并在 RViz2 中观察模型和 TF。

### 常用启动参数

| 参数 | 默认值 | 说明 |
| --- | --- | --- |
| `cs_type` | 无 | 机器人型号，必填 |
| `safety_limits` | `true` | 是否启用安全软限位 |
| `safety_pos_margin` | `0.15` | 距离关节上下限的安全裕量 |
| `safety_k_position` | `20` | 安全控制器的位置增益 |
| `tf_prefix` | 空 | TF 与关节名称前缀，适用于多机器人场景 |
| `description_package` | `elite_robots_description` | 提供描述文件的 ROS 2 包 |
| `description_file` | `cs.urdf.xacro` | 要加载的描述文件 |

例如，使用 TF 前缀并关闭安全软限位：

```bash
ros2 launch elite_robots_description view_cs.launch.py \
  cs_type:=cs66 \
  tf_prefix:=robot1_ \
  safety_limits:=false
```

## 生成 URDF

编译并加载工作空间环境后，可直接展开 Xacro：

```bash
xacro "$(ros2 pkg prefix elite_robots_description)/share/elite_robots_description/urdf/cs.urdf.xacro" \
  cs_type:=cs63 \
  name:=cs63 \
  > /tmp/cs63.urdf
```

对于 `cs520h`，请使用 5 轴入口文件：

```bash
xacro "$(ros2 pkg prefix elite_robots_description)/share/elite_robots_description/urdf_5f/cs.urdf.xacro" \
  cs_type:=cs520h \
  name:=cs520h \
  > /tmp/cs520h.urdf
```

主 Xacro 还提供真实硬件、Fake Hardware、Gazebo/Ignition 仿真、工具串口通信及初始关节位置等参数，可在集成驱动或仿真系统时按需传入。

## 参数文件

每个机器人型号在 `config/<型号>/` 下包含：

- `joint_limits.yaml`：关节位置、速度等限制
- `default_kinematics.yaml`：默认运动学参数
- `physical_parameters.yaml`：连杆质量、惯量等物理参数
- `visual_parameters.yaml`：模型网格及外观参数

仿真的初始关节位置位于 `config/initial_positions*.yaml`。

## 项目结构

```text
.
├── config/          # 各型号参数及仿真初始位置
├── launch/          # RViz2 预览启动文件
├── meshes/          # 视觉与碰撞网格
├── rviz/            # RViz2 配置
├── test/            # Xacro/URDF 与启动测试
├── urdf/            # 通用 6 轴机器人描述
└── urdf_5f/         # 5 轴机器人描述
```

## 测试

从工作空间根目录执行：

```bash
colcon test --packages-select elite_robots_description
colcon test-result --verbose
```

测试会检查 Xacro 能否正确展开为 URDF，并验证 RViz 描述启动文件。

## 许可证

本项目采用 [Apache License 2.0](LICENSE)。
