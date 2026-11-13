[Setup]
AppName=Restaurante Moscato
AppVersion=1.0
AppPublisher=Moscato Software
DefaultDirName={autopf}\Restaurante Moscato
DefaultGroupName=Restaurante Moscato
; La carpeta donde se guardará tu Instalador final
OutputDir=C:\Users\manue\proyectos\Proyecto_v.3\Instalador
OutputBaseFilename=Instalar_Moscato
SetupIconFile=C:\Users\manue\proyectos\Proyecto_v.3\moscato_logo.ico
Compression=lzma
SolidCompression=yes
; Pide permisos de administrador sólo al instalar
PrivilegesRequired=admin

[Files]
; Ruta de tu ejecutable generado por PyInstaller
Source: "C:\Users\manue\proyectos\Proyecto_v.3\dist\MoscatoSystem.exe"; DestDir: "{app}"; Flags: ignoreversion

[Dirs]
; Damos permisos de modificación a la carpeta para que el programa pueda crear su db_config.json, app.log y la carpeta de imágenes del menú
Name: "{app}"; Permissions: users-modify

[Icons]
Name: "{group}\Restaurante Moscato"; Filename: "{app}\MoscatoSystem.exe"
Name: "{autodesktop}\Restaurante Moscato"; Filename: "{app}\MoscatoSystem.exe"; Tasks: desktopicon

[Tasks]
Name: "desktopicon"; Description: "Crear un icono en el escritorio"; GroupDescription: "Accesos directos:"

Name: "desktopicon"; Description: "Crear un icono en el escritorio"; GroupDescription: "Accesos directos:"