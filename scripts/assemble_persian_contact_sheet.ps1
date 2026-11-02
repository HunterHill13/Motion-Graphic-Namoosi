Add-Type -AssemblyName System.Drawing

$claudeDir = Join-Path $PSScriptRoot "..\renders\claude"
$claudeDir = [System.IO.Path]::GetFullPath($claudeDir)

$stills = @(
  "persian_act1_f50.png",
  "persian_act2_f140.png",
  "persian_act3_f270.png",
  "persian_act4_f410.png"
)

$labels = @(
  "ACT 1: PERSIAN HERO MONOLITH & INTERACTIVE CURSOR (f50/f95)",
  "ACT 2: LISSAJOUS PARAMETRIC ORBIT & SVG VECTOR MORPH (f140)",
  "ACT 3: 2.5D ISOMETRIC SAAS CONSOLE & LIVING TELEMETRY (f270)",
  "ACT 4: 100% SOVEREIGN CALIBRATION CLIMAX & OPTICAL BOKEH (f410)"
)

$cellWidth = 960
$cellHeight = 540
$headerHeight = 44
$gridWidth = $cellWidth * 2
$gridHeight = ($cellHeight + $headerHeight) * 2

$sheetBmp = New-Object System.Drawing.Bitmap($gridWidth, $gridHeight)
$g = [System.Drawing.Graphics]::FromImage($sheetBmp)
$g.Clear([System.Drawing.Color]::FromArgb(2, 6, 23))

$font = New-Object System.Drawing.Font("Arial", 12, [System.Drawing.FontStyle]::Bold)
$brush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
$bannerBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(15, 23, 42))

for ($i = 0; $i -lt 4; $i++) {
  $col = $i % 2
  $row = [Math]::Floor($i / 2)
  $x = $col * $cellWidth
  $y = $row * ($cellHeight + $headerHeight)

  $g.FillRectangle($bannerBrush, $x, $y, $cellWidth, $headerHeight)
  $g.DrawString($labels[$i], $font, $brush, ($x + 16), ($y + 12))

  $imgPath = Join-Path $claudeDir $stills[$i]
  if (Test-Path $imgPath) {
    $img = [System.Drawing.Image]::FromFile($imgPath)
    $g.DrawImage($img, $x, ($y + $headerHeight), $cellWidth, $cellHeight)
    $img.Dispose()
  }
}

$sheetPath = Join-Path $claudeDir "CLAUDE_PERSIAN_CONTACT_SHEET.png"
$sheetBmp.Save($sheetPath, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$sheetBmp.Dispose()
Write-Host "Created $sheetPath"
