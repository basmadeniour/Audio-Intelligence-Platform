# ===========================
# Collect Full Project Code (FINAL FIXED VERSION)
# ===========================

$ProjectPath = (Get-Location).Path
$OutputFile = Join-Path $ProjectPath "FullProjectCode.txt"

# حذف الملف القديم لو موجود
if (Test-Path $OutputFile) {
    Remove-Item $OutputFile -Force
}

# الامتدادات المطلوبة
$Extensions = @(".py", ".js", ".jsx", ".json", ".txt", ".md")

# فولدرات مستبعدة
$ExcludeDirs = @("node_modules", "__pycache__", ".git")

# جمع الملفات
$files = Get-ChildItem -Path $ProjectPath -Recurse -File |
Where-Object {

    $fullPath = $_.FullName.ToLower()

    # استبعاد الفولدرات
    $isExcluded = $false
    foreach ($dir in $ExcludeDirs) {
        if ($fullPath -like "*$dir*") {
            $isExcluded = $true
        }
    }

    # التحقق من الامتداد
    $validExt = $_.Extension.ToLower() -in $Extensions

    (-not $isExcluded) -and $validExt
}

# لو مفيش ملفات
if (-not $files -or $files.Count -eq 0) {
    Write-Host "❌ No matching files found!"
    Write-Host "👉 Check if your folders contain .py / .js / .jsx files"
    exit
}

# كتابة الملفات في ملف واحد
foreach ($file in ($files | Sort-Object FullName)) {

    $RelativePath = $file.FullName.Substring($ProjectPath.Length + 1)

    $fileHeader = @"
=============================
FILE: $RelativePath
=============================
"@

    $fileContent = Get-Content $file.FullName -Raw

    "$fileHeader`n$fileContent`n`n" | Out-File -Append $OutputFile -Encoding UTF8
}

Write-Host "✅ Done! Project collected successfully."
Write-Host "📄 Output file:"
Write-Host $OutputFile

Invoke-Item $OutputFile