# Captures the real terminal output shown in Episode 1
$root = Split-Path -Parent $PSScriptRoot
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$OutputEncoding = [Text.Encoding]::UTF8
$o = "$env:LOCALAPPDATA\Programs\Ollama\ollama.exe"
$out = Join-Path $root "runs\ep01-setup"; New-Item -ItemType Directory -Force $out | Out-Null
(& python --version 2>&1 | Out-String) | Out-File -Encoding utf8 "$out\python_version.txt"
(& $o pull llama3.2:3b 2>&1 | Out-String) | Out-File -Encoding utf8 "$out\pull.txt"
$sw = [Diagnostics.Stopwatch]::StartNew()
(& $o run llama3.2:3b "Explain what a large language model is, in two short sentences." 2>&1 | Out-String) | Out-File -Encoding utf8 "$out\run.txt"
"seconds: $([math]::Round($sw.Elapsed.TotalSeconds,1))" | Out-File -Append -Encoding utf8 "$out\run.txt"
$tmp = Join-Path $env:TEMP "venvtest"; Remove-Item $tmp -Recurse -Force -ErrorAction SilentlyContinue; New-Item -ItemType Directory $tmp | Out-Null
Copy-Item "$root\requirements.txt" $tmp
Push-Location $tmp
(& python -m venv .venv 2>&1 | Out-String) | Out-File -Encoding utf8 "$out\venv.txt"
(& .\.venv\Scripts\python.exe -m pip install -r requirements.txt 2>&1 | Out-String) | Out-File -Append -Encoding utf8 "$out\venv.txt"
Pop-Location
& $o list 2>&1 | Out-File -Encoding utf8 "$out\list.txt"
"DONE" | Out-File -Encoding utf8 "$out\_capture_done.txt"
