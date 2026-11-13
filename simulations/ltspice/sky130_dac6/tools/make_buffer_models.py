#!/usr/bin/env python3
"""Select exact foundry model cards covering this buffer's geometries.

No fit coefficients or bin limits change. Inclusive boundary candidates are kept
so the simulator makes the same bin choice as in the full source library.
The result is for buffer-only verification; the DAC needs the full library.
"""
from pathlib import Path
import argparse,re,hashlib

def select(text):
    lines=text.splitlines(keepends=True);out=[];kept=removed=0;i=0
    while i<len(lines):
        if not lines[i].lower().startswith('.model '):out.append(lines[i]);i+=1;continue
        j=i+1
        while j<len(lines) and (not lines[j].strip() or lines[j].lstrip().startswith(('+','*'))):j+=1
        block=''.join(lines[i:j]);name=lines[i].split()[1]
        dims={k.lower():float(v) for k,v in re.findall(r'\b(lmin|lmax|wmin|wmax)\s*=\s*([0-9.eE+-]+)',block)}
        use=False
        if any(f'__{p}fet_g5v0d10v5__model.' in name for p in ['n','p']) and len(dims)==4:
            use=any(dims['lmin']-1e-15<=l*1e-6<=dims['lmax']+1e-15 and dims['wmin']-1e-15<=7e-6<=dims['wmax']+1e-15 for l in [1,2,4,8])
        if use:out.append(block);kept+=1
        else:removed+=1
        i=j
    return ''.join(out),kept,removed

if __name__=='__main__':
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('source',type=Path);p.add_argument('output',type=Path);a=p.parse_args()
    text,k,r=select(a.source.read_text());a.output.write_text('* Exact buffer geometry subset of '+a.source.name+'\n* Source SHA256 '+hashlib.sha256(a.source.read_bytes()).hexdigest()+'\n'+text)
    print(f'{k} original model cards retained; {r} unused cards omitted')
