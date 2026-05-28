# E10 App — Deployment Guide

This document lists the commands and procedures to deploy and run the E10 Streamlit app on a Windows server (IIS + WinSW wrapper). Run PowerShell as Administrator for all host-level operations.

## Overview
- App process: Streamlit app served on loopback `127.0.0.1:8502`.
- Public access: IIS reverse proxy (`E10AppProxy`) listens on port `4040` and rewrites to `127.0.0.1:8502`.
- Windows service: WinSW wrapper `E10AppService` runs `scripts\start_e10_app.bat` to launch Streamlit.

## Prerequisites (server)
- Windows Server with IIS + Application Request Routing (ARR) installed.
- PowerShell (run elevated) and administrative access.
- .NET/WinSW will be downloaded by the installer script.
- Python and required packages installed in repo `.venv` or system-wide.

## Repository layout (important files)
- `scripts\start_e10_app.bat` — starts Streamlit using repo `.venv` and writes logs.
- `scripts\install_winsw_service.ps1` — creates `winsw\E10AppService.exe` + `.xml` and can install the service.
- `scripts\winsw\E10AppService.xml` — template service XML (keeps path to `start_e10_app.bat`).
- `scripts\deploy_iis_reverse_proxy.ps1` — creates the `E10AppProxy` IIS site and `iis_proxy_site\web.config` rewrite rule.
- `.env` — environment values (APP_ROOT, STREAMLIT_PORT=8502, PUBLIC_PORT=4040, SERVICE_USER, SERVICE_PASS).
- `.streamlit\config.toml` — optional Streamlit config. Keep server.port = 8502.

## Quick deploy steps (recommended, full automation)
1. Open an elevated PowerShell prompt in the repo root (`E:\apps\e10_file_processor`).

2. Ensure Python venv is present and dependencies installed (from repo root):

```powershell
# create venv if missing (optional)
python -m venv .venv
# activate and install
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

3. Verify `.env` values (set `STREAMLIT_PORT=8502`, `PUBLIC_PORT=4040`):

```powershell
Get-Content .\.env
```

4. Ensure `.streamlit\config.toml` port aligns (recommended to set values consistent with CLI args used in start script):

- In `.streamlit\config.toml` set:
```
[server]
port = 8502
headless = true
enableCORS = false
enableXsrfProtection = false
```

5. (Optional) Test run Streamlit manually to check it starts:

```powershell
# from repo root
.\.venv\Scripts\python.exe -m streamlit run .\streamlit_app.py --server.address 127.0.0.1 --server.port 8502
# or use helper script
powershell -NoProfile -ExecutionPolicy Bypass -File .\run_streamlit.ps1
```

6. Install WinSW wrapper and service (canonical name `E10AppService`):

```powershell
# from repo root, run elevated
Set-Location .\scripts
powershell -NoProfile -ExecutionPolicy Bypass -File .\install_winsw_service.ps1 -ServiceName E10AppService -DisplayName 'E10 App Service' -Install
```

This will:
- download WinSW into `scripts\winsw\E10AppService.exe`,
- write `scripts\winsw\E10AppService.xml` (pointing at `start_e10_app.bat`),
- install and start the `E10AppService` Windows service.

7. Confirm service and process are running:

```powershell
Get-Service -Name E10AppService
# find process
Get-Process -Id (Get-WmiObject Win32_Service -Filter "Name='E10AppService'").ProcessId -ErrorAction SilentlyContinue
```

8. Configure IIS reverse proxy (ARR) site:

```powershell
# Run the script (requires IIS/appcmd present and Admin)
Set-Location .\scripts
powershell -NoProfile -ExecutionPolicy Bypass -File .\deploy_iis_reverse_proxy.ps1 -SiteName E10AppProxy -PublicPort 4040 -StreamlitPort 8502
```

This will create `iis_proxy_site\web.config` and an IIS site `E10AppProxy` bound to public port 4040.

9. Open Windows Firewall for the public port (4040):

```powershell
New-NetFirewallRule -DisplayName 'E10AppProxy (4040)' -Direction Inbound -Action Allow -Protocol TCP -LocalPort 4040 -Profile Any -Enabled True
```

10. Test locally on the server:

```powershell
# direct Streamlit
Invoke-WebRequest -Uri http://127.0.0.1:8502/ -UseBasicParsing
# via IIS proxy
Invoke-WebRequest -Uri http://localhost:4040/ -UseBasicParsing
```

If both return HTTP 200, the app is running and proxying correctly.

## Proxy header guidance

When enabling Streamlit's built-in CORS/XSRF protections (`enableCORS = true` and `enableXsrfProtection = true`) you must ensure the reverse proxy preserves required headers and cookies. Recommended IIS/ARR settings and checks:

- Preserve the original Host header so Streamlit sees the expected host (the deploy script sets `/preserveHostHeader:"True"`).
- Ensure ARR forwards `X-Forwarded-For`, `X-Forwarded-Proto`, and `X-Forwarded-Host` so downstream code can reconstruct client details.
- Do not strip cookies or authentication headers; XSRF protection depends on cookies and `Origin`/`Referer` headers being preserved.
- If you rewrite hostnames or domains, verify ARR's `reverseRewriteHostInResponseHeaders` setting — enabling it may be required for some hostname rewrite scenarios, but test redirects/cookie domains after changing it.
- Enable WebSockets in IIS if the app uses them (`-InstallWebSockets` in `deploy_iis_reverse_proxy.ps1`).

Testing tips:

- From the server, test direct Streamlit and proxy endpoints:
```powershell
Invoke-WebRequest -Uri http://127.0.0.1:8502/ -UseBasicParsing
Invoke-WebRequest -Uri http://localhost:4040/ -UseBasicParsing
```
- From a remote client, open DevTools and check for blocked XHRs or missing cookies; XSRF failures usually show `403` and missing/invalid `_streamlit_xsrf` cookie.

If you observe XSRF 403s, confirm the proxy preserves cookies and the `Origin`/`Referer` headers required by Streamlit's XSRF checks.

## Uninstall / cleanup (if you need to remove old wrappers or sites)
- Stop and remove WinSW service (canonical name `E10AppService`) and any legacy `E10App` service:

```powershell
Set-Location .\scripts\winsw
# stop service
.\E10AppService.exe stop 2>$null
.\E10AppService.exe uninstall 2>$null
# fallback
Stop-Service -Name 'E10AppService' -Force -ErrorAction SilentlyContinue
sc.exe delete 'E10AppService'

