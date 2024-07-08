from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import (
    LaunchConfiguration,
    PathJoinSubstitution,
)
from launch_ros.substitutions import FindPackageShare


# THIS FUNCTION IS NOT WORKING POROPERLY, DO NOT USE
def generate_launch_description():
    return LaunchDescription([
        # Node(
        #     package='aloha_ros2',
        #     executable='one_side_op',
        #     name='one_side_op',
        #     emulate_tty=True,
        # ),
        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource(
        #         PathJoinSubstitution([
        #             FindPackageShare('interbotix_xsarm_control'),
        #             'launch',
        #             'xsarm_control.launch.py'
        #         ]),
        #     ),
        #     launch_arguments={
        #         'robot_model': 'vx300s',
        #         'robot_name': 'vx300s',
        #         'mode_configs': PathJoinSubstitution([
        #             FindPackageShare('aloha_ros2'),
        #             'config',
        #             'puppet_modes_left.yaml'
        #         ]),
        #         'use_rviz': 'false',
        #         'base_link_frame': 'base_link',
        #         'use_world_frame': 'false',
        #     }.items(),
        # ),
        # IncludeLaunchDescription(
        #     PythonLaunchDescriptionSource(
        #         PathJoinSubstitution([
        #             FindPackageShare('interbotix_xsarm_control'),
        #             'launch',
        #             'xsarm_control.launch.py'
        #         ]),
        #     ),
        #     launch_arguments={
        #         'robot_model': 'wx250s',
        #         'robot_name': 'wx250s',
        #         'mode_configs': PathJoinSubstitution([
        #             FindPackageShare('aloha_ros2'),
        #             'config',
        #             'master_modes_left.yaml'
        #         ]),
        #         'use_rviz': 'false',
        #         'base_link_frame': 'base_link',
        #         'use_world_frame': 'false',
        #     }.items(),
        # ),        

    ])