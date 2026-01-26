#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
╔════════════════════════════════════════════════════════════════════════════╗
║        🚀 TERMINAL CLI - COMPREHENSIVE HELP SYSTEM v3.0.0 🚀               ║
╚════════════════════════════════════════════════════════════════════════════╝
  
  File: plugins/help.py
  Author: Sebastian Januchowski
  Email: polsoft.its@fastservice.com
  GitHub: https://github.com/seb07uk
  Version: 3.1.0
  Date: January 19, 2026
  License: MIT
  
  ✨ Professional Help System with Complete Plugin Documentation ✨
  
  Provides detailed help for all CLI commands with usage examples,
  syntax variations, tips, and quick references.
  
  📚 Get Started:
     - Type 'help' to see all available commands
     - Type 'help <command>' for detailed information about a specific command
     - Use aliases for quick navigation
  
  💡 Pro Tips:
     - Commands are case-insensitive
     - Aliases work the same way as command names
     - Press [Tab] for command auto-completion
     - Use 'exit' or 'quit' to return to main menu
"""

import os
import sys
import shutil
import textwrap
import json

# --- METADATA (Read by cli.py) ---
__author__ = "Sebastian Januchowski"
__category__ = "help & info"
__group__ = "core"
__desc__ = "Professional help system for all available plugins and commands"
__version__ = "3.1.0"
__updated__ = "January 19, 2026"
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
        "aliases": ["chdir", "jump"],
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
        "aliases": ["path", "where"],
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
        "aliases": ["clear", "clean", "c"],
        "syntax": ["cls", "clear", "c"],
        "examples": [("cls", "Clear the entire screen")],
        "tips": ["Keyboard shortcuts for quick access", "Useful after large outputs"],
        "performance": "Instantaneous screen clear"
    },
    
    "echo": {
        "name": "echo",
        "category": "output",
        "description": "Displays the provided text in green",
        "aliases": ["say", "repeat", "e"],
        "syntax": ["echo <text>", "say <text>"],
        "examples": [
            ("echo Hello World", "Prints text in green"),
            ("say Process completed", "Display message")
        ],
        "tips": ["Output is colored green by default", "Supports multi-word messages", "Useful in scripts for feedback"]
    },
    
    "calculator": {
        "name": "calculator",
        "category": "math",
        "description": "Professional scientific calculator with history logging and mathematical functions",
        "aliases": ["calc", "math", "kalk"],
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
        "supported_types": [".json", ".py", ".log", ".md", ".csv", ".txt", ".xml", ".yaml"],
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
        "aliases": ["note", "n"],
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
    
    "browser": {
        "name": "browser",
        "category": "web browser",
        "description": "psBrowser CLI: Full Suite with History & Quick Links - Full-featured CLI web browser with history, cookies, and screenshot functionality",
        "aliases": ["web", "www"],
        "syntax": ["browser [url]", "web [url]", "www [url]"],
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
            ("browser github.com", "Browse GitHub"),
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
            "Snake CLI",
            "Hangman",
            "Racer CLI",
            "Tetris Mini"
        ],
        "examples": [
            ("games", "Show available games"),
            ("play rock-paper-scissors", "Launch game"),
            ("play hangman", "Play Hangman")
        ],
        "tips": ["Press [q] to quit any game", "Games are fully interactive", "High scores may be tracked", "6 games available: Rock-Paper-Scissors, Tic-Tac-Toe, Snake CLI, Hangman, Racer CLI, Tetris Mini"],
        "storage": r"%projectroot%\games"
    },
    
    "ascii": {
        "name": "ascii",
        "category": "ascii art",
        "description": "ASCII Center - launcher for ASCII animations and scripts from the /ascii folder",
        "aliases": ["art", "a"],
        "syntax": ["ascii", "ascii <asset_name>", "ascii <ID>"],
        "features": [
            "Scans the /ascii folder",
            "Supports .cmd, .bat, .ps1, .vbs, .exe, .py",
            "Launches in a new console window",
            "Descriptions loaded from metadata files in /metadata"
        ],
        "examples": [
            ("ascii", "Show the list of available assets"),
            ("ascii parrot", "Launch the Parrot animation"),
            ("ascii 1", "Launch the asset with ID 1")
        ],
        "tips": [
            "Type the asset name or ID",
            "For .cmd/.bat scripts, cmd /c is used",
            "For .ps1, PowerShell with Bypass is used",
            "Add descriptions in metadata/<filename>.json"
        ],
        "storage": r"%userprofile%\.polsoft\psCLI\ascii"
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
        "category": "paint cli",
        "description": "Paint application for drawing in terminal - ASCII art creation with multiple colors",
        "aliases": ["p"],
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
    },
    
    "hack": {
        "name": "hack",
        "category": "hacking",
        "description": "Hacking Tools - dynamic launcher for system tools",
        "aliases": ["tools", "exploit"],
        "syntax": ["hack", "hack <tool_name>"],
        "features": [
            "Dynamic system tools launcher",
            "Metadata-driven tool management",
            "Tool categorization and organization",
            "Easy tool execution",
            "Tool information display"
        ],
        "examples": [
            ("hack", "Show available tools"),
            ("hack pmas", "Execute PMAS activation tool"),
            ("hack Office_365", "Execute Office 365 batch script"),
            ("hack mas", "Execute Microsoft Activation Scripts"),
            ("hack fido", "Launch Windows ISO downloader")
        ],
        "tips": ["Tools are loaded from /tools/ directory", "Metadata stored in /metadata/", "Easy integration of new tools"],
        "storage": r"v:\tools"
    },
    
    "pmas": {
        "name": "pmas",
        "category": "activation",
        "description": "PowerShell Multi Activation System - Windows activation tool",
        "aliases": ["activate"],
        "syntax": ["pmas"],
        "authors": ["Abdullah Ertürk", "mephistooo2", "Dark Vador", "Windows_Addict"],
        "features": [
            "Windows activation",
            "Multi-activation system",
            "PowerShell-based automation",
            "Secure script verification"
        ],
        "examples": [
            ("pmas", "Launch PowerShell Multi Activation System"),
            ("activate", "Quick activation tool (alias)")
        ],
        "tips": ["Requires administrator privileges", "Script includes integrity verification", "Supports multiple languages"],
        "group": "microsoft"
    },

    "office_365": {
        "name": "office_365",
        "category": "microsoft",
        "description": "Microsoft Office 365 installation and activation tool",
        "aliases": ["ms365", "msoffice"],
        "syntax": ["office_365.bat"],
        "features": [
            "Office 365 deployment",
            "Automatic download and extraction",
            "Configuration-based installation",
            "64-bit Office support"
        ],
        "examples": [
            ("office_365.bat", "Install Microsoft Office 365"),
            ("ms365", "Quick launch (alias)")
        ],
        "tips": ["Downloads Office Deployment Tool automatically", "Requires internet connection", "Creates configuration files dynamically"],
        "group": "microsoft",
        "requires": "Administrator privileges, Internet connection"
    },
    
    "file": {
        "name": "file",
        "category": "file manager",
        "description": "CMD Cli File Manager: full suite with history and quick links",
        "aliases": ["fm", "fileman"],
        "syntax": ["file"],
        "features": [
            "Navigate directories and parent path",
            "Disk usage information",
            "Create/delete files and folders",
            "Rename, copy, move items",
            "Backup (mirror) directories",
            "Search files recursively",
            "Save file list reports",
            "Open saved reports folder"
        ],
        "examples": [("file", "Launch the File Manager")],
        "tips": ["Use menu options [1-18]", "Reports saved with timestamps"],
        "storage": r"%userprofile%\.polsoft\psCLI\FileList"
    },
    
    "lg2txt": {
        "name": "lg2txt",
        "category": "file list",
        "description": "Terminal file list generator with global settings sync",
        "aliases": ["lg", "listgen"],
        "syntax": ["lg2txt"],
        "features": [
            "Generate lists of files and folders",
            "Files-only mode",
            "Extension filter mode",
            "Preview generated output",
            "Sync settings in terminal.json"
        ],
        "examples": [("lg2txt", "Open interactive list generator")],
        "tips": ["Change source/output paths from menu", "Logs written to List.log"],
        "storage": r"%userprofile%\.polsoft\psCLI\Log\List.log"
    },
    
    "edit": {
        "name": "edit",
        "category": "editor",
        "description": "Edit - terminal text editor (external binary)",
        "aliases": ["ed"],
        "syntax": ["edit"],
        "features": [
            "Runs as an external binary",
            "Integrated via metadata file edit.exe.json",
            "Quick editing of text files"
        ],
        "examples": [
            ("edit", "Launch the text editor in terminal")
        ],
        "tips": [
            "Requires edit.exe to be available in plugins/",
            "Alias: ed"
        ]
    },
    
    "mas": {
        "name": "mas",
        "category": "microsoft",
        "description": "Microsoft Activation Scripts (MAS) - Windows/Office activation tool",
        "aliases": ["mas", "activation", "kms"],
        "syntax": ["mas", "MAS.cmd"],
        "features": [
            "Windows activation",
            "Office activation",
            "Multiple activation methods"
        ],
        "examples": [("hack mas", "Execute Microsoft Activation Scripts")],
        "tips": ["Requires administrator privileges", "Loaded via hack tools menu"],
        "group": "hacking"
    },
    
    "wat": {
        "name": "wat",
        "category": "microsoft",
        "description": "Windows Activation Tools (WAT) - zarządzanie licencją i aktywacją",
        "aliases": ["wat", "winact"],
        "syntax": ["wat"],
        "features": [
            "Activation status",
            "License information (basic/detailed)",
            "BIOS/UEFI product key",
            "Restart licensing service",
            "Enter product key",
            "Activate system"
        ],
        "examples": [
            ("hack wat", "Launch WAT from tools menu"),
            ("wat", "Run directly from tools directory")
        ],
        "tips": [
            "Administrator privileges required for some operations",
            "Operates under hacking group (Microsoft tools)"
        ],
        "group": "microsoft"
    },
    
    "activstatus": {
        "name": "activstatus",
        "category": "microsoft",
        "description": "Windows Activation Status - quick check of system activation state",
        "aliases": ["activstatus", "stats"],
        "syntax": ["activstatus"],
        "features": [
            "Windows activation check",
            "License status report"
        ],
        "examples": [
            ("hack activstatus", "Launch activation status from hack menu"),
            ("activstatus", "Run script directly from tools")
        ],
        "tips": [
            "Requires console with appropriate privileges",
            "Fast license diagnostics"
        ],
        "group": "microsoft"
    },
    
    "sudo": {
        "name": "sudo",
        "category": "system",
        "description": "Execute programs with administrator privileges",
        "aliases": ["admin", "elevate"],
        "syntax": ["sudo <command> [args]"],
        "examples": [
            ("sudo calc", "Run Calculator as administrator"),
            ("sudo notepad.exe README.md", "Open Notepad with admin rights")
        ],
        "tips": ["Triggers UAC elevation prompt", "Actions are logged to terminal.json"],
        "storage": r"%userprofile%\.polsoft\psCli\settings\terminal.json"
    },
    
    "passwd": {
        "name": "passwd",
        "category": "system",
        "description": "Password manager and protected launcher for modules and CLI commands",
        "aliases": ["password", "pass"],
        "syntax": [
            "passwd",
            "passwd help",
            "passwd protect <command...>",
            "passwd unprotect <command...>",
            "passwd list",
            "passwd clear",
            "passwd module <name>"
        ],
        "features": [
            "Manage master password (change/reset)",
            "Protect CLI commands (requires password on run)",
            "Protect Python modules under modules/",
            "Interactive menu to run and toggle protection",
            "Persistent storage in protected.json"
        ],
        "examples": [
            ("passwd", "Open interactive password manager"),
            ("passwd protect directx jawa vcredis", "Protect selected commands"),
            ("passwd list", "Show protected commands"),
            ("passwd module mymod", "Run protected Python module from modules/")
        ],
        "tips": [
            "Protected commands require password before execution",
            "Modules protection stored under 'modules' section in protected.json",
            "Use 'clear' to remove all protection",
            "Aliases: password, pass"
        ],
        "storage": r"%userprofile%\.polsoft\psCli\settings\protected.json"
    },
    
    "fido": {
        "name": "fido",
        "category": "microsoft",
        "description": "Fido - Microsoft Windows ISO downloader (PowerShell script)",
        "aliases": ["fido", "iso", "win-iso"],
        "syntax": ["fido.ps1"],
        "features": [
            "Download Windows 10/11 official ISO",
            "Command-line mode support",
            "Locale, edition and architecture selection"
        ],
        "examples": [
            ("hack fido", "Launch Fido ISO downloader"),
            ("fido.ps1", "Run as standalone PowerShell script")
        ],
        "tips": ["Requires PowerShell", "Internet connection needed"],
        "group": "microsoft"
    },
    
    "owner": {
        "name": "owner",
        "category": "info",
        "description": "Owner and environment information viewer with network status and optional metadata save",
        "aliases": ["about", "me", "whoami"],
        "syntax": ["owner", "owner save", "owner mac", "owner mac <adapter_name>", "owner mac set <adapter_name>"],
        "features": [
            "Display username, host, home directory and OS",
            "Show local IP, online status and public IP (if available)",
            "Detailed OS info: release, version, build, machine, processor, Python",
            "Display MAC address",
            "List adapters and set preferred adapter for MAC display in CLI",
            "Save metadata to user profile",
            "Simple CLI output with color"
        ],
        "examples": [
            ("owner", "Show owner and environment information"),
            ("owner save", "Save metadata to echo.json"),
            ("owner mac", "List adapters and MAC addresses"),
            ("owner mac set Ethernet", "Set preferred adapter to 'Ethernet'")
        ],
        "tips": [
            "Use 'owner save' to persist info",
            "Use 'owner mac set <name>' to change adapter (shown in CLI)",
            "Network detection uses DNS connectivity check",
            "MAC discovery falls back to 'ipconfig /all' if 'getmac' unavailable",
            "Supports localized 'Adres fizyczny' in ipconfig output"
        ],
        "storage": r"%userprofile%\.polsoft\psCLI\metadata\echo.json"
    },

    "installer": {
        "name": "installer",
        "category": "utilities",
        "description": "Installer Manager - launcher for installer modules and scripts with metadata support",
        "aliases": ["install", "ins"],
        "syntax": ["installer", "install [module_name]"],
        "features": [
            "Display available installers",
            "Execute installer scripts",
            "Load metadata from JSON files",
            "Support .py, .bat, .cmd, .ps1, .vbs, .exe files",
            "Interactive installer selection"
        ],
        "examples": [
            ("installer", "Show available installers"),
            ("install DirectX", "Execute DirectX installer")
        ],
        "tips": ["Installers stored in /install/ directory", "Metadata files in /metadata/", "Easy integration of new installers"],
        "storage": r"%projectroot%\install"
    },

    "health": {
        "name": "health",
        "category": "system",
        "description": "Health Tools - system health check and maintenance utilities",
        "aliases": ["check", "restore"],
        "syntax": ["health [tool_name]"],
        "features": [
            "System health diagnostics",
            "Performance monitoring",
            "Health restoration scripts",
            "System cleanup utilities"
        ],
        "examples": [
            ("health", "Show health tools"),
            ("health restore", "Run restoration utility")
        ],
        "tips": ["Health tools in /health/ directory", "Scripts with metadata support", "Safe system maintenance"],
        "storage": r"%projectroot%\health"
    },

    "reboot": {
        "name": "reboot",
        "category": "system",
        "description": "System reboot utility with optional delayed restart functionality",
        "aliases": ["restart", "r"],
        "syntax": ["reboot", "restart [seconds]"],
        "features": [
            "Immediate system restart",
            "Delayed restart with countdown",
            "Clean shutdown",
            "Process termination before restart"
        ],
        "examples": [
            ("reboot", "Restart system immediately"),
            ("restart 60", "Restart after 60 seconds")
        ],
        "tips": ["Close applications before reboot", "Save your work first", "Countdown can be interrupted"],
        "requires": "Administrator privileges"
    },

    "shutdown": {
        "name": "shutdown",
        "category": "system",
        "description": "System shutdown utility with optional delayed shutdown and message display",
        "aliases": ["power", "off", "stop"],
        "syntax": ["shutdown", "power [seconds]", "shutdown -c"],
        "features": [
            "Immediate system shutdown",
            "Delayed shutdown with countdown",
            "Cancel scheduled shutdown",
            "Message display before shutdown"
        ],
        "examples": [
            ("shutdown", "Shutdown system immediately"),
            ("power 120", "Shutdown after 120 seconds"),
            ("shutdown -c", "Cancel scheduled shutdown")
        ],
        "tips": ["Save work before shutdown", "Use -c to cancel", "Supports countdown timer"],
        "requires": "Administrator privileges"
    },

    "tcp_ip": {
        "name": "tcp_ip",
        "category": "network",
        "description": "Network diagnostics and TCP/IP utilities - connectivity testing and network analysis",
        "aliases": ["net", "network", "ping", "ipconfig"],
        "syntax": ["tcp_ip", "tcp_ip [host]", "tcp_ip analyze"],
        "features": [
            "Network connectivity testing",
            "IP configuration display",
            "DNS resolution",
            "Route analysis",
            "Network adapter information"
        ],
        "examples": [
            ("tcp_ip", "Show network status"),
            ("tcp_ip google.com", "Test connectivity to host"),
            ("tcp_ip analyze", "Analyze network configuration")
        ],
        "tips": ["Displays local and public IP", "Network status check", "DNS and routing information"],
        "storage": r"%userprofile%\.polsoft\psCli\network"
    },

    "tree": {
        "name": "tree",
        "category": "file system",
        "description": "Directory tree viewer - displays folder structure in visual tree format",
        "aliases": ["dtree", "filetree"],
        "syntax": ["tree [path] [depth]"],
        "features": [
            "Visual directory tree display",
            "Configurable depth limit",
            "File and folder counts",
            "ASCII art formatting",
            "Recursive folder traversal"
        ],
        "examples": [
            ("tree", "Show current directory tree"),
            ("tree .", "Show tree of current folder"),
            ("tree . 3", "Show tree 3 levels deep")
        ],
        "tips": ["Limit depth for large folders", "Visual ASCII representation", "Shows folder structure clearly"],
        "output": "ASCII tree with folders and file counts"
    },

    "aliases": {
        "name": "aliases",
        "category": "configuration",
        "description": "Command aliases management - view and manage command shortcuts",
        "aliases": ["alias", "shortcuts"],
        "syntax": ["aliases", "aliases list", "aliases add <alias> <command>"],
        "features": [
            "List all command aliases",
            "View alias definitions",
            "Add custom aliases",
            "Remove aliases",
            "Save alias configuration"
        ],
        "examples": [
            ("aliases", "Show all aliases"),
            ("aliases list", "Display alias list"),
            ("aliases add g games", "Create shortcut 'g' for 'games'")
        ],
        "tips": ["Aliases reduce typing", "Case-insensitive", "Persist across sessions"],
        "storage": r"%userprofile%\.polsoft\psCli\aliases.json"
    },

    "html": {
        "name": "html",
        "category": "reports",
        "description": "HTML Reports & Hub - manage, open and view generated reports (offline-ready)",
        "aliases": ["report", "export", "reports", "show-reports"],
        "syntax": [
            "reports",
            "show-report <number|name>",
            "reports-hub",
            "reports-setup"
        ],
        "features": [
            "List and open generated HTML reports",
            "Interactive Reports Hub dashboard",
            "Offline assets installer (CSS/JS stored locally)",
            "Local styling via Pico.css and Highlight.js",
            "Automatic asset fallback if download fails"
        ],
        "examples": [
            ("reports", "Show available HTML reports"),
            ("show-report 1", "Open the latest report by index"),
            ("reports-hub", "Open Reports Hub dashboard"),
            ("reports-setup", "Download local CSS/JS assets for offline mode")
        ],
        "tips": [
            "Use 'reports-setup' once to install local assets",
            "Reports are saved under the Reports folder",
            "Reports Hub references local assets for offline viewing",
            "If asset download fails, minimal inline styles are used"
        ],
        "storage": r"%userprofile%\.polsoft\psCli\reports",
        "assets": r"%userprofile%\.polsoft\psCli\reports\assets"
    },
    
    "integrate": {
        "name": "integrate",
        "category": "maintenance",
        "description": "Automatyczna integracja: wykrywa moduły, tworzy metadane i rejestruje",
        "aliases": ["autometadata", "genmeta"],
        "syntax": ["integrate", "autometadata", "genmeta"],
        "examples": [
            ("integrate", "Detect and integrate new modules")
        ],
        "tips": [
            "Automatically creates metadata in the metadata directory",
            "Supports: plugins/, games/, ascii/, health/, tools/, install/"
        ]
    },
    
    "build": {
        "name": "build",
        "category": "build",
        "description": "Build standalone psCLI.exe (PyInstaller onefile)",
        "aliases": ["pack", "compress"],
        "syntax": ["build", "pack", "compress"],
        "examples": [
            ("build", "Build psCLI.exe")
        ],
        "tips": [
            "Adds icon if icon.ico exists",
            "Includes data: plugins, games, metadata, ascii, health, tools, install"
        ]
    }
}

_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
_meta_dir = os.path.join(_root, "metadata")
_dirs = {
    "ascii": os.path.join(_root, "ascii"),
    "health": os.path.join(_root, "health"),
    "tools": os.path.join(_root, "tools"),
    "install": os.path.join(_root, "install"),
}

def _augment_metadata_docs():
    try:
        if not os.path.exists(_meta_dir):
            return
        for mf in os.listdir(_meta_dir):
            if not mf.lower().endswith(".json"):
                continue
            mp = os.path.join(_meta_dir, mf)
            try:
                with open(mp, "r", encoding="utf-8") as fh:
                    md = json.load(fh)
            except:
                continue
            base = os.path.splitext(mf)[0]
            k = base.lower()
            k_nice = k.replace(".bat", "").replace(".cmd", "").replace(".ps1", "").replace(".exe", "").replace(".vbs", "")
            if k in PLUGINS_DB or k_nice in PLUGINS_DB:
                continue
            found_path = None
            for dname, dpath in _dirs.items():
                candidates = [
                    os.path.join(dpath, base),
                    os.path.join(dpath, k_nice + ".bat"),
                    os.path.join(dpath, k_nice + ".cmd"),
                    os.path.join(dpath, k_nice + ".ps1"),
                    os.path.join(dpath, k_nice + ".exe"),
                    os.path.join(dpath, k_nice + ".vbs"),
                ]
                if any(os.path.exists(p) for p in candidates):
                    found_path = dname
                    break
            if not found_path:
                continue
            name_key = k_nice
            syntax = [name_key]
            if base != name_key:
                syntax.append(base)
            PLUGINS_DB[name_key] = {
                "name": name_key,
                "category": md.get("category", found_path),
                "description": md.get("desc", "Tool"),
                "aliases": md.get("aliases", []),
                "syntax": syntax,
                "examples": [(f"{'hack' if found_path=='tools' else found_path} {name_key}", "Launch")],
                "tips": ["Auto-documented from metadata", f"Loaded from /{found_path}/"],
                "group": md.get("group", found_path)
            }
    except:
        pass

_augment_metadata_docs()

# ======================== HELP ENGINE ========================

def _term_width(default=76):
    try:
        w = shutil.get_terminal_size((default, 20)).columns
        return max(50, min(w, 120))
    except:
        return default

def format_section(title):
    return f"{YELLOW}{title.upper()}:{RESET}"

def format_command(cmd, desc):
    width = _term_width()
    cmd_col = 25
    prefix = f"  {GREEN}{cmd.ljust(cmd_col)}{RESET} "
    wrap_width = max(20, width - (cmd_col + 3))
    desc_lines = textwrap.wrap(desc, width=wrap_width)
    if not desc_lines:
        return prefix
    lines = [prefix + desc_lines[0]]
    subsequent_indent = " " * (cmd_col + 3)
    for line in desc_lines[1:]:
        lines.append(subsequent_indent + line)
    return "\n".join(lines)

def format_tip(tip):
    width = _term_width()
    bullet = f"  {MAGENTA}-{RESET} "
    wrap_width = max(20, width - 6)
    return textwrap.fill(tip, width=wrap_width, initial_indent=bullet, subsequent_indent="    ")

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
        box_width = 82
        print(f"\n{CYAN}{BOLD}{'╔' + '═' * 80 + '╗'}{RESET}")
        
        line1 = f"  🚀 TERMINAL CLI - HELP SYSTEM v{__version__}  "
        padding1 = 82 - len(line1) - 4
        print(f"{CYAN}{BOLD}║ {line1}{' ' * max(0, padding1)}║{RESET}")
        
        module_count = len(PLUGINS_DB)
        line2 = f"  Professional CLI with {module_count} documented modules - Updated 2026-01-19  "
        padding2 = 82 - len(line2) - 4
        print(f"{CYAN}{BOLD}║ {line2}{' ' * max(0, padding2)}║{RESET}")
        
        print(f"{CYAN}{BOLD}{'╚' + '═' * 80 + '╝'}{RESET}\n")
        
        # Quick start section
        print(f"{YELLOW}{BOLD}⭐ QUICK START:{RESET}")
        print(f"  {GREEN}help{RESET}                - Show all available commands")
        print(f"  {GREEN}help <cmd>{RESET}         - Get detailed help for a command")
        print(f"  {GREEN}? <cmd>{RESET}            - Quick help shorthand")
        print(f"  {GREEN}help all{RESET}           - Show complete help for all commands\n")
        
        # Group commands by category
        categories = {}
        for cmd, data in PLUGINS_DB.items():
            cat = data.get("category", "other")
            if cat not in categories:
                categories[cat] = []
            categories[cat].append((cmd, data['description']))
        
        # Display categories with visual separators
        for cat in sorted(categories.keys()):
            print(f"{MAGENTA}{BOLD}▶ {cat.upper()}{RESET}")
            for cmd, desc in sorted(categories[cat]):
                print(format_command(cmd, desc))
            print()
        
        # Footer information
        print(f"{CYAN}{BOLD}{'─' * 82}{RESET}")
        print(f"{GRAY}💡 Tip: Type {GREEN}'help <command>'{RESET}{GRAY} for detailed information about a command.{RESET}")
        print(f"{GRAY}📚 All commands are case-insensitive and support aliases!{RESET}\n")
        print(f"{GRAY}Type 'help all' to see complete documentation for all commands.{RESET}\n")
        return
    
    # Show help for "all" command
    if cmd_name.lower() == "all":
        print(f"\n{CYAN}{BOLD}📖 COMPLETE COMMAND DOCUMENTATION{RESET}")
        print(f"{CYAN}{BOLD}{'═' * 82}{RESET}\n")
        
        for cmd_name_sorted in sorted(PLUGINS_DB.keys()):
            _display_command_help(cmd_name_sorted)
        return
    
    # Show help for specific command
    cmd_name = cmd_name.lower()
    _display_command_help(cmd_name)

def _display_command_help(cmd_name):
    """Display detailed help for a specific command."""
    if cmd_name not in PLUGINS_DB:
        print(f"\n{RED}❌ Error: Command '{cmd_name}' is not yet documented.{RESET}")
        print(f"{GRAY}Available commands: {', '.join(sorted(PLUGINS_DB.keys()))}{RESET}\n")
        return
    
    info = PLUGINS_DB[cmd_name]
    print(f"{CYAN}{BOLD}{'╔' + '═' * 80 + '╗'}{RESET}")
    print(f"{CYAN}{BOLD}║  📚 {info['name'].upper().ljust(75)} ║{RESET}")
    print(f"{CYAN}{BOLD}{'╚' + '═' * 80 + '╝'}{RESET}\n")
    
    # Description
    width = _term_width()
    desc_wrapped = textwrap.fill(info['description'], width=max(40, width - 2))
    print(f"{WHITE}{BOLD}{desc_wrapped}{RESET}\n")
    
    # Aliases if available
    if "aliases" in info and info["aliases"]:
        aliases_str = ", ".join(f"{GREEN}{a}{RESET}" for a in info["aliases"])
        print(f"{YELLOW}🏷️  Aliases:{RESET} {aliases_str}\n")
    
    # Authors if available
    if "authors" in info and info["authors"]:
        authors_str = ", ".join(info["authors"])
        print(f"{YELLOW}✍️  Authors:{RESET} {authors_str}\n")
    
    # Syntax
    print(format_section("💻 Syntax"))
    for syntax_line in info['syntax']:
        syn_wrapped = textwrap.fill(syntax_line, width=max(40, _term_width() - 4), initial_indent="  ", subsequent_indent="  ")
        print(f"{GREEN}{syn_wrapped}{RESET}")
    print()
    
    # Options
    if "options" in info:
        print(format_section("⚙️  Options"))
        for opt in info['options']:
            opt_wrapped = textwrap.fill(opt, width=max(40, _term_width() - 4), initial_indent="  ", subsequent_indent="  ")
            print(f"{BLUE}{opt_wrapped}{RESET}")
        print()
    
    # Features
    if "features" in info:
        print(format_section("✨ Features"))
        for feature in info['features']:
            print(format_tip(feature))
        print()
    
    # Supported types
    if "supported_types" in info:
        print(format_section("📄 Supported Types"))
        types_str = ", ".join(info["supported_types"])
        types_wrapped = textwrap.fill(types_str, width=max(40, _term_width() - 4), initial_indent="  ", subsequent_indent="  ")
        print(f"{types_wrapped}\n")
    
    # Color palette
    if "color_palette" in info:
        print(format_section("🎨 Color Palette"))
        for color in info["color_palette"]:
            print(format_tip(color))
        print()
    
    # Examples
    print(format_section("📋 Examples"))
    for cmd, desc in info['examples']:
        print(format_command(cmd, desc))
    print()
    
    # Shortcuts
    if "shortcuts" in info:
        print(format_section("⌨️  Keyboard Shortcuts"))
        for shortcut in info["shortcuts"]:
            print(format_tip(shortcut))
        print()
    
    # Tips
    if "tips" in info:
        print(format_section("💡 Pro Tips"))
        for tip in info['tips']:
            print(format_tip(tip))
        print()
    
    # Additional information
    if "storage" in info:
        print(f"{GRAY}💾 DATA LOCATION:{RESET} {info['storage']}")
    
    if "output" in info:
        print(f"{GRAY}📤 OUTPUT:{RESET} {info['output']}")
    
    if "output_format" in info:
        print(f"{GRAY}📊 OUTPUT FORMAT:{RESET} {info['output_format']}")
    
    if "pagination" in info:
        print(f"{GRAY}📑 PAGINATION:{RESET} {info['pagination']}")
    
    if "performance" in info:
        print(f"{GRAY}⚡ PERFORMANCE:{RESET} {info['performance']}")
    
    if "automation" in info:
        print(f"{GRAY}🔄 AUTOMATION:{RESET} {info['automation']}")
    
    if "requires" in info:
        print(f"{GRAY}📦 REQUIREMENTS:{RESET} {info['requires']}")
    
    # Available games
    if "available_games" in info:
        print(f"\n{YELLOW}🎮 Available Games:{RESET}")
        for game in info["available_games"]:
            print(f"  {MAGENTA}▸{RESET} {game}")
    
    print(f"\n{CYAN}{BOLD}{'─' * 82}{RESET}\n")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        show_help(sys.argv[1])
    else:
        show_help()
