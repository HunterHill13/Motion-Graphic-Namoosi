"""
Generate Three Diverse High-Quality Cinematic Musical Candidates (v3.1)
Candidate A: Cinematic Scientific Ambient (Deep sub-bass, organic breathing pad, evolving analog filter)
Candidate B: Futuristic Scientific Electronic (Clockwork pulse, arpeggiated drive, rising harmonic tension)
Candidate C: Energetic Cinematic Science (Hybrid orchestral swell, dramatic sub-impact drops, climactic resolution)
"""

import numpy as np
import wave
from pathlib import Path

def create_stereo_wav(filename: str, left: np.ndarray, right: np.ndarray, sample_rate: int = 44100):
    left_pcm = np.clip(left * 32767, -32768, 32767).astype(np.int16)
    right_pcm = np.clip(right * 32767, -32768, 32767).astype(np.int16)
    stereo = np.empty((len(left_pcm) * 2,), dtype=np.int16)
    stereo[0::2] = left_pcm
    stereo[1::2] = right_pcm

    p = Path(filename)
    p.parent.mkdir(parents=True, exist_ok=True)
    with wave.open(str(p), 'wb') as wf:
        wf.setnchannels(2)
        wf.setsampwidth(2)
        wf.setframerate(sample_rate)
        wf.writeframes(stereo.tobytes())
    print(f"Generated candidate: {filename}")

def build_candidates(duration_sec: float = 35.0, sample_rate: int = 44100):
    total_samples = int(duration_sec * sample_rate)
    t = np.linspace(0, duration_sec, total_samples, endpoint=False)
    
    # Standard smooth fade envelopes
    env = np.ones(total_samples, dtype=np.float32)
    fade_in = int(2.0 * sample_rate)
    fade_out = int(3.5 * sample_rate)
    env[:fade_in] = np.linspace(0, 1, fade_in)
    env[-fade_out:] = np.linspace(1, 0, fade_out)

    # -------------------------------------------------------------
    # Candidate A: Cinematic Scientific Ambient (Organic, Evolving)
    # -------------------------------------------------------------
    # Deep fundamental D1 (36.7 Hz) + D2 (73.4 Hz)
    sub_a = np.sin(2 * np.pi * 36.7 * t) * 0.40
    # Breathing fifth (A2 = 110 Hz)
    lfo_a = 0.5 + 0.5 * np.sin(2 * np.pi * 0.15 * t)
    fifth_a = np.sin(2 * np.pi * 110.0 * t) * 0.25 * lfo_a
    # Warm pad chords (D3, F3, A3)
    pad_a = (
        np.sin(2 * np.pi * 146.8 * t) * 0.18 +
        np.sin(2 * np.pi * 174.6 * t + 0.4) * 0.15 +
        np.sin(2 * np.pi * 220.0 * t + 0.9) * 0.12
    )
    # Sub-harmonic shimmer
    shimmer_a = np.sin(2 * np.pi * 587.3 * t) * (np.sin(2 * np.pi * 0.5 * t)**4) * 0.05
    left_a = (sub_a + fifth_a * 0.85 + pad_a * 0.9 + shimmer_a) * env * 0.5
    right_a = (sub_a + fifth_a * 1.1 + pad_a * 0.85 + shimmer_a * 1.2) * env * 0.5
    create_stereo_wav("audio/music/candidate_a_ambient.wav", left_a, right_a, sample_rate)

    # -------------------------------------------------------------
    # Candidate B: Futuristic Scientific Electronic (Rhythmic, Modular)
    # -------------------------------------------------------------
    # Root C2 (65.4 Hz) with rhythmic 92 BPM clock pulse
    bpm_b = 92.0 / 60.0
    pulse_b = (np.sin(2 * np.pi * bpm_b * t) ** 18)
    sub_b = (np.sin(2 * np.pi * 65.4 * t) * 0.35) * (0.7 + 0.3 * pulse_b)
    # Arpeggiator notes cycling through C3, Eb3, G3, Bb3
    arp_rate = bpm_b * 4 # 16th notes
    arp_step = np.floor(t * arp_rate) % 4
    arp_freq = np.where(arp_step == 0, 130.8,
               np.where(arp_step == 1, 155.6,
               np.where(arp_step == 2, 196.0, 233.1)))
    arp_sound = np.sin(2 * np.pi * arp_freq * t) * 0.15 * (np.sin(2 * np.pi * arp_rate * t)**2)
    left_b = (sub_b + arp_sound * 0.9) * env * 0.45
    right_b = (sub_b + arp_sound * 1.1) * env * 0.45
    create_stereo_wav("audio/music/candidate_b_electronic.wav", left_b, right_b, sample_rate)

    # -------------------------------------------------------------
    # Candidate C: Energetic Cinematic Science (Hybrid Arc: Tension -> Climax)
    # -------------------------------------------------------------
    # Dynamic tension builder with dramatic crescendos at t = 10s and t = 22s
    crescendo = 0.6 + 0.4 * (t / duration_sec)
    sub_c = np.sin(2 * np.pi * 43.65 * t) * 0.38 * crescendo # F1
    # Low strings drone
    cellos = (np.sin(2 * np.pi * 87.3 * t) * 0.22 + np.sin(2 * np.pi * 130.8 * t) * 0.18) * crescendo
    # High celestial tension harmonics
    high_harmonics = np.sin(2 * np.pi * 698.4 * t) * 0.08 * (0.3 + 0.7 * (t / duration_sec)**2)
    # Climactic pulse impacts at 7.0s, 14.5s, 22.0s
    impact_pulse = np.zeros_like(t)
    for hit_t in [7.0, 14.5, 22.0]:
        hit_dist = np.abs(t - hit_t)
        hit_wave = np.exp(-hit_dist * 8.0) * np.sin(2 * np.pi * 55.0 * t) * 0.3
        impact_pulse += hit_wave

    left_c = (sub_c + cellos * 0.9 + high_harmonics * 0.8 + impact_pulse) * env * 0.5
    right_c = (sub_c + cellos * 1.05 + high_harmonics * 1.1 + impact_pulse) * env * 0.5
    create_stereo_wav("audio/music/candidate_c_cinematic_arc.wav", left_c, right_c, sample_rate)
    # Also save Candidate C as the upgraded master music asset
    create_stereo_wav("public/music/scientific_ambient_pulse.wav", left_c, right_c, sample_rate)
    print("Candidate C chosen as primary upgraded underscore for production.")

if __name__ == "__main__":
    build_candidates()
