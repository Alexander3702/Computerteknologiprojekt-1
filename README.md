# Computerteknologiprojekt-1

TurtleBot3 Obstacle Detection and Navigation System with Color-Based Victim Detection

## Overview

This project implements an autonomous navigation system for TurtleBot3 robots using ROS2 (Robot Operating System 2). The robot can:
- Detect and avoid obstacles using LIDAR sensor data
- Navigate autonomously in an environment
- Detect colored markers (victims) using an RGB color sensor
- Track collision events and calculate average speed
- Control an LED indicator for victim detection

## Prerequisites

### Hardware Requirements
- TurtleBot3 robot (Burger or Waffle)
- Raspberry Pi (with GPIO support)
- RGB Color Sensor (I2C interface at address 0x44)
- LED connected to GPIO pin 18
- LIDAR sensor

### Software Requirements
- Ubuntu 22.04 (or compatible Linux distribution)
- ROS2 Humble Hawksbill
- Python 3.10+
- Visual Studio Code (recommended for development)

## Setting Up Visual Studio Code

### 1. Install VS Code Extensions

Open VS Code and install the recommended extensions. When you open this project, VS Code will prompt you to install them automatically, or you can install them manually:

- **Python** (ms-python.python) - Python language support
- **Pylance** (ms-python.vscode-pylance) - Python language server
- **C/C++** (ms-vscode.cpptools) - C++ support for ROS2 packages
- **ROS** (ms-iot.vscode-ros) - ROS development tools
- **XML** (redhat.vscode-xml) - For launch files
- **YAML** (redhat.vscode-yaml) - For configuration files
- **Even Better TOML** (tamasfe.even-better-toml) - For package.xml files

### 2. Install ROS2 Humble

```bash
# Add ROS2 apt repository
sudo apt update && sudo apt install software-properties-common
sudo add-apt-repository universe
sudo apt update && sudo apt install curl -y
sudo curl -sSL https://raw.githubusercontent.com/ros/rosdistro/master/ros.key -o /usr/share/keyrings/ros-archive-keyring.gpg

echo "deb [arch=$(dpkg --print-architecture) signed-by=/usr/share/keyrings/ros-archive-keyring.gpg] http://packages.ros.org/ros2/ubuntu $(. /etc/os-release && echo $UBUNTU_CODENAME) main" | sudo tee /etc/apt/sources.list.d/ros2.list > /dev/null

# Install ROS2 Humble
sudo apt update
sudo apt install ros-humble-desktop -y

# Install ROS2 dependencies
sudo apt install ros-humble-rclpy -y
sudo apt install ros-humble-geometry-msgs -y
sudo apt install ros-humble-sensor-msgs -y
sudo apt install ros-humble-turtlebot3* -y
```

### 3. Install Python Dependencies

```bash
# Install pip if not already installed
sudo apt install python3-pip -y

# Install Python packages
pip3 install -r requirements.txt
```

### 4. Source ROS2 Environment

Add this to your `~/.bashrc` to automatically source ROS2 on terminal startup:

```bash
echo "source /opt/ros/humble/setup.bash" >> ~/.bashrc
echo "export ROS_DOMAIN_ID=30" >> ~/.bashrc
source ~/.bashrc
```

### 5. Configure TurtleBot3 Model

```bash
echo "export TURTLEBOT3_MODEL=burger" >> ~/.bashrc
# Or for Waffle model:
# echo "export TURTLEBOT3_MODEL=waffle" >> ~/.bashrc
source ~/.bashrc
```

## Running the Agent in VS Code

### Method 1: Using VS Code Debugger (Recommended for Development)

1. Open the project folder in VS Code
2. Open `main.py`
3. Press `F5` or go to **Run and Debug** (Ctrl+Shift+D)
4. Select **"Python: Main (TurtleBot3 Agent)"** from the dropdown
5. Click the green play button

This will run the agent with debugging capabilities, allowing you to set breakpoints and inspect variables.

### Method 2: Using VS Code Tasks

1. Press `Ctrl+Shift+P` to open the Command Palette
2. Type **"Tasks: Run Task"**
3. Select **"Run TurtleBot3 Agent"**

This will run the agent in the integrated terminal.

### Method 3: Using Integrated Terminal

