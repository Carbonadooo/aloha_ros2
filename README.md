# ALOHA_ROS2

## Description

This is a package modified from [ALOHA](https://github.com/tonyzhaozh/aloha) to ROS2 and it's under development.

## Tested in

- ROS 2 Humble
- Interbotix ROS packages

## Installation

1. Clone the repository into your workspace:
   ```bash
   cd ~/interbotix/src
   git clone https://github.com/Carbonadooo/aloha_ros2.git
   ```

2. Build the package:
   ```bash
   cd ~/interbotix/src
   colcon build
   ```

3. Source the workspace:
   ```bash
   source install/setup.bash
   ```

## Usage of Mirror Action (Teleoperation)

1. Follow [ALOHA README](https://github.com/tonyzhaozh/aloha?tab=readme-ov-file#hardware-installation) to bind each robot to a fixed symlink port with the following mapping:
   - ``ttyDXL_leader_arm``: the controller arm that the operator would be holding (using wx250s)
   - ``ttyDXL_follower_arm``: the robotic arm that performs the task (using vx300s)
2. Assume that you automatically source interbotix workspace for each new terminal, otherwise you may modify [mirror_control.sh](scripts/mirror_control.sh).
3. Run the launch file:
   ```bash
   ros2 launch aloha_ros2 mirror_control.launch.py
   ```
   
4. Wait 10 seconds and then use can control the leader arm with gravity compensation.
5. To terminate, put the leader arm as low as you can, and the follower arm will go down, too. Hold the arms to avoid collapse and damage, and terminate all terminal windows.

## To-Do List

- [x] Single side tele-operation
- [ ] Two sides tele-operation
- [ ] Avoid sudden movements when the follower arm exits the dead zone
- [ ] Automate the termination
- [ ] What else?