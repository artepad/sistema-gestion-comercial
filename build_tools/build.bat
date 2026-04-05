@echo off
echo ========================================
echo  Build: Sistema de Gestion Comercial
echo ========================================
echo.

cd /d "%~dp0.."

echo [1/2] Generando ejecutable con PyInstaller...
.\venv\Scripts\pyinstaller.exe build_tools\app.spec --distpath build_tools\dist --workpath build_tools\build --noconfirm

if errorlevel 1 (
    echo.
    echo ERROR: Fallo PyInstaller. Revisa los mensajes anteriores.
    pause
    exit /b 1
)

echo.
echo [2/2] Ejecutable generado en: build_tools\dist\SistemaGestion\
echo.
echo Para crear el instalador .exe:
echo   1. Abre Inno Setup
echo   2. File ^> Open ^> build_tools\installer.iss
echo   3. Build ^> Compile
echo   4. El instalador quedara en: build_tools\Instalador_SistemaGestion_v3.0.0.exe
echo.
pause
