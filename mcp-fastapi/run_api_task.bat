@echo off
setlocal

REM Ensure execution starts from this script's folder.
cd /d "%~dp0"

if not exist ".venv\Scripts\python.exe" (
    echo [ERROR] Virtual environment Python not found at .venv\Scripts\python.exe
    exit /b 1
)

REM Start API server in a separate process so this terminal is released immediately.
if not exist "logs" mkdir "logs"
powershell -NoProfile -NonInteractive -ExecutionPolicy Bypass -Command "$out = Join-Path '%CD%' 'logs\uvicorn.out.log'; $err = Join-Path '%CD%' 'logs\uvicorn.err.log'; $p = Start-Process -FilePath '%CD%\.venv\Scripts\python.exe' -ArgumentList '-m','uvicorn','app.api:app','--host','0.0.0.0','--port','8000','--no-use-colors' -WindowStyle Hidden -RedirectStandardOutput $out -RedirectStandardError $err -PassThru; Write-Output '[INFO] FastAPI server started in background.'; Write-Output '[INFO] Uvicorn running on all interfaces (0.0.0.0:8000)'; Write-Output '[INFO] Open http://127.0.0.1:8000/docs locally or http://<your-ip>:8000/docs from another device.'; Write-Output ('[INFO] Started server process [' + $p.Id + '].'); Write-Output ('[INFO] Logs: ' + $out + ' | ' + $err)"
exit /b %ERRORLEVEL%
