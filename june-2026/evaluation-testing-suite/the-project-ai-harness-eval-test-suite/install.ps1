param(
  [string]$Target = "."
)

New-Item -ItemType Directory -Force -Path "$Target\.github" | Out-Null
New-Item -ItemType Directory -Force -Path "$Target\scripts" | Out-Null
New-Item -ItemType Directory -Force -Path "$Target\runbooks\ai-evals" | Out-Null
Copy-Item -Recurse -Force ".github\evals" "$Target\.github\evals"
Copy-Item -Force "scripts\ai_eval_*.py" "$Target\scripts\"
Copy-Item -Force "runbooks\*.md" "$Target\runbooks\ai-evals\"
Write-Host "Installed the project AI eval test suite into $Target"
