Add-Type -AssemblyName System.Drawing

$claudeDir = Join-Path $PSScriptRoot "..\renders\claude"
$claudeDir = [System.IO.Path]::GetFullPath($claudeDir)

$stills = @(
  "intro_act1_f220.png",
  "intro_act2_f480.png",
  "intro_act3_f950.png",
  "intro_act4_f1450.png"
)

$labels = @(
  "ACT 1 (X=0): GLASSMORPHIC MONOLITH & LIQUID SQUASH CLICK (f220)",
  "ACT 2 (X=1500): STOP-MOTION 4-STAGE STEPPER & ENLARGED MORPH (f480)",
  "ACT 3 (X=3000): BLUEPRINT CONSOLE WITH KINETIC BAR CHARTS (f950)",
  "ACT 4 (X=4300): GRAND DOCKED PAVILION & 100% GOLD CALIBRATION (f1450)"
)

$cellWidth = 960
$cellHeight = 540
$headerHeight = 44
$gridWidth = $cellWidth * 2
$gridHeight = ($cellHeight + $headerHeight) * 2

$sheetBmp = New-Object System.Drawing.Bitmap($gridWidth, $gridHeight)
$g = [System.Drawing.Graphics]::FromImage($sheetBmp)
$g.Clear([System.Drawing.Color]::FromArgb(2, 26, 20))

$font = New-Object System.Drawing.Font("Arial", 12, [System.Drawing.FontStyle]::Bold)
$brush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
$bannerBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(2, 44, 34))

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

$sheetPath = Join-Path $claudeDir "SKILL_INTRO_CONTACT_SHEET.png"
$sheetBmp.Save($sheetPath, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$sheetBmp.Dispose()
Write-Host "Created $sheetPath"
