$files = @(".\__init__.py", ".\manifest.json", ".\README.md")
$dest = ".\auto-reveal.zip"
if (Test-Path $dest) { Remove-Item $dest }
Compress-Archive -Path $files -DestinationPath $dest
Write-Host "Packed $dest successfully."
