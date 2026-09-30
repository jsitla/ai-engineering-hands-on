# Starts the web app, sends a real request, takes a browser screenshot, stops the app.
$env:PYTHONIOENCODING = "utf-8"
$ProgressPreference = "SilentlyContinue"   # the progress bar makes Invoke-WebRequest very slow
Set-Location $PSScriptRoot
$out = Join-Path $PSScriptRoot "..\runs\ep29-capstone"; New-Item -ItemType Directory -Force $out | Out-Null
$server = Start-Process python -ArgumentList "-m", "uvicorn", "app:app", "--port", "8000" -PassThru -WindowStyle Hidden -RedirectStandardError "$out\server_log.txt" -RedirectStandardOutput "$out\server_out.txt"
Start-Sleep 25
$body = '{"text": "Hi! Which of my orders cost more than 50 euros?"}'
$sw = [Diagnostics.Stopwatch]::StartNew()
$r = Invoke-WebRequest -UseBasicParsing -Method Post -Uri http://127.0.0.1:8000/ask -ContentType "application/json" -Body $body
"POST /ask -> $($r.StatusCode) in $([math]::Round($sw.Elapsed.TotalSeconds,1)) s`n$($r.Content)" | Out-File -Encoding utf8 "$out\request.txt"
$edge = "${env:ProgramFiles(x86)}\Microsoft\Edge\Application\msedge.exe"
if (-not (Test-Path $edge)) { $edge = "$env:ProgramFiles\Microsoft\Edge\Application\msedge.exe" }
Start-Process $edge -ArgumentList "--headless=new", "--disable-gpu", "--window-size=1280,720", "--timeout=30000", "--screenshot=`"$out\screenshot.png`"", "`"http://127.0.0.1:8000/?q=How%20much%20did%20I%20pay%20for%20shipping%20in%20total%3F`"" -Wait   # wait until the screenshot is saved
Start-Sleep 5
Stop-Process -Id $server.Id -Force
"DONE" | Out-File -Encoding utf8 "$out\_done.txt"
