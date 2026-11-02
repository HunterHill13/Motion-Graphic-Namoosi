Add-Type -AssemblyName System.Drawing

$claudeDir = Join-Path (Get-Location) "renders\claude"

$stills = @(
  "cm_scene1_hook_f45.png",
  "cm_scene2_flow_f145.png",
  "cm_scene3_metrics_f255.png",
  "cm_scene4_climax_f335.png"
)

$labels = @(
  "SCENE 1: KINETIC HOOK & TITLE (f45) - Kinetic Typography & Spec Preview Card",
  "SCENE 2: ARCHITECTURE FLOW (f145) - Multi-Agent Federation & Conduit Pulses",
  "SCENE 3: METRIC VISUALIZER (f255) - Spring Counters, Gauge & Resource Breakdown",
  "SCENE 4: CLIMAX & CTA (f335) - Enterprise Synthesis & Deployed Action Container"
)

# 2x2 grid layout (1920 x 1080 total)
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

  # Header label
  $g.FillRectangle($bannerBrush, $x, $y, $cellWidth, $headerHeight)
  $g.DrawString($labels[$i], $font, $brush, ($x + 16), ($y + 12))

  # Image
  $imgPath = Join-Path $claudeDir $stills[$i]
  if (Test-Path $imgPath) {
    $img = [System.Drawing.Image]::FromFile($imgPath)
    $g.DrawImage($img, $x, ($y + $headerHeight), $cellWidth, $cellHeight)
    $img.Dispose()
  }
}

$sheetPath = Join-Path $claudeDir "CLAUDE_MOTION_CONTACT_SHEET.png"
$sheetBmp.Save($sheetPath, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$sheetBmp.Dispose()
Write-Host "Created $sheetPath"
