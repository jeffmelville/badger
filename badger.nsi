;NSIS Modern User Interface
;Basic Example Script
;Written by Joost Verburg

;--------------------------------
;Include Modern UI

  !include "MUI2.nsh"

;--------------------------------
;General

!define MULTIUSER_EXECUTIONLEVEL Highest
!include MultiUser.nsh

!macro BadgerPrompt
  MessageBox MB_OKCANCEL "Please ensure Badger is not running" IDOK badger_prompt_next IDCANCEL badger_prompt_quit
  badger_prompt_quit:
  quit
  badger_prompt_next:
!macroend

Function .onInit
  !insertmacro MULTIUSER_INIT
  !insertmacro BadgerPrompt
FunctionEnd

Function un.onInit
  !insertmacro MULTIUSER_UNINIT
  !insertmacro BadgerPrompt
FunctionEnd

  ;Name and file
  Name "Badger"

  !ifdef VERSION
  OutFile "badger-v${VERSION}.exe"
  !else
  OutFile "badger_install.exe"
  !endif

  Icon "src\badger.ico"
  ;LicenseText "License"
  ;LicenseData "LICENSE"
  ;Default installation folder
  InstallDir "$PROGRAMFILES\Badger"
  
  ;Request application privileges for Windows Vista
  ;RequestExecutionLevel user

;--------------------------------
;Interface Settings

  !define MUI_ABORTWARNING

;--------------------------------
;Pages

  !insertmacro MUI_PAGE_LICENSE LICENSE
  !insertmacro MUI_PAGE_COMPONENTS
  !insertmacro MUI_PAGE_DIRECTORY
  !insertmacro MUI_PAGE_INSTFILES
  
  !insertmacro MUI_UNPAGE_CONFIRM
  !insertmacro MUI_UNPAGE_INSTFILES
  
;--------------------------------
;Languages
 
  !insertmacro MUI_LANGUAGE "English"

;--------------------------------
;Installer Sections

Section "Badger Core" SecCore

  SetOutPath "$INSTDIR"
  
  ;ADD YOUR OWN FILES HERE...
  File /r "dist\*.*"
  
  ;Store installation folder

  
  ;Create uninstaller
  WriteUninstaller "$INSTDIR\Uninstall.exe"

SectionEnd

Section "Add Start Menu entries" SecStartMenu
    SetOutPath "$INSTDIR"
    CreateDirectory "$SMPROGRAMS\Badger"
    CreateShortcut "$SMPROGRAMS\Badger\Badger.lnk" "$INSTDIR\badger.exe"
    CreateShortcut "$SMPROGRAMS\Badger\Uninstall Badger.lnk" "$INSTDIR\Uninstall.exe"
SectionEnd

Section "Launch Badger at Startup" SecStartup
  SetOutPath "$INSTDIR"
  CreateShortcut "$SMSTARTUP\Badger.lnk" "$INSTDIR\badger.exe"
SectionEnd

;--------------------------------
;Descriptions

  ;Language strings
  LangString DESC_SecCore ${LANG_ENGLISH} "Badger core components (required)"

  ;Assign language strings to sections
  !insertmacro MUI_FUNCTION_DESCRIPTION_BEGIN
    !insertmacro MUI_DESCRIPTION_TEXT ${SecCore} $(DESC_SecCore)
  !insertmacro MUI_FUNCTION_DESCRIPTION_END

;--------------------------------
;Uninstaller Section

Section "Uninstall"

  ;ADD YOUR OWN FILES HERE...

  Delete "$INSTDIR\Uninstall.exe"

  RMDir /r "$INSTDIR"
  Delete "$SMSTARTUP\Badger.lnk"
  RMDir /r "$SMPROGRAMS\Badger"

SectionEnd