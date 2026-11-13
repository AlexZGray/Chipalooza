#!/usr/bin/env python3
"""Verify all 540 LTspice matrix results after running the 25 LT_AC_*.cir files."""
from pathlib import Path
import argparse,json
import numpy as np
from rawio import read_raw
B=Path(__file__).resolve().parent
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--partial',action='store_true',help='Report available matrices without claiming complete coverage');a=p.parse_args()
meta=json.loads((B/'ac_cases.json').read_text());results=[];missing=[]
for stem,cases in meta.items():
 f=B/(stem+'.raw')
 if not f.exists():missing.append(stem);continue
 try:r=read_raw(f)
 except (ValueError,KeyError):
  if a.partial:missing.append(stem);continue
  raise
 freq=r['frequency'].real;gain=-r['v(out)']/r['v(fb)'];cuts=np.r_[0,np.where(np.diff(freq)<0)[0]+1,len(freq)]
 if len(cuts)!=len(cases)+1:raise ValueError(f'{stem}: expected {len(cases)} complete steps')
 for case,l,h in zip(cases,cuts,cuts[1:]):
  x=freq[l:h];z=gain[l:h];db=20*np.log10(abs(z));ph=np.unwrap(np.angle(z))*180/np.pi;j=np.where(np.diff(np.sign(db))<0)[0]
  if len(j)!=1 or db[-1]>=0:raise ValueError(f'{stem}/{case["case"]}: check unity crossings')
  j=j[0];u=db[j]/(db[j]-db[j+1]);q=dict(matrix=stem,**case,gain_db=float(db[0]),pm_deg=float(180+ph[j]*(1-u)+ph[j+1]*u),ugf_hz=float(np.exp(np.log(x[j])*(1-u)+np.log(x[j+1])*u)))
  if q['pm_deg']<60:raise ValueError(f'{stem}/{case["case"]}: phase margin below 60 degrees')
  results.append(q)
if missing and not a.partial:raise SystemExit('Run these matrices first: '+', '.join(missing))
out=dict(status='PARTIAL' if missing else 'PASS',cases=len(results),missing=missing,min_phase_margin=min(results,key=lambda x:x['pm_deg']),min_gain=min(results,key=lambda x:x['gain_db']),min_unity_frequency=min(results,key=lambda x:x['ugf_hz']),results=results)
f=B.parent/'results/latest_lt_ac.json';f.write_text(json.dumps(out,indent=2)+'\n');print(json.dumps({k:v for k,v in out.items() if k!='results'},indent=2))
