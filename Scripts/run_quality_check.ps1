Set-Location "$PSScriptRoot\.."

& ".\.venv\Scripts\python.exe" -c "from src.quality.dq_runner import run_quality_pipeline; result = run_quality_pipeline(); print(result); exit(0 if result['status'] == 'PASS' else 1)"

if ($LASTEXITCODE -ne 0) {
    Write-Error "Data quality check failed."
    exit $LASTEXITCODE
}

Write-Host "Data quality check completed successfully."