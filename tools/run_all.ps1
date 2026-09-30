# Runs every demo script and saves its output to runs\<episode>\<script>.txt
param([string[]]$Only = @(), [string]$Script = "")
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
  @("ep03-roles", "assistant.py"),
  @("ep04-tokens-cost", "count_tokens.py"),
  @("ep04-tokens-cost", "cost.py"),
  @("ep04-tokens-cost", "context.py"),
  @("ep04-tokens-cost", "cap.py"),
  @("ep05-temperature", "temperature.py"),
  @("ep05-temperature", "next_token.py"),
  @("ep05-temperature", "accuracy.py"),
  @("ep06-prompting", "compare_prompts.py"),
  @("ep06-prompting", "nova_v2.py"),
  @("ep06-prompting", "think.py"),
  @("ep07-json", "extract.py"),
  @("ep07-json", "extract_pydantic.py"),
  @("ep07-json", "missing.py"),
  @("ep08-chatbot-memory", "memory_demo.py"),
  @("ep08-chatbot-memory", "growth.py"),
  @("ep08-chatbot-memory", "forget.py"),
  @("ep08-chatbot-memory", "chat.py")
)
foreach ($j in $jobs) {
  if ($Only.Count -and -not ($Only -contains $j[0])) { continue }
  if ($Script -and $j[1] -ne $Script) { continue }
  $dir = Join-Path $root $j[0]
  $outDir = Join-Path $root ("runs\" + $j[0]); New-Item -ItemType Directory -Force $outDir | Out-Null
  $out = Join-Path $outDir ($j[1] -replace '\.py$', '.txt')
  Push-Location $dir
  $sw = [Diagnostics.Stopwatch]::StartNew()
  if (Test-Path ($j[1] -replace '\.py$', '_script.txt')) {
    $text = Get-Content ($j[1] -replace '\.py$', '_script.txt') | & python $j[1] 2>&1 | Out-String
  } else {
    $text = & python $j[1] 2>&1 | Out-String
  }
  $sw.Stop()
  Pop-Location
  "$text`n[exit $LASTEXITCODE, $([math]::Round($sw.Elapsed.TotalSeconds,1)) s, $(Get-Date -Format s)]" | Out-File -Encoding utf8 $out
}
"ALL DONE $(Get-Date -Format s)" | Out-File -Encoding utf8 (Join-Path $root "runs\_done.txt")
