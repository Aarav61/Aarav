#define MyAppName "PC Shutdown Timer"
#define MyAppVersion "1.0.0"
#define MyAppPublisher "Aarav61"
#define MyAppExeName "PC-Shutdown-Timer.exe"

[Setup]
AppId={{7E7E0F75-8C1A-4D4D-9E7D-3C6D8B4B8B21}
AppName={#MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
DefaultDirName={autopf}\PC Shutdown Timer
DefaultGroupName={#MyAppName}
OutputDir=installer
OutputBaseFilename=PC-Shutdown-Timer-Setup
Compression=lzma
SolidCompression=yes
WizardStyle=modern
PrivilegesRequired=lowest
Uninstallable=yes

[Files]
Source: "dist\PC-Shutdown-Timer.exe"; DestDir: "{app}"; Flags: ignoreversion

[Icons]
Name: "{autoprograms}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{autodesktop}\{#MyAppName}"; Filename: "{app}\{#MyAppExeName}"

[UninstallDelete]
Type: filesandordirs; Name: "{app}"
