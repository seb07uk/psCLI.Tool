@echo off
chcp 65001 >nul

:: Checking administrator privileges
net session >nul 2>&1
if %errorlevel% neq 0 (
    echo.
    echo Ten skrypt wymaga uprawnien administratora.
    echo Uruchamianie ponownie z uprawnieniami admina...
    echo.
    powershell -Command "Start-Process '%~f0' -Verb RunAs"
    exit /b
)

:: Enable ANSI support
reg query HKCU\Console /v VirtualTerminalLevel >nul 2>&1
if %errorlevel% neq 0 (
    reg add HKCU\Console /f /v VirtualTerminalLevel /t REG_DWORD /d 1 >nul
)

:: Generate ESC
for /f "delims=" %%a in ('echo prompt $E^| cmd') do set "ESC=%%a"

:: Colors
set "BLUE=%ESC%[34m"
set "CYAN=%ESC%[36m"
set "GREEN=%ESC%[32m"
set "YELLOW=%ESC%[33m"
set "RED=%ESC%[31m"
set "RESET=%ESC%[0m"

:: ============================
:: LANGUAGE SELECTION
:: ============================

:LANGUAGE
cls
echo.
echo  ▄█       █▄   ▄█  ███▄▄▄▄   ████████▄   ▄██████▄   ▄█      █▄     ▄████████         
echo  ███      ███ ███  ███▀▀▀██▄ ███   ▀███ ███    ███ ███      ███   ███    ███  
echo  ███      ███ ███▌ ███   ███ ███    ███ ███    ███ ███      ███   ███    █▀   
echo  ███      ███ ███▌ ███   ███ ███    ███ ███    ███ ███      ███   ███         
echo  ███      ███ ███▌ ███   ███ ███    ███ ███    ███ ███      ███ ▀███████████  
echo  ███      ███ ███  ███   ███ ███    ███ ███    ███ ███      ███           ███  
echo  ███ ▄█▄ ███ ███  ███   ███ ███   ▄███ ███    ███ ███ ▄█▄ ███    ▄█    ███  
echo   ▀███▀███▀  █▀    ▀█   █▀  ████████▀   ▀██████▀   ▀███▀███▀   ▄████████▀   © 2026 polsoft.ITS™ London
echo.
echo      ▄████████  ▄████████     ███      ▄█   ▄█    █▄     ▄████████     ███      ▄█   ▄██████▄  ███▄▄▄▄
echo     ███    ███ ███    ███ ▀█████████▄ ███  ███    ███   ███    ███ ▀█████████▄ ███  ███    ███ ███▀▀▀██▄
echo     ███    ███ ███    █▀     ▀███▀▀██ ███▌ ███    ███   ███    ███    ▀███▀▀██ ███▌ ███    ███ ███   ███
echo     ███    ███ ███            ███   ▀ ███▌ ███    ███   ███    ███     ███   ▀ ███▌ ███    ███ ███   ███
echo   ▀███████████ ███            ███     ███▌ ███    ███ ▀███████████     ███     ███▌ ███    ███ ███   ███
echo     ███    ███ ███    █▄      ███     ███  ███    ███   ███    ███     ███     ███  ███    ███ ███   ███
echo     ███    ███ ███    ███     ███     ███  ███    ███   ███    ███     ███     ███  ███    ███ ███   ███
echo     ███    █▀  ████████▀     ▄████▀   █▀    ▀██████▀    ███    █▀     ▄████▀    █▀   ▀██████▀   ▀█   █▀
echo.
echo      ███      ▄██████▄   ▄██████▄   ▄█          ▄████████              
echo  ▀█████████▄ ███    ███ ███    ███ ███         ███    ███              ┌───────────────────────────────┐
echo     ▀███▀▀██ ███    ███ ███    ███ ███         ███    █▀               │        Select language        │
echo      ███   ▀ ███    ███ ███    ███ ███         ███                     ├───────────────────────────────┤
echo      ███     ███    ███ ███    ███ ███       ▀███████████              │  %GREEN%1%RESET% - English                  │
echo      ███     ███    ███ ███    ███ ███                ███              ├───────────────────────────────┤
echo      ███     ███    ███ ███    ███ ███▌    ▄    ▄█    ███              │  %GREEN%2%RESET% - Polski                   │
echo     ▄████▀    ▀██████▀   ▀██████▀  █████▄▄██  ▄████████▀               ├───────────────────────────────┤
echo                                    ▀                                   │  %YELLOW%3%RESET% - Help / Pomoc             │
echo                                                                        └───────────────────────────────┘
choice /c 123 /n
set "lang=%errorlevel%"

