@echo off
setlocal

REM Load variables from .env if present (SERVICE_USER and SERVICE_PASS can be set here)
if exist "%~dp0.env" (
	for /f "usebackq tokens=1,2 delims==" %%A in ("%~dp0.env") do set "%%A=%%B"
)

REM Supervisor selection: if SERVICE_SUPERVISOR or SUPERVISOR is set to "service", install WinSW service instead
if defined SERVICE_SUPERVISOR (
	set "SUPERVISOR=%SERVICE_SUPERVISOR%"
) 
if not defined SUPERVISOR (
	set "SUPERVISOR="
) 

if /I "%SUPERVISOR%"=="service" (
	REM Install WinSW service wrapper
	set PS_ARGS=-NoProfile -ExecutionPolicy Bypass -File "%~dp0install_winsw_service.ps1" -ServiceName E10AppService -DisplayName "E10 App Service" -Install
	if defined SERVICE_USER (
		set "PS_ARGS=%PS_ARGS% -ServiceUser \"%SERVICE_USER%\""
	)
	if defined SERVICE_PASS (
		set "PS_ARGS=%PS_ARGS% -ServicePassword \"%SERVICE_PASS%\""
	)
	powershell %PS_ARGS%
	echo WinSW service install attempted.
) else (
	REM Build PowerShell args: include service account if provided
	set PS_ARGS=-NoProfile -ExecutionPolicy Bypass -File "%~dp0create_scheduled_task.ps1"
	if defined SERVICE_USER (
		set "PS_ARGS=%PS_ARGS% -ServiceUser \"%SERVICE_USER%\""
	)
	if defined SERVICE_PASS (
		set "PS_ARGS=%PS_ARGS% -ServicePassword \"%SERVICE_PASS%\""
	)

	powershell %PS_ARGS%

	REM Start the task immediately (the PS script already starts it, but keep this for compatibility)
	schtasks /run /tn "E10AppService" 2>nul || echo "Scheduled task start attempted."
)