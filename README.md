# toto_simulation_ros2

1. Install the repository in the `src` folder of your ros2 workspace.

2. Add this lines in your `.bashrc` file:

  a. source /opt/ros/foxy/setup.bash
  
  b. source ~/sim_toto2/install/setup.bash
  
  c. export ROS_DOMAIN_ID=0 
  
  d. export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/home/sumukh/sim_toto2/src/toto2_description/models/
  
  e. source /usr/share/gazebo/setup.sh
  
  f. source /usr/share/colcon_cd/function/colcon_cd.sh
  
  g. export _colcon_cd_root=~/sim_toto2
  
**Note:**__ Change `sim_toto2` with name of your workspace & change `sumukh` with username in your PC.

3. Run `ros2 launch toto2_description l3.launch.py` to launch Gazebo and RViz.

4. Run `ros2 run teleop_twist_keyboard teleop_twist_keyboard` to control toto using your keyboard.
