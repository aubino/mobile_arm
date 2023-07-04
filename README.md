# Projet_ROS
A mobile manipulator with automatic detection (Detects the dreen boxes automatically)

# DEMO
[Watch The Demo](demo.mp4)

__Dependancies Installation__
The following dependencies have been added (to add in you catkin workspace) :

__UR5__ : 
Used to generate a urdf file to merge to the base  . *Install* with : 
```
cd $HOME/catkin_ws/src
git clone https://github.com/ros-industrial/universal_robot.git
```
__robotiq__ : 
Used to generate a gripper urdf file to merge to the base . *Install* with : 
```
cd $HOME/catkin_ws/src
git clone https://github.com/filesmuggler/robotiq.git
catkin build # (or cd .. && catkin_make)
```
__Moveit__ :
 The standard robot arm manipulation for ROS. See installation instruction [HERE](https://moveit.ros.org/install/) :
 
https://github.com/ros-planning/moveit_resources/blob/master/panda_moveit_config/config/panda.srdf

For cartesian command usage 
```
rosrun object_identificator arm_cartesian_command_node -h
```
Install trac_ik_kinematics_plugin : 
```
sudo apt-get install ros-$ROS_DISTRO-trac-ik-kinematics-plugin
```
__Usage__ : 
Launch the nodes with :
After compiling the repository
 ```
 roslaunch mobile_manipulator mobile_manipulator_show.launch
 ```
 For grabbing enabling (although it will most likely fail due to bad frame transformation) : 
 ```
 rosrun object_identificator arm_cartesian_command_node -a arm_body -t gripper_body -m /arm/goal
 ```
 And then, in another properly sourced terminal terminal

```
rosrun mobile_manipulator orchestra.py
```
