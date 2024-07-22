# ALOHA_ROS2

## Usage of Mirror Action

1. `source {path to interbotix workspace}/install/setup.bash`  
1. Go to `aloha_ros2/scripts` directory
2. Run two scripts (`start_vx_left.sh` and `start_wx_left.sh`) in seperate terminal to start the master and puppet robot arms
3. Run `python3 -m aloha_ros2.main`
4. Wait for a while you may see two arms rise to a ready pose at the same time.
5. Hold the master arm (WidowX 250s) and press the gripper a little bit to start the mirror action.

## Description

This is a package transplanting [ALOHA](https://github.com/tonyzhaozh/aloha) to ROS2 and it's under development.

## To-Do List

- [x] Single side tele-operation
- [ ] Two sides tele-operation
- [ ] What else?