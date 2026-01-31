@echo off
setlocal enabledelayedexpansion

REM Enable colored output
for /F "tokens=1,2 delims=#" %%a in ('"prompt #$H#$E# & echo on & for %%b in (1) do rem"') do (
  set ESC=%%b
)

REM Define colors
set "RED=%ESC%[91m"
set "GREEN=%ESC%[92m"
set "YELLOW=%ESC%[93m"
set "BLUE=%ESC%[94m"
set "MAGENTA=%ESC%[95m"
set "CYAN=%ESC%[96m"
set "WHITE=%ESC%[97m"
set "RESET=%ESC%[0m"

cls
echo %CYAN%================================================%RESET%
echo %MAGENTA%  Icon Tool - Full Directory Bundle to EXE%RESET%
echo %CYAN%================================================%RESET%
echo.

REM Get current directory
set "CURRENT_DIR=%CD%"
echo %CYAN%Current directory:%RESET% %WHITE%!CURRENT_DIR!%RESET%
echo.

REM Check Python installation
echo %YELLOW%[1/8]%RESET% Checking Python installation...
python --version >nul 2>&1
if errorlevel 1 (
    echo %RED%ERROR: Python is not installed or not in PATH!%RESET%
    echo %YELLOW%Please install Python from https://www.python.org%RESET%
    pause
    exit /b 1
)
python --version
echo %GREEN%✓ Python found%RESET%
echo.

REM Check if required files exist
echo %YELLOW%[2/8]%RESET% Checking required files...
if not exist "cli.py" (
    echo %RED%ERROR: icon_tool_enhanced.py not found!%RESET%
    echo %YELLOW%Make sure the Python script is in the same folder as this batch file.%RESET%
    pause
    exit /b 1
)
echo %GREEN%✓ icon_tool_enhanced.py found%RESET%

REM Check optional files
if exist "icon.ico" (
    echo %GREEN%✓ icon.ico found%RESET%
    set ICON_PARAM=--icon=icon.ico
) else (
    echo %YELLOW%⚠ icon.ico not found - creating without custom icon%RESET%
    set ICON_PARAM=--icon=NONE
)

echo.

REM Scan directory for files and folders
echo %YELLOW%[3/8]%RESET% Scanning directory for files and folders...
echo %CYAN%Building file list...%RESET%
echo.

set FILE_COUNT=0
set FOLDER_COUNT=0
set DATA_PARAMS=

REM Count files and folders
for /f %%i in ('dir /b /a-d 2^>nul ^| find /c /v ""') do set FILE_COUNT=%%i
for /f %%i in ('dir /b /ad 2^>nul ^| find /c /v ""') do set FOLDER_COUNT=%%i

echo %CYAN%Found:%RESET%
echo   %WHITE%Files:%RESET% !FILE_COUNT!
echo   %WHITE%Folders:%RESET% !FOLDER_COUNT!
echo.

REM Display directory structure
echo %YELLOW%Directory structure:%RESET%
tree /F /A | more
echo.

REM Ask for confirmation
echo %YELLOW%Do you want to include ALL files and folders in the EXE?%RESET%
echo %RED%WARNING: This will make the EXE larger!%RESET%
echo.
choice /c YN /n /m "Include all files and folders? (Y/N): "
if errorlevel 2 (
    echo %YELLOW%Cancelled by user.%RESET%
    pause
    exit /b 0
)

echo %GREEN%✓ Including all files and folders%RESET%
echo.

REM Check if pip is available
echo %YELLOW%[4/8]%RESET% Checking pip installation...
python -m pip --version >nul 2>&1
if errorlevel 1 (
    echo %RED%ERROR: pip is not installed!%RESET%
    echo %YELLOW%Please reinstall Python with pip included.%RESET%
    pause
    exit /b 1
)
echo %GREEN%✓ pip found%RESET%
echo.

REM Check/Install PyInstaller
echo %YELLOW%[5/8]%RESET% Checking PyInstaller...
python -m pip show pyinstaller >nul 2>&1
if errorlevel 1 (
    echo %YELLOW%PyInstaller not found. Installing...%RESET%
    python -m pip install pyinstaller
    if errorlevel 1 (
        echo %RED%ERROR: Failed to install PyInstaller!%RESET%
        echo %YELLOW%Check your internet connection and try again.%RESET%
        pause
        exit /b 1
    )
    echo %GREEN%✓ PyInstaller installed successfully%RESET%
) else (
    echo %GREEN%✓ PyInstaller already installed%RESET%
)
echo.

