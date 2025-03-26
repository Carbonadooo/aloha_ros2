import os
from launch import LaunchDescription
from launch.actions import OpaqueFunction


def launch_setup(context, *args, **kwargs):
    script_path = os.path.join(
        os.getenv("HOME"),
        "fyp_ws/src/aloha_ros2/scripts/mirror_control_recv_socket.sh",
    )
    os.system(f"bash {script_path}")
    return []


def generate_launch_description():
    return LaunchDescription([OpaqueFunction(function=launch_setup)])
