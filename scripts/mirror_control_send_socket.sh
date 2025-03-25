#!/bin/bash

# Define mode config paths
LEADER_ARM_MODES="/home/robot/interbotix_ws/src/aloha_ros2/config/leader_arm_modes.yaml"
FOLLOWER_ARM_MODES="/home/robot/interbotix_ws/src/aloha_ros2/config/follower_arm_modes.yaml"

tmux new-session -d -s launch_wx250s "ros2 launch interbotix_xsarm_gravity_compensation interbotix_gravity_compensation.launch.py robot_model:=wx250s \
mode_configs:='$LEADER_ARM_MODES' use_rviz:=false; bash" 

sleep 3

tmux new-session -d -s service_wx250s "ros2 service call /wx250s/gravity_compensation_enable std_srvs/srv/SetBool 'data: true'; bash" 

sleep 3

tmux new-session -d -s mirror_control "ros2 run aloha_ros2 mirror_control_send_socket"

echo "tmux sessions:"
tmux ls

# use "tmux kill-server" to kill all
