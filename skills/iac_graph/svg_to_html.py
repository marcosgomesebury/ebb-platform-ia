#!/usr/bin/env python3
import subprocess, sys, re

dot_input = sys.stdin.buffer.read()

# SVG is vector — DPI flag is meaningless and makes dimensions huge, skip it
result = subprocess.run(
    ['dot', '-Tsvg'],
    input=dot_input,
    capture_output=True
)
svg = result.stdout.decode('utf-8', errors='replace')
svg = svg[svg.find('<svg'):]

# dot emits width/height in pt (e.g. "1200pt") — convert to px so browser renders correctly
def pt_to_px(m):
    val = float(m.group(1))
    attr = m.group(0).split('=')[0]
    px = int(val * 96 / 72)  # 1pt = 96/72 px
    return f'{attr}="{px}px"'

# dot emits width/height in pt — extract viewBox and set explicit px dimensions
# so the SVG renders correctly inside the absolute-positioned container
vb_match = re.search(r'viewBox="([\d.]+)\s+([\d.]+)\s+([\d.]+)\s+([\d.]+)"', svg)
if vb_match:
    vb_w = float(vb_match.group(3))
    vb_h = float(vb_match.group(4))
    # viewBox values are in Graphviz pts; convert to px (96dpi/72dpi)
    px_w = int(vb_w * 96 / 72)
    px_h = int(vb_h * 96 / 72)
    svg = re.sub(r'<svg\s+width="[^"]*"\s+height="[^"]*"',
                 f'<svg width="{px_w}" height="{px_h}"', svg)
else:
    # fallback: just strip pt units → px
    svg = re.sub(r'(width|height)="([\d.]+)pt"',
                 lambda m: f'{m.group(1)}="{int(float(m.group(2))*96/72)}px"', svg)

import json, os
perm_data = {}
try:
    with open('/tmp/ebb-perm-data.json') as f:
        perm_data = json.load(f)
except Exception:
    pass

template = open('/tmp/svg_template.html').read()
html = template.replace('__SVG__', svg)
html = html.replace('__PERM_JSON__', json.dumps(perm_data, ensure_ascii=False))
sys.stdout.write(html)
