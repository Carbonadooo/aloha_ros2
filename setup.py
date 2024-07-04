from setuptools import find_packages, setup

package_name = 'aloha_ros2'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
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
        ],
    },
)
