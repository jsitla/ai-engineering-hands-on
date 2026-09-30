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
  @("ep08-chatbot-memory", "chat.py"),
  @("ep09-streaming", "no_stream.py"),
  @("ep09-streaming", "stream.py"),
  @("ep09-streaming", "pieces.py"),
  @("ep09-streaming", "chat_stream.py"),
  @("ep09-streaming", "usage_stream.py"),
  @("ep10-tool-calling", "no_tools.py"),
  @("ep10-tool-calling", "tools.py"),
  @("ep10-tool-calling", "raw_call.py"),
  @("ep10-tool-calling", "two_tools.py"),
  @("ep11-embeddings", "embed_one.py"),
  @("ep11-embeddings", "similarity.py"),
  @("ep11-embeddings", "search.py"),
  @("ep11-embeddings", "extra.py"),
  @("ep12-chunking", "compare.py"),
  @("ep12-chunking", "sizes.py"),
  @("ep13-rag", "rag.py"),
  @("ep13-rag", "show_prompt.py"),
  @("ep14-vector-db", "index.py"),
  @("ep14-vector-db", "query.py"),
  @("ep14-vector-db", "speed.py"),
  @("ep14-vector-db", "update.py"),
  @("ep15-hybrid-rerank", "compare.py"),
  @("ep15-hybrid-rerank", "top3.py"),
  @("ep16-evals", "run_evals.py"),
  @("ep16-evals", "run_evals_c.py"),
  @("ep17-llm-judge", "judge.py"),
  @("ep17-llm-judge", "pairwise.py"),
  @("ep19-prompt-caching", "cache.py"),
  @("ep20-guardrails", "poisoned.py"),
  @("ep20-guardrails", "guards.py"),
  @("ep21-tracing", "traced_rag.py"),
  @("ep21-tracing", "why_slow.py"),
  @("ep22-faster-cheaper", "compare.py"),
  @("ep24-agent-loop", "agent.py"),
  @("ep24-agent-loop", "agent_v2.py"),
  @("ep24-agent-loop", "agent_v3.py"),
  @("ep24-agent-loop", "compare_models.py"),
  @("ep25-mcp-server", "client.py"),
  @("ep25-mcp-server", "nova_mcp.py"),
  @("ep26-agent-memory", "memory_agent.py"),
  @("ep26-agent-memory", "memory_agent_v2.py"),
  @("ep26-agent-memory", "memory_agent_v3.py"),
  @("ep28-images", "make_receipt.py"),
  @("ep28-images", "read_receipt.py"),
  @("ep28-images", "make_tricky.py"),
  @("ep28-images", "read_tricky.py"),
  @("ep27-fine-tuning", "baseline.py"),
  @("ep27-fine-tuning", "train_lora.py"),
  @("ep27-fine-tuning", "evaluate.py"),
  @("ep27-fine-tuning", "bigger_model.py"),
  @("ep29-capstone", "chat.py"),
  @("ep29-capstone", "final_evals.py")
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
