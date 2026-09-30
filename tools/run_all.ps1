# Runs every demo script and saves its output to runs\<episode>\<script>.txt
param([string[]]$Only = @())
$root = Split-Path -Parent $PSScriptRoot
$Only = @($Only | ForEach-Object { $_ -split "," } | Where-Object { $_ })
$env:PYTHONIOENCODING = "utf-8"
[Console]::OutputEncoding = [Text.Encoding]::UTF8
$OutputEncoding = [Text.Encoding]::UTF8
$jobs = @(
  @("ep01-setup", "check_setup.py"),
  @("ep02-first-call", "first_call.py"),
  @("ep02-first-call", "ask.py"),
  @("ep02-first-call", "inspect_response.py"),
  @("ep03-roles", "system_prompt.py"),
  @("ep03-roles", "roles.py"),
  @("ep04-tokens-cost", "count_tokens.py"),
  @("ep04-tokens-cost", "cost.py"),
  @("ep05-temperature", "temperature.py"),
  @("ep06-prompting", "compare_prompts.py"),
  @("ep07-json", "extract.py"),
  @("ep08-chatbot-memory", "memory_demo.py")
)
foreach ($j in $jobs) {
  if ($Only.Count -and -not ($Only -contains $j[0])) { continue }
  $dir = Join-Path $root $j[0]
  $outDir = Join-Path $root ("runs\" + $j[0]); New-Item -ItemType Directory -Force $outDir | Out-Null
  $out = Join-Path $outDir ($j[1] -replace '\.py$', '.txt')
  Push-Location $dir
  $sw = [Diagnostics.Stopwatch]::StartNew()
  $text = & python $j[1] 2>&1 | Out-String
  $sw.Stop()
  Pop-Location
  "$text`n[exit $LASTEXITCODE, $([math]::Round($sw.Elapsed.TotalSeconds,1)) s, $(Get-Date -Format s)]" | Out-File -Encoding utf8 $out
}
"ALL DONE $(Get-Date -Format s)" | Out-File -Encoding utf8 (Join-Path $root "runs\_done.txt")
