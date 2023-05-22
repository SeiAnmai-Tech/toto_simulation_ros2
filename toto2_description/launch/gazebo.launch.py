import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
import xacro
import tempfile

def generate_launch_description():
    # robot_description_cmd = [
    #     'xacro',
    #     os.path.join(get_package_share_directory('toto2_description'), 'urdf/toto.xacro'),
    # ]
    temp_file = tempfile.NamedTemporaryFile(delete=False)
    temp_file.write(xacro.process_file(os.path.join(get_package_share_directory('toto2_description'), 'urdf/toto.xacro')).toxml().encode('utf-8'))
    temp_file.close()

    model_path = LaunchConfiguration('model', default=temp_file.name)
    gui_enabled = LaunchConfiguration('gui', default='true')
    rviz_config_path = os.path.join(get_package_share_directory('toto2_description'), 'launch/urdf.rviz')

    robot_description_cmd = [
        'xacro',
        ' ', model_path,
    ]

    robot_description = SetEnvironmentVariable('robot_description', Command(robot_description_cmd))

    spawn_urdf_node = Node(
        package='gazebo_ros',
        executable='spawn_model',
        name='spawn_urdf',
        arguments=['-param', 'robot_description', '-urdf', '-model', 'toto']
    )

    empty_world_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('gazebo_ros'), 'launch/empty_world.launch')),
        launch_arguments={
            'world_name': os.path.join(get_package_share_directory('toto2_gazebo'), 'worlds/testworld.xml'),
            'paused': 'false',
            'use_sim_time': 'true',
            'gui': 'true',
            'headless': 'false',
            'debug': 'false'
        }.items()
    )

    return LaunchDescription([
        robot_description,
        spawn_urdf_node,
        empty_world_launch
    ])
