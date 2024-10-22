import glob
import os

from setuptools import find_packages
from setuptools import setup

package_name = 'turtlebot3_drl'

setup(
    name=package_name,
    version='2.0.0',
    packages=find_packages(),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch', glob.glob(os.path.join('launch', 'turtlebot3_drl_stage1.launch.py'))),
        ('share/' + package_name + '/launch', glob.glob(os.path.join('launch', 'turtlebot3_drl_stage2.launch.py'))),
        ('share/' + package_name + '/launch', glob.glob(os.path.join('launch', 'turtlebot3_drl_stage3.launch.py'))),
        ('share/' + package_name + '/launch', glob.glob(os.path.join('launch', 'turtlebot3_drl_stage4.launch.py'))),
        ('share/' + package_name + '/launch', glob.glob(os.path.join('launch', 'turtlebot3_drl_stage5.launch.py'))),
        ('share/' + package_name + '/launch', glob.glob(os.path.join('launch', 'turtlebot3_drl_stage6.launch.py'))),
    ],
    install_requires=['setuptools', 'launch'],
    zip_safe=True,
    maintainer='varunl11',
    maintainer_email='varunl11@todo.todo',
    keywords=['ROS', 'ROS2', 'examples', 'rclpy'],
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'environment = turtlebot3_drl.q_learning_environment.environment:main',
            'gazebo_goals = turtlebot3_drl.q_learning_gazebo.gazebo:main',
            'train_agent = turtlebot3_drl.drl_agent.drl_agent:main_train',
            'test_agent = turtlebot3_drl.drl_agent.drl_agent:main_test',
        ],
    },
)
