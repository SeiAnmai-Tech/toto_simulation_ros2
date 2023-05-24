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
  
**Note:**__ Change `sim_toto2` with name of your workspace & change `sumukh` with username in your PC.

**Gazebo Simulations:**

1. Run `ros2 launch toto2_description l3.launch.py` to launch Gazebo and RViz.

2. Run `ros2 run teleop_twist_keyboard teleop_twist_keyboard` to control toto using your keyboard.

**SLAM:**

There are **2** options:

Using Cartographer (Publishing LidarScan values but are not getting captured by RViz) - 

1. Run `ros2 launch toto2_description house.launch.py`.
2. Run `ros2 launch toto2_cartographer cartographer.launch.py`.
3. For keyboard control, run `ros2 run teleop_twist_keyboard teleop_twist_keyboard`.

Using SLAM Toolbox (Mapping of TOTO is not correct) - 

1. Run `ros2 launch toto2_description l5.launch.py slam:=True`.
2. For keyboard control, run `ros2 run teleop_twist_keyboard teleop_twist_keyboard`.
