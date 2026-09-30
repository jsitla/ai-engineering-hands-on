# Starts the flaky proxy, runs both demos against it, then stops it.
$env:PYTHONIOENCODING = "utf-8"
Set-Location $PSScriptRoot
$out = Join-Path $PSScriptRoot "..\runs\ep18-errors-retries"; New-Item -ItemType Directory -Force $out | Out-Null
foreach ($name in "no_retry", "with_retry") {
  $fails = 2
  $proxy = Start-Process python -ArgumentList "flaky_proxy.py", $fails -PassThru -WindowStyle Hidden -RedirectStandardOutput "$out\proxy_$name.txt"
  Start-Sleep 2
  (& python "$name.py" 2>&1 | Out-String) | Out-File -Encoding utf8 "$out\$name.txt"
  Stop-Process -Id $proxy.Id -Force
}
(& python timeout_demo.py 2>&1 | Out-String) | Out-File -Encoding utf8 "$out\timeout_demo.txt"
"DONE" | Out-File -Encoding utf8 "$out\_done.txt"