# legacy cleanup
Stop-Service -Name 'E10App' -ErrorAction SilentlyContinue
sc.exe delete 'E10App'
Remove-Item .\E10App.exe -Force -ErrorAction SilentlyContinue
Remove-Item .\E10App.xml -Force -ErrorAction SilentlyContinue
```

- Remove IIS site and app pool (via appcmd):

```powershell
# stop site
& $env:SystemRoot\system32\inetsrv\appcmd.exe stop site /site.name:"E10AppProxy"
# delete site
& $env:SystemRoot\system32\inetsrv\appcmd.exe delete site "E10AppProxy"
# optionally delete the apppool if used
& $env:SystemRoot\system32\inetsrv\appcmd.exe list apppool /name:E10AppProxy | Out-Null
& $env:SystemRoot\system32\inetsrv\appcmd.exe delete apppool "E10AppProxy" 2>$null
```

## Logs and diagnostics
- WinSW wrapper logs: `scripts\logs\E10AppService\E10AppService.wrapper.log`
- Streamlit app logs (created by batch): top-level logs directory: `logs\streamlit_YYYYmmdd_HHMMSS.log`

Useful commands:

```powershell
# tail wrapper log
Get-Content .\scripts\logs\E10AppService\E10AppService.wrapper.log -Tail 200 -Wait

# tail the latest streamlit log
Get-ChildItem E:\apps\e10_file_processor -Filter 'streamlit_*.log' -Recurse | Sort-Object LastWriteTime -Descending | Select-Object -First 1 | ForEach-Object { Get-Content $_.FullName -Tail 200 -Wait }

# check listening ports
netstat -ano | findstr ":8502\|:4040"

# check service status
Get-Service -Name E10AppService, E10App -ErrorAction SilentlyContinue | Format-Table Name,Status

# check IIS site
& $env:SystemRoot\system32\inetsrv\appcmd.exe list site /name:E10AppProxy
```

## Common issues & fixes
- Duplicate service names
  - Problem: legacy `E10App` wrapper and new `E10AppService` both present can cause install conflicts.
  - Fix: remove legacy wrapper as shown in Uninstall section, then reinstall the canonical wrapper.

- Streamlit port mismatch
  - Problem: CLI flags in `scripts\start_e10_app.bat` may disagree with `.streamlit\config.toml`.
  - Fix: ensure both use `8502` and that the deploy script rewrites to `127.0.0.1:8502`.

- Missing `common.ps1` when running `install_winsw_service.ps1`
  - Symptom: script errors referencing `Ensure-Strict` or `Assert-Admin`.
  - Fix: run the installer from the repo root (so `scripts\common.ps1` is available), or add safe fallbacks in the installer (the repo includes a resilient installer version in case `common.ps1` is absent).

- IIS/ARR not proxying websockets or large responses
  - Use `-InstallWebSockets` flag in `deploy_iis_reverse_proxy.ps1` to enable the `Web-WebSockets` feature. Increase `RequestTimeout` parameter if necessary.

## Security notes
- Do NOT commit `SERVICE_PASS` or other secrets into the repo. Store them in secure secrets manager or provide them at deployment time.

## Repro checklist (quick)
- [ ] Python `.venv` present and packages installed
- [ ] `.env` contains `STREAMLIT_PORT=8502` and `PUBLIC_PORT=4040`
- [ ] `scripts\start_e10_app.bat` uses `--server.address 127.0.0.1 --server.port 8502`
- [ ] `E10AppService` installed and running
- [ ] `E10AppProxy` site exists in IIS bound to port 4040
- [ ] Firewall allows inbound TCP 4040 for required profiles
- [ ] Wrapper and streamlit logs show healthy startup and no errors


