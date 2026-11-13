from pathlib import Path
import re,json,hashlib,subprocess
from adapt_passives import adapt_passives
import argparse
PIN='29b55153fd9f4badef05a02667184b81789d1f61'
p=argparse.ArgumentParser(description='Rebuild the pinned Sky130 LTspice model subset')
p.add_argument('upstream',type=Path,help='Git checkout of skywater-pdk-libs-sky130_fd_pr')
p.add_argument('--output',type=Path,default=Path(__file__).resolve().parents[1],help='Target circuit folder; contains models/')
a=p.parse_args();U=a.upstream.resolve();O=a.output.resolve()
revision=subprocess.check_output(['git','-C',str(U),'rev-parse','HEAD'],text=True).strip()
if revision!=PIN:raise SystemExit('Source revision differs from the validated pin: '+PIN)
(O/'models').mkdir(parents=True,exist_ok=True)
used={}
def flatten(p):
 p=p.resolve();t=p.read_text();used[str(p.relative_to(U))]=hashlib.sha256(p.read_bytes()).hexdigest()
 return '\n* SOURCE '+str(p.relative_to(U))+'\n'+re.sub(r'^\.include\s+["\']?([^\s"\']+)["\']?\s*$',lambda m:flatten(p.parent/m.group(1)),t,flags=re.M|re.I)
def params(t):
 out=[];take=False
 for ln in t.splitlines():
  s=ln.strip()
  if s.startswith('.param'):take=True;out.append(ln)
  elif s.startswith('+') and take:out.append(ln)
  elif s and not s.startswith('*'):take=False
 return '\n'.join(out)+'\n'
families=['nfet_01v8','pfet_01v8','nfet_g5v0d10v5','pfet_g5v0d10v5']
for corner in ['tt','ff','ss','fs','sf']:
 t='* Sky130 subset; BSIM coefficients and bins retained from upstream.\n.param MC_MM_SWITCH=0 MC_PR_SWITCH=0\n'
 t+='\n'.join(f'.param sky130_fd_pr__{f}__dlc_rotweak=0' for f in families)+'\n'
 t+=flatten(U/'models/parameters/lod.spice')
 for f in families:
  p=U/'cells'/f/f'sky130_fd_pr__{f}__{corner}.corner.spice'
  t+=flatten(p)
  t+=flatten(U/'cells'/f/f'sky130_fd_pr__{f}__mismatch.corner.spice')
 for name in ['res_typical__cap_typical.spice','res_typical__cap_typical__lin.spice']:
  t+=params(flatten(U/'models/r+c'/name))

 for f in ['res_high_po_0p69','res_high_po_1p41']:
  t+=flatten(U/'cells/res_high_po'/f'sky130_fd_pr__{f}.model.spice')
 t+=flatten(U/'cells/res_xhigh_po'/'sky130_fd_pr__res_xhigh_po_0p35.model.spice')
 t+=flatten(U/'cells/res_xhigh_po'/'sky130_fd_pr__res_xhigh_po__base.model.spice')
 t+=flatten(U/'cells/cap_mim_m3'/'sky130_fd_pr__cap_mim_m3_1.model.spice')
 # Explicit SI conversion replaces the PDK global scale=1u, preserving wrapper arguments in micrometres.
 lines=t.splitlines()
 for i,ln in enumerate(lines):
  if ln.lstrip().lower().startswith('msky130_'):
   for k,factor in [('l','1u'),('w','1u'),('ad','1p'),('as','1p'),('pd','1u'),('ps','1u'),('sa','1u'),('sb','1u'),('sd','1u')]:
    ln=re.sub(r'\b'+k+r'\s*=\s*\{'+k+r'\}',k+'={'+k+'*'+factor+'}',ln,flags=re.I)
   ln+=' m={mult}'
   lines[i]=ln
 t='\n'.join(lines)+'\n'
 # LTspice's normal variate function has one argument. This maps ngspice's AGAUSS convention.
 t=re.sub(r'AGAUSS\(0,\s*1(?:\.0)?,\s*1\)', 'PDK_GAUSS(1)',t,flags=re.I)
 t=re.sub(r"'([^'\n]+)'",r'{\1}',t)
 # A common explicit temperature parameter keeps voltage-dependent resistor expressions portable.
 t=re.sub(r'\btemper\b','PDK_TEMP',t,flags=re.I)
 t=adapt_passives(t)
 (O/'models'/f'sky130_{corner}.lib').write_text(t)

for name in ['LICENSE','NOTICE']:
 if (U/name).exists(): (O/'models'/name).write_bytes((U/name).read_bytes())
(O/'models/provenance.json').write_text(json.dumps({'upstream':'https://github.com/fossi-foundation/skywater-pdk-libs-sky130_fd_pr','commit':subprocess.check_output(['git','-C',str(U),'rev-parse','HEAD'],text=True).strip(),'source_sha256':used,'adaptations':['Include expansion, selected device subset','Explicit um/um2 to SI conversion at internal MOS geometry parameters; no global scale','AGAUSS(0,1,1) mapped to per-engine standard normal function PDK_GAUSS','Single quoted expressions converted to braces','Resistor expression temper renamed to PDK_TEMP, which testbenches set equal to .temp','Internal MOS m={mult} implements explicit parallel-device multiplicity; verified against repeated native instances','Voltage-dependent resistor TC is expressed as multiplication by the original polynomial about 27 C','Capacitor c= spelling removed and zero TC terms omitted for LTspice compatibility'],'coefficients':'No BSIM fit coefficients or geometry bin boundaries changed'},indent=2))
print('Wrote model corners',O)
