# Visual Studio Code Setup Guide

## How to Use This Agent in VS Code

This document provides detailed instructions on setting up and using the TurtleBot3 obstacle detection agent in Visual Studio Code.

## Prerequisites Checklist

Before you begin, ensure you have:

- [ ] Ubuntu 22.04 or compatible Linux system
- [ ] Visual Studio Code installed
- [ ] ROS2 Humble installed (`ros-humble-desktop`)
- [ ] Python 3.10 or newer
- [ ] TurtleBot3 hardware (or simulator)

## Step-by-Step Setup

### Step 1: Install Visual Studio Code

If you haven't already:

```bash
# Download and install VS Code
sudo snap install code --classic

# Or use the .deb package from https://code.visualstudio.com/
```

### Step 2: Clone and Open the Project

```bash
# Clone the repository (if not already done)
git clone https://github.com/Alexander3702/Computerteknologiprojekt-1.git
cd Computerteknologiprojekt-1

# Open in VS Code using the workspace file
code turtlebot3-agent.code-workspace
```

### Step 3: Install Recommended Extensions

When VS Code opens, you'll see a notification to install recommended extensions. Click **"Install All"**.

#### Manual Installation (if needed):

1. Press `Ctrl+Shift+X` to open Extensions view
2. Search and install each extension:
   - Python (`ms-python.python`)
   - Pylance (`ms-python.vscode-pylance`)
   - C/C++ (`ms-vscode.cpptools`)
   - ROS (`ms-iot.vscode-ros`)
   - XML (`redhat.vscode-xml`)
   - YAML (`redhat.vscode-yaml`)
   - Even Better TOML (`tamasfe.even-better-toml`)

### Step 4: Configure Python Interpreter

1. Open Command Palette: `Ctrl+Shift+P`
2. Type: `Python: Select Interpreter`
3. Choose: `/usr/bin/python3` or your system Python 3.10+

The workspace settings already include ROS2 paths for IntelliSense.

### Step 5: Install Python Dependencies

```bash
# Open integrated terminal: Ctrl+`
pip3 install -r requirements.txt

# Or system-wide:
sudo apt install python3-smbus2 python3-gpiozero python3-rpi.gpio
```

### Step 6: Source ROS2 Environment

Add to your `~/.bashrc`:

```bash
source /opt/ros/humble/setup.bash
export ROS_DOMAIN_ID=30
export TURTLEBOT3_MODEL=burger  # or waffle
```

Then reload:
```bash
source ~/.bashrc
```

## Running the Agent

### Method 1: Debug Mode (Recommended for Development)

1. Open `main.py`
2. Press `F5` to start debugging
3. Or click Run → Start Debugging
4. Or click the green play button in the Run and Debug panel

**Benefits:**
- Set breakpoints by clicking left of line numbers
- Inspect variables while paused
- Step through code line by line
- View call stack and debug console

### Method 2: Run Without Debugging

1. Press `Ctrl+Shift+P`
2. Type: `Tasks: Run Build Task`
3. Or press `Ctrl+Shift+B`

This runs the default task which executes `python3 main.py`.

### Method 3: Terminal

```bash
# Open terminal: Ctrl+`
python3 main.py
```

## VS Code Features Configured

### 1. IntelliSense & Auto-Complete

- ROS2 packages are automatically detected
- Type hints for `rclpy`, `geometry_msgs`, `sensor_msgs`
- Function signatures and documentation on hover

### 2. Debugging

Three debug configurations available:

| Configuration | Purpose |
|--------------|---------|
| Python: Main (TurtleBot3 Agent) | Debug the main entry point |
| Python: Current File | Debug any Python file |
| Python: TurtleBot3 Obstacle Detection Module | Debug the core module |

**Debug Controls:**
- `F5` - Start/Continue
- `F9` - Toggle Breakpoint
- `F10` - Step Over
- `F11` - Step Into
- `Shift+F11` - Step Out
- `Shift+F5` - Stop

### 3. Tasks

Access via `Ctrl+Shift+P` → "Tasks: Run Task":

| Task | Description |
|------|-------------|
| Run TurtleBot3 Agent | Execute the agent |
| Check Python Syntax | Validate Python syntax |
| Source ROS2 Environment | Load ROS2 into terminal |
| List ROS2 Topics | Show active ROS2 topics |
| Check ROS2 Node Status | List running nodes |

### 4. Settings Configured

The workspace includes these optimized settings:

```json
{
  "python.defaultInterpreterPath": "/usr/bin/python3",
  "python.analysis.extraPaths": [
    "/opt/ros/humble/lib/python3.10/site-packages"
  ],
  "python.linting.flake8Enabled": true,
  "terminal.integrated.env.linux": {
    "ROS_DOMAIN_ID": "30"
  }
}
```

## Workflow Examples

### Example 1: Debug a Specific Function

1. Open `turtlebot3_obstacle_detection.py`
2. Find the `detect_obstacle()` function (line 115)
3. Click left of line 115 to set a breakpoint
4. Press `F5` to start debugging
5. When the breakpoint is hit:
   - View `self.scan_ranges` in Variables panel
   - Check `middle_min` value
   - Step through the logic with `F10`

### Example 2: Test Color Detection

1. Open `turtlebot3_obstacle_detection.py`
2. Set breakpoint in `check_for_color()` function (line 251)
3. Run with `F5`
4. When paused, check RGB values in Variables panel
5. Evaluate expressions in Debug Console:
   ```python
   self.red > 95
   self.red > self.green
   ```

### Example 3: Modify and Test

1. Open `main.py`
2. Change runtime: `end_time = start_time + 60.0` (60 seconds)
3. Save file (`Ctrl+S`)
4. Run with `Ctrl+Shift+B`
5. Monitor output in terminal

## Customizing Your Workspace

### Add Your Own Task

Edit `.vscode/tasks.json`:

```json
{
  "label": "My Custom Task",
  "type": "shell",
  "command": "python3",
  "args": ["${workspaceFolder}/my_script.py"],
  "group": "build"
}
```

### Customize Debug Configuration

Edit `.vscode/launch.json`:

```json
{
  "name": "My Debug Config",
  "type": "python",
  "request": "launch",
  "program": "${workspaceFolder}/my_file.py",
  "args": ["--my-arg", "value"],
  "env": {
    "MY_VAR": "value"
  }
}
```

### Adjust Editor Settings

Edit `.vscode/settings.json` to customize:
- Line length (`editor.rulers`)
- Format on save (`editor.formatOnSave`)
- Linter rules
- Color theme
- Font size

## Troubleshooting

### Issue: Import errors for ROS2 packages

**Solution:**
```bash
# Verify ROS2 is installed
ls /opt/ros/humble

