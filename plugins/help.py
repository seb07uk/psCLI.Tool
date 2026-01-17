#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
================================================================================
  TERMINAL CLI - COMPREHENSIVE HELP SYSTEM v3.0.0
================================================================================
  File: plugins/help.py
  Author: Sebastian Januchowski
  Email: polsoft.its@fastservice.com
  GitHub: https://github.com/seb07uk
  Version: 3.0.0
  Date: January 17, 2026
  License: MIT
================================================================================
  Professional Help System with Complete Plugin Documentation
  Provides detailed help for all CLI commands with usage examples,
  syntax variations, tips, and quick references.
================================================================================
"""

import os
import sys

# --- METADATA (Read by cli.py) ---
__author__ = "Sebastian Januchowski"
__category__ = "help & info"
__group__ = "core"
__desc__ = "Professional help system for all available plugins and commands"
__version__ = "3.0.0"
__config__ = r"%userprofile%\.polsoft\psCli\settings\terminal.json"

# Handle both direct execution and import from cli.py
try:
    from cli import command, Color
    # Add MAGENTA if not available
    if not hasattr(Color, 'MAGENTA'):
        Color.MAGENTA = '\033[95m'
except (ImportError, ModuleNotFoundError):
    class Color:
        CYAN = '\033[96m'
        GREEN = '\033[92m'
        YELLOW = '\033[93m'
        GRAY = '\033[90m'
        RED = '\033[91m'
        WHITE = '\033[97m'
        BOLD = '\033[1m'
        BLUE = '\033[94m'
        MAGENTA = '\033[95m'
        RESET = '\033[0m'
    
    def command(name=None, aliases=None):
        def decorator(func):
            return func
        return decorator

# Short references for cleaner code
BOLD, RESET = Color.BOLD, Color.RESET
CYAN, GREEN, YELLOW = Color.CYAN, Color.GREEN, Color.YELLOW
GRAY, RED, WHITE, BLUE = Color.GRAY, Color.RED, Color.WHITE, Color.BLUE
MAGENTA = getattr(Color, 'MAGENTA', '\033[95m')

# ======================== PLUGIN DOCUMENTATION DATABASE ========================

PLUGINS_DB = {
    "cd": {
        "name": "cd",
        "category": "file system",
        "description": "Changes the current working directory with support for shortcuts and environment variables",
        "aliases": ["chdir"],
        "syntax": ["cd <path>", "cd ..", "cd ~", "cd -", "cd %VAR%"],
        "examples": [
            ("cd plugins", "Enter the plugins folder"),
            ("cd ..", "Go to parent directory"),
            ("cd -", "Toggle between directories"),
            ("cd %TEMP%", "Jump to temporary folder"),
            ("cd ~", "Return to home directory")
        ],
        "tips": ["Use 'cd -' to quickly switch back", "Environment variables work like %TEMP%", "Path completion with Tab key available"]
    },
    
    "pwd": {
        "name": "pwd",
        "category": "file system",
        "description": "Professional Directory Auditor & Path Telemetry Tool - displays comprehensive directory analysis",
        "aliases": ["where", "pwd"],
        "syntax": ["pwd [path]", "where [path]"],
        "examples": [
            ("pwd", "Analyze current directory"),
            ("where %TEMP%", "Inspect Temp folder"),
            ("pwd ..", "Check parent directory size")
        ],
        "tips": ["Shows disk space and file distribution at a glance", "Displays file count and total size", "Color-coded output for easy reading"],
        "output": "Displays directory path, file count, total size, and subdirectory breakdown"
    },
    
    "dir": {
        "name": "dir",
        "category": "file system",
        "description": "Dynamic directory explorer with sorting and type-based coloring - list files with various options",
        "aliases": ["ls", "list"],
        "syntax": ["dir [path] [option]", "ls [path] [option]"],
        "options": [
            "-t (Sort by Type)",
            "-n (Sort by Name - default)",
            "-s (Sort by Size)",
            "-d (Sort by Date)",
            "-r (Reverse order)"
        ],
        "examples": [
            ("dir", "List current directory"),
            ("dir -s", "Sort by largest files"),
            ("ls -d", "Show newest files first"),
            ("dir plugins", "List specific directory"),
            ("dir -t", "Group by file type")
        ],
        "tips": ["Supports sorting by size, name, date, and type", "Pagination for large folders", "Color-coded file types"]
    },
    
    "cls": {
        "name": "cls",
        "category": "system",
        "description": "Clears the console screen instantly and refreshes the display",
        "aliases": ["clear", "c"],
        "syntax": ["cls", "clear", "c"],
        "examples": [("cls", "Clear the entire screen")],
        "tips": ["Keyboard shortcuts for quick access", "Useful after large outputs"],
        "performance": "Instantaneous screen clear"
    },
    
    "echo": {
        "name": "echo",
        "category": "output",
        "description": "Displays text in colored output - useful for status messages and notifications",
        "aliases": ["say", "print-text"],
        "syntax": ["echo <text>", "say <text>"],
        "examples": [
            ("echo Hello World", "Prints text in green"),
            ("say Process completed", "Display message")
        ],
        "tips": ["Output is colored green by default", "Supports multi-word messages", "Useful in scripts for feedback"]
    },
    
    "calculator": {
        "name": "calculator",
        "category": "mathematics",
        "description": "Professional scientific calculator with history logging and mathematical functions",
        "aliases": ["calc", "math"],
        "syntax": ["calculator", "calc", "math"],
        "storage": r"%userprofile%\.polsoft\psCli\Calculator\history.txt",
        "features": [
            "Basic arithmetic (+, -, *, /)",
            "Power operations (**)",
            "Trigonometric functions (sin, cos, tan - in degrees)",
            "Square root and logarithms",
            "Persistent history logging",
            "Interactive mode"
        ],
        "examples": [("calc", "Launch interactive mode")],
        "tips": ["Trigonometry uses degrees, not radians", "View history with [h] command", "History saved automatically"]
    },
    
    "print": {
        "name": "print",
        "category": "file operations",
        "description": "Display file contents with syntax highlighting and optional text search",
        "aliases": ["cat", "type"],
        "syntax": ["print <file>", "cat <file>", "cat <file> <search_term>"],
        "supported_types": [".json", ".py", ".log", ".md", ".csv", ".txt", ".xml"],
        "examples": [
            ("print script.py", "View Python code with highlighting"),
            ("cat log.txt ERROR", "Search for 'ERROR' in log"),
            ("print metadata.json", "Display formatted JSON"),
            ("cat CHANGELOG.md", "View markdown file")
        ],
        "tips": ["Supports syntax highlighting for code files", "Pagination: 20 lines per screen", "Search results are highlighted"],
        "pagination": "Press [space] for next page, [q] to quit"
    },
    
    "notepad": {
        "name": "notepad",
        "category": "text editing",
        "description": "Interactive text editor with AutoSave and note management - full-featured text editor",
        "aliases": ["note", "edit"],
        "syntax": ["notepad", "note [filename]", "edit [filename]"],
        "storage": r"%userprofile%\.polsoft\psCLI\Notepad",
        "shortcuts": [
            "CTRL+Z then ENTER to save",
            "CTRL+X to cut",
            "CTRL+C to copy",
            "CTRL+V to paste",
            "ESC to cancel/exit"
        ],
        "examples": [
            ("note", "Open editor with new file"),
            ("note filename.txt", "Edit specific file")
        ],
        "tips": ["Auto-saves with timestamps", "Files stored with date/time naming", "Supports basic text formatting"]
    },
    
    "browse": {
        "name": "browse",
        "category": "web browser",
        "description": "Full-featured CLI web browser with history, cookies, and screenshot functionality",
        "aliases": ["web", "browser"],
        "syntax": ["browse [url]", "web [url]"],
        "features": [
            "Full HTML rendering in CLI",
            "Numbered link navigation",
            "Cookie and session persistence",
            "History tracking (last 50 URLs)",
            "Screenshot capability",
            "Back/forward navigation"
        ],
        "examples": [
            ("web google.com", "Open Google"),
            ("browse github.com", "Browse GitHub"),
            ("web", "Open home page")
        ],
        "shortcuts": [
            "[u] - Go back",
            "[snap] - Take screenshot",
            "[h] - Show history",
            "[q] - Quit"
        ],
        "tips": ["Links are numbered for easy clicking", "Cookies stored automatically", "Screenshots saved to Browser folder"],
        "storage": r"%userprofile%\.polsoft\psCli\Browser"
    },
    
    "venv": {
        "name": "venv",
        "category": "environment",
        "description": "Virtual environment manager - create, activate, deactivate, and manage Python virtual environments",
        "aliases": ["virtualenv", "env"],
        "syntax": [
            "venv create <name>",
            "venv activate <name>",
            "venv deactivate",
            "venv list",
            "venv delete <name>"
        ],
        "features": [
            "Create isolated Python environments",
            "Activate/deactivate environments",
            "List all environments",
            "Delete environments",
            "Install packages in venv",
            "Environment persistence"
        ],
        "examples": [
            ("venv create myenv", "Create new environment"),
            ("venv activate myenv", "Activate environment"),
            ("venv list", "Show all environments"),
            ("venv deactivate", "Exit current environment")
        ],
        "tips": ["Environments isolated for each project", "Dependencies don't conflict", "Always activate before installing packages"],
        "storage": r"%userprofile%\.polsoft\psCli\venv"
    },
    
    "games": {
        "name": "games",
        "category": "entertainment",
        "description": "Games Center - dynamic launcher for console games with multiple play options",
        "aliases": ["play", "game"],
        "syntax": ["games", "play [game_name]"],
        "available_games": [
            "Rock-Paper-Scissors",
            "Tic-Tac-Toe",
            "Snake CLI"
        ],
        "examples": [
            ("games", "Show available games"),
            ("play rock-paper-scissors", "Launch game")
        ],
        "tips": ["Press [q] to quit any game", "Games are fully interactive", "High scores may be tracked"]
    },
    
    "core": {
        "name": "core",
        "category": "system",
        "description": "Core Module Viewer - displays essential system plugins and core functionality",
        "aliases": ["sys", "base"],
        "syntax": ["core", "sys"],
        "examples": [("core", "Show core modules")],
        "tips": ["Shows system-critical plugins", "Foundation of CLI operation"]
    },
    
    "office": {
        "name": "office",
        "category": "office",
        "description": "Office Suite - manages documents and metadata previews",
        "aliases": ["docs", "work"],
        "syntax": ["office", "docs"],
        "features": [
            "Document management",
            "Metadata viewing",
            "File organization",
            "Office tools access"
        ],
        "examples": [("office", "Show office tools")],
        "tips": ["Centralizes document operations", "Metadata preview functionality"]
    },
    
    "save": {
        "name": "save",
        "category": "system",
        "description": "Saves file list with detailed folder summary to save directory with timestamp",
        "aliases": ["/s"],
        "syntax": ["save", "save -h"],
        "storage": r"%userprofile%\.polsoft\psCli\Save",
        "output_format": "Text file with command-style format (print file.txt # description)",
        "examples": [("save", "Create snapshot of current directory")],
        "tips": ["Files automatically timestamped", "Useful for project snapshots", "Naming: save_YYYY-MM-DD_HH-MM-SS.txt"],
        "automation": "Perfect for scheduled backups and documentation"
    },
    
    "paint": {
        "name": "paint",
        "category": "graphics",
        "description": "Paint application for drawing in terminal - ASCII art creation with multiple colors",
        "aliases": ["draw", "art"],
        "syntax": ["paint", "draw"],
        "features": [
            "Terminal-based drawing",
            "Multiple colors available",
            "Save artwork as ASCII",
            "Interactive brush controls",
            "Palette selection"
        ],
        "color_palette": [
            "1 - Green (#)",
            "2 - Red (#)",
            "3 - Blue (#)",
            "4 - Yellow (#)",
            "5 - Magenta (#)"
        ],
        "examples": [("paint", "Launch paint application")],
        "tips": ["Arrow keys for navigation", "Select color from palette", "Save your creations"],
        "storage": r"%userprofile%\.polsoft\psCli\Paint"
    }
}

# ======================== HELP ENGINE ========================

def format_section(title):
    """Format a help section title."""
    return f"{YELLOW}{title.upper()}:{RESET}"

def format_command(cmd, desc):
    """Format a command line."""
    return f"  {GREEN}{cmd.ljust(25)}{RESET} {desc}"

def format_tip(tip):
    """Format a tip line."""
    return f"  {MAGENTA}-{RESET} {tip}"

def print_separator(char="=", length=75):
    """Print a visual separator."""
    print(f"{GRAY}{char * length}{RESET}")

@command(name="help", aliases=["?", "h"])
def show_help(cmd_name=None):
    """
    Main help command logic with comprehensive documentation.
    
    Usage:
        help              - Show all commands
        help <command>    - Show detailed help for command
        ? <command>       - Shorthand for help
    """
    
    if not cmd_name:
        # Show all commands grouped by category
        box_width = 76
        print(f"\n{CYAN}{BOLD}{'=' * 76}{RESET}")
        
        line1 = f" TERMINAL CLI - COMPREHENSIVE HELP SYSTEM v{__version__} "
        padding1 = box_width - len(line1)
        print(f"{CYAN}{BOLD}{line1}{' ' * padding1}{RESET}")
        
        line2 = f" Professional CLI environment with {len(PLUGINS_DB)} documented modules "
        padding2 = box_width - len(line2)
        print(f"{CYAN}{BOLD}{line2}{' ' * padding2}{RESET}")
        
        print(f"{CYAN}{BOLD}{'=' * 76}{RESET}\n")
        
        # Quick start section
        print(f"{YELLOW}{BOLD}QUICK START:{RESET}")
        print(f"  {GREEN}help <command>{RESET}      Get detailed help about a specific command")
        print(f"  {GREEN}help all{RESET}            Show complete help for all commands")
        print(f"  {GREEN}?{RESET}                   Same as help\n")
        
        # Group commands by category
        categories = {}
        for cmd, data in PLUGINS_DB.items():
            cat = data.get("category", "other")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append((cmd, data['description']))
        
        # Display categories
        for cat in sorted(categories.keys()):
            print(f"{MAGENTA}{BOLD}> {cat.upper()}{RESET}")
            for cmd, desc in sorted(categories[cat]):
                print(format_command(cmd, desc))
            print()
        
        # Footer information
        print_separator("-")
        print(f"{GRAY}Type 'help <command>' for detailed information about a command.{RESET}")
        print(f"{GRAY}Type 'help all' to see complete documentation for all commands.{RESET}\n")
        return
    
    # Show help for "all" command
    if cmd_name.lower() == "all":
        print(f"\n{CYAN}{BOLD}COMPLETE COMMAND DOCUMENTATION{RESET}")
        print_separator("=")
        
        for cmd_name_sorted in sorted(PLUGINS_DB.keys()):
            _display_command_help(cmd_name_sorted)
        return
    
    # Show help for specific command
    cmd_name = cmd_name.lower()
    _display_command_help(cmd_name)

def _display_command_help(cmd_name):
    """Display detailed help for a specific command."""
    if cmd_name not in PLUGINS_DB:
        print(f"\n{RED}Error: Command '{cmd_name}' is not yet documented.{RESET}")
        print(f"{GRAY}Available commands: {', '.join(sorted(PLUGINS_DB.keys()))}{RESET}\n")
        return
    
    info = PLUGINS_DB[cmd_name]
    print(f"\n{CYAN}{BOLD}{'-' * 75}{RESET}")
    print(f"{CYAN}{BOLD}DOCUMENTATION: {info['name'].upper()}{RESET}")
    print(f"{CYAN}{BOLD}{'-' * 75}{RESET}\n")
    
    # Description
    print(f"{WHITE}{info['description']}{RESET}\n")
    
    # Aliases if available
    if "aliases" in info and info["aliases"]:
        aliases_str = ", ".join(f"{GREEN}{a}{RESET}" for a in info["aliases"])
        print(f"{YELLOW}Aliases:{RESET} {aliases_str}\n")
    
    # Syntax
    print(format_section("Syntax"))
    for syntax_line in info['syntax']:
        print(f"  {GREEN}{syntax_line}{RESET}")
    print()
    
    # Options
    if "options" in info:
        print(format_section("Options"))
        for opt in info['options']:
            print(f"  {BLUE}{opt}{RESET}")
        print()
    
    # Features
    if "features" in info:
        print(format_section("Features"))
        for feature in info['features']:
            print(f"  {MAGENTA}-{RESET} {feature}")
        print()
    
    # Supported types
    if "supported_types" in info:
        print(format_section("Supported Types"))
        types_str = ", ".join(info["supported_types"])
        print(f"  {types_str}\n")
    
    # Color palette
    if "color_palette" in info:
        print(format_section("Color Palette"))
        for color in info["color_palette"]:
            print(f"  {MAGENTA}-{RESET} {color}")
        print()
    
    # Examples
    print(format_section("Examples"))
    for cmd, desc in info['examples']:
        print(format_command(cmd, desc))
    print()
    
    # Shortcuts
    if "shortcuts" in info:
        print(format_section("Keyboard Shortcuts"))
        for shortcut in info["shortcuts"]:
            print(f"  {MAGENTA}-{RESET} {shortcut}")
        print()
    
    # Tips
    if "tips" in info:
        print(format_section("Tips"))
        for tip in info['tips']:
            print(format_tip(tip))
        print()
    
    # Additional information
    if "storage" in info:
        print(f"{GRAY}DATA LOCATION:{RESET} {info['storage']}")
    
    if "output" in info:
        print(f"{GRAY}OUTPUT:{RESET} {info['output']}")
    
    if "output_format" in info:
        print(f"{GRAY}OUTPUT FORMAT:{RESET} {info['output_format']}")
    
    if "pagination" in info:
        print(f"{GRAY}PAGINATION:{RESET} {info['pagination']}")
    
    if "performance" in info:
        print(f"{GRAY}PERFORMANCE:{RESET} {info['performance']}")
    
    if "automation" in info:
        print(f"{GRAY}AUTOMATION:{RESET} {info['automation']}")
    
    # Available games
    if "available_games" in info:
        print(f"\n{YELLOW}Available Games:{RESET}")
        for game in info["available_games"]:
            print(f"  {MAGENTA}-{RESET} {game}")
    
    print()

if __name__ == "__main__":
    if len(sys.argv) > 1:
        show_help(sys.argv[1])
    else:
        show_help()