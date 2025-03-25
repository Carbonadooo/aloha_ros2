from setuptools import find_packages, setup
from glob import glob
import os

package_name = 'aloha_ros2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.launch.py')),
        (os.path.join('share', package_name, 'config'), glob('config/*.yaml')),
    ],
    install_requires=[
        'setuptools',
        'rclpy',
        'std_msgs',
    ],
    zip_safe=True,
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'one_side_op = aloha_ros2.main:teleop',
            'mirror_control = aloha_ros2.mirror_control:main',
            'mirror_control_send_socket = aloha_ros2.mirror_control_send_socket:main',
        ],
    },
)
