# toto_simulation_ros2

Run the following commands  in terminal to install and setup ROS2 Foxy:
1. `wget https://raw.githubusercontent.com/ROBOTIS-GIT/robotis_tools/master/install_ros2_foxy.sh`
2. `sudo chmod 755 ./install_ros2_foxy.sh`
3. `bash ./install_ros2_foxy.sh`
4. `sudo apt-get install ros-foxy-gazebo-ros`
5. `sudo apt-get install ros-foxy-xacro`

**Note:** After this a workspace named `colcon_ws` will be created where you can install TOTO files or you can create your own ros2 workspace.

4. Install the repository in the `src` folder of your ros2 workspace.

5. Add this lines in your `.bashrc` file:

   * `source ~/{name of ros2 workspace}/install/setup.bash`
   * `export ROS_DOMAIN_ID=0` 
   * `export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/home/sumukh/{name of ros2 workspace}/src/toto_simulation_ros2/toto2_description/models/`
   * `source /usr/share/gazebo/setup.sh`
   * `source /usr/share/colcon_cd/function/colcon_cd.sh`
   * `export _colcon_cd_root=~/{name of ros2 workspace}`
  
**Note:** Change `sumukh` with username in your PC and change GAZEBO_MODEL_PATH to place where the repo is cloned.

**Important:**

After adding above lines to `.bashrc`, follow these steps:
1. Go to terminal, run `gazebo`.
2. Go to the "Insert" tab at the top of left bar.
3. From the drop-down menu of your "GAZEBO_MODEL_PATH" directory, add `toto2` and `TOTO House` to the gazebo environment.
4. Now you can close Gazebo.

**Gazebo Simulations:**

1. Run `ros2 launch toto2_description simulation.launch.py` to launch Gazebo and RViz.
2. Run `ros2 run toto2_teleop teleop_keyboard` to control TOTO using your keyboard.

**SLAM:** 

Install Robot Localization package by running `sudo apt install ros-foxy-robot-localization` & SLAM Toolbox by running `sudo apt install ros-foxy-slam-toolbox` in your terminal.

1. Run `ros2 launch toto2_description nav2.launch.py slam:=True`.
2. For keyboard control, run `ros2 run toto2_teleop teleop_keyboard`.
3. To save your map, run to `cd {your_workspace}/src/toto_simulation_ros2/toto2_description/maps/` and then to save map run `ros2 run nav2_map_server map_saver_cli -f ~/{name_of_your_map}`

**Navigation:**

**If you are using your own map**, follow these steps before starting the Navigation Stack:

1. Change `static_map_path = os.path.join(pkg_share, 'maps', 'house.yaml')` to `static_map_path = os.path.join(pkg_share, 'maps', '{name_of_your_map}.yaml')` in **/toto2_description/launch/nav2.launch.py**.
2. Change `default_value=os.path.join(map_dir, 'maps', 'house.yaml')` to `default_value=os.path.join(map_dir, 'maps', '{name_of_your_map}.yaml')` in **/toto2_navigation/launch/localization.launch.py**.
3. Change `yaml_filename: "house.yaml"` to `yaml_filename: "{name_of_your_map}.yaml"` in **/toto2_navigation/params/toto2_nav2_params.yaml**.

To launch the navigation stack:

Install Nvigation Stack package by running `sudo apt install ros-foxy-navigation2` & `sudo apt install ros-foxy-nav2-bringup`.

1. Run `ros2 launch toto2_description nav2.launch.py`.
2. Click the **2D Pose Estimate button** in the RViz2 menu. (Position of the robot will be near outside wall and below main gate of the house).
3. Click on the map where the robot is located in gazebo and drag the large green arrow toward the direction where the robot is facing.
4. After this, click the **Navigation2 Goal** button in the RViz2 menu.
5. Click on the map to set the destination of the robot and drag the green arrow toward the direction where the robot will be facing.

Waypoint Navigation:

1. Run `ros2 launch toto2_description nav2.launch.py`.
2. Click the **2D Pose Estimate** button in the RViz2 menu. (Position of the robot will be near outside wall and below main gate of the house).
3. Now click the **Waypoint mode** button in the bottom left corner of RViz. Clicking this button puts the system in waypoint follower mode.
4. Click **Navigation2 Goal** button, and click on areas of the map where you would like your robot to go (i.e. select your waypoints). Select as many waypoints as you want.
5. When you’re ready for the robot to follow the waypoints, click the **Start Navigation** button in the bottom left corner of RViz.

**Note:** 
* This green arrow is a marker that can specify the destination of the robot.
* The root of the arrow is x, y coordinate of the destination, and the angle θ is determined by the orientation of the arrow.
* As soon as x, y, θ are set, TOTO will start moving to the destination immediately.
