# Run all validation cases as separate subprocess calls
# Using $probId to avoid conflict with PowerShell's reserved $pid variable

$root = "c:\Users\Pratham\OneDrive\Desktop\research-code-evaluator"
$python = "python"

$combos = @(
    # P001
    @("P001","python","correct"), @("P001","python","wrong"), @("P001","python","error"),
    @("P001","java","correct"),   @("P001","java","wrong"),   @("P001","java","error"),
    @("P001","cpp","correct"),    @("P001","cpp","wrong"),
    @("P001","javascript","correct"), @("P001","javascript","wrong"),
    # P002
    @("P002","python","correct"), @("P002","python","wrong"),
    @("P002","java","correct"),
    @("P002","cpp","correct"),
    @("P002","javascript","correct"), @("P002","javascript","wrong"),
    # P003
    @("P003","python","correct"), @("P003","python","wrong"),
    @("P003","java","correct"),
    @("P003","cpp","correct"),
    @("P003","javascript","correct"),
    # P004
    @("P004","python","correct"), @("P004","python","wrong"),
    @("P004","java","correct"),
    @("P004","cpp","correct"),
    @("P004","javascript","correct"),
    # P005
    @("P005","python","correct"), @("P005","python","wrong"),
    @("P005","java","correct"),
    @("P005","cpp","correct"),
    @("P005","javascript","correct"), @("P005","javascript","wrong"),
    # P006
    @("P006","python","correct"), @("P006","python","wrong"),
    @("P006","java","correct"),
    @("P006","cpp","correct"),
    @("P006","javascript","correct"),
    # P007
    @("P007","python","correct"), @("P007","python","wrong"),
    @("P007","java","correct"),
    @("P007","cpp","correct"),
    @("P007","javascript","correct"),
    # P008
    @("P008","python","correct"), @("P008","python","wrong"),
    @("P008","java","correct"),
    @("P008","cpp","correct"),
    @("P008","javascript","correct"),
    # P009
    @("P009","python","correct"), @("P009","python","wrong"),
    @("P009","java","correct"),
    @("P009","cpp","correct"),
    @("P009","javascript","correct"),
    # P010
    @("P010","python","correct"), @("P010","python","wrong"),
    @("P010","java","correct"),
    @("P010","cpp","correct"),
    @("P010","javascript","correct"), @("P010","javascript","wrong"),
    # P011
    @("P011","python","correct"), @("P011","python","wrong"), @("P011","python","error"),
    @("P011","java","correct"),   @("P011","java","wrong"),
    @("P011","cpp","correct"),    @("P011","cpp","wrong"),
    @("P011","javascript","correct"), @("P011","javascript","wrong"),
    # P012
    @("P012","python","correct"), @("P012","python","wrong"),
    @("P012","java","correct"),
    @("P012","cpp","correct"),
    @("P012","javascript","correct"), @("P012","javascript","wrong"),
    # P013
    @("P013","python","correct"), @("P013","python","wrong"),
    @("P013","java","correct"),
    @("P013","cpp","correct"),
    @("P013","javascript","correct"),
    # P014
    @("P014","python","correct"), @("P014","python","wrong"),
    @("P014","java","correct"),
    @("P014","cpp","correct"),
    @("P014","javascript","correct"),
    # P015
    @("P015","python","correct"), @("P015","python","wrong"),
    @("P015","java","correct"),
    @("P015","cpp","correct"),
    @("P015","javascript","correct"),
    # P016
    @("P016","python","correct"), @("P016","python","wrong"),
    @("P016","java","correct"),
    @("P016","cpp","correct"),
    @("P016","javascript","correct"), @("P016","javascript","wrong"),
    # P017
    @("P017","python","correct"), @("P017","python","wrong"),
    @("P017","java","correct"),
    @("P017","cpp","correct"),
    @("P017","javascript","correct"),
    # P018
    @("P018","python","correct"), @("P018","python","wrong"),
    @("P018","java","correct"),
    @("P018","cpp","correct"),
    @("P018","javascript","correct"),
    # P019
    @("P019","python","correct"), @("P019","python","wrong"),
    @("P019","java","correct"),
    @("P019","cpp","correct"),
    @("P019","javascript","correct"),
    # P020
    @("P020","python","correct"), @("P020","python","wrong"),
    @("P020","java","correct"),
    @("P020","cpp","correct"),
    @("P020","javascript","correct"), @("P020","javascript","wrong")
)

$passed = 0; $failed = 0; $failures = @()

foreach ($combo in $combos) {
    $probId  = $combo[0]
    $lang    = $combo[1]
    $variant = $combo[2]

    $out = & $python "$root\validate_runner.py" $probId $lang $variant 2>&1
    $exitCode = $LASTEXITCODE

    $line = ($out | Where-Object { $_ -match "^(PASS|FAIL|SKIP|ERROR)" } | Select-Object -First 1)
    if (-not $line) { $line = "FAIL ${probId} [${lang}] ${variant}: no output" }
    Write-Host $line

    if ($exitCode -eq 0) {
        $passed++
    } else {
        $failed++
        $failures += "${probId} [${lang}] ${variant}"
    }

    # Brief pause between C++ runs to avoid AppControl timing issues
    if ($lang -eq "cpp") { Start-Sleep -Milliseconds 2000 }
}

Write-Host ""
Write-Host ("=" * 60)
Write-Host "TOTAL: $($passed+$failed)  PASSED: $passed  FAILED: $failed"
if ($failed -gt 0) {
    Write-Host "FAILURES:"
    foreach ($r in $failures) { Write-Host "  $r" }
    exit 1
} else {
    Write-Host "ALL CHECKS PASSED"
    exit 0
}
