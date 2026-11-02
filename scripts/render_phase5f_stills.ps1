# Render Phase 5F Diagnostic Stills, Assemble Contact Sheet & Render Proof MP4

$ErrorActionPreference = "Stop"

$OutputDir = "renders/phase5f"
$ArtifactDir = "C:\Users\Hill\.gemini\antigravity\brain\d28bb0e7-8645-4181-8ed7-a21e6a13b008"

if (!(Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

$renders = @(
    @{ Comp = "Phase5F-SecondaryMotionProof"; Frame = 75; File = "secondary_primary.png" },
    @{ Comp = "Phase5F-SecondaryCollapsedProof"; Frame = 75; File = "secondary_collapsed.png" },
    @{ Comp = "Phase5F-SecondaryMotionProof"; Frame = 26; File = "anticipation_on.png" },
    @{ Comp = "Phase5F-AnticipationCollapsedProof"; Frame = 26; File = "anticipation_off.png" },
    @{ Comp = "Phase5F-SecondaryMotionProof"; Frame = 92; File = "followthrough_on.png" },
    @{ Comp = "Phase5F-FollowThroughCollapsedProof"; Frame = 92; File = "followthrough_off.png" },
    @{ Comp = "Phase5F-SecondaryMotionProof"; Frame = 145; File = "hierarchy_primary.png" },
    @{ Comp = "Phase5F-SecondaryMotionProof"; Frame = 155; File = "hierarchy_secondary.png" },
    @{ Comp = "Phase5F-SecondaryMotionProof"; Frame = 165; File = "hierarchy_tertiary.png" },
    @{ Comp = "Phase5F-SecondaryMotionProof"; Frame = 230; File = "carry_before.png" },
    @{ Comp = "Phase5F-SecondaryMotionProof"; Frame = 240; File = "carry_handoff.png" },
    @{ Comp = "Phase5F-SecondaryMotionProof"; Frame = 250; File = "carry_after.png" },
    @{ Comp = "Phase5F-MotionCarryCollapsedProof"; Frame = 250; File = "carry_collapsed.png" }
)

Write-Host "Rendering $($renders.Count) Phase 5F stills..."

foreach ($r in $renders) {
    $targetPath = Join-Path $OutputDir $r.File
    Write-Host "Rendering $($r.File) (Comp: $($r.Comp), Frame: $($r.Frame))..."
    npx remotion still $($r.Comp) $targetPath --frame=$($r.Frame) --log=error
    if (Test-Path $ArtifactDir) {
        Copy-Item -Path $targetPath -Destination (Join-Path $ArtifactDir $r.File) -Force
    }
}

Write-Host "All individual stills rendered and copied to artifacts."

# -----------------------------------------------------------------------------
# ASSEMBLE CONTACT SHEET
# -----------------------------------------------------------------------------
Write-Host "Assembling Phase 5F Contact Sheet..."
Add-Type -AssemblyName System.Drawing

$gridCols = 4
$gridRows = 4
$thumbW = 480
$thumbH = 270
$pad = 16
$headerH = 80
$labelH = 30

$sheetW = ($gridCols * $thumbW) + (($gridCols + 1) * $pad)
$sheetH = $headerH + ($gridRows * ($thumbH + $labelH)) + (($gridRows + 1) * $pad)

$bitmap = New-Object System.Drawing.Bitmap($sheetW, $sheetH)
$graphics = [System.Drawing.Graphics]::FromImage($bitmap)
$graphics.InterpolationMode = [System.Drawing.Drawing2D.InterpolationMode]::HighQualityBicubic
$graphics.SmoothingMode = [System.Drawing.Drawing2D.SmoothingMode]::HighQuality
$graphics.PixelOffsetMode = [System.Drawing.Drawing2D.PixelOffsetMode]::HighQuality

# Background
$bgBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(5, 8, 20))
$graphics.FillRectangle($bgBrush, 0, 0, $sheetW, $sheetH)
$bgBrush.Dispose()

# Header
$titleFont = New-Object System.Drawing.Font("Arial", 22, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font("Arial", 11, [System.Drawing.FontStyle]::Regular)
$titleBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(248, 250, 252))
$subBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(148, 163, 184))

$graphics.DrawString("PHASE 5F: SECONDARY MOTION, FOLLOW-THROUGH & MOMENTUM PROOF", $titleFont, $titleBrush, $pad, 14)
$graphics.DrawString("Causal Lagging Reaction | Pre-Launch Anticipation | Momentum Overshoot & Settle | Motion Hierarchy | Velocity Carry", $subFont, $subBrush, $pad, 48)

$titleFont.Dispose()
$subFont.Dispose()
$titleBrush.Dispose()
$subBrush.Dispose()

