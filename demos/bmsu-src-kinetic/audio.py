# -*- coding: utf-8 -*-
"""
BMSU Student Research & Technology Committee — Cinematic Kinetic Master Soundtrack
MGAudio procedural synthesis + Master Persian Voiceover + Frame-Accurate Procedural SFX
Mastered to EBU R128 (-14 LUFS integrated, True Peak <= -1.1 dBTP)
"""
import sys
import os
import json
import numpy as np
import soundfile as sf
import scipy.signal

HERE = os.path.dirname(os.path.abspath(__file__))
ROOT = os.path.abspath(os.path.join(HERE, '..', '..'))
sys.path.insert(0, os.path.join(ROOT, 'lib', 'audio'))

import mgaudio as mg
from mgaudio import recipes, sfx, synth, samples

cues_path = os.path.join(HERE, 'cues.json')
with open(cues_path, 'r', encoding='utf-8') as f:
    cues = json.load(f)

FR = cues['frames']
T = lambda k: FR[k] / 30.0
F = lambda n: n / 30.0
TOTAL_DUR = cues.get('duration', 64.0)

# 1. Procedural soundtrack bed calibrated to D minor
m = recipes.explainer(
    duration=TOTAL_DUR,
    bpm=cues['bpm'],
    key=cues['key'],
    mode=cues['mode'],
    build=cues.get('build', 42.0),
    drop=cues.get('drop', 46.5),
    outro=cues.get('outro', 59.5),
    music_level=-22.0,
    sfx_duck=4.0
)

# 2. Add and master the voiceover track
voice_path = os.path.join(ROOT, 'public', 'audio', 'bmsu_intro_clip_master_voice.wav')
if os.path.exists(voice_path):
    v_data, v_sr = sf.read(voice_path, dtype='float32')
    if v_sr != 48000:
        num_s = int(len(v_data) * 48000 / v_sr)
        v_data = scipy.signal.resample(v_data, num_s).astype(np.float32)
    if v_data.ndim == 1:
        v_data = np.stack([v_data, v_data], axis=-1)
    
    # Clip or pad to duration
    target_samples = int(TOTAL_DUR * 48000)
    if len(v_data) > target_samples:
        v_data = v_data[:target_samples]
    
    vox_sound = mg.Sound(v_data)
    vox_track = m.track('voiceover', level=-14.0, group='voice')
    vox_track.add(vox_sound, 0.0)
    print(f"[audio.py] Loaded master voiceover: {len(v_data)/48000:.2f}s")

# 3. Duck background music tracks when voiceover is speaking
for trk_name in ('pad', 'arp', 'chords', 'lead', 'saw'):
    if trk_name in m.tracks:
        try:
            m[trk_name].duck(by='voiceover', depth=5.5, release=0.25)
        except Exception:
            pass

# 4. Attach frame-accurate procedural SFX
m.sfx(sfx.impact('trailer'), at=T('hook_burst'), gain=0.0)
m.sfx(sfx.whoosh(0.42, 'swish', direction=1, peak=0.4), at=T('hook_punch'), gain=-6.0)
m.sfx(sfx.whoosh(0.50, 'air', direction=1, peak=0.5), at=T('title_slam'), gain=-8.0)

# Stars launch
m.sfx(sfx.pop('mouth', pitch=0.85), at=T('stars_launch'), gain=-4.0)
m.sfx(sfx.sparkle(0.7, key='D'), at=T('stars_lock'), gain=-8.0)

# Counter & Photo 1
m.sfx(sfx.whoosh(0.45, 'air', direction=1, peak=0.5), at=T('counter_launch'), gain=-7.0)
m.sfx(sfx.impact('soft'), at=T('photo1_reveal'), gain=-6.0)

# Pillars of authority morph
m.sfx(sfx.transition(0.55, 'swish_pop'), at=T('pillars_morph'), gain=-6.0)
m.sfx(sfx.sparkle(0.6, key='D'), at=T('pillars_nodes'), gain=-9.0)

