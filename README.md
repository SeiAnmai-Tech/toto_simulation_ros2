# toto_simulation_ros2

1. Install the repository in the `src` folder of your ros2 workspace.

2. Add this lines in your `.bashrc` file:

   * `source /opt/ros/foxy/setup.bash`
   * `source ~/sim_toto2/install/setup.bash`
   * `export ROS_DOMAIN_ID=0` 
   * `export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/home/sumukh/sim_toto2/src/toto2_description/models/`
   * `source /usr/share/gazebo/setup.sh`
   * `source /usr/share/colcon_cd/function/colcon_cd.sh`
   * `export _colcon_cd_root=~/sim_toto2`
  
**Note:** Change `sim_toto2` with name of your workspace, change `sumukh` with username in your PC and change GAZEBO_MODEL_PATH to place where the repo is cloned.

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

1. Run `ros2 launch toto2_description nav2.launch.py`.
2. Click the **2D Pose Estimate button** in the RViz2 menu. (Position of the robot will be near outside wall and below main gate of the house).
3. Click on the map where the robot is located in gazebo and drag the large green arrow toward the direction where the robot is facing.
4. After this, click the **Navigation2 Goal** button in the RViz2 menu.
5. Click on the map to set the destination of the robot and drag the green arrow toward the direction where the robot will be facing.

**Note:** 
* This green arrow is a marker that can specify the destination of the robot.
* The root of the arrow is x, y coordinate of the destination, and the angle θ is determined by the orientation of the arrow.
* As soon as x, y, θ are set, TOTO will start moving to the destination immediately.
=======
  
   * `source ~/sim_toto2/install/setup.bash`
  
   * `export ROS_DOMAIN_ID=0` 
  
   * `export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/home/sumukh/sim_toto2/src/toto2_description/models/`
  
   * `source /usr/share/gazebo/setup.sh`
  
   * `source /usr/share/colcon_cd/function/colcon_cd.sh`
  
   * `export _colcon_cd_root=~/sim_toto2`
  
**Note:**__ Change `sim_toto2` with name of your workspace & change `sumukh` with username in your PC.

3. Run `ros2 launch toto2_description l3.launch.py` to launch Gazebo and RViz.

4. Run `ros2 run teleop_twist_keyboard teleop_twist_keyboard` to control toto using your keyboard.
