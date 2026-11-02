Add-Type -AssemblyName System.Drawing

$benchmarkDir = Join-Path (Get-Location) "renders\benchmark"

# -----------------------------------------------------------------------------
# 1. NARRATIVE CONTACT SHEET (3x3 GRID OF 9 SHOTS)
# -----------------------------------------------------------------------------
$stills = @(
  "00_establish.png",
  "01_anticipation.png",
  "02_deformation.png",
  "03_rupture.png",
  "04_fragmentation.png",
  "05_secondary_response.png",
  "06_motion_carry.png",
  "07_reassembly.png",
  "08_resolution.png"
)

$labels = @(
  "SHOT 01: ESTABLISH (f30)",
  "SHOT 02: ANTICIPATION (f150)",
  "SHOT 02: DEFORMATION (f200)",
  "SHOT 03: RUPTURE (f240)",
  "SHOT 04: FRAGMENTATION (f320)",
  "SHOT 04: SECONDARY RESPONSE (f370)",
  "SHOT 05: TRACKING & CARRY (f450)",
  "SHOT 07: REASSEMBLY (f550)",
  "SHOT 08: RESOLUTION (f680)"
)

$cellWidth = 640
$cellHeight = 360
$headerHeight = 40
$gridWidth = $cellWidth * 3
$gridHeight = ($cellHeight + $headerHeight) * 3

$sheetBmp = New-Object System.Drawing.Bitmap($gridWidth, $gridHeight)
$g = [System.Drawing.Graphics]::FromImage($sheetBmp)
$g.Clear([System.Drawing.Color]::FromArgb(15, 23, 42))

$font = New-Object System.Drawing.Font("Arial", 14, [System.Drawing.FontStyle]::Bold)
$brush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
$bannerBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(30, 41, 59))

for ($i = 0; $i -lt 9; $i++) {
  $col = $i % 3
  $row = [Math]::Floor($i / 3)
  $x = $col * $cellWidth
  $y = $row * ($cellHeight + $headerHeight)

  # Header label
  $g.FillRectangle($bannerBrush, $x, $y, $cellWidth, $headerHeight)
  $g.DrawString($labels[$i], $font, $brush, ($x + 12), ($y + 8))

  # Image
  $imgPath = Join-Path $benchmarkDir $stills[$i]
  if (Test-Path $imgPath) {
    $img = [System.Drawing.Image]::FromFile($imgPath)
    $g.DrawImage($img, $x, ($y + $headerHeight), $cellWidth, $cellHeight)
    $img.Dispose()
  }
}

$sheetPath = Join-Path $benchmarkDir "CINEMATIC_BENCHMARK_CONTACT_SHEET.png"
$sheetBmp.Save($sheetPath, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$sheetBmp.Dispose()
Write-Host "Created $sheetPath"

# -----------------------------------------------------------------------------
# 2. ABLATION CONTACT SHEET (7 MODES)
# -----------------------------------------------------------------------------
$ablationStills = @(
  "ablation_full.png",
  "ablation_no_secondary.png",
  "ablation_no_depth.png",
  "ablation_no_camera.png",
  "ablation_no_material.png",
  "ablation_no_lighting.png",
  "ablation_no_carry.png"
)

$ablationLabels = @(
  "MODE 1: FULL SYSTEM (All Layers Active)",
  "MODE 2: NO SECONDARY (Lag & Follow-Through Collapsed)",
  "MODE 3: NO DEPTH (Flat Z=0.5, No Parallax)",
  "MODE 4: NO CAMERA (Static Zoom=1, No Orbit/Punch)",
  "MODE 5: NO MATERIAL (Flat Monochrome Graphic)",
  "MODE 6: NO LIGHTING (Flat Ambient White 1.0)",
  "MODE 7: NO CARRY (Handoff Velocity Clamped to 0)"
)

$ablCols = 4
$ablRows = 2
$ablGridWidth = $cellWidth * $ablCols
$ablGridHeight = ($cellHeight + $headerHeight) * $ablRows

$ablBmp = New-Object System.Drawing.Bitmap($ablGridWidth, $ablGridHeight)
$gAbl = [System.Drawing.Graphics]::FromImage($ablBmp)
$gAbl.Clear([System.Drawing.Color]::FromArgb(15, 23, 42))

for ($i = 0; $i -lt 7; $i++) {
  $col = $i % $ablCols
  $row = [Math]::Floor($i / $ablCols)
  $x = $col * $cellWidth
  $y = $row * ($cellHeight + $headerHeight)

  $gAbl.FillRectangle($bannerBrush, $x, $y, $cellWidth, $headerHeight)
  $gAbl.DrawString($ablationLabels[$i], $font, $brush, ($x + 10), ($y + 8))

  $imgPath = Join-Path $benchmarkDir $ablationStills[$i]
  if (Test-Path $imgPath) {
    $img = [System.Drawing.Image]::FromFile($imgPath)
    $gAbl.DrawImage($img, $x, ($y + $headerHeight), $cellWidth, $cellHeight)
    $img.Dispose()
  }
}

$ablSheetPath = Join-Path $benchmarkDir "CINEMATIC_BENCHMARK_ABLATION_CONTACT_SHEET.png"
$ablBmp.Save($ablSheetPath, [System.Drawing.Imaging.ImageFormat]::Png)
$gAbl.Dispose()
$ablBmp.Dispose()
Write-Host "Created $ablSheetPath"
