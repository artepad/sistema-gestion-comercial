@echo off
echo ========================================
echo  Build: Sistema de Gestion Comercial
echo  Version 3.0.5
echo ========================================
echo.

cd /d "%~dp0.."

echo [1/2] Generando ejecutable con PyInstaller...
.\venv\Scripts\python.exe -m PyInstaller build_tools\app.spec --distpath build_tools\dist --workpath build_tools\build --noconfirm

if errorlevel 1 (
    echo.
    echo ERROR: Fallo PyInstaller. Revisa los mensajes anteriores.
    pause
    exit /b 1
)

echo.
echo [2/2] Creando instalador con Inno Setup...
"C:\Program Files (x86)\Inno Setup 6\ISCC.exe" build_tools\installer.iss 2>nul
if errorlevel 1 (
    "C:\Program Files\Inno Setup 7\ISCC.exe" build_tools\installer.iss 2>nul
    if errorlevel 1 (
        echo.
        echo ERROR: No se encontro Inno Setup. Verifica la instalacion.
        echo Rutas buscadas:
        echo   C:\Program Files (x86)\Inno Setup 6\ISCC.exe
        echo   C:\Program Files\Inno Setup 7\ISCC.exe
        pause
        exit /b 1
    )
)

echo.
echo ========================================
echo  BUILD COMPLETADO EXITOSAMENTE
echo ========================================
echo.
echo  Instalador generado en:
echo  build_tools\Instalador_SistemaGestion_v3.0.5.exe
echo.
pause
