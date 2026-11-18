#!/usr/bin/env python3
"""Build LTspice AC matrices with unchanged foundry cards for used geometries."""
from pathlib import Path
import json,re,itertools,hashlib
from make_buffer_models import select
ROOT=Path(__file__).resolve().parents[1];V=ROOT/'validation';M=V/'models';M.mkdir(exist_ok=True)
rcs=json.loads((ROOT/'models/rc_corners.json').read_text());inventory={}
for c in ['tt','ff','ss','fs','sf']:
 source=(ROOT/'models'/f'sky130_{c}.lib').read_text()
 for rc in [None,'hh','hl','lh','ll']:
  s=source
  if rc:
   for k,v in rcs[rc].items():s=re.sub(r'(?mi)^((?:\.param\s+|\+\s*)'+re.escape(k)+r'\s*=\s*)(\{[^}]+\}|\S+)',lambda m:m[1]+v,s)
  s,kept,removed=select(s);name=f'buffer_{c}'+('_'+rc if rc else '')+'.lib'
  (M/name).write_text('* Exact buffer geometry subset; original model cards retained.\n'+s)
  cases=[(t,v,b,vi,cl) for t in [-40,25,110] for v in [3.135,3.465] for b in [.8,1.2] for vi in [.3,1.65,2.9578125] for cl in [0,20]] if rc is None else [(t,3.135,.8,vi,20) for t in [-40,25,110] for vi in [.3,1.65,2.9578125]]
  stem=f'LT_AC_{c}'+('_'+rc if rc else '')
  z=[f'LTspice buffer AC matrix {c} RC {rc or "nominal"}',f'.include models/{name}', '.include ../Sky130_Adapters.lib','.include buffer_circuit.lib','.func PDK_GAUSS(s) {gauss(s)}','.param CASE=1']
  for idx,p in enumerate(['TEMP_C','AVDD','IREF','VIN_DC','CLOAD']):
   val=lambda q:q[idx]*(1e-6 if p=='IREF' else 1e-12 if p=='CLOAD' else 1)
   z.append(f'.param {p}=table(CASE,'+','.join(f'{i},{val(q):.12g}' for i,q in enumerate(cases,1))+')')
  z+=['.param PDK_TEMP={TEMP_C}','.temp {TEMP_C}','VDD VDD 0 {AVDD}','IB VDD IBIAS {IREF}','VIN VIN 0 {VIN_DC}','VTEST FB OUT 0 AC 1','XBUF VIN FB VDD 0 IBIAS OUT Sky_OTA','RL OUT 0 100k','CL OUT 0 {CLOAD}','.nodeset V(OUT)={VIN_DC} V(FB)={VIN_DC}',f'.step param CASE 1 {len(cases)} 1','.ac dec 60 1 100Meg','.save V(OUT) V(FB)','.meas ac T_USED PARAM TEMP_C','.meas ac INPUT_USED PARAM VIN_DC','.options solver=alt plotwinsize=0 reltol=1e-4 abstol=1e-14 vntol=1e-7 gmin=1e-14 itl1=500','.end']
  (V/(stem+'.cir')).write_text('\n'.join(z)+'\n')
  inventory[stem]=[dict(case=i,corner=c,rc=rc or 'nom',temp=t,vdd=v,ibias_uA=b,vin=vi,cl_pF=cl) for i,(t,v,b,vi,cl) in enumerate(cases,1)]
(V/'ac_cases.json').write_text(json.dumps(inventory,indent=2)+'\n');print('Created',len(inventory),'LTspice matrices with',sum(map(len,inventory.values())),'operating points')
