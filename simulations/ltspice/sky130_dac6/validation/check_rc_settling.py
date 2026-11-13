#!/usr/bin/env python3
"""Check large-step buffer settling at 60 MOS/temperature/RC combinations."""
from pathlib import Path
import argparse,concurrent.futures,json,shutil,subprocess
import numpy as np
from rawio import read_raw
B=Path(__file__).resolve().parent;R=B.parent;W=B/'.work';W.mkdir(exist_ok=True)
p=argparse.ArgumentParser(description=__doc__);p.add_argument('--ngspice',default=shutil.which('ngspice'));p.add_argument('--jobs',type=int,default=4);a=p.parse_args()
if not a.ngspice:raise SystemExit('Install ngspice or specify --ngspice')

def run(q):
 c,t,rc=q;name=f'rc_step_{c}_{t}_{rc}';m=B/'models'/f'buffer_{c}_{rc}.lib'
 z=['Sky130 physical buffer RC settling','.func PDK_GAUSS(s) {agauss(0,s,1)}',f'.param PDK_TEMP={t}',f'.temp {t}',f'.include "{m}"',f'.include "{R/"Sky130_Adapters.lib"}"',f'.include "{B/"buffer_circuit.lib"}"','VDD VDD 0 3.135','IB VDD IBIAS .8u','VIN VIN 0 PULSE(.3 2.9578125 10u 100n 100n 40u 200u)','XBUF VIN OUT VDD 0 IBIAS OUT Sky_OTA','RL OUT 0 100k','CL OUT 0 20p','.options method=gear reltol=1e-5','.tran 20n 100u','.save V(VIN) V(OUT)','.end']
 f=W/(name+'.cir');f.write_text('\n'.join(z)+'\n');q=subprocess.run([a.ngspice,'-b','-r',name+'.raw','-o',name+'.log',f.name],cwd=W,capture_output=True)
 if q.returncode:raise RuntimeError(f'{name}: inspect the log')
 r=read_raw(f.with_suffix('.raw'));time=r['time'];v=r['v(out)'];settles=[]
 for start,stop,target in [(10e-6,50e-6,2.9578125),(50.1e-6,99e-6,.3)]:
  bad=np.where((time>=start)&(time<stop)&(abs(v-target)>.5*2.7/64))[0]
  elapsed=float((time[bad[-1]+1]-start)*1e6) if len(bad) else 0
  if elapsed>20 or abs(np.interp(stop,time,v)-target)>.5*2.7/64:raise ValueError(f'{name}: settling failed')
  settles.append(elapsed)
 return dict(corner=c,temp=t,rc=rc,rise_us=settles[0],fall_us=settles[1])
cases=[(c,t,rc) for c in ['tt','ff','ss','fs','sf'] for t in [-40,25,110] for rc in ['hh','hl','lh','ll']]
with concurrent.futures.ThreadPoolExecutor(max_workers=a.jobs) as ex:result=list(ex.map(run,cases))
f=R/'results/latest_rc_settling.json';f.write_text(json.dumps(result,indent=2)+'\n');print('PASS:',len(result),'cases; worst',max(max(x['rise_us'],x['fall_us']) for x in result),'us')
