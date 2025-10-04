# heartbeat.ps1
Write-Host "🔁 Running heartbeat check..."

$modules = @(
    "dispatch_wordpress",
    "dispatch_linkedin",
    "dispatch_facebook",
    "dispatch_email"
)

foreach ($module in $modules) {
    $path = "F:\Realms\realms_core_alpha\realms_agentic_core\$module.py"
    if (Test-Path $path) {
        Write-Host "✅ Checking $module..."
        try {
            python $path
        } catch {
            Write-Host "❌ $module failed: $($_.Exception.Message)"
        }
    } else {
        Write-Host "⚠️ $module not found."
    }
}

Write-Host "🧠 Heartbeat complete."