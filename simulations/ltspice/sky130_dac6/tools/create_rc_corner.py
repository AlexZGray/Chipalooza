#!/usr/bin/env python3
"""Create one MOS/RC combination from the bundled, pinned foundry parameter sets."""
import argparse,json,re
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--mos',choices=['tt','ff','ss','fs','sf'],required=True);p.add_argument('--rc',choices=['hh','hl','lh','ll'],required=True);p.add_argument('--output',type=Path,required=True);a=p.parse_args()
s=(ROOT/'models'/f'sky130_{a.mos}.lib').read_text()
for k,v in json.loads((ROOT/'models/rc_corners.json').read_text())[a.rc].items():
 s=re.sub(r'(?mi)^((?:\.param\s+|\+\s*)'+re.escape(k)+r'\s*=\s*)(\{[^}]+\}|\S+)',lambda m:m[1]+v,s)
a.output.write_text(f'* MOS {a.mos}; official RC {a.rc}; see provenance.json\n'+s)
