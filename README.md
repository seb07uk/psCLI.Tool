# 🚀 psCLI.Tool - Professional Terminal CLI Framework

> ✨ **A sophisticated, extensible command-line interface framework for Windows** with plugin architecture, dynamic command loading, and comprehensive help system.
>
> *Transform your terminal into a powerful development environment with professional-grade tools, games, and utilities.*

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python Version](https://img.shields.io/badge/Python-3.7%2B-blue)](https://www.python.org/)
[![Platform](https://img.shields.io/badge/Platform-Windows-0078D4)](https://www.microsoft.com/en-us/windows)

---

## 📋 Table of Contents

- [✨ Features](#-features)
- [📁 Project Structure](#-project-structure)
- [⚙️ Installation & Setup](#️-installation--setup)
- [🎯 Quick Start](#-quick-start)
- [📖 Available Commands](#-available-commands)
- [🔌 Plugin Architecture](#-plugin-architecture)
- [🛠️ Creating Custom Plugins](#️-creating-custom-plugins)
- [⚡ Configuration](#-configuration)
- [📚 Built-in Plugins](#-built-in-plugins)
- [🎮 Games](#-games)
- [🔧 Tools](#-tools)
- [📄 License](#-license)

---

## ✨ Features

### 🎯 Core Capabilities

- 🔌 **Plugin-Based Architecture** — Dynamically load Python modules, PowerShell scripts, batch files, and executables
- 🎨 **ANSI Color Support** — Rich, colorized terminal output with themed commands and professional styling
- ⚡ **Command Aliasing** — Define aliases for frequently used commands for quick access
- 📚 **Professional Help System** — Comprehensive documentation and usage examples for all commands
- 📘 **Adaptive Help Output** — Line wrapping based on terminal width for optimal readability
- 🎮 **Integrated Games** — Built-in terminal games (Tic-Tac-Toe, Snake, Rock-Paper-Scissors)
- 📊 **Scientific Calculator** — Advanced calculator with history logging and complex functions
- 🔧 **Metadata System** — JSON-based configuration for plugin metadata
- 📝 **Settings Management** — Centralized configuration via JSON settings file
- 🔄 **Hot Reload** — Reload plugins without restarting the CLI

---

## 📁 Project Structure

```
psCLI.Tool/
├── cli.py                          # 🚀 Main CLI dispatcher and core framework
├── README.md                       # 📖 This file
├── plugins/                        # 🔌 Plugin modules directory
│   ├── __init__.py                # Package initialization
│   ├── core.py                    # Core system plugin viewer
│   ├── help.py                    # 📚 Professional help system
│   ├── calculator.py              # 🧮 Scientific calculator with history
│   ├── games.py                   # 🎮 Games center launcher
│   ├── browser.py                 # 🌐 Browser launcher
│   ├── notepad.py                 # 📝 Text editor launcher
│   ├── paint.py                   # 🎨 Paint application launcher
│   ├── office.py                  # 📊 MS Office suite launcher
│   ├── file.py                    # 📁 File Manager CLI
│   ├── lg2txt.py                  # 📋 File list generator
│   ├── echo.py                    # 🔊 Echo/print utilities
│   ├── print.py                   # 🖨️ Print file operations
│   ├── cls.py                     # 🧹 Clear screen command
│   ├── pwd.py                     # 📍 Print working directory
│   ├── cd.py                      # 🚪 Change directory
│   ├── dir.py                     # 📂 Directory listing   ├── tree.py                   # 🌳 Directory tree visualizer│   ├── save.py                    # 💾 File saving utilities
│   ├── venv.py                    # 🐍 Virtual environment management
│   ├── ascii.py                   # 🎭 ASCII Center launcher
│   ├── installer.py               # 📦 Installers Manager
│   ├── owner.py                   # 👤 Owner & environment info
│   ├── sudo.py                    # 🔐 Run with admin privileges
│   └── __pycache__/               # Python cache directory
├── ascii/                         # 🎪 ASCII assets launched by ascii.py
│   └── parrot.cmd                 # 🦜 Parrot colorful ASCII animation
├── tools/                         # 🔧 External tools launcher
│   ├── MAS.cmd                    # Windows activation scripts
│   ├── Office_365.bat             # Office 365 installer/activator
│   └── pmas.cmd                   # PowerShell Multi Activation System
├── games/                         # 🎯 Standalone game modules
│   ├── Tic-Tac-Toe.py            # Tic-Tac-Toe game
│   ├── Snake CLI.py               # Snake game
│   ├── Tetris Mini.py             # Tetris game
│   ├── Racer CLI.py               # Racer game
│   └── Rock-Paper-Scissors.py     # Rock-Paper-Scissors game
├── metadata/                      # ⚙️ Metadata and configuration
│   └── *.json                     # Plugin configuration files
└── __pycache__/                   # Python cache directory
```

---

## ⚙️ Installation & Setup

### 📋 Requirements

- **Python 3.7+** — Ensure Python is installed and available in PATH
- **Windows OS** — Optimized for Windows (PowerShell support for advanced features)
- **ANSI color support** — Enabled automatically in modern terminals

### 🚀 Setup Instructions

1. **Clone the repository:**
   ```bash
   git clone https://github.com/seb07uk/psCLI.Tool.git
   cd psCLI.Tool
   ```

2. **Create Python virtual environment (recommended):**
   ```bash
   python -m venv .venv
   .venv\Scripts\activate
   ```

3. **Create directories (automatic on first run):**
   The CLI automatically creates required directories:
   ```
   %USERPROFILE%\.polsoft\psCli\settings\
   %USERPROFILE%\.polsoft\psCli\Calculator\
   ```

4. **Run the CLI:**
   ```bash
   python cli.py
   ```

   Or from any location:
   ```bash
   python C:\path\to\psCLI.Tool\cli.py
   ```

---

## 🎯 Quick Start

### 🚀 Starting the CLI

```bash
python cli.py
```

This displays the main menu with available command groups and ready-to-use utilities.

### 💻 Interactive Mode

Launch the CLI and explore commands interactively:

```
psCLI.Tool > help                    # 📚 Show comprehensive help system
psCLI.Tool > all                     # 📋 Show all available commands
psCLI.Tool > core                    # 🔧 View core system modules
psCLI.Tool > calculator              # 🧮 Launch scientific calculator
psCLI.Tool > games                   # 🎮 Start games center
psCLI.Tool > ascii                   # 🎭 Open ASCII Center
psCLI.Tool > owner                   # 👤 Show owner & environment info
psCLI.Tool > reload                  # 🔄 Reload plugins (hot reload)
psCLI.Tool > exit                    # 🚪 Exit the CLI
```

### ⚡ Direct Command Execution

Execute commands directly without entering interactive mode:

```bash
python cli.py calculator
python cli.py games
python cli.py help
python cli.py ascii parrot
```

---

## 📖 Available Commands

### 📌 Menu Group Commands

| Command | Aliases | Description |
|---------|---------|-------------|
| `help` | `h`, `?` | 📚 Professional help system for all plugins |
| `core` | `sys`, `base` | 🔧 Core system modules viewer |
| `games` | `play`, `g` | 🎮 Games center with Tic-Tac-Toe, Snake, Tetris |
| `ascii` | `art`, `a` | 🎭 ASCII Center launcher for animations |

### 🖥️ Office Group Commands

| Command | Aliases | Description |
|---------|---------|-------------|
| `calculator` | `calc`, `math`, `kalk` | 🧮 Scientific calculator with history |
| `notepad` | `note`, `n` | 📝 Launch Notepad text editor |
| `paint` | `p` | 🎨 Launch Paint application |
| `print` | `cat`, `type` | 🖨️ Print file contents with highlighting |
| `browser` | `web`, `www` | 🌐 Launch CLI web browser |
| `office` | `docs`, `work` | 📊 Microsoft Office utilities launcher |
| `edit` | `ed` | ✏️ Terminal text editor (external binary) |

### 🔧 System Group Commands

| Command | Aliases | Description |
|---------|---------|-------------|
| `cls` | `clear`, `clean`, `c` | 🧹 Clear terminal screen |
| `pwd` | `path`, `where` | 📍 Print current working directory |
| `cd` | `chdir`, `jump` | 🚪 Change directory |
| `dir` | `ls`, `list` | 📂 List directory contents with advanced sorting |
| `tree` | `ls` | 🌳 Visualize directory structure in tree format |
| `echo` | `say`, `repeat`, `e` | 🔊 Echo text to console |
| `owner` | `about`, `me`, `whoami` | 👤 Owner information & environment |
| `sudo` | `admin`, `elevate` | 🔐 Run processes with admin privileges |

### 🛠️ Utility Group Commands

| Command | Aliases | Description |
|---------|---------|-------------|
| `save` | `/s` | 💾 File saving utilities |
| `venv` | `ve` | 🐍 Virtual environment management |
| `file` | `fm`, `fileman` | 📁 File Manager CLI |
| `lg2txt` | `lg`, `listgen` | 📋 File list generator |
| `installer` | `inst`, `i` | 📦 Installers Manager |

---

## 🔌 Plugin Architecture

### 🎯 How Plugins Work

The dispatcher (`cli.py`) automatically loads all plugin files from the `plugins/` directory:

1. **Python Modules** (`.py` files) — Imported and scanned for `@command` decorated functions
2. **External Binaries** (`.bat`, `.cmd`, `.ps1`, `.exe`, `.vbs`) — Registered and executed via subprocess
3. **Metadata** — Optional JSON files for plugin configuration and aliases

### 📥 Command Loading Process

```
1. Scan plugins/ directory
2. For each .py file:
   - Import the module
   - Extract module-level metadata (__author__, __category__, __group__, __desc__)
   - Find all @command decorated functions
   - Register commands and aliases
   - Display in appropriate groups (menu, core, office, utility)
```

### 📝 Plugin Metadata

Each plugin module should include:

```python
__author__ = "Author Name"
__category__ = "Category Name"
__group__ = "menu|core|office|utility"
__desc__ = "Short description of the plugin"
__version__ = "1.0.0"
```

### 🔗 External Asset & Tool Metadata Mapping

- External commands and assets are registered via JSON metadata files placed in `metadata/`
- Naming convention: `metadata/<filename>.<ext>.json` matches a file in `plugins/`, `ascii/`, or `tools/`
- Examples:
  - `metadata/parrot.cmd.json` → `ascii/parrot.cmd`
  - `metadata/edit.exe.json` → `plugins/edit.exe`
  - `metadata/adb-installer.py.json` → `plugins/adb-installer.py`

---

## 🛠️ Creating Custom Plugins

### 📦 Basic Plugin Template

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

### 🎨 Using Color Output

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

### 📄 Plugin with External File Support

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

---

## ⚡ Configuration

### ⚙️ Settings File

Configuration is stored in:
```
%USERPROFILE%\.polsoft\psCli\settings\terminal.json
```

### 📋 Example Configuration

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

### 🔧 Configuration Options

- `dispatcher.plugins_folder` — Relative path to plugins directory
- `dispatcher.metadata_folder` — Relative path to metadata directory
- `ui.clear_on_menu` — Clear screen when displaying menu (true/false)
- `ui.default_prompt` — Default prompt format (`{root_dir}` available variable)

---

## 📚 Built-in Plugins

### 🧮 Calculator (`calculator.py`)

Advanced scientific calculator with history logging:

```bash
psCLI.Tool > calculator
```

**Features:**
- ➕ Basic arithmetic operations (+, -, *, /)
- 📐 Scientific functions (sin, cos, tan, sqrt, log, etc.)
- 📊 Calculation history saved to `%USERPROFILE%\.polsoft\psCli\Calculator\history.txt`
- 🌍 Support for both comma and dot decimal separators

### 📚 Help System (`help.py`)

Comprehensive help documentation:

```bash
psCLI.Tool > help
```

**Features:**
- 📖 Detailed command documentation with examples
- 💡 Tips, tricks, and keyboard shortcuts
- 🎨 Adaptive line wrapping for readable output
- 🔍 Quick reference guide for all commands

### 🔧 Core Viewer (`core.py`)

View core system plugins:

```bash
psCLI.Tool > core
```

### 📁 File Manager (`file.py`)

Full-screen file manager with common filesystem operations:

```bash
psCLI.Tool > file
```

**Features:**
- 🗂️ Navigate directories and parent paths
- 💾 Disk usage information
- 🔄 Create/delete/rename/copy/move operations
- 🛡️ Backup (mirror) directories
- 🔎 Recursive search and list save

### 🌐 Browser (`browser.py`)

CLI web browser with history, cookies and link navigation:

```bash
psCLI.Tool > browser
```

### 📋 LG2TXT (`lg2txt.py`)

Interactive file list generator with global settings sync:

```bash
psCLI.Tool > lg2txt
```

### � Tree Visualizer (`tree.py`)

Elegant directory tree visualization with color-coded file types for instant visual hierarchy understanding:

```bash
psCLI.Tool > tree
psCLI.Tool > tree C:\Users
psCLI.Tool > tree . -d 2
psCLI.Tool > tree -a
```

**Features:**
- 🎨 Color-coded files by extension (executables, archives, documents, media)
- 📊 Display directory structure at a glance with beautiful ASCII art
- 🔍 Limit recursion depth for large directory hierarchies
- 👁️ Show hidden files with `-a` flag for complete visibility
- 📈 Recursive traversal with intuitive visual branch symbols

**Color Scheme:**
- 🔴 **Red** — Archives (.zip, .rar, .7z, .tar, .gz)
- 🟢 **Green** — Executables (.exe, .py, .ps1, .bat, .cmd)
- 🔵 **Cyan** — Documents (.pdf, .docx, .txt, .log, .md)
- 🟡 **Yellow** — Media (.jpg, .png, .gif, .mp4, .wav)
- ⚫ **Gray** — Configuration files (.json, .yaml, .ini)

### �🎭 ASCII Center (`ascii.py`)

Launcher for ASCII animations and scripts:

```bash
psCLI.Tool > ascii
ascii parrot
```

**Features:**
- 🎪 Intelligently scans the `/ascii` folder for available animations
- 🎬 Supports multiple formats: `.cmd`, `.bat`, `.ps1`, `.vbs`, `.exe`, `.py`
- 🖼️ Seamlessly launches assets in a new console window
- 📝 Automatically loads rich descriptions from matching JSON files in `metadata/`

### 👤 Owner (`owner.py`)

Comprehensive owner and environment information at your fingertips:

```bash
psCLI.Tool > owner
psCLI.Tool > owner mac
psCLI.Tool > owner mac set Ethernet
```

**Features:**
- 👥 Complete system identity: username, hostname, home directory, OS details
- 🌐 Real-time network status detection (online/offline) with IP information
- 📡 MAC address discovery with preferred adapter selection
- 💻 Detailed OS telemetry: release, build number, architecture, Python version
- 🔧 Persistent MAC address preference storage

### 🔐 Sudo (`sudo.py`)

Run commands with administrator privileges:

```bash
psCLI.Tool > sudo calc
psCLI.Tool > sudo notepad.exe README.md
```

**Notes:**
- ⚠️ Triggers UAC prompt
- 📝 Actions can be logged in `terminal.json`

### 📦 Installer Manager (`installer.py`)

Streamlined installer management with comprehensive metadata support:

```bash
psCLI.Tool > installer
installer adb-installer
```

**Features:**
- 📥 Intelligent scanning of `/plugins` folder for installer scripts
- 🏷️ Smart filtering by installer classification (`__group__ = "installer"`)
- 📊 Rich metadata display: description, aliases, author, and more
- 🔄 Unified support for multiple formats: Python, PowerShell, batch, and executables
- 🎯 One-command execution with argument pass-through

---

## 🎮 Games

The games center provides multiple terminal-based games:

### 🎲 Tic-Tac-Toe
Classic Tic-Tac-Toe game vs. computer AI
```bash
psCLI.Tool > games
> tic-tac-toe
```

### 🐍 Snake CLI
Navigate the snake to collect food
```bash
psCLI.Tool > games
> snake
```

### 🎭 Tetris Mini
Classic Tetris experience in the terminal
```bash
psCLI.Tool > games
> tetris
```

### 🎯 Rock-Paper-Scissors
Play against the computer with statistics
```bash
psCLI.Tool > games
> rock-paper-scissors
```

### 🏎️ Racer CLI
Drive your car and avoid obstacles
```bash
psCLI.Tool > games
> racer
```

---

## 🔧 Tools

External tools available:

- 📦 `MAS.cmd` — Microsoft Activation Scripts
- 📦 `pmas.cmd` — PowerShell Multi Activation System
- 📦 `Office_365.bat` — Office 365 installer/activator
- 📦 `fido.ps1` — Microsoft Windows ISO downloader

Usage:
```bash
psCLI.Tool > installer
installer adb-installer
```

---

## 🚀 Development

### 📊 Project Information

- **Author**: Sebastian Januchowski
- **Email**: polsoft.its@fastservice.com
- **GitHub**: https://github.com/seb07uk
- **License**: MIT
- **Created**: January 18, 2026
- **Latest Version**: 3.1.0

### 🤝 Contributing

To contribute to this project:

1. 🍴 Fork the repository
2. 🌿 Create a feature branch (`git checkout -b feature/amazing-feature`)
3. 📝 Create a new plugin in the `plugins/` directory
4. ✅ Include proper metadata headers
5. 🧪 Test with the CLI thoroughly
6. 💾 Commit your changes (`git commit -m 'Add amazing feature'`)
7. 📤 Push to the branch (`git push origin feature/amazing-feature`)
8. 🔄 Open a Pull Request

### 💡 Development Tips & Best Practices

- 🔄 **Hot Reload** — Use the `reload` command to instantly apply plugin changes during development without restarting
- 📚 **Help Integration** — Verify your plugin appears correctly in the `help` system and ensure documentation is complete
- 📖 **Clear Documentation** — Add comprehensive docstrings to your command functions for automatic help generation
- 🏷️ **Smart Aliasing** — Design meaningful aliases for frequently-used commands to improve productivity
- 🧪 **Thorough Testing** — Test with multiple argument combinations, edge cases, and error scenarios
- 🎨 **Consistent Styling** — Use the `Color` class responsibly to maintain a cohesive visual experience
- 📝 **Self-Documenting Code** — Document plugins directly in the help system using built-in help functions
- 🎯 **Error Handling** — Implement graceful error handling with informative messages for better UX

---

## 📄 License

This project is licensed under the **MIT License** - see the LICENSE file for details.

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

## 🌟 Quick Links

- 📖 [Full Documentation](#)
- 🐛 [Report Issues](https://github.com/seb07uk/psCLI.Tool/issues)
- 💬 [Discussions](https://github.com/seb07uk/psCLI.Tool/discussions)
- 📮 [Contact](mailto:polsoft.its@fastservice.com)

---

<div align="center">

**Version**: 3.1.0 (with Tree Visualizer)  
**Last Updated**: January 19, 2026

Made with ❤️ by Sebastian Januchowski

[⬆ Back to top](#)

</div>