REM Choose build mode
echo %YELLOW%[6/8]%RESET% Select build mode:
echo   %CYAN%[1]%RESET% Without console window (clean, for end users)
echo   %CYAN%[2]%RESET% With console window (for debugging)
echo.

choice /c 12 /n /m "Select option (1 or 2): "

if errorlevel 2 (
    set WINDOWED_PARAM=
    echo %GREEN%✓ Creating with console window (debug mode)%RESET%
) else (
    set WINDOWED_PARAM=--windowed
    echo %GREEN%✓ Creating without console window (release mode)%RESET%
)

echo.

REM Clean previous build
echo %YELLOW%[7/8]%RESET% Cleaning previous builds...
if exist "build" (
    rmdir /s /q "build" 2>nul
    echo %GREEN%✓ Removed build folder%RESET%
)
if exist "dist" (
    rmdir /s /q "dist" 2>nul
    echo %GREEN%✓ Removed dist folder%RESET%
)
if exist "IconTool.spec" (
    del /q "IconTool.spec" 2>nul
    echo %GREEN%✓ Removed spec file%RESET%
)
echo.

REM Build --add-data parameters for all files and folders
echo %YELLOW%[8/8]%RESET% Preparing bundle parameters...
echo %CYAN%Adding files and folders to bundle...%RESET%

REM Create temporary file list
set TEMP_LIST=%TEMP%\pyinstaller_files.txt
if exist "%TEMP_LIST%" del "%TEMP_LIST%"

REM Add all files (excluding build artifacts and scripts)
for %%f in (*) do (
    set "filename=%%~nxf"
    if not "!filename!"=="pytoexe.bat" (
        if not "!filename!"=="pytoexe_full.bat" (
            if not "!filename!"=="icon_tool_enhanced.py" (
                if not "!filename:~-5!"==".spec" (
                    echo   %GREEN%+%RESET% %%~nxf
                    set DATA_PARAMS=!DATA_PARAMS! --add-data "%%~nxf;."
                )
            )
        )
    )
)

REM Add all folders (excluding build artifacts)
for /d %%d in (*) do (
    set "foldername=%%~nxd"
    if not "!foldername!"=="build" (
        if not "!foldername!"=="dist" (
            if not "!foldername!"=="__pycache__" (
                echo   %GREEN%+%RESET% %%~nxd\ (folder)
                set DATA_PARAMS=!DATA_PARAMS! --add-data "%%~nxd;%%~nxd"
            )
        )
    )
)

echo.
echo %CYAN%Bundle prepared!%RESET%
echo.

REM Create executable
echo %CYAN%Converting to executable...%RESET%
echo %YELLOW%This may take several minutes...%RESET%
echo.

pyinstaller --onefile %WINDOWED_PARAM% --name="IconTool" %ICON_PARAM% %DATA_PARAMS% icon_tool_enhanced.py

if errorlevel 1 (
    echo.
    echo %RED%================================================%RESET%
    echo %RED%ERROR: Conversion failed!%RESET%
    echo %RED%================================================%RESET%
    echo.
    echo %YELLOW%Common issues:%RESET%
    echo   - Missing dependencies (Pillow/PIL)
    echo   - Corrupted Python installation
    echo   - Antivirus blocking PyInstaller
    echo   - Too many files (try excluding some)
    echo.
    echo %YELLOW%Try installing dependencies:%RESET%
    echo   python -m pip install Pillow
    echo.
    pause
    exit /b 1
)

echo.
echo %GREEN%================================================%RESET%
echo %GREEN%         Conversion Successful!%RESET%
echo %GREEN%================================================%RESET%
echo.
echo %CYAN%Executable location:%RESET% %WHITE%dist\IconTool.exe%RESET%
echo.
echo %YELLOW%File size:%RESET%
for %%A in ("dist\IconTool.exe") do (
    set SIZE=%%~zA
    set /a SIZE_KB=!SIZE!/1024
    set /a SIZE_MB=!SIZE_KB!/1024
    echo   %WHITE%!SIZE! bytes (!SIZE_KB! KB / !SIZE_MB! MB)%RESET%
)
echo.
echo %CYAN%Bundled contents:%RESET%
echo   %WHITE%All files and folders from:%RESET% !CURRENT_DIR!
echo.
echo %GREEN%You can now distribute IconTool.exe with all resources!%RESET%
echo %CYAN%================================================%RESET%
echo.

REM Open dist folder
echo %YELLOW%Do you want to open the dist folder? (Y/N)%RESET%
choice /c YN /n /m ""
if errorlevel 2 (
    echo %CYAN%Done! Press any key to exit...%RESET%
) else (
    explorer "dist"
    echo %GREEN%✓ Opening dist folder...%RESET%
)

pause
