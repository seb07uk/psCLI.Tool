@echo off
setlocal

:: Ustawienie ścieżki do systemowego folderu TEMP
set "TEMP_INSTALLER=%TEMP%\dxwebsetup.exe"

echo [1/3] Pobieranie instalatora DirectX do folderu TEMP...
powershell -Command "Invoke-WebRequest -Uri 'https://download.microsoft.com/download/1/7/1/1718CCC4-6315-4D8E-9543-8E28A4E18C4C/dxwebsetup.exe' -OutFile '%TEMP_INSTALLER%'"

if not exist "%TEMP_INSTALLER%" (
    echo [BLAD] Nie udalo sie pobrac pliku do %TEMP%. Sprawdz polaczenie.
    pause
    exit /b
)

echo [2/3] Instalacja DirectX w toku (tryb cichy)...
:: Uruchomienie z uprawnieniami instalatora
start /wait "" "%TEMP_INSTALLER%" /Q

echo [3/3] Czyszczenie pliku tymczasowego...
del /f /q "%TEMP_INSTALLER%"

echo.
echo Operacja zakonczona sukcesem. System DirectX zostal zaktualizowany.
pause