import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, SetEnvironmentVariable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from launch.conditions import IfCondition
import xacro
import tempfile


def generate_launch_description():
    # model_path = LaunchConfiguration('model', default=xacro.process_file(os.path.join(get_package_share_directory('toto2_description'), 'urdf/toto.xacro')))
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

    use_gui = SetEnvironmentVariable('use_gui', gui_enabled)

    joint_state_publisher_node = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher'
    )

    robot_state_publisher_node = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher'
    )

    rviz_node = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        arguments=['-d', rviz_config_path],
        condition=IfCondition(gui_enabled)
    )

    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(get_package_share_directory('toto2_description'), 'launch/gazebo.launch.py'))
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'model',
            default_value=model_path,
            description='Path to the robot model'
        ),
        DeclareLaunchArgument(
            'gui',
            default_value=gui_enabled,
            description='Enable joint_state_publisher GUI'
        ),
        # DeclareLaunchArgument(
        #     'rvizconfig',
        #     default_value=rviz_config_path,
        #     description='Path to the RViz configuration file'
        # ),
        robot_description,
        use_gui,
        joint_state_publisher_node,
        robot_state_publisher_node,
        # rviz_node,
        gazebo_launch
    ])
