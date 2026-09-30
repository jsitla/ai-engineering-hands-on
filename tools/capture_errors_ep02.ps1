# Episode 2: capture the two most common errors, for real
$root = Split-Path -Parent $PSScriptRoot
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$env:PYTHONIOENCODING = "utf-8"
$out = Join-Path $root "runs\ep02-first-call"; New-Item -ItemType Directory -Force $out | Out-Null
Push-Location (Join-Path $root "ep02-first-call")
$code = (Get-Content first_call.py -Raw) -replace '11434', '11435'
Set-Content -Encoding utf8 "$env:TEMP\wrong_port.py" $code
(& python "$env:TEMP\wrong_port.py" 2>&1 | Out-String) | Out-File -Encoding utf8 "$out\error_wrong_port.txt"
$env:MODEL = "llama3.2:3"
(& python ask.py 2>&1 | Out-String) | Out-File -Encoding utf8 "$out\error_wrong_model.txt"
Remove-Item Env:MODEL
Pop-Location
"DONE" | Out-File -Encoding utf8 "$out\_errors_done.txt"