# 1395 Milad & Lancet
m.sfx(sfx.whoosh(0.40, 'swish', direction=1, peak=0.5), at=T('nephro_launch'), gain=-7.0)
m.sfx(sfx.shimmer_hit('D5'), at=T('photo2_reveal'), gain=-8.0)

# Shanghai Citation Leap
m.sfx(sfx.whoosh(0.60, 'air', direction=1, peak=0.6), at=T('shanghai_rise'), gain=-8.0)
m.sfx(sfx.impact('soft'), at=T('photo3_reveal'), gain=-7.0)

# COVID-19 & General Salami plaque
m.sfx(sfx.impact('cinematic'), at=T('covid_impact'), gain=-3.0)
m.sfx(sfx.pop('crisp', pitch=0.9), at=T('photo4_reveal'), gain=-6.0)

# Macro-Region 10 Secretariat
m.sfx(sfx.whoosh(0.48, 'swish', direction=1, peak=0.5), at=T('region10_launch'), gain=-7.0)
m.sfx(sfx.sparkle(0.8, key='D'), at=T('photo5_reveal'), gain=-9.0)

# 24th National Annual Congress
m.sfx(sfx.impact('cinematic'), at=T('congress24_blast'), gain=-4.0)
m.sfx(sfx.transition(0.50, 'swish_pop'), at=T('photo6_reveal'), gain=-6.0)

# Noora Vaccine Clinical Trial
m.sfx(sfx.whoosh(0.45, 'swish', direction=1, peak=0.5), at=T('noora_vaccine'), gain=-6.0)
m.sfx(sfx.shimmer_hit('A5'), at=T('photo7_reveal'), gain=-8.0)

# Geneva World Medal
m.sfx(sfx.sparkle(1.0, key='D'), at=T('geneva_medal'), gain=-6.0)
m.sfx(sfx.pop('crisp', pitch=1.1), at=T('photo8_reveal'), gain=-6.0)

# Golden Statues
m.sfx(sfx.impact('cinematic'), at=T('gold_trophies'), gain=-3.0)
m.sfx(sfx.sparkle(0.9, key='D'), at=T('photo9_reveal'), gain=-7.0)

# Clause K Elites Stagger
m.sfx(sfx.whoosh(0.55, 'air', direction=1, peak=0.5), at=T('elites_launch'), gain=-7.0)
stagger_start = FR['elites_stagger_start']
for idx in range(13):
    f_pop = stagger_start + idx * 7
    if f_pop < FR['elites_stagger_end']:
        m.sfx(sfx.pop('bubble', pitch=0.9 + 0.05 * (idx % 6)), at=F(f_pop), gain=-12.0)

# Future Horizon
m.sfx(sfx.whoosh(0.70, 'air', direction=1, peak=0.6), at=T('future_ai'), gain=-6.0)
m.sfx(sfx.shimmer_hit('D5'), at=T('future_build'), gain=-8.0)

# Logomotion Finale & Living Hold
m.sfx(sfx.transition(0.75, 'swish_pop'), at=T('logomotion_start'), gain=-5.0)
m.sfx(sfx.shimmer_hit('D6'), at=T('brand_lockup'), gain=-6.0)
m.sfx(sfx.sparkle(1.2, key='D'), at=T('brand_lockup') + F(5), gain=-8.0)

# 5. Export Master Audio
out_dir = os.path.join(HERE, 'out')
os.makedirs(out_dir, exist_ok=True)
out_wav = os.path.join(out_dir, 'audio.wav')

print(f"[audio.py] Rendering master audio ({TOTAL_DUR}s)...")
rep = m.export(out_wav)
print(f"[audio.py] Done export: {out_wav}")
print(f"[audio.py] EBU R128 Loudness: {rep.get('lufs', 'N/A')} LUFS | True Peak: {rep.get('true_peak', 'N/A')} dBTP")