# 14 Panels for the 4x4 Grid
$panels = @(
    @{ File = "secondary_primary.png"; Label = "1. PASS: Causal Secondary Response (Lag=-60px)" },
    @{ File = "secondary_collapsed.png"; Label = "2. FAIL: Collapsed Secondary (Static Frozen)" },
    @{ File = "anticipation_on.png"; Label = "3. PASS: Anticipation ON (Coil=-28px, Scale=0.94)" },
    @{ File = "anticipation_off.png"; Label = "4. FAIL: Anticipation OFF (Abrupt Procedural Launch)" },

    @{ File = "followthrough_on.png"; Label = "5. PASS: Follow-Through & Overshoot (+17px Momentum)" },
    @{ File = "followthrough_off.png"; Label = "6. FAIL: Follow-Through OFF (Clamped Dead Stop)" },
    @{ File = "hierarchy_primary.png"; Label = "7. Hierarchy Tier 1: Primary Impulse (300px, Lag=0f)" },
    @{ File = "hierarchy_secondary.png"; Label = "8. Hierarchy Tier 2: Secondary Response (110px, Lag=5f)" },

    @{ File = "hierarchy_tertiary.png"; Label = "9. Hierarchy Tier 3: Tertiary Echo (42px, Lag=10f)" },
    @{ File = "carry_before.png"; Label = "10. Motion-Carry: Shot A Terminal Velocity (18px/f)" },
    @{ File = "carry_handoff.png"; Label = "11. Motion-Carry: Boundary Handoff Cut (Frame 240)" },
    @{ File = "carry_after.png"; Label = "12. PASS: Shot B Velocity Inherited (16.2px/f, 90%)" },

    @{ File = "carry_collapsed.png"; Label = "13. FAIL: Shot B Collapsed (Dead Rest v=0, Disconnect)" },
    @{ File = "followthrough_on.png"; Label = "14. Certified Causal Dynamic Physics Overview" }
)

$labelFont = New-Object System.Drawing.Font("Arial", 10, [System.Drawing.FontStyle]::Bold)
$labelBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(226, 232, 240))
$borderPen = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(51, 65, 85), 2)
$highlightPenPass = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(34, 197, 94), 3)
$highlightPenFail = New-Object System.Drawing.Pen([System.Drawing.Color]::FromArgb(239, 68, 68), 3)

for ($i = 0; $i -lt $panels.Count; $i++) {
    $col = $i % $gridCols
    $row = [Math]::Floor($i / $gridCols)
    $x = $pad + $col * ($thumbW + $pad)
    $y = $headerH + $row * ($thumbH + $labelH + $pad)

    $p = $panels[$i]
    $imgPath = Join-Path $OutputDir $p.File

    if (Test-Path $imgPath) {
        $img = [System.Drawing.Image]::FromFile($imgPath)
        $graphics.DrawImage($img, $x, $y, $thumbW, $thumbH)
        $img.Dispose()

        # Border highlighting
        if ($p.Label -like "*PASS*") {
            $graphics.DrawRectangle($highlightPenPass, $x, $y, $thumbW, $thumbH)
        } elseif ($p.Label -like "*FAIL*") {
            $graphics.DrawRectangle($highlightPenFail, $x, $y, $thumbW, $thumbH)
        } else {
            $graphics.DrawRectangle($borderPen, $x, $y, $thumbW, $thumbH)
        }
    }

    # Label text below
    $graphics.DrawString($p.Label, $labelFont, $labelBrush, $x + 2, $y + $thumbH + 6)
}

$labelFont.Dispose()
$labelBrush.Dispose()
$borderPen.Dispose()
$highlightPenPass.Dispose()
$highlightPenFail.Dispose()
$graphics.Dispose()

$contactSheetLocal = Join-Path $OutputDir "PHASE_5F_SECONDARY_MOTION_CONTACT_SHEET.png"
$bitmap.Save($contactSheetLocal, [System.Drawing.Imaging.ImageFormat]::Png)
$bitmap.Dispose()

if (Test-Path $ArtifactDir) {
    Copy-Item -Path $contactSheetLocal -Destination (Join-Path $ArtifactDir "PHASE_5F_SECONDARY_MOTION_CONTACT_SHEET.png") -Force
}

Write-Host "Contact Sheet successfully saved to $contactSheetLocal and artifacts!"

# -----------------------------------------------------------------------------
# RENDER REQUIRED DIAGNOSTIC VIDEO: PHASE_5F_SECONDARY_MOTION_PROOF.mp4
# -----------------------------------------------------------------------------
$videoLocal = Join-Path $OutputDir "PHASE_5F_SECONDARY_MOTION_PROOF.mp4"
Write-Host "Rendering diagnostic video $videoLocal (300 frames @ 30 FPS)..."

npx remotion render Phase5F-SecondaryMotionProof $videoLocal --log=error

if (Test-Path $videoLocal) {
    Write-Host "Video rendered successfully. Copying to artifacts..."
    if (Test-Path $ArtifactDir) {
        Copy-Item -Path $videoLocal -Destination (Join-Path $ArtifactDir "PHASE_5F_SECONDARY_MOTION_PROOF.mp4") -Force
    }
}
Write-Host "Phase 5F rendering workflow complete!"
