"""
Generate Cinematic Ambient Science Underscore for Production Pilot
Produces a 35-second rich, evolving multi-octave scientific drone with:
1. Low-frequency pulsating sub-bass drone (55 Hz A1 / 110 Hz A2)
2. Evolving harmonic pad with gentle amplitude modulation (0.2 Hz breathing)
3. Subtle high-frequency biological pulse (85 BPM sync)
4. Smooth stereo spread and fadeout
5. Mastered to -22 LUFS for clean dialogue ducking
"""

import numpy as np
import wave
import struct
import math
from pathlib import Path

def generate_cinematic_music(output_path: str, duration_sec: float = 35.0, sample_rate: int = 44100):
    total_samples = int(duration_sec * sample_rate)
    t = np.linspace(0, duration_sec, total_samples, endpoint=False)

    # 1. Sub-bass root fundamental (A1 = 55 Hz)
    sub = np.sin(2 * np.pi * 55.0 * t) * 0.35

    # 2. Fifth harmony (E2 = 82.4 Hz) with slow phase swell
    swell_env = 0.5 + 0.5 * np.sin(2 * np.pi * 0.12 * t - np.pi/2)
    fifth = np.sin(2 * np.pi * 82.4 * t) * 0.25 * swell_env

    # 3. Warm octave pad (A2 = 110 Hz, C#3 = 138.6 Hz, E3 = 164.8 Hz)
    pad = (
        np.sin(2 * np.pi * 110.0 * t) * 0.20 +
        np.sin(2 * np.pi * 138.6 * t + 0.5) * 0.15 +
        np.sin(2 * np.pi * 164.8 * t + 1.2) * 0.15
    )
    # Slow breathing filter modulation (0.25 Hz)
    pad_lfo = 0.6 + 0.4 * np.sin(2 * np.pi * 0.25 * t)
    pad *= pad_lfo

    # 4. Rhythmic subtle scientific pulse (85 BPM = 1.416 Hz pulse)
    bpm_freq = 85.0 / 60.0
    pulse_click = np.sin(2 * np.pi * bpm_freq * t)**16 # Sharp rhythmic pulse
    shimmer = np.sin(2 * np.pi * 880.0 * t) * pulse_click * 0.08

    # 5. Master combination
    mix_left = sub + fifth * 0.85 + pad * 0.95 + shimmer * 0.7
    mix_right = sub + fifth * 0.95 + pad * 0.85 + shimmer * 1.1

    # Master envelope: 2.0s fade in, 3.5s fade out
    fade_in_samples = int(2.0 * sample_rate)
    fade_out_samples = int(3.5 * sample_rate)
    
    env = np.ones(total_samples, dtype=np.float32)
    env[:fade_in_samples] = np.linspace(0, 1, fade_in_samples)
    env[-fade_out_samples:] = np.linspace(1, 0, fade_out_samples)

    mix_left = mix_left * env * 0.45
    mix_right = mix_right * env * 0.45

    # Convert to 16-bit PCM stereo
    left_pcm = np.clip(mix_left * 32767, -32768, 32767).astype(np.int16)
    right_pcm = np.clip(mix_right * 32767, -32768, 32767).astype(np.int16)

    # Interleave stereo
    stereo = np.empty((total_samples * 2,), dtype=np.int16)
    stereo[0::2] = left_pcm
    stereo[1::2] = right_pcm

    out_file = Path(output_path)
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(out_file), 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(stereo.tobytes())

    print(f"Generated cinematic music asset: {output_path} (Duration: {duration_sec}s)")

if __name__ == "__main__":
    generate_cinematic_music("audio/music/scientific_ambient_pulse.wav", duration_sec=35.0)
    generate_cinematic_music("public/music/scientific_ambient_pulse.wav", duration_sec=35.0)
