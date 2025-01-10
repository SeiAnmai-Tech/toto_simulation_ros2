#!/bin/bash

# Setting locale to UTF-8
sudo apt update && sudo apt install locales
sudo locale-gen en_US en_US.UTF-8
sudo update-locale LC_ALL=en_US.UTF-8 LANG=en_US.UTF-8
export LANG=en_US.UTF-8

# Setup Sources
sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg
echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS2 Humble
sudo apt update
sudo apt upgrade
sudo apt install ros-humble-desktop -y
sudo apt install ros-dev-tools
source /opt/ros/humble/setup.bash

# Install ROS2 Gazebo packages
sudo apt install ros-humble-gazebo-ros -y
sudo apt install ros-humble-gazebo-ros2-control -y
sudo apt install ros-humble-gazebo-ros-pkgs -y

# Install ROS2 Navigation packages
sudo apt install ros-humble-navigation2 -y
sudo apt install ros-humble-nav2-bringup -y

# Install ROS2 SLAM Toolbox
sudo apt install ros-humble-slam-toolbox -y
sudo apt install ros-humble-robot-localization -y

# Install ROS2 Xacro
sudo apt install ros-humble-xacro -y

# Install Python3 Colcon Common Extensions
sudo apt install python3-colcon-common-extensions -y

# Write custom commands to .bashrc
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
echo "source ~/ros2_ws/install/setup.bash" >> ~/.bashrc
echo "export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:/home/sumukh/ros2_ws/src/toto_simulation_ros2/toto2_description/models/" >> ~/.bashrc
echo "source /usr/share/gazebo/setup.sh" >> ~/.bashrc
echo "source /usr/share/colcon_cd/function/colcon_cd.sh" >> ~/.bashrc
echo "export _colcon_cd_root=~/ros2_ws" >> ~/.bashrc
echo "source /usr/share/colcon_argcomplete/hook/colcon-argcomplete.bash" >> ~/.bashrc
echo "export ROS_DOMAIN_ID=0" >> ~/.bashrc

# Source the modified .bashrc file
source ~/.bashrc

# Finished installing dependencies
echo "ROS2 Humble and other packages installed successfully & .bashrc updated."
