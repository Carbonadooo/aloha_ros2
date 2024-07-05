source /home/intern/interbotix_ws/install/setup.bash
ros2 launch interbotix_xsarm_control xsarm_control.launch.py robot_model:=vx300s mode_configs:="/home/intern/interbotix_ws/src/aloha_ros2/config/puppet_modes_left.yaml"
