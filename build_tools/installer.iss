; Script de Inno Setup - Sistema de Gestión Comercial
; Requiere Inno Setup 6: https://jrsoftware.org/isinfo.php

[Setup]
AppName=Sistema de Gestión Comercial
AppVersion=3.0.3
AppPublisher=Miguel Ángel Saavedra
DefaultDirName={localappdata}\SistemaGestion
DefaultGroupName=Sistema de Gestión Comercial
OutputDir=.
OutputBaseFilename=Instalador_SistemaGestion_v3.0.3
Compression=lzma
SolidCompression=yes
DisableProgramGroupPage=yes
PrivilegesRequired=lowest

[Languages]
Name: "spanish"; MessagesFile: "compiler:Languages\Spanish.isl"

[Tasks]
Name: "desktopicon"; Description: "Crear acceso directo en el escritorio"; GroupDescription: "Iconos adicionales:"

[Files]
Source: "dist\SistemaGestion\*"; DestDir: "{app}"; Flags: ignoreversion recursesubdirs

[Icons]
Name: "{group}\Sistema de Gestión Comercial"; Filename: "{app}\SistemaGestion.exe"
Name: "{group}\Desinstalar"; Filename: "{uninstallexe}"
Name: "{commondesktop}\Sistema de Gestión Comercial"; Filename: "{app}\SistemaGestion.exe"; Tasks: desktopicon

[Run]
Filename: "{app}\SistemaGestion.exe"; Description: "Ejecutar ahora"; Flags: nowait postinstall skipifsilent
