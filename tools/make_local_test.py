#!/usr/bin/env python3
"""Make kamerton_local_test.html (works from file://, relative paths) out of index.html / kamerton.html."""
import re, sys
src = sys.argv[1] if len(sys.argv) > 1 else 'kamerton.html'
out = sys.argv[2] if len(sys.argv) > 2 else 'kamerton_local_test.html'
CDN = 'https://cdn.jsdelivr.net/gh/Pianocharmer/EarTrainer@main/sounds/'
s = open(src, encoding='utf-8').read()
s = s.replace('<link rel="preconnect" href="https://cdn.jsdelivr.net" crossorigin>\n', '')
s = re.sub(r'<link rel="preload"[^>]*>\n', '', s)    # file:// cannot fetch() it, the file would be downloaded twice
s = s.replace("'" + CDN + "'", "'./sounds/'").replace(CDN, 'sounds/')
open(out, 'w', encoding='utf-8').write(s)
