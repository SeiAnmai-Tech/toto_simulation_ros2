# toto_simulation_ros2

Install the repository in the `src` folder of your ros2 workspace.

Add this lines in your `.bashrc` file:
  `source /opt/ros/foxy/setup.bash
  source ~/sim_toto2/install/setup.bash
  export ROS_DOMAIN_ID=0 #TURTLEBOT3 - 30
  export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/home/sumukh/sim_toto2/src/toto2_description/models/
  source /usr/share/gazebo/setup.sh
  source /usr/share/colcon_cd/function/colcon_cd.sh
  export _colcon_cd_root=~/sim_toto2`
  
Change `sim_toto2` with name of your workspace & change `sumukh` with username in your PC.

Run `ros2 launch toto2_description l3.launch.py` to launch Gazebo and RViz.

Run `ros2 run teleop_twist_keyboard teleop_twist_keyboard` to control toto using your keyboard.
