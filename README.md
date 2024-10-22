# Final Project Group -17 - Intelligent Robotic Navigation

| Name                        | E-Mail ID         |
|-----------------------------|-------------------|
| Sai Jagadeesh Muralikrishnan| jagkrish@umd.edu  |
| Varun Lakshmanan            | varunl11@umd.edu  |

This project demonstrates the implementation of Dueling Double DQN performance comparison with eisting DQN Learning with TurtleBot3 in a Gazebo simulation environment. It includes setting up the ROS2 and Gazebo environment, configuring the project, and running training and testing sequences using 2 different deep reinforcement learning algorithms.

## Prerequisites

- Ubuntu 20.04 LTS (Focal Fossa)
- ROS2 Foxy
- Gazebo 11
- PyTorch


## Installation

### Step 1: Install Ubuntu 20.04 LTS or WSL 2 verison

Download and install Ubuntu 20.04 LTS from [Ubuntu Official Site](https://releases.ubuntu.com/20.04/).

### Step 2: Install ROS2 Foxy

Follow the installation instructions for ROS2 Foxy available at [ROS 2 Documentation: Foxy](https://docs.ros.org/en/foxy/Installation/Ubuntu-Install-Debians.html).

### Step 3: Install Gazebo 11

Execute the following commands in your terminal to install Gazebo 11 along with necessary ROS packages:

```bash
curl -sSL http://get.gazebosim.org | sh
sudo apt install ros-foxy-gazebo-ros-pkgs
sudo apt install ros-foxy-ros-core ros-foxy-geometry2
sudo apt-get install ros-foxy-turtlebot3-description
```

### Step 4: Install Pytorch and Dependencies
- Run the following commands to install Python dependencies needed for the project:

```bash
sudo apt install python3-pip
pip3 install matplotlib pandas pyqtgraph==0.12.4 PyQt5==5.14.1 torch==1.10.0+cu113 -f https://download.pytorch.org/whl/cu113/torch_stable.html
```

## Project Setup

### Extract and Configure the Workspace

- Extract 'varun_saijagadeesh_ENPM690_final_project_codes.zip'
- There should be workspace 'final_project_RL' inside the extracted folder 'varun_saijagadeesh_ENPM690_final_project_codes'
- Move the extracted final_project_RL workspace to your desired directory in Ubuntu 20.04.
- Modify the model path in the directory to match your Ubuntu USERNAME or if using wsl use the HOSTNAME.
- the folder inside model folder which we submitted will be under our username 'VarunL' and you need to change that.
* Example: 

varunl11@VarunL:~/final_project_RL$ tree
.
└── src
    ├── turtlebot3_drl
    │   ├── model
    │   │   └── VarunL
    │   │       ├── dqn_4_stage_4

- The name VarunL needs to changed to your HOSTANME if wsl or USERNAME is Dual Boot

below mentioned is the correct format for WSL version 
```ruby
USERNAME@HOSTNAME:~/final_project_RL/src/turtlebot3_drl/model/HOSTNAME$
```
- cd to the workspace final_project_RL
```bash
cd final_project_RL
```
- install the rosdep tools
```bash
sudo apt install python3-rosdep2
rosdep update
rosdep install -i --from-path src --rosdistro foxy -y
sudo apt update
sudo apt install python3-colcon-common-extensions
```
### Update .bashrc File

- Add the following lines to your .bashrc file to set up the environment:

```bash
export ROS_DOMAIN_ID=1
WORKSPACE_DIR=~/final_project_RL
export DRLNAV_BASE_PATH=$WORKSPACE_DIR
source $WORKSPACE_DIR/install/setup.bash
export GAZEBO_MODEL_PATH=$GAZEBO_MODEL_PATH:$WORKSPACE_DIR/src/turtlebot3_simulations/turtlebot3_gazebo/models
export TURTLEBOT3_MODEL=burger
export GAZEBO_PLUGIN_PATH=$GAZEBO_PLUGIN_PATH:$WORKSPACE_DIR/src/turtlebot3_simulations/turtlebot3_gazebo/models/turtlebot3_drl_world/obstacle_plugin/lib
```
### Build the Workspace

- Navigate to the workspace directory and build it:

```bash
cd final_project_RL
colcon build
source install/setup.bash
```

## Running the Project

### Launching the Simulation

- Open four new terminals and execute the following commands in each to start the simulation and RL agents:
Follow the order of terminal commands

### Terminal -1 - Gazebo world
* Choose the world you wish to visulaize

* Our custom made world used for testing - ros2 launch turtlebot3_gazebo turtlebot3_drl_stage9.launch.py

* World used for training - ros2 launch turtlebot3_gazebo turtlebot3_drl_stage4.launch.py

```bash
ros2 launch turtlebot3_gazebo turtlebot3_drl_stage9.launch.py
```

### Terminal -2 - Environment intialization

```bash
ros2 run turtlebot3_drl environment
```

### Terminal -3 - Goal points intialization 

```bash
ros2 run turtlebot3_drl gazebo_goals
```
### Terminal -4 

Choices can be made from below commands

### You can adjust the number of episodes as needed. The maximum episodes are 5000 for Dueling DQN and 3000 for DQN.

- Training of dueling double DQN model from 3000 saved episodes- 
```bash
ros2 run turtlebot3_drl train_agent dueling_dqn "dueling_dqn_6_stage_4" 3000

```
- Testing of dueling double DQN model from 3000 saved episodes- 
```bash
ros2 run turtlebot3_drl test_agent dueling_dqn "dueling_dqn_6_stage_4" 3000
```

## To compare the results with existing DQN model performance
- Training of DQN at 3000 episodes and after- 
```bash
ros2 run turtlebot3_drl train_agent dqn "dqn_4_stage_4" 3000
```
Testing of DQN at 3000 episodes and after-
```bash
ros2 run turtlebot3_drl test_agent dqn "dqn_4_stage_4" 3000
```
## Working Videos 
* Video Results for the training at phase -1 (1700 episodes of training): 
https://drive.google.com/file/d/1qH-McJhEq93v7Rdqwxw6BZ8j4bVdsPM-/view?usp=sharing 

* Video Results for the training at phase -2 (3000 episodes of training): 
https://drive.google.com/file/d/1tsFBgujWl74BMfZTGFvLvy3U1bwCoKbR/view?usp=sharing 

* Video Results for the Comparison of 20 episodes test results (3000 episodes of training): 
https://drive.google.com/file/d/12PErRUwAVW8FRP7aUm8Ux1sWXIeSSM-0/view?usp=sharing 

* Video Results for Dueling DQN (5000 episodes of training): 
https://drive.google.com/file/d/1NFG_7DQoTRUQjtM-QYpQCgTMvu_C78V3/view?usp=sharing 

## Notes if any errors faced
- If Terminal 4 faces error "Waiting for new goal... (if persists: reset gazebo_goals node)", you have to end the the terminal 3 and run the Terminal 3 again and now run the terminal 4 again and it should run fine. Try once again if it doesn't 
- Ensure all paths and usernames are correctly set according to your local setup.
- Ensure that the folder inside the model name is changed from 'VarunL'
- Exit all terminals and restart it if any changes are made to the .bashrc file for the changes to take effect.

## References:
   https://github.com/tomasvr/turtlebot3_drlnav
   This is an review project of how implementing Dueling Double DQN to the existing Vanilla DQN improves the performance of the model we used the turtlebot packages and other codes from the above mentioned github repository. 
   Our part in this project is changing the existing DQN to Dueling Double DQN and adding addtional layers to the main network changing the activation function and so on.
   I have attached our report of analysis for reference.
   
