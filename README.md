# psCLI.Tool - Professional Terminal CLI Framework

> A sophisticated, extensible command-line interface framework for Windows with plugin architecture, dynamic command loading, and comprehensive help system.

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D4)](https://www.microsoft.com/en-us/windows)

## Table of Contents

- [Features](#features)
- [Project Structure](#project-structure)
- [Installation & Setup](#installation--setup)
- [Quick Start](#quick-start)
- [Available Commands](#available-commands)
- [Plugin Architecture](#plugin-architecture)
- [Creating Custom Plugins](#creating-custom-plugins)
- [Configuration](#configuration)
- [Built-in Plugins](#built-in-plugins)
- [Games](#games)
- [License](#license)

## Features

✨ **Core Features:**

- 🔌 **Plugin-Based Architecture** - Dynamically load Python modules, PowerShell scripts, batch files, and executables
- 🎨 **ANSI Color Support** - Rich, colorized terminal output with themed commands
- ⚡ **Command Aliasing** - Define aliases for frequently used commands
- 📚 **Professional Help System** - Comprehensive documentation and usage examples for all commands
- 🎮 **Integrated Games** - Built-in terminal games (Tic-Tac-Toe, Snake, Rock-Paper-Scissors)
- 📊 **Calculator & Tools** - Scientific calculator with history logging
- 🔧 **Metadata System** - JSON-based configuration for plugin metadata
- 📝 **Settings Management** - Centralized configuration via JSON settings file
- 🔄 **Hot Reload** - Reload plugins without restarting the CLI

## Project Structure

```
psCLI.Tool/
├── cli.py                          # Main CLI dispatcher and core framework
├── README.md                       # This file
├── plugins/                        # Plugin modules directory
│   ├── __init__.py                # Package initialization
│   ├── core.py                    # Core system plugin viewer
│   ├── help.py                    # Professional help system
│   ├── calculator.py              # Scientific calculator with history
│   ├── games.py                   # Games center launcher
│   ├── browser.py                 # Browser launcher
│   ├── notepad.py                 # Text editor launcher
│   ├── paint.py                   # Paint application launcher
│   ├── office.py                  # MS Office suite launcher
│   ├── echo.py                    # Echo/print utilities
│   ├── print.py                   # Print file operations
│   ├── cls.py                     # Clear screen command
│   ├── pwd.py                     # Print working directory
│   ├── cd.py                      # Change directory
│   ├── dir.py                     # Directory listing
│   ├── save.py                    # File saving utilities
│   ├── venv.py                    # Virtual environment management
│   └── __pycache__/               # Python cache directory
├── games/                         # Standalone game modules
│   ├── Tic-Tac-Toe.py            # Tic-Tac-Toe game
│   ├── Snake CLI.py               # Snake game
│   └── Rock-Paper-Scissors.py     # Rock-Paper-Scissors game
├── metadata/                      # Metadata and configuration
│   ├── venv.py.json              # Virtual environment settings
│   └── (other plugin metadata files)
└── __pycache__/                   # Python cache directory
```

## Installation & Setup

### Requirements

- **Python 3.7+**
- **Windows OS** (PowerShell support for advanced features)
- **ANSI color support** (enabled automatically)

### Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/seb07uk/psCLI.Tool.git
   cd psCLI.Tool
   ```

2. **Create directories (automatic on first run):**
   The CLI automatically creates required directories:
   ```
   %USERPROFILE%\.polsoft\psCli\settings\
   %USERPROFILE%\.polsoft\psCli\Calculator\
   ```

3. **Run the CLI:**
   ```bash
   python cli.py
   ```

   Or from any location:
   ```bash
   python C:\path\to\psCLI.Tool\cli.py
   ```

## Quick Start

### Starting the CLI

```bash
python cli.py
```

This displays the main menu with available command groups.

### Interactive Mode

```
psCLI.Tool > help                    # Show comprehensive help
psCLI.Tool > full                    # Show all available commands
psCLI.Tool > core                    # View core system modules
psCLI.Tool > calculator              # Launch scientific calculator
psCLI.Tool > games                   # Start games center
psCLI.Tool > reload                  # Reload plugins (hot reload)
psCLI.Tool > exit                    # Exit the CLI
```

### Direct Command Execution

Execute commands directly without entering interactive mode:

```bash
python cli.py calculator
python cli.py games
python cli.py help
```

## Available Commands

### Menu Group Commands

| Command | Aliases | Description |
|---------|---------|-------------|
| `help` | `h` | Professional help system for all available plugins |
| `core` | `sys`, `base` | Core system modules viewer |
| `games` | `play`, `g` | Games center with Tic-Tac-Toe, Snake, Rock-Paper-Scissors |

### Office Group Commands

| Command | Aliases | Description |
|---------|---------|-------------|
| `calculator` | `calc` | Scientific calculator with calculation history |
| `notepad` | `edit` | Launch Notepad text editor |
| `paint` | `draw` | Launch Paint application |
| `browser` | `web` | Launch default web browser |
| `office` | `ms` | Microsoft Office suite launcher |

### System Group Commands

| Command | Aliases | Description |
|---------|---------|-------------|
| `cls` | `clear` | Clear terminal screen |
| `pwd` | `current` | Print current working directory |
| `cd` | `chdir` | Change directory |
| `dir` | `ls` | List directory contents |
| `echo` | `print` | Echo text to console |
| `print` | `type` | Print file contents |

### Utility Group Commands

| Command | Aliases | Description |
|---------|---------|-------------|
| `save` | `export` | File saving utilities |
| `venv` | `virtualenv` | Virtual environment management |

## Plugin Architecture

### How Plugins Work

The dispatcher (`cli.py`) automatically loads all plugin files from the `plugins/` directory:

1. **Python Modules** (`.py` files) - Imported and scanned for `@command` decorated functions
2. **External Binaries** (`.bat`, `.cmd`, `.ps1`, `.exe`, `.vbs`) - Registered and executed via subprocess
3. **Metadata** - Optional JSON files for plugin configuration and aliases

### Command Loading Process

```
1. Scan plugins/ directory
2. For each .py file:
   - Import the module
   - Extract module-level metadata (__author__, __category__, __group__, __desc__, __version__)
   - Find all @command decorated functions
   - Register commands and aliases
   - Display in appropriate groups
```

### Plugin Metadata

Each plugin module should include:

```python
__author__ = "Author Name"
__category__ = "Category Name"
__group__ = "menu|core|office|utility"
__desc__ = "Short description of the plugin"
__version__ = "1.0.0"
```

## Creating Custom Plugins

### Basic Plugin Template

Create a new file in the `plugins/` directory:

```python
# plugins/my_plugin.py
from cli import command, Color

# --- METADATA ---
__author__ = "Your Name"
__category__ = "my_category"
__group__ = "utility"
__desc__ = "Brief description of your plugin"

@command(name="mycommand", aliases=["mc", "cmd"])
def my_command(*args):
    """Detailed description shown in help."""
    print(f"{Color.GREEN}Hello from my plugin!{Color.RESET}")
    if args:
        print(f"Arguments: {', '.join(args)}")

# Optional: Another command in the same plugin
@command(name="other")
def other_function(*args):
    """Another command in this plugin."""
    print(f"{Color.CYAN}This is another command{Color.RESET}")
```

### Using Color Output

The `Color` class provides ANSI color codes:

```python
from cli import Color

print(f"{Color.BLUE}Blue text{Color.RESET}")
print(f"{Color.GREEN}Green text{Color.RESET}")
print(f"{Color.YELLOW}Yellow text{Color.RESET}")
print(f"{Color.RED}Red text{Color.RESET}")
print(f"{Color.CYAN}Cyan text{Color.RESET}")
print(f"{Color.GRAY}Gray text{Color.RESET}")
print(f"{Color.BOLD}Bold text{Color.RESET}")
```

### Plugin with External File Support

```python
from cli import command, Color
import os

__author__ = "Your Name"
__category__ = "file_ops"
__group__ = "utility"
__desc__ = "File operations plugin"

@command(name="readfile", aliases=["read"])
def read_file(filename):
    """Read and display file contents."""
    try:
        if not os.path.exists(filename):
            print(f"{Color.RED}File not found: {filename}{Color.RESET}")
            return
        
        with open(filename, 'r', encoding='utf-8') as f:
            print(f"{Color.GREEN}=== {filename} ==={Color.RESET}")
            print(f.read())
    except Exception as e:
        print(f"{Color.RED}Error: {e}{Color.RESET}")
```

## Configuration

### Settings File

Configuration is stored in:
```
%USERPROFILE%\.polsoft\psCli\settings\terminal.json
```

### Example Configuration

```json
{
  "dispatcher": {
    "plugins_folder": "plugins",
    "metadata_folder": "metadata"
  },
  "ui": {
    "clear_on_menu": true,
    "default_prompt": "{root_dir} > "
  }
}
```

### Configuration Options

- `dispatcher.plugins_folder` - Relative path to plugins directory
- `dispatcher.metadata_folder` - Relative path to metadata directory
- `ui.clear_on_menu` - Clear screen when displaying menu (true/false)
- `ui.default_prompt` - Default prompt format (`{root_dir}` available variable)

## Built-in Plugins

### Calculator (`calculator.py`)

Advanced scientific calculator with history logging:

```bash
psCLI.Tool > calculator
```

**Features:**
- Basic arithmetic operations (+, -, *, /)
- Scientific functions (sin, cos, tan, sqrt, log, etc.)
- Calculation history saved to `%USERPROFILE%\.polsoft\psCli\Calculator\history.txt`
- Support for both comma and dot decimal separators

### Help System (`help.py`)

Comprehensive help documentation:

```bash
psCLI.Tool > help
```

**Features:**
- Detailed command documentation
- Usage examples and syntax variations
- Tips and tricks
- Quick reference guide

### Core Viewer (`core.py`)

View core system plugins:

```bash
psCLI.Tool > core
```

## Games

The games center provides three terminal-based games:

### Tic-Tac-Toe
Classic Tic-Tac-Toe game vs. computer AI
```bash
psCLI.Tool > games
> 1
```

### Snake CLI
Navigate the snake to collect food
```bash
psCLI.Tool > games
> 2
```

### Rock-Paper-Scissors
Play against the computer
```bash
psCLI.Tool > games
> 3
```

## Development

### Project Information

- **Author**: Sebastian Januchowski
- **Email**: polsoft.its@fastservice.com
- **GitHub**: https://github.com/seb07uk
- **License**: MIT
- **Created**: January 17, 2026

### Contributing

To contribute:

1. Create a new plugin in the `plugins/` directory
2. Include proper metadata headers
3. Use the `@command` decorator
4. Test with the CLI
5. Submit a pull request

### Development Tips

- Use `reload` command to hot-reload plugins during development
- Check the `help` system to ensure your plugin appears correctly
- Add comprehensive docstrings to your command functions
- Use meaningful aliases for quick access
- Test with multiple argument combinations

## License

This project is licensed under the MIT License - see the LICENSE file for details.

```
MIT License

Copyright (c) 2026 Sebastian Januchowski

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.
```

---

**Version**: 3.0.0  
**Last Updated**: January 17, 2026
