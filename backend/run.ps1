# Run backend from this folder. Use from project root: cd backend; .\run.ps1
# Uses port 3002 (avoids Windows reserved ranges that cause WinError 10013 on 8000/8080).
Set-Location $PSScriptRoot
$port = if ($env:CHATBOT_PORT) { $env:CHATBOT_PORT } else { "3002" }
python -m uvicorn main:app --host 0.0.0.0 --port $port
