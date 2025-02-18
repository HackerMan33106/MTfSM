@echo off
chcp 1251 >nul

cd /d "%~dp0"

:: Проверяем, установлен ли PyInstaller
pyinstaller --version >nul 2>&1
if %errorlevel% neq 0 (
    echo PyInstaller не найден, устанавливаем...
    pip install pyinstaller
) else (
    echo PyInstaller уже установлен.
)

:: Компиляция main.py
echo Компиляция main.py...
pyinstaller --onefile --distpath "%~dp0\build" --workpath "%~dp0\temp" --specpath "%~dp0\spec" main.py

:: Проверяем, скомпилировался ли main.exe
if exist "%~dp0\build\main.exe" (
    echo Перемещение main.exe в текущую папку...
    move /Y "%~dp0\build\main.exe" "%~dp0\main.exe"
) else (
    echo Ошибка: main.exe не найден!
    pause
    exit /b 1
)

:: Удаление временных папок
echo Удаление временных файлов...
rd /s /q "%~dp0\build"
rd /s /q "%~dp0\spec"
rd /s /q "%~dp0\temp"

echo Компиляция завершена! Нажмите любую клавишу для выхода...
pause >nul
exit