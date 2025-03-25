#!/bin/bash

# Define mode config paths
FOLLOWER_ARM_MODES="/home/robot/interbotix_ws/src/aloha_ros2/config/follower_arm_modes.yaml"

# Function to open a new terminal and run a command
open_terminal() {
    gnome-terminal --tab -- bash -c "$1; exec bash"
}

sleep 3

open_terminal "ros2 launch interbotix_xsarm_control xsarm_control.launch.py robot_model:=vx300s \
mode_configs:='$FOLLOWER_ARM_MODES' use_rviz:=false"

sleep 2

open_terminal "ros2 run aloha_ros2 mirror_control_recv_socket"
