#!/usr/bin/env python3
"""Split the full FluidR3_GM files (gleitz/midi-js-soundfonts) into per-range files.

Usage: python3 trim_sounds.py ORIGINALS_DIR OUTPUT_DIR

ORIGINALS_DIR holds the originals (88 notes each), e.g.
  https://raw.githubusercontent.com/gleitz/midi-js-soundfonts/gh-pages/FluidR3_GM/violin-mp3.js

For every instrument except the bass guitar three files are written, one per training range
(MIDI note numbers, with 2 semitones of margin on each side):
  <name>_low-mp3.js   C1-B3   (24-59)  -> notes 22-61
  <name>_mid-mp3.js   E3-G5   (52-79)  -> notes 50-81
  <name>_high-mp3.js  G4-C7   (67-96)  -> notes 65-98
The bass guitar always plays E1-G3 (28-55), so it gets one file with notes 26-57.
Inside each file the JavaScript variable is renamed to match the file name, because the
local (file://) loader looks the data up by file name. Samples themselves are not changed.
Keep these ranges in step with RANGES in kamerton.html.
"""
import re, sys, os
NOTES = {'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def midi(name):
    m = re.match(r'^([A-G])([b#]?)(-?\d+)$', name)
    n = NOTES[m.group(1)] + (1 if m.group(2)=='#' else -1 if m.group(2)=='b' else 0)
    return 12*(int(m.group(3))+1) + n
RANGES = {'low': (22, 61), 'mid': (50, 81), 'high': (65, 98)}
BASS = 'electric_bass_finger'; BASS_RANGE = (26, 57)
src, dst = sys.argv[1], sys.argv[2]
os.makedirs(dst, exist_ok=True)
def write(name, outname, lo, hi):
    out, kept = [], 0
    for line in open(os.path.join(src, name + '-mp3.js'), encoding='utf-8'):
        m = re.match(r'^"([A-G][b#]?\d+)":', line)
        if m:
            if not (lo <= midi(m.group(1)) <= hi): continue
            kept += 1
        out.append(re.sub(r'^(MIDI\.Soundfont\.)\w+( = )', r'\g<1>' + outname + r'\2', line))
    path = os.path.join(dst, outname + '-mp3.js')
    open(path, 'w', encoding='utf-8').write(''.join(out))
    print(outname, kept, 'notes', os.path.getsize(path))
for f in sorted(os.listdir(src)):
    if not f.endswith('-mp3.js'): continue
    name = f[:-7]
    if name == BASS: write(name, name, *BASS_RANGE)
    else:
        for rid, (lo, hi) in RANGES.items(): write(name, name + '_' + rid, lo, hi)
