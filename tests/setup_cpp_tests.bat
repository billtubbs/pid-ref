@echo off
REM Setup script for C++ tests on Windows

echo Setting up C++ PID Controller Tests
echo ====================================
echo.

REM Check if catch.hpp exists
if not exist "catch.hpp" (
    echo Downloading Catch2 v2.13.10...

    REM Try to download using PowerShell
    powershell -Command "& {Invoke-WebRequest -Uri 'https://github.com/catchorg/Catch2/releases/download/v2.13.10/catch.hpp' -OutFile 'catch.hpp'}"

    if errorlevel 1 (
        echo Error: Failed to download catch.hpp
        echo Please download manually from:
        echo https://github.com/catchorg/Catch2/releases/download/v2.13.10/catch.hpp
        pause
        exit /b 1
    )

    echo [OK] Downloaded catch.hpp
) else (
    echo [OK] catch.hpp already exists
)

REM Check if data directory exists
if not exist "data" (
    echo.
    echo Generating I/O data files...
    cd ..
    python tests\generate_io_data.py
    cd tests
    echo [OK] Generated I/O data files
) else (
    echo [OK] I/O data files exist
)

echo.
echo Setup complete!
echo.
echo Note: This script only sets up test data.
echo For Windows, you need to:
echo   1. Install MinGW or use WSL for make/g++
echo   2. Or use Visual Studio / CMake to build
echo.
echo See tests/CPP_SETUP.md for more details.
echo.
pause
