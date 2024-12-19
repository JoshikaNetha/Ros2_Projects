Create an SDF model for Gazebo and use it in a custom world file

Steps to Create an SDF Model for Gazebo
1. Create the Model Files
First, you'll need to create two files for your Gazebo model:

model.sdf – The main model description file in SDF format.
model.config – A configuration file for Gazebo to recognize the model.

Check line_follow folder.

2. Create the Model Directory
Once you have your model.sdf and model.config files, create a new folder for your model inside the Gazebo models directory.

On a Linux system using Gazebo 11, the directory is typically located at:
/usr/share/gazebo-11/models/
Create a new folder for your model, for example, line_follow.

In the terminal:
sudo mkdir /usr/share/gazebo-11/models/line_follow

sudo cp model.sdf model.config /usr/share/gazebo-11/models/line_follow/

3. Add the Model to Your World File
Now, you can include your custom model in a Gazebo world file. Open your custom world file (e.g., my_world.world) and include the following code to insert your model into the simulation:

Check line_follower.world file line 30

4. Launch Your World in Gazebo
Once you’ve created your world file, you can load it into Gazebo. Use the following command in the terminal:

gazebo --verbose Ros2_Projects/LineFollowerRobotSimulation/ros2_ws/src/line_follower_robot/worlds/line_follower_world.world