1. Open the integrated terminal in VS Code (Ctrl+`)
2. Run the following commands:

```bash
source /opt/ros/humble/setup.bash
python3 main.py
```

## VS Code Features Available

### Tasks (Ctrl+Shift+P → "Tasks: Run Task")

- **Run TurtleBot3 Agent**: Execute the main agent script
- **Check Python Syntax**: Validate Python syntax for the current file
- **Source ROS2 Environment**: Source the ROS2 setup script
- **List ROS2 Topics**: Show all active ROS2 topics
- **Check ROS2 Node Status**: Display running ROS2 nodes

### Debug Configurations (F5)

- **Python: Main (TurtleBot3 Agent)**: Debug the main agent script
- **Python: Current File**: Debug any Python file currently open
- **Python: TurtleBot3 Obstacle Detection Module**: Debug the obstacle detection module

### Settings

The project includes preconfigured settings for:
- Python interpreter path
- ROS2 package paths for IntelliSense
- Linting with flake8
- Python formatting with autopep8
- File associations for ROS launch files
- Terminal environment variables (ROS_DOMAIN_ID)

## Project Structure

```
.
├── main.py                           # Main entry point for the robot controller
├── turtlebot3_obstacle_detection.py  # Core obstacle detection and navigation logic
├── backup.py                         # Backup version of the detection code
├── requirements.txt                  # Python dependencies
├── README.md                         # This file
└── .vscode/                          # VS Code configuration
    ├── settings.json                 # Workspace settings
    ├── launch.json                   # Debug configurations
    ├── tasks.json                    # Task definitions
    └── extensions.json               # Recommended extensions
```

## How It Works

### Main Components

1. **main.py**: Initializes the ROS2 node and runs the robot for a specified duration (120 seconds by default)
2. **turtlebot3_obstacle_detection.py**: Contains the `Turtlebot3ObstacleDetection` class with:
   - LIDAR scan processing for obstacle detection
   - Navigation logic with multi-zone detection (front, left, right, far left, far right)
   - Color sensor integration for victim detection (red markers)
   - Collision counting and tracking
   - Average speed calculation
   - LED control for victim pickup indication

### Key Features

#### Obstacle Detection
- Uses 7 detection zones to analyze LIDAR data
- Implements smart turning decisions based on available space
- Maintains safe distance of 0.25m from obstacles
- Tracks collision events (within 0.1m range)

#### Color Detection
- Detects red markers as "victims" to be rescued
- Uses I2C RGB sensor at address 0x44
- Implements debouncing to prevent false detections
- Blinks LED on successful victim detection
- Tracks total victims picked up

#### Performance Metrics
- Calculates and logs average linear speed
- Counts total collision events
- Reports total victims rescued at mission completion

## Troubleshooting

### Common Issues

**1. ImportError: No module named 'rclpy'**
```bash
source /opt/ros/humble/setup.bash
```

**2. Cannot connect to robot**
- Ensure TurtleBot3 is powered on and connected to the same network
- Check ROS_DOMAIN_ID matches on both robot and development machine
- Verify topics with: `ros2 topic list`

**3. GPIO/I2C errors**
- Ensure user has permissions: `sudo usermod -a -G i2c,gpio $USER`
- Reboot after adding user to groups
- Check sensor connections

**4. LIDAR not detected**
- Check USB connection to LIDAR
- Verify LIDAR driver is running: `ros2 node list`
- Check permissions: `sudo chmod 666 /dev/ttyUSB0`

**5. VS Code Python IntelliSense not working**
- Reload VS Code window (Ctrl+Shift+P → "Developer: Reload Window")
- Check Python interpreter is set correctly (Ctrl+Shift+P → "Python: Select Interpreter")
- Verify ROS2 paths in `.vscode/settings.json`

## Customization

### Adjust Robot Speed
Edit `turtlebot3_obstacle_detection.py`:
```python
twist.linear.x = 0.2  # Adjust forward speed (m/s)
```

### Change Detection Distance
Edit `turtlebot3_obstacle_detection.py`:
```python
self.stop_distance = 0.25  # Distance in meters
```

### Modify Runtime Duration
Edit `main.py`:
```python
end_time = start_time + 120.0  # Duration in seconds
```

## Contributing

Feel free to submit issues, fork the repository, and create pull requests for any improvements.

## License

Copyright 2019 ROBOTIS CO., LTD.

Licensed under the Apache License, Version 2.0

## Authors

- Ryan Shim
- Gilbert
- Jeonggeun Lim