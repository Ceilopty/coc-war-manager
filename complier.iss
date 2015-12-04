#define MyAppName "COC Clan War Manager"
#define MyAppVersion "1.2.0"
#define MyAppPublisher "Ceilopty"
#define MyAppURL "http://www.ceilopty.com/"
#define MyAppExeName "COC.exe" 

[Setup]
; NOTE: The value of AppId uniquely identifies this application.
; Do not use the same AppId value in installers for other applications.
; (To generate a new GUID, click Tools | Generate GUID inside the IDE.)
AppId={{9D77BFD8-A90F-4C87-A2AF-8FFDB7308755}
AppName={cm:MyAppName}
AppVersion={#MyAppVersion}
AppPublisher={#MyAppPublisher}
AppPublisherURL={#MyAppURL}
AppSupportURL={#MyAppURL}
AppUpdatesURL={#MyAppURL}
DefaultDirName={pf}\{#MyAppName}
DefaultGroupName={cm:MyAppName}
AllowNoIcons=yes
AlwaysShowComponentsList=no
ChangesAssociations=yes
InfoBeforeFile=License\Regulation.txt
InfoAfterFile=License\ReadMe.txt
OutputDir=.
OutputBaseFilename={#MyAppName}{#MyAppVersion} setup
SetupIconFile=data\Clan.ico
Password=CEILOPTY
Compression=lzma
SolidCompression=yes

[Languages]
Name: "english"; MessagesFile: "compiler:Default.isl"; LicenseFile:"License\License.txt"
Name: "japanese"; MessagesFile: "compiler:Languages\Japanese.isl"; LicenseFile:"License\License.txt"
Name: "chinese"; MessagesFile: "compiler:Languages\ChineseSimplified.isl"; LicenseFile:"License\License_cn.txt"

[Tasks]
Name: "desktopicon"; Description: "{cm:CreateDesktopIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked
Name: "quicklaunchicon"; Description: "{cm:CreateQuickLaunchIcon}"; GroupDescription: "{cm:AdditionalIcons}"; Flags: unchecked; OnlyBelowVersion: 0,6.1

[CustomMessages]
english.MyAppName=COC Clan War Manager
english.MainFiles=Main Files
english.SaveFiles=Saved War Data
english.FullInstallation=Full Installation
english.CompactInstallation=Compact Installation
english.CustomInstallation=Custom Installation
english.SourceCode=Source Code
japanese.MyAppName=COCクラン対戦管理
japanese.MainFiles=主要
japanese.SaveFiles=セーブデータ
japanese.FullInstallation=フルインストール
japanese.CompactInstallation=コンパクトインストール
japanese.CustomInstallation=カスタムインストール
japanese.SourceCode=ソースコード
chinese.MyAppName=COC对战管理
chinese.MainFiles=主程序
chinese.SaveFiles=存档
chinese.FullInstallation=完全安装
chinese.CompactInstallation=精简安装
chinese.CustomInstallation=自定义安装
chinese.SourceCode=源代码

[Dirs]
Name: "{app}\save"; Components: not save
         
[Types]
Name: "full"; Description: "{cm:FullInstallation}"
Name: "compact"; Description: "{cm:CompactInstallation}"
Name: "custom"; Description: "{cm:CustomInstallation}"; Flags: iscustom

[Components]
Name: "main"; Description: "{cm:MainFiles}"; Types: full compact custom; Flags: fixed
Name: "save"; Description: "{cm:SaveFiles}"; Types: full
Name: "code"; Description: "{cm:SourceCode}"; Types: full

[Files]
;Source: "Tools\msvcr100.dll_x86\msvcr100.dll"; DestDir: "{sys}"; Components: main; Flags: 32bit onlyifdoesntexist uninsneveruninstall
Source: "build\exe.win32-3.4\COC.exe"; DestDir: "{app}"; Components: main; Flags: ignoreversion
Source: "data\Clan"; DestDir: "{app}\data"; Components: main; Flags: ignoreversion
Source: "data\Clan.ico"; DestDir: "{app}\data"; Components: main; Flags: ignoreversion
Source: "data\member"; DestDir: "{app}\data"; Components: main; Flags: ignoreversion
Source: "data\member.ini"; DestDir: "{app}\data"; Components: main; Flags: ignoreversion
Source: "data\config.ini"; DestDir: "{app}\data"; Components: main; Flags: ignoreversion
Source: "save\data.cld"; DestDir: "{app}\save"; Components: save; Flags: ignoreversion 
Source: "save\history.clh"; DestDir: "{app}\save"; Components: save; Flags: ignoreversion 
Source: "Clan_py3.py"; DestDir: "{app}\{cm:SourceCode}\COC"; Components: code; Flags: ignoreversion
Source: "__init__.py"; DestDir: "{app}\{cm:SourceCode}\COC"; Components: code; Flags: ignoreversion
Source: "MultiCall.py"; DestDir: "{app}\{cm:SourceCode}\COC"; Components: code; Flags: ignoreversion
Source: "my_class.py"; DestDir: "{app}\{cm:SourceCode}\COC"; Components: code; Flags: ignoreversion
Source: "my_coding.py"; DestDir: "{app}\{cm:SourceCode}\COC"; Components: code; Flags: ignoreversion
Source: "my_constant.py"; DestDir: "{app}\{cm:SourceCode}\COC"; Components: code; Flags: ignoreversion
Source: "my_font.py"; DestDir: "{app}\{cm:SourceCode}\COC"; Components: code; Flags: ignoreversion
Source: "my_input.py"; DestDir: "{app}\{cm:SourceCode}\COC"; Components: code; Flags: ignoreversion
Source: "my_io.py"; DestDir: "{app}\{cm:SourceCode}\COC"; Components: code; Flags: ignoreversion
Source: "my_menu.py"; DestDir: "{app}\{cm:SourceCode}\COC"; Components: code; Flags: ignoreversion
Source: "my_pack.py"; DestDir: "{app}\{cm:SourceCode}\COC"; Components: code; Flags: ignoreversion
Source: "my_play.py"; DestDir: "{app}\{cm:SourceCode}\COC"; Components: code; Flags: ignoreversion
Source: "my_widget.py"; DestDir: "{app}\{cm:SourceCode}\COC"; Components: code; Flags: ignoreversion
Source: "setup.py"; DestDir: "{app}\{cm:SourceCode}\COC"; Components: code; Flags: ignoreversion
Source: "setup.bat"; DestDir: "{app}\{cm:SourceCode}\COC"; Components: code; Flags: ignoreversion
Source: "complier.iss"; DestDir: "{app}\{cm:SourceCode}\COC"; Components: code; Flags: ignoreversion
Source: "License\License.txt"; DestDir: "{app}\License"; Components: main; Languages: english japanese; Flags: ignoreversion
Source: "License\License_cn.txt"; DestDir: "{app}\License"; Components: main; Languages: chinese; Flags: ignoreversion
Source: "License\ReadMe.txt"; DestDir: "{app}\License"; Components: main; Flags: ignoreversion
Source: "License\Regulation.txt"; DestDir: "{app}\License"; Components: main; Flags: ignoreversion
Source: "Tools\*"; DestDir: "{app}\Tools"; Components: main; Flags: ignoreversion recursesubdirs createallsubdirs
Source: "build\exe.win32-3.4\tcl\auto.tcl"; DestDir: "{app}\tcl"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tcl\init.tcl"; DestDir: "{app}\tcl"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tcl\tclIndex"; DestDir: "{app}\tcl"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\_bz2.pyd"; DestDir: "{app}"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\_ctypes.pyd"; DestDir: "{app}"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\_tkinter.pyd"; DestDir: "{app}"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\library.zip"; DestDir: "{app}"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\python34.dll"; DestDir: "{app}"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\unicodedata.pyd"; DestDir: "{app}"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tcl86t.dll"; DestDir: "{app}"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk86t.dll"; DestDir: "{app}"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\button.tcl"; DestDir: "{app}\tk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\entry.tcl"; DestDir: "{app}\tk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\icons.tcl"; DestDir: "{app}\tk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\listbox.tcl"; DestDir: "{app}\tk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\menu.tcl"; DestDir: "{app}\tk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\obsolete.tcl"; DestDir: "{app}\tk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\optMenu.tcl"; DestDir: "{app}\tk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\palette.tcl"; DestDir: "{app}\tk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\panedwindow.tcl"; DestDir: "{app}\tk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\pkgIndex.tcl"; DestDir: "{app}\tk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\safetk.tcl"; DestDir: "{app}\tk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\scale.tcl"; DestDir: "{app}\tk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\scrlbar.tcl"; DestDir: "{app}\tk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\spinbox.tcl"; DestDir: "{app}\tk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\tclIndex"; DestDir: "{app}\tk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\tearoff.tcl"; DestDir: "{app}\tk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\text.tcl"; DestDir: "{app}\tk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\tk.tcl"; DestDir: "{app}\tk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\tkfbox.tcl"; DestDir: "{app}\tk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\unsupported.tcl"; DestDir: "{app}\tk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\xmfbox.tcl"; DestDir: "{app}\tk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\ttk\altTheme.tcl"; DestDir: "{app}\tk\ttk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\ttk\button.tcl"; DestDir: "{app}\tk\ttk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\ttk\clamTheme.tcl"; DestDir: "{app}\tk\ttk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\ttk\classicTheme.tcl"; DestDir: "{app}\tk\ttk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\ttk\combobox.tcl"; DestDir: "{app}\tk\ttk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\ttk\cursors.tcl"; DestDir: "{app}\tk\ttk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\ttk\defaults.tcl"; DestDir: "{app}\tk\ttk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\ttk\entry.tcl"; DestDir: "{app}\tk\ttk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\ttk\fonts.tcl"; DestDir: "{app}\tk\ttk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\ttk\menubutton.tcl"; DestDir: "{app}\tk\ttk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\ttk\notebook.tcl"; DestDir: "{app}\tk\ttk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\ttk\panedwindow.tcl"; DestDir: "{app}\tk\ttk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\ttk\progress.tcl"; DestDir: "{app}\tk\ttk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\ttk\scale.tcl"; DestDir: "{app}\tk\ttk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\ttk\scrollbar.tcl"; DestDir: "{app}\tk\ttk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\ttk\sizegrip.tcl"; DestDir: "{app}\tk\ttk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\ttk\spinbox.tcl"; DestDir: "{app}\tk\ttk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\ttk\treeview.tcl"; DestDir: "{app}\tk\ttk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\ttk\ttk.tcl"; DestDir: "{app}\tk\ttk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\ttk\utils.tcl"; DestDir: "{app}\tk\ttk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\ttk\vistaTheme.tcl"; DestDir: "{app}\tk\ttk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\ttk\winTheme.tcl"; DestDir: "{app}\tk\ttk"; Components: main; Flags: ignoreversion
Source: "build\exe.win32-3.4\tk\ttk\xpTheme.tcl"; DestDir: "{app}\tk\ttk"; Components: main; Flags: ignoreversion
; NOTE: Don't use "Flags: ignoreversion" on any shared system files

[Registry]
Root: HKCR; Subkey: "COC_Donation.File"; ValueType: string; ValueData: "COC Donation File"; Flags: uninsdeletekey
Root: HKCR; Subkey: "COC_Donation.File\DefaultIcon"; ValueType: string; ValueData: "{app}\data\Clan.ico"; Flags: uninsdeletekey
Root: HKCR; Subkey: "COC_Donation.File\shell\open\command"; ValueType: string; ValueData: "{app}\{#MyAppExeName} %1"; Flags: uninsdeletekey
Root: HKCR; Subkey: "COC_Donation.File\shell\edit\command"; ValueType: string; ValueData: "{sys}\NOTEPAD.EXE %1"; Flags: uninsdeletekey
Root: HKCR; Subkey: "COC_History.File"; ValueType: string; ValueData: "COC History File"; Flags: uninsdeletekey
Root: HKCR; Subkey: "COC_History.File\DefaultIcon"; ValueType: string; ValueData: "{app}\data\Clan.ico"; Flags: uninsdeletekey
Root: HKCR; Subkey: "COC_History.File\shell\open\command"; ValueType: string; ValueData: "{app}\{#MyAppExeName} %1"; Flags: uninsdeletekey
Root: HKCR; Subkey: "COC_History.File\shell\edit\command"; ValueType: string; ValueData: "{sys}\NOTEPAD.EXE %1"; Flags: uninsdeletekey
Root: HKCR; Subkey: ".clh"; ValueType: string; ValueData: "COC_History.File"; Flags: uninsdeletekey
Root: HKCR; Subkey: ".clh"; ValueType: string; ValueName: "PerceivedType"; ValueData: "text";
Root: HKCR; Subkey: ".clh\OpenWithProgIDs"; Flags: uninsdeletekey
Root: HKCR; Subkey: ".clh\OpenWithProgIDs"; ValueType: string; ValueName: "COC_History.File";
Root: HKCR; Subkey: ".cld"; ValueType: string; ValueData: "COC_Donation.File"; Flags: uninsdeletekey
Root: HKCR; Subkey: ".cld"; ValueType: string; ValueName: "PerceivedType"; ValueData: "text";
Root: HKCR; Subkey: ".cld\OpenWithProgIDs"; Flags: uninsdeletekey
Root: HKCR; Subkey: ".cld\OpenWithProgIDs"; ValueType: string; ValueName: "COC_Donation.File";

[Icons]
Name: "{group}\{cm:MyAppName}"; Filename: "{app}\{#MyAppExeName}"
Name: "{group}\{cm:UninstallProgram,{cm:MyAppName}}"; Filename: "{uninstallexe}"
Name: "{commondesktop}\{cm:MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: desktopicon
Name: "{userappdata}\Microsoft\Internet Explorer\Quick Launch\{cm:MyAppName}"; Filename: "{app}\{#MyAppExeName}"; Tasks: quicklaunchicon

[Run]
Filename: "{app}\{#MyAppExeName}"; Description: "{cm:LaunchProgram,{cm:MyAppName}}"; Flags: nowait postinstall skipifsilent

