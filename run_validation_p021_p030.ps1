$root   = "c:\Users\Pratham\OneDrive\Desktop\research-code-evaluator"
$python = "python"
$runner = "$root\validate_runner_p021_p030.py"

$combos = @(
    @("P021","python","correct"), @("P021","python","wrong"),
    @("P021","java","correct"),   @("P021","java","wrong"),
    @("P021","cpp","correct"),    @("P021","cpp","wrong"),
    @("P021","javascript","correct"), @("P021","javascript","wrong"),

    @("P022","python","correct"), @("P022","python","wrong"),
    @("P022","java","correct"),
    @("P022","cpp","correct"),
    @("P022","javascript","correct"),

    @("P023","python","correct"), @("P023","python","wrong"),
    @("P023","java","correct"),
    @("P023","cpp","correct"),
    @("P023","javascript","correct"),

    @("P024","python","correct"), @("P024","python","wrong"),
    @("P024","java","correct"),
    @("P024","cpp","correct"),
    @("P024","javascript","correct"),

    @("P025","python","correct"), @("P025","python","wrong"),
    @("P025","java","correct"),
    @("P025","cpp","correct"),
    @("P025","javascript","correct"),

    @("P026","python","correct"), @("P026","python","wrong"),
    @("P026","java","correct"),
    @("P026","cpp","correct"),
    @("P026","javascript","correct"),

    @("P027","python","correct"), @("P027","python","wrong"),
    @("P027","java","correct"),
    @("P027","cpp","correct"),
    @("P027","javascript","correct"),

    @("P028","python","correct"), @("P028","python","wrong"),
    @("P028","java","correct"),
    @("P028","cpp","correct"),
    @("P028","javascript","correct"),

    @("P029","python","correct"), @("P029","python","wrong"),
    @("P029","java","correct"),
    @("P029","cpp","correct"),
    @("P029","javascript","correct"),

    @("P030","python","correct"), @("P030","python","wrong"),
    @("P030","java","correct"),
    @("P030","cpp","correct"),
    @("P030","javascript","correct")
)

$passed = 0; $failed = 0; $failures = @()

foreach ($combo in $combos) {
    $probId  = $combo[0]
    $lang    = $combo[1]
    $variant = $combo[2]

    $out = & $python $runner $probId $lang $variant 2>&1
    $exitCode = $LASTEXITCODE

    $line = ($out | Where-Object { $_ -match "^(PASS|FAIL|SKIP|ERROR)" } | Select-Object -First 1)
    if (-not $line) { $line = "FAIL ${probId} [${lang}] ${variant}: no output" }
    Write-Host $line

    if ($exitCode -eq 0) { $passed++ }
    else { $failed++; $failures += "${probId} [${lang}] ${variant}" }

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