if %lang%==1 goto MENU_EN
if %lang%==2 goto MENU_PL
if %lang%==3 (
    start "" "%~dp0help.html"
    goto LANGUAGE
)

goto LANGUAGE


:: ============================================================
:: =======================  ENGLISH MENU  ======================
:: ============================================================

:MENU_EN
cls
echo.
echo(
ECHO  ©2026 WinTool's - Windows Activation Tools by Sebastian Januchowski.
echo.
echo      dMMMMb  .aMMMb  dMP    .dMMMb  .aMMMb  dMMMMMP dMMMMMMP       dMP dMMMMMMP .dMMMb ™
echo     dMP.dMP dMP"dMP dMP    dMP" VP dMP"dMP dMP        dMP        amr    dMP   dMP"  SJ
echo    dMMMMP" dMP dMP dMP     VMMMb  dMP dMP dMMMP      dMP        dMP    dMP    VMMMb
echo   dMP     dMP.aMP dMP    dP .dMP dMP.aMP dMP        dMP  amr  dMP    dMP   dP .dMP
echo  dMP      VMMMP" dMMMMMP VMMMP"  VMMMP" dMP        dMP  dMP  dMP    dMP    VMMMP"
echo(
echo %BLUE%===========================%RESET%
echo %CYAN%        LICENSE TOOLS%RESET%
echo %BLUE%===========================%RESET%
echo.
echo  %GREEN%1%RESET% - Activation status
echo  %GREEN%2%RESET% - Basic license info
echo  %GREEN%3%RESET% - Detailed license info
echo  %GREEN%4%RESET% - BIOS/UEFI product key
echo  %GREEN%5%RESET% - Restart licensing service
echo  %GREEN%6%RESET% - Enter product key
echo  %GREEN%7%RESET% - Activate system
echo  %GREEN%8%RESET% - Help
echo  %YELLOW%9%RESET% - Exit
echo.
echo Choose an option:

choice /c 123456789 /n
set "wybor=%errorlevel%"

if %wybor%==1 goto AKTYWACJA_STATUS_EN
if %wybor%==2 goto INFO_BASIC_EN
if %wybor%==3 goto INFO_FULL_EN
if %wybor%==4 goto BIOSKEY_EN
if %wybor%==5 goto RESTART_EN
if %wybor%==6 goto WPROWADZ_KLUCZ_EN
if %wybor%==7 goto AKTYWACJA_EN
if %wybor%==8 goto HELP_EN
if %wybor%==9 exit

goto MENU_EN


:: ============================================================
:: =======================  POLSKIE MENU  ======================
:: ============================================================

:MENU_PL
cls
echo.
echo(
ECHO  ©2026 WinTool's - Windows Activation Tools by Sebastian Januchowski.
echo.
echo      dMMMMb  .aMMMb  dMP    .dMMMb  .aMMMb  dMMMMMP dMMMMMMP      dMP dMMMMMMP .dMMMb ™
echo     dMP.dMP dMP"dMP dMP    dMP" VP dMP"dMP dMP        dMP        amr    dMP   dMP" SJ
echo    dMMMMP" dMP dMP dMP     VMMMb  dMP dMP dMMMP      dMP        dMP    dMP    VMMMb
echo   dMP     dMP.aMP dMP    dP .dMP dMP.aMP dMP        dMP  amr  dMP    dMP   dP .dMP
echo  dMP      VMMMP" dMMMMMP VMMMP"  VMMMP" dMP        dMP  dMP  dMP    dMP    VMMMP"
echo(
echo %BLUE%===========================%RESET%
echo %CYAN%    NARZĘDZIA LICENCYJNE%RESET%
echo %BLUE%===========================%RESET%
echo.
echo  %GREEN%1%RESET% - Status aktywacji
echo  %GREEN%2%RESET% - Podstawowe info licencji
echo  %GREEN%3%RESET% - Szczegółowe info licencji
echo  %GREEN%4%RESET% - Klucz produktu BIOS/UEFI
echo  %GREEN%5%RESET% - Restart usługi licencjonowania
echo  %GREEN%6%RESET% - Wprowadź klucz produktu
echo  %GREEN%7%RESET% - Aktywuj system
echo  %GREEN%8%RESET% - Pomoc
echo  %YELLOW%9%RESET% - Wyjście
echo.
echo Wybierz opcję:

choice /c 123456789 /n
set "wybor=%errorlevel%"

if %wybor%==1 goto AKTYWACJA_STATUS
if %wybor%==2 goto INFO_BASIC
if %wybor%==3 goto INFO_FULL
if %wybor%==4 goto BIOSKEY
if %wybor%==5 goto RESTART
if %wybor%==6 goto WPROWADZ_KLUCZ
if %wybor%==7 goto AKTYWACJA
if %wybor%==8 goto POMOC
if %wybor%==9 exit

goto MENU_PL


:: ============================================================
:: ==========  TWOJE ORYGINALNE FUNKCJE — POLSKIE  ============
:: ============================================================

:WPROWADZ_KLUCZ
cls
echo %CYAN%============================================%RESET%
echo %CYAN%        WPROWADZANIE KLUCZA PRODUKTU%RESET%
echo %CYAN%============================================%RESET%
echo.
set /p KEY=Podaj klucz produktu (XXXXX-XXXXX-XXXXX-XXXXX-XXXXX): 
echo.
slmgr /ipk %KEY%
echo.
echo %GREEN%Klucz został zainstalowany.%RESET%
echo.
pause
goto MENU_PL

:AKTYWACJA_STATUS
cls
echo %CYAN%STATUS AKTYWACJI%RESET%
echo.
slmgr /xpr
echo.
goto MENU_PL

:AKTYWACJA
cls
echo %CYAN%============================================%RESET%
echo %CYAN%               AKTYWACJA SYSTEMU%RESET%
echo %CYAN%============================================%RESET%
echo.
slmgr /ato
echo.
echo %GREEN%System został aktywowany (jeśli klucz jest poprawny).%RESET%
echo.
goto MENU_PL

:INFO_FULL
cls
echo %CYAN%SZCZEGÓŁOWE INFORMACJE O LICENCJI%RESET%
echo.
slmgr /dlv
echo.
goto MENU_PL

:INFO_BASIC
cls
echo %CYAN%PODSTAWOWE INFORMACJE O LICENCJI%RESET%
echo.
slmgr /dli
echo.
goto MENU_PL

:BIOSKEY
cls
echo %CYAN%KLUCZ PRODUKTU BIOS/UEFI%RESET%
echo.
wmic path softwarelicensingservice get OA3xOriginalProductKey
echo.
pause
goto MENU_PL

:RESTART
cls
echo %YELLOW%RESTARTOWANIE USŁUGI LICENCJONOWANIA...%RESET%
echo.
net stop sppsvc
net start sppsvc
echo.
echo %GREEN%Usługa została zrestartowana.%RESET%
echo.
pause
goto MENU_PL

:POMOC
cls
echo %BLUE%===========================%RESET%
echo %CYAN%            POMOC%RESET%
echo %BLUE%===========================%RESET%
echo.
echo %GREEN%1 - Status aktywacji%RESET%
echo Pokazuje, czy system Windows jest aktywowany.
echo.
echo %GREEN%2 - Podstawowe informacje o licencji%RESET%
echo Skrócony raport licencyjny.
echo.
echo %GREEN%3 - Szczegółowe informacje o licencji%RESET%
echo Pełny raport licencyjny.
echo.
echo %GREEN%4 - Klucz produktu BIOS/UEFI%RESET%
echo Odczytuje klucz OEM zapisany w firmware.
echo.
echo %GREEN%5 - Restart usługi licencjonowania%RESET%
echo Restartuje usługę sppsvc.
echo.
echo %GREEN%6 - Wprowadź klucz produktu%RESET%
echo Instalacja nowego klucza Windows.
echo.
echo %GREEN%7 - Aktywacja systemu%RESET%
echo Próba aktywacji Windows.
echo.
echo %GREEN%8 - Pomoc%RESET%
echo Wyświetla ten ekran.
echo.
echo %YELLOW%9 - Wyjście%RESET%
echo.
echo %BLUE%===========================%RESET%
echo %CYAN%      INFORMACJE O AUTORZE%RESET%
echo %BLUE%===========================%RESET%
echo Sebastian Januchowski
echo polsoft.its@fastservice.com
echo https://github.com/seb07uk
echo © 2026 polsoft.ITS London
echo.
pause
goto MENU_PL


:: ============================================================
:: ==========  TWOJE ORYGINALNE FUNKCJE — ENGLISH  ============
:: ============================================================

:WPROWADZ_KLUCZ_EN
cls
echo %CYAN%============================================%RESET%
echo %CYAN%        ENTER PRODUCT KEY%RESET%
echo %CYAN%============================================%RESET%
echo.
set /p KEY=Enter product key (XXXXX-XXXXX-XXXXX-XXXXX-XXXXX): 
echo.
slmgr /ipk %KEY%
echo.
echo %GREEN%The key has been installed.%RESET%
echo.
pause
goto MENU_EN

:AKTYWACJA_STATUS_EN
cls
echo %CYAN%ACTIVATION STATUS%RESET%
echo.
slmgr /xpr
echo.
goto MENU_EN

:AKTYWACJA_EN
cls
echo %CYAN%============================================%RESET%
echo %CYAN%              SYSTEM ACTIVATION%RESET%
echo %CYAN%============================================%RESET%
echo.
slmgr /ato
echo.
echo %GREEN%The system has been activated (if the key is valid).%RESET%
echo.
goto MENU_EN

:INFO_FULL_EN
cls
echo %CYAN%DETAILED LICENSE INFORMATION%RESET%
echo.
slmgr /dlv
echo.
goto MENU_EN

:INFO_BASIC_EN
cls
echo %CYAN%BASIC LICENSE INFORMATION%RESET%
echo.
slmgr /dli
echo.
goto MENU_EN

:BIOSKEY_EN
cls
echo %CYAN%BIOS/UEFI PRODUCT KEY%RESET%
echo.
wmic path softwarelicensingservice get OA3xOriginalProductKey
echo.
pause
goto MENU_EN

:RESTART_EN
cls
echo %YELLOW%RESTARTING LICENSING SERVICE...%RESET%
echo.
net stop sppsvc
net start sppsvc
echo.
echo %GREEN%The service has been restarted.%RESET%
echo.
pause
goto MENU_EN

:HELP_EN
cls
echo %BLUE%===========================%RESET%
echo %CYAN%              HELP%RESET%
echo %BLUE%===========================%RESET%
echo.
echo %GREEN%1 - Activation status%RESET%
echo Shows whether Windows is activated.
echo.
echo %GREEN%2 - Basic license information%RESET%
echo Displays a short license report.
echo.
echo %GREEN%3 - Detailed license information%RESET%
echo Displays a full license report.
echo.
echo %GREEN%4 - BIOS/UEFI product key%RESET%
echo Reads the OEM key stored in firmware.
echo.
echo %GREEN%5 - Restart licensing service%RESET%
echo Restarts the sppsvc service.
echo.
echo %GREEN%6 - Enter product key%RESET%
echo Installs a new Windows product key.
echo.
echo %GREEN%7 - Activate system%RESET%
echo Attempts to activate Windows.
echo.
echo %GREEN%8 - Help%RESET%
echo Displays this screen.
echo.
echo %YELLOW%9 - Exit%RESET%
echo.
echo %BLUE%===========================%RESET%
echo %CYAN%        AUTHOR INFO%RESET%
echo %BLUE%===========================%RESET%
echo Sebastian Januchowski
echo polsoft.its@fastservice.com
echo https://github.com/seb07uk
echo © 2026 polsoft.ITS London
echo.
pause
goto MENU_EN