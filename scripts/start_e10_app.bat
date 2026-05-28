@echo off
setlocal

REM Load variables from repo-root .env if present
for %%I in ("%~dp0..") do set "REPO_ROOT=%%~fI\"
if exist "%REPO_ROOT%.env" (
	for /f "tokens=1* delims==" %%A in ('findstr /r /v "^[#;]" "%REPO_ROOT%.env"') do (
		if not "%%A"=="" set "%%A=%%B"
	)
)

REM Fallback defaults
if not defined APP_ROOT (
	for %%I in ("%~dp0..") do set "APP_ROOT=%%~fI\"
)
if not defined STREAMLIT_PORT set "STREAMLIT_PORT=8502"

REM Ensure log directory
set "LOG_DIR=%APP_ROOT%logs"
if not exist "%LOG_DIR%" mkdir "%LOG_DIR%"

REM Timestamp for log filenames (yyyyMMdd_HHmmss)
for /f %%i in ('powershell -NoProfile -Command "(Get-Date).ToString(\"yyyyMMdd_HHmmss\")"') do set "TS=%%i"

cd /d "%APP_ROOT%"

call "%APP_ROOT%\.venv\Scripts\activate.bat"

set "OUT_LOG=%LOG_DIR%\streamlit_%TS%.log"
set "ERR_LOG=%LOG_DIR%\streamlit_%TS%_err.log"

echo [%DATE% %TIME%] Starting Streamlit >> "%OUT_LOG%"

REM Run Streamlit via PowerShell Tee-Object so output is both logged and forwarded to stdout
powershell -NoProfile -Command "python -m streamlit run 'streamlit_app.py' --server.port %STREAMLIT_PORT% --server.address 127.0.0.1 --server.headless true --browser.gatherUsageStats false 2>&1 | Tee-Object -FilePath '%OUT_LOG%'"

exit /b %ERRORLEVEL%