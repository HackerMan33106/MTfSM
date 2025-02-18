@echo off
chcp 1251 >nul

cd /d "%~dp0"

:: ���������, ���������� �� PyInstaller
pyinstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller �� ������, �������������...
    pip install pyinstaller
) else (
    echo PyInstaller ��� ����������.
)

:: ���������� main.py
echo ���������� main.py...
pyinstaller --onefile --distpath "%~dp0\build" --workpath "%~dp0\temp" --specpath "%~dp0\spec" main.py

:: ���������, ��������������� �� main.exe
if exist "%~dp0\build\main.exe" (
    echo ����������� main.exe � ������� �����...
    move /Y "%~dp0\build\main.exe" "%~dp0\main.exe"
) else (
    echo ������: main.exe �� ������!
    pause
    exit /b 1
)

:: �������� ��������� �����
echo �������� ��������� ������...
rd /s /q "%~dp0\build"
rd /s /q "%~dp0\spec"
rd /s /q "%~dp0\temp"

echo ���������� ���������! ������� ����� ������� ��� ������...
pause >nul
exit