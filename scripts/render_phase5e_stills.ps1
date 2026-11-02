# Render Phase 5E Diagnostic Stills and Assemble Contact Sheet

$ErrorActionPreference = "Stop"

$OutputDir = "renders/phase5e"
$ArtifactDir = "C:\Users\Hill\.gemini\antigravity\brain\d28bb0e7-8645-4181-8ed7-a21e6a13b008"

if (!(Test-Path $OutputDir)) {
    New-Item -ItemType Directory -Path $OutputDir -Force | Out-Null
}

$renders = @(
    @{ Comp = "Phase5E-CameraProof"; Frame = 0; File = "camera_static.png" },
    @{ Comp = "Phase5E-CameraProof"; Frame = 20; File = "camera_push_in_start.png" },
    @{ Comp = "Phase5E-CameraProof"; Frame = 35; File = "camera_push_in_mid.png" },
    @{ Comp = "Phase5E-CameraProof"; Frame = 54; File = "camera_push_in_end.png" },
    @{ Comp = "Phase5E-CameraProof"; Frame = 55; File = "camera_pull_out_start.png" },
    @{ Comp = "Phase5E-CameraProof"; Frame = 85; File = "camera_pull_out_end.png" },
    @{ Comp = "Phase5E-CameraProof"; Frame = 55; File = "camera_orbit_start.png" },
    @{ Comp = "Phase5E-CameraProof"; Frame = 72; File = "camera_orbit_mid.png" },
    @{ Comp = "Phase5E-CameraProof"; Frame = 89; File = "camera_orbit_end.png" },
    @{ Comp = "Phase5E-CameraStaticProof"; Frame = 120; File = "camera_tracking_static.png" },
    @{ Comp = "Phase5E-CameraProof"; Frame = 120; File = "camera_tracking_active.png" },
    @{ Comp = "Phase5E-CameraProof"; Frame = 90; File = "camera_lead_room_before.png" },
    @{ Comp = "Phase5E-CameraProof"; Frame = 130; File = "camera_lead_room_after.png" },
    @{ Comp = "Phase5E-CameraProof"; Frame = 180; File = "camera_parallax.png" },
    @{ Comp = "Phase5E-CameraProof"; Frame = 45; File = "camera_depth_push.png" },
    @{ Comp = "Phase5E-CameraProof"; Frame = 295; File = "camera_exit.png" },
    @{ Comp = "Phase5E-CameraProof"; Frame = 265; File = "camera_motion_carry_a.png" },
    @{ Comp = "Phase5E-CameraProof"; Frame = 280; File = "camera_motion_carry_b.png" },
    @{ Comp = "Phase5E-CameraProof"; Frame = 215; File = "camera_punctuation_before.png" },
    @{ Comp = "Phase5E-CameraProof"; Frame = 229; File = "camera_punctuation_event.png" },
    @{ Comp = "Phase5E-CameraProof"; Frame = 245; File = "camera_punctuation_after.png" },
    @{ Comp = "Phase5E-CameraGlobalTransformProof"; Frame = 180; File = "camera_global_transform.png" },
    @{ Comp = "Phase5E-CameraProof"; Frame = 180; File = "camera_spatial_camera.png" }
)

Write-Host "Rendering $($renders.Count) Phase 5E stills..."

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
Write-Host "Assembling Phase 5E Contact Sheet..."
Add-Type -AssemblyName System.Drawing

$gridCols = 4
$gridRows = 5
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
$bgBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(10, 15, 29))
$graphics.FillRectangle($bgBrush, 0, 0, $sheetW, $sheetH)
$bgBrush.Dispose()

# Header
$titleFont = New-Object System.Drawing.Font("Arial", 22, [System.Drawing.FontStyle]::Bold)
$subFont = New-Object System.Drawing.Font("Arial", 11, [System.Drawing.FontStyle]::Regular)
$titleBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(248, 250, 252))
$subBrush = New-Object System.Drawing.SolidBrush([System.Drawing.Color]::FromArgb(148, 163, 184))

$graphics.DrawString("PHASE 5E: CINEMATIC CAMERA & COMPOSITION RUNTIME PROOF", $titleFont, $titleBrush, $pad, 14)
$graphics.DrawString("2.5D Depth-Aware Camera Projection vs Flat Global Transform | Depth Parallax | Focal Orbit | Lead Room | Punctuation", $subFont, $subBrush, $pad, 48)

$titleFont.Dispose()
$subFont.Dispose()
$titleBrush.Dispose()
$subBrush.Dispose()

# 20 Selected Diagnostic Panels for the 4x5 Grid
$panels = @(
    @{ File = "camera_static.png"; Label = "1. Static Control (Frame 0)" },
    @{ File = "camera_push_in_start.png"; Label = "2. Push-In Start (Frame 20)" },
    @{ File = "camera_push_in_mid.png"; Label = "3. Push-In Mid (Frame 35)" },
    @{ File = "camera_push_in_end.png"; Label = "4. Push-In Climax (Frame 54)" },

    @{ File = "camera_orbit_start.png"; Label = "5. Orbit Pivot Start (Frame 55)" },
    @{ File = "camera_orbit_mid.png"; Label = "6. Orbit Peak Angle (Frame 72)" },
    @{ File = "camera_orbit_end.png"; Label = "7. Orbit Recovered (Frame 89)" },
    @{ File = "camera_pull_out_end.png"; Label = "8. Pull-Out Wide Context (Frame 85)" },

    @{ File = "camera_lead_room_before.png"; Label = "9. Tracking Start (Frame 90)" },
    @{ File = "camera_lead_room_after.png"; Label = "10. Lead Room Ahead (Frame 130)" },
    @{ File = "camera_tracking_static.png"; Label = "11. Passive Camera (Drift Offscreen)" },
    @{ File = "camera_tracking_active.png"; Label = "12. Active Tracking (Centered Framing)" },

    @{ File = "camera_punctuation_before.png"; Label = "13. Pre-Impact Event (Frame 215)" },
    @{ File = "camera_punctuation_event.png"; Label = "14. Event Punctuation Punch (Frame 229)" },
    @{ File = "camera_punctuation_after.png"; Label = "15. Settle Recovery (Frame 245)" },
    @{ File = "camera_depth_push.png"; Label = "16. Depth Push Perspective (Frame 45)" },

    @{ File = "camera_motion_carry_a.png"; Label = "17. Motion-Carry Energy (Frame 265)" },
    @{ File = "camera_exit.png"; Label = "18. Entity World Exit (Frame 295)" },
    @{ File = "camera_global_transform.png"; Label = "19. FAIL: Flat Global Transform (Uniform)" },
    @{ File = "camera_spatial_camera.png"; Label = "20. PASS: Spatial Camera (True Parallax)" }
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

        # Border
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

$contactSheetLocal = Join-Path $OutputDir "PHASE_5E_CAMERA_CONTACT_SHEET.png"
$bitmap.Save($contactSheetLocal, [System.Drawing.Imaging.ImageFormat]::Png)
$bitmap.Dispose()

if (Test-Path $ArtifactDir) {
    Copy-Item -Path $contactSheetLocal -Destination (Join-Path $ArtifactDir "PHASE_5E_CAMERA_CONTACT_SHEET.png") -Force
}

Write-Host "Contact Sheet successfully saved to $contactSheetLocal and artifacts!"
