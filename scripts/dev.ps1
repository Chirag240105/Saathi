$root = Split-Path -Parent $PSScriptRoot
$back = Start-Process -PassThru -NoNewWindow -WorkingDirectory "$root\backend" -FilePath ".venv\Scripts\uvicorn.exe" -ArgumentList "app.main:app","--reload","--port","8000"
try { Set-Location "$root\frontend"; npm run dev } finally { Stop-Process -Id $back.Id -ErrorAction SilentlyContinue }
