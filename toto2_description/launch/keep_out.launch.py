import os
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription, ExecuteProcess
from launch.conditions import IfCondition
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import Command, LaunchConfiguration, PythonExpression
from launch_ros.actions import Node
from launch_ros.substitutions import FindPackageShare

def generate_launch_description():

    # Set the path to different files and folders.
    pkg_gazebo_ros = FindPackageShare(package='gazebo_ros').find('gazebo_ros')   
    pkg_share = FindPackageShare(package='toto2_description').find('toto2_description')
    param_pkg_share = FindPackageShare(package='toto2_navigation').find('toto2_navigation')
    default_model_path = os.path.join(pkg_share, 'models/toto2.xacro')
    robot_localization_file_path = os.path.join(pkg_share, 'config/ekf.yaml') 
    default_rviz_config_path = os.path.join(pkg_share, 'rviz/nav2_config.rviz')
    world_file_name = 'toto_world/h.world'
    world_path = os.path.join(pkg_share, 'worlds', world_file_name)
    nav2_launch_dir = os.path.join(param_pkg_share, 'launch') 
    static_map_path = os.path.join(pkg_share, 'maps', 'h_world.yaml')
    nav2_params_path = os.path.join(param_pkg_share, 'params', 'toto2_nav2_params.yaml')
    nav2_bt_path = FindPackageShare(package='nav2_bt_navigator').find('nav2_bt_navigator')
    behavior_tree_xml_path = os.path.join(nav2_bt_path, 'behavior_trees', 'navigate_w_replanning_and_recovery.xml')
    
    # Launch configuration variables
    autostart = LaunchConfiguration('autostart')
    default_bt_xml_filename = LaunchConfiguration('default_bt_xml_filename')
    headless = LaunchConfiguration('headless')
    map_yaml_file = LaunchConfiguration('map')
    model = LaunchConfiguration('model')
    namespace = LaunchConfiguration('namespace')
    params_file = LaunchConfiguration('params_file')
    rviz_config_file = LaunchConfiguration('rviz_config_file')
    slam = LaunchConfiguration('slam')
    use_namespace = LaunchConfiguration('use_namespace')
    use_robot_state_pub = LaunchConfiguration('use_robot_state_pub')
    use_rviz = LaunchConfiguration('use_rviz')
    use_sim_time = LaunchConfiguration('use_sim_time')
    use_simulator = LaunchConfiguration('use_simulator')
    world = LaunchConfiguration('world')

    # Declare the launch arguments
    declare_namespace_cmd = DeclareLaunchArgument('namespace', default_value='', description='Top-level namespace')
    declare_use_namespace_cmd = DeclareLaunchArgument('use_namespace', default_value='False', description='Whether to apply a namespace to the navigation stack')
    declare_autostart_cmd = DeclareLaunchArgument('autostart', default_value='true', description='Automatically startup the nav2 stack')
    declare_bt_xml_cmd = DeclareLaunchArgument('default_bt_xml_filename', default_value=behavior_tree_xml_path, description='Full path to the behavior tree xml file to use')
    declare_map_yaml_cmd = DeclareLaunchArgument('map', default_value=static_map_path, description='Full path to map file to load')
    declare_model_path_cmd = DeclareLaunchArgument('model', default_value=default_model_path, description='Absolute path to robot urdf file')
    declare_params_file_cmd = DeclareLaunchArgument('params_file', default_value=nav2_params_path, description='Full path to the ROS2 parameters file to use for all launched nodes')
    declare_rviz_config_file_cmd = DeclareLaunchArgument('rviz_config_file', default_value=default_rviz_config_path, description='Full path to the RVIZ config file to use')
    declare_simulator_cmd = DeclareLaunchArgument('headless', default_value='False', description='Whether to execute gzclient')
    declare_slam_cmd = DeclareLaunchArgument('slam', default_value='False', description='Whether to run SLAM')
    declare_use_robot_state_pub_cmd = DeclareLaunchArgument('use_robot_state_pub', default_value='True', description='Whether to start the robot state publisher')
    declare_use_rviz_cmd = DeclareLaunchArgument('use_rviz', default_value='True', description='Whether to start RVIZ')
    declare_use_sim_time_cmd = DeclareLaunchArgument('use_sim_time', default_value='True', description='Use simulation (Gazebo) clock if true')
    declare_use_simulator_cmd = DeclareLaunchArgument('use_simulator', default_value='True', description='Whether to start the simulator')
    declare_world_cmd = DeclareLaunchArgument('world', default_value=world_path, description='Full path to the world model file to load')

    # Specify the actions

    # Start the keep_out.py script first
    execute_python_script_cmd = ExecuteProcess(
        cmd=['python3', '/home/krushna/st/src/toto_simulation_ros2/toto2_description/scripts/keep_out.py'],
        output='screen'
    )

    # Start Gazebo server
    start_gazebo_server_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_gazebo_ros, 'launch', 'gzserver.launch.py')),
        condition=IfCondition(use_simulator),
        launch_arguments={'world': world}.items()
    )

    # Start Gazebo client    
    start_gazebo_client_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_gazebo_ros, 'launch', 'gzclient.launch.py')),
        condition=IfCondition(PythonExpression([use_simulator, ' and not ', headless]))
    )

    # Start robot localization
    start_robot_localization_cmd = Node(
        package='robot_localization',
        executable='ekf_node',
        name='ekf_filter_node',
        output='screen',
        parameters=[robot_localization_file_path, {'use_sim_time': use_sim_time}]
    )

    # Start robot state publisher
    start_robot_state_publisher_cmd = Node(
        condition=IfCondition(use_robot_state_pub),
        package='robot_state_publisher',
        executable='robot_state_publisher',
        namespace=namespace,
        parameters=[{'use_sim_time': use_sim_time, 'robot_description': Command(['xacro ', model])}],
        remappings=[('/tf', 'tf'), ('/tf_static', 'tf_static')],
        arguments=[default_model_path]
    )

    # Launch RViz
    start_rviz_cmd = Node(
        condition=IfCondition(use_rviz),
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', rviz_config_file]
    )    

    # Launch the ROS 2 Navigation Stack
    start_ros2_navigation_cmd = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(nav2_launch_dir, 'bringup_launch.py')),
        launch_arguments={
            'namespace': namespace,
            'use_namespace': use_namespace,
            'slam': slam,
            'map': map_yaml_file,
            'use_sim_time': use_sim_time,
            'params_file': params_file,
            'default_bt_xml_filename': default_bt_xml_filename,
            'autostart': autostart
        }.items()
    )

    # Create the launch description and populate
    ld = LaunchDescription()

    # Declare the launch options
    ld.add_action(declare_namespace_cmd)
    ld.add_action(declare_use_namespace_cmd)
    ld.add_action(declare_autostart_cmd)
    ld.add_action(declare_bt_xml_cmd)
    ld.add_action(declare_map_yaml_cmd)
    ld.add_action(declare_model_path_cmd)
    ld.add_action(declare_params_file_cmd)
    ld.add_action(declare_rviz_config_file_cmd)
    ld.add_action(declare_simulator_cmd)
    ld.add_action(declare_slam_cmd)
    ld.add_action(declare_use_robot_state_pub_cmd)  
    ld.add_action(declare_use_rviz_cmd) 
    ld.add_action(declare_use_sim_time_cmd)
    ld.add_action(declare_use_simulator_cmd)
    ld.add_action(declare_world_cmd)

    # Add actions in the desired order
    ld.add_action(execute_python_script_cmd)  # First, run the keep_out script
    ld.add_action(start_gazebo_server_cmd)
    ld.add_action(start_gazebo_client_cmd)
    ld.add_action(start_robot_localization_cmd)
    ld.add_action(start_robot_state_publisher_cmd)
    ld.add_action(start_rviz_cmd)
    ld.add_action(start_ros2_navigation_cmd)

    return ld
