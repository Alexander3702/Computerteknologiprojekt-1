# Quick Start Guide - TurtleBot3 Agent in VS Code

## For First-Time Users

### 1. Open the Project in VS Code

**Option A: Open Workspace File (Recommended)**
```bash
# Navigate to the project directory
cd /path/to/Computerteknologiprojekt-1

# Open the workspace in VS Code
code turtlebot3-agent.code-workspace
```

**Option B: Open Folder**
```bash
# Open the project folder directly
code .
```

### 2. Install Recommended Extensions

When you first open the project, VS Code will show a notification asking if you want to install the recommended extensions. Click **"Install All"**.

If you missed the notification:
1. Press `Ctrl+Shift+P`
2. Type "Extensions: Show Recommended Extensions"
3. Click "Install Workspace Recommended Extensions"

### 3. Select Python Interpreter

1. Press `Ctrl+Shift+P`
2. Type "Python: Select Interpreter"
3. Choose `/usr/bin/python3` or the Python 3.10+ interpreter with ROS2 packages

### 4. Run the Agent

**Using the Debugger (Best for Development):**
1. Press `F5` or click the "Run and Debug" icon in the sidebar
2. Select "Python: Main (TurtleBot3 Agent)" from the dropdown
3. Click the green play button

**Using Tasks:**
1. Press `Ctrl+Shift+B` (default build task)
2. Or press `Ctrl+Shift+P` → "Tasks: Run Task" → "Run TurtleBot3 Agent"

**Using Terminal:**
```bash
# Open integrated terminal (Ctrl+`)
python3 main.py
```

## Common Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| `F5` | Start debugging |
| `Ctrl+Shift+B` | Run build task (runs the agent) |
| `Ctrl+Shift+P` | Open command palette |
| `Ctrl+` ` | Open integrated terminal |
| `Ctrl+Shift+D` | Open Run and Debug view |
| `F9` | Toggle breakpoint |
| `F10` | Step over (when debugging) |
| `F11` | Step into (when debugging) |
| `Shift+F11` | Step out (when debugging) |

## Available Tasks

Access tasks via `Ctrl+Shift+P` → "Tasks: Run Task":

- **Run TurtleBot3 Agent** - Run the main application
- **Check Python Syntax** - Validate syntax of current file
- **Source ROS2 Environment** - Source ROS2 setup script
- **List ROS2 Topics** - Show all active ROS2 topics
- **Check ROS2 Node Status** - Display running ROS2 nodes

## Debugging Tips

### Setting Breakpoints
1. Click in the left margin next to any line number
2. A red dot appears - that's your breakpoint
3. Run with `F5`, and execution will pause at that line

### Inspecting Variables
When paused at a breakpoint:
- Hover over any variable to see its value
- Use the "Variables" panel on the left
- Use the "Watch" panel to monitor specific expressions
- Use the Debug Console to evaluate expressions

### Common Debug Configurations
- **Python: Main (TurtleBot3 Agent)** - Debug the main agent
- **Python: Current File** - Debug any open Python file
- **Python: TurtleBot3 Obstacle Detection Module** - Debug the detection module

## Troubleshooting in VS Code

### Python Import Errors
If you see red squiggles under `import rclpy`:
1. Make sure ROS2 is installed
2. Check Python interpreter: `Ctrl+Shift+P` → "Python: Select Interpreter"
3. Reload window: `Ctrl+Shift+P` → "Developer: Reload Window"

### IntelliSense Not Working
1. Open `.vscode/settings.json`
2. Verify the paths match your ROS2 installation
3. Reload window: `Ctrl+Shift+P` → "Developer: Reload Window"

### Terminal Shows Wrong Environment
1. Close all terminals
2. Open new terminal (`Ctrl+` `)
3. The ROS_DOMAIN_ID should be set automatically

### Debug Breakpoints Not Hit
- Ensure "justMyCode" is set to `false` in launch.json (already configured)
- Make sure you're running with debugger (`F5`), not just running the file

## Next Steps

1. **Explore the Code**: Open `main.py` and `turtlebot3_obstacle_detection.py`
2. **Read the Full README**: See `README.md` for detailed documentation
3. **Customize Settings**: Modify `.vscode/settings.json` as needed
4. **Create Your Own Tasks**: Add custom tasks to `.vscode/tasks.json`

## Getting Help

- **ROS2 Documentation**: https://docs.ros.org/en/humble/
- **TurtleBot3 Manual**: https://emanual.robotis.com/docs/en/platform/turtlebot3/
- **VS Code Python Documentation**: https://code.visualstudio.com/docs/python/python-tutorial

---

**Ready to code? Press F5 to start debugging!** 🚀