# Check Python can find rclpy
python3 -c "import rclpy; print(rclpy.__file__)"

# Update settings.json with correct path
```

### Issue: Debugger doesn't stop at breakpoints

**Solution:**
- Ensure you're using `F5` (debug) not `Ctrl+Shift+B` (run)
- Check breakpoint is enabled (should be red, not gray)
- Verify `"justMyCode": false` in launch.json

### Issue: Tasks not appearing

**Solution:**
```bash
# Reload window
Ctrl+Shift+P → "Developer: Reload Window"
```

### Issue: Terminal doesn't have ROS2 environment

**Solution:**
- Close all terminals in VS Code
- Open new terminal (`Ctrl+``)
- Environment variables are loaded automatically from settings

### Issue: GPIO/I2C permission errors

**Solution:**
```bash
# Add user to groups
sudo usermod -a -G i2c,gpio $USER

# Reboot
sudo reboot
```

## Best Practices

### 1. Use Virtual Environments (Optional)

```bash
# Create virtual environment
python3 -m venv venv

# Activate in VS Code
Ctrl+Shift+P → "Python: Select Interpreter" → "./venv/bin/python"
```

### 2. Enable Auto-Save

Add to settings:
```json
{
  "files.autoSave": "afterDelay",
  "files.autoSaveDelay": 1000
}
```

### 3. Use Git Integration

- View changes: `Ctrl+Shift+G`
- Stage files: Click `+` icon
- Commit: Type message and click checkmark
- Push: Click `...` → Push

### 4. Keyboard Shortcuts

Learn these essential shortcuts:
- `Ctrl+P` - Quick file open
- `Ctrl+Shift+F` - Search in files
- `Ctrl+/` - Toggle comment
- `Alt+Up/Down` - Move line up/down
- `Ctrl+D` - Select next occurrence

## Performance Tips

### Reduce IntelliSense CPU Usage

Add to settings:
```json
{
  "python.analysis.memory.keepLibraryAst": false
}
```

### Exclude Large Directories

Add to `.vscode/settings.json`:
```json
{
  "files.watcherExclude": {
    "**/build/**": true,
    "**/install/**": true
  }
}
```

## Next Steps

1. ✅ Complete this setup guide
2. 📖 Read `README.md` for project details
3. 🚀 Try `QUICKSTART.md` for quick reference
4. 🔧 Customize settings to your preference
5. 🐛 Start debugging with `F5`
6. 🤖 Test with your TurtleBot3 robot

## Additional Resources

- [VS Code Python Tutorial](https://code.visualstudio.com/docs/python/python-tutorial)
- [VS Code Debugging](https://code.visualstudio.com/docs/editor/debugging)
- [ROS2 Humble Documentation](https://docs.ros.org/en/humble/)
- [TurtleBot3 e-Manual](https://emanual.robotis.com/docs/en/platform/turtlebot3/)

---

**Happy coding! 🎉**

Need help? Check the README.md or open an issue on GitHub.
