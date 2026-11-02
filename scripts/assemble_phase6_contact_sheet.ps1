Add-Type -AssemblyName System.Drawing

$phase6Dir = Join-Path (Get-Location) "renders\phase6"

$stills = @(
  "p6_shot1_f45.png",
  "p6_shot2_f165.png",
  "p6_shot3_f192.png",
  "p6_shot4_f285.png",
  "p6_shot5_f390.png"
)

$labels = @(
  "SHOT 1: THE LIVING MICROCOSM (f45) - Cytoplasmic Respiration & Eukaryotic Morphology",
  "SHOT 2: KINETIC VECTOR & TENSION (f165) - Retrograde Coil, Indentation & Shockwave",
  "SHOT 3: ASYMMETRIC RUPTURE (f192) - Cavitation Flash, Cleavage Furrow & Spindle Recoil",
  "SHOT 4: DEEP PARALLAX FLIGHT (f285) - Lead Room Framing & Secondary Lag Offset",
  "SHOT 5: HARMONIC EQUILIBRIUM (f390) - Centripetal Settle & Mature Organelle Core"
)

# 3 columns layout: 2 rows (row 1 has 3 shots, row 2 has 2 shots + 1 summary card)
$cellWidth = 640
$cellHeight = 360
$headerHeight = 44
$gridWidth = $cellWidth * 3
$gridHeight = ($cellHeight + $headerHeight) * 2

$sheetBmp = New-Object System.Drawing.Bitmap($gridWidth, $gridHeight)
$g = [System.Drawing.Graphics]::FromImage($sheetBmp)
$g.Clear([System.Drawing.Color]::FromArgb(2, 6, 23))

$font = New-Object System.Drawing.Font("Arial", 11, [System.Drawing.FontStyle]::Bold)
$titleFont = New-Object System.Drawing.Font("Arial", 16, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font("Arial", 11, [System.Drawing.FontStyle]::Regular)
$brush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::White)
$cyanBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(56, 189, 248))
$bannerBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(15, 23, 42))
$cardBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(10, 18, 38))

for ($i = 0; $i -lt 5; $i++) {
  $col = $i % 3
  $row = [Math]::Floor($i / 3)
  $x = $col * $cellWidth
  $y = $row * ($cellHeight + $headerHeight)

  # Header label
  $g.FillRectangle($bannerBrush, $x, $y, $cellWidth, $headerHeight)
  $g.DrawString($labels[$i], $font, $brush, ($x + 12), ($y + 12))

  # Image
  $imgPath = Join-Path $phase6Dir $stills[$i]
  if (Test-Path $imgPath) {
    $img = [System.Drawing.Image]::FromFile($imgPath)
    $g.DrawImage($img, $x, ($y + $headerHeight), $cellWidth, $cellHeight)
    $img.Dispose()
  }
}

# Slot 6 (Row 1 Col 2): Summary Specification Card
$cardX = 2 * $cellWidth
$cardY = 1 * ($cellHeight + $headerHeight)

$g.FillRectangle($bannerBrush, $cardX, $cardY, $cellWidth, $headerHeight)
$g.DrawString("PHASE 6 VISUAL DIRECTOR: SPECIFICATION & AUDIT", $font, $cyanBrush, ($cardX + 12), ($cardY + 12))

$g.FillRectangle($cardBrush, $cardX, ($cardY + $headerHeight), $cellWidth, $cellHeight)
$cardG = [System.Drawing.Graphics]::FromImage($sheetBmp)

$summaryLines = @(
  "SEQUENCE SPECIFICATIONS:",
  "- Total Duration: 420 Frames (14.0 Seconds @ 30 FPS)",
  "- Resolution: 1920 x 1080 (Landscape FHD)",
  "- Visual Standard: True Pictorial Biological Authorship",
  "",
  "ARTISTIC AUDIT & HARDENING:",
  "- Zero Cartoon Eyeball / Plastic Button Primitives",
  "- True Eukaryotic Architecture: Chromatin, Nucleoli, Cristae",
  "- Layered Translucent Phospholipid Bilayer & Glycocalyx Cilia",
  "- Dynamic Undulating Shockwave with Ion Dispersion",
  "- Mitotic Spindle Apparatus with Cleavage Furrow Tension",
  "- Multi-tier Collagen Matrix with Parallax Depth Haze"
)

$lineY = $cardY + $headerHeight + 24
foreach ($line in $summaryLines) {
  if ($line.StartsWith("-") -or $line -eq "") {
    $g.DrawString($line, $subFont, $brush, ($cardX + 24), $lineY)
  } else {
    $g.DrawString($line, $font, $cyanBrush, ($cardX + 24), $lineY)
  }
  $lineY += 26
}

$sheetPath = Join-Path $phase6Dir "PHASE6_VISUAL_BENCHMARK_CONTACT_SHEET.png"
$sheetBmp.Save($sheetPath, [System.Drawing.Imaging.ImageFormat]::Png)
$g.Dispose()
$sheetBmp.Dispose()
Write-Host "Created $sheetPath"
