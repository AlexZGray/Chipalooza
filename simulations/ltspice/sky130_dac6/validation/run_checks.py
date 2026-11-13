#!/usr/bin/env python3
"""Reproduce pre-layout checks with ngspice; LTspice schematics are the primary examples.

Requires Python >=3.9, numpy and ngspice. Generated files stay in .work/.
AC matrix deliberately uses the middle input voltage: endpoint AC qualification
is separate from the validated transient range and full-code LTspice tests.
"""
import argparse, concurrent.futures, itertools, json, re, shutil, subprocess
from pathlib import Path
import numpy as np
from rawio import read_raw
BASE=Path(__file__).resolve().parent; ROOT=BASE.parent; WORK=BASE/'.work'; LSB=2.7/64
P=argparse.ArgumentParser(description=__doc__)
P.add_argument('--suite',choices=['smoke','range','ac','rc','mismatch','all'],default='smoke')
P.add_argument('--ngspice',default=shutil.which('ngspice'));P.add_argument('--runs',type=int,default=100)
P.add_argument('--jobs',type=int,default=4);A=P.parse_args()
if not A.ngspice:raise SystemExit('Install ngspice or pass --ngspice /path/to/ngspice')
WORK.mkdir(exist_ok=True)

def model(corner='tt',rc=None,mm=False):
    if not rc and not mm:return ROOT/'models'/f'sky130_{corner}.lib'
    p=WORK/f'model_{corner}_{rc or "nom"}_{int(mm)}.lib'
    if p.exists():return p
    s=(ROOT/'models'/f'sky130_{corner}.lib').read_text()
    if mm:s=s.replace('MC_MM_SWITCH=0','MC_MM_SWITCH=1')
    if rc:
        for key,value in json.loads((ROOT/'models/rc_corners.json').read_text())[rc].items():
            pattern=r'(?mi)^((?:\.param\s+|\+\s*)'+re.escape(key)+r'\s*=\s*)(\{[^}]+\}|\S+)'
            s=re.sub(pattern,lambda m:m[1]+value,s)
    p.write_text(s);return p

def header(corner='tt',temp=25,rc=None,mm=False):
    return ['Sky130 reproducible pre-layout check','.func PDK_GAUSS(s) {agauss(0,s,1)}',
            f'.param PDK_TEMP={temp}',f'.temp {temp}',f'.include "{model(corner,rc,mm)}"',
            f'.include "{ROOT/"Sky130_Adapters.lib"}"',f'.include "{BASE/"buffer_circuit.lib"}"',
            '.options reltol=1e-4 abstol=1e-14 vntol=1e-7 gmin=1e-14 itl1=500 itl2=500']

def run(name,lines,control=None):
    p=WORK/(name+'.cir')
    if control:lines+=['.control',*control,'.endc']
    lines+=['.end'];p.write_text('\n'.join(lines)+'\n')
    args=[A.ngspice,'-b','-o',name+'.log']
    if control is None:args+=['-r',name+'.raw']
    args+=[p.name];q=subprocess.run(args,cwd=WORK,capture_output=True)
    raw=WORK/(name+'.raw')
    if q.returncode or not raw.exists():raise RuntimeError(f'{name}: inspect {p.with_suffix(".log")}')
    return read_raw(raw)

def buffer(corner='tt',temp=25,vdd=3.3,ib=1,cl=20,vin='1.65',ac=False,rc=None,mm=False):
    z=header(corner,temp,rc,mm)+[f'VDD VDD 0 {vdd}',f'IB VDD IBIAS {ib}u',f'VIN VIN 0 {vin}',
       f'X_XBUF VIN {"FB" if ac else "OUT"} VDD 0 IBIAS OUT Sky_OTA','RL OUT 0 100k',f'CL OUT 0 {cl}p']
    if ac:z+=['VTEST FB OUT 0 AC 1']
    return z

def phase(r):
    f=r['frequency'].real;a=-r['v(out)']/r['v(fb)'];db=20*np.log10(abs(a));ph=np.unwrap(np.angle(a))*180/np.pi
    j=np.where(np.diff(np.sign(db))<0)[0]
    if not len(j):raise ValueError('No unity loop-gain crossing')
    j=j[0];u=db[j]/(db[j]-db[j+1]);return dict(gain_db=float(db[0]),ugf_hz=float(np.exp(np.log(f[j])*(1-u)+np.log(f[j+1])*u)),pm_deg=float(180+ph[j]*(1-u)+ph[j+1]*u))

def ac_case(q):
    c,t,v,b,cl,rc=q;name=f'ac_{c}_{t}_{v}_{b}_{cl}_{rc or "nom"}'
    z=buffer(c,t,v,b,cl,ac=True,rc=rc)
    z+=['.save V(OUT) V(FB) V(x_xbuf.g2) V(x_xbuf.x_xoutput.n001)']
    r=run(name,z,['set keepopinfo','ac dec 80 1 100Meg',f'write {name}.raw all','setplot op1',f'write {name}_op.raw all'])
    op=read_raw(WORK/(name+'_op.raw'));out=float(op['v(out)'][0]);drop=float(op['v(x_xbuf.g2)'][0]-op['v(x_xbuf.x_xoutput.n001)'][0])
    if abs(out-1.65)>.005 or abs(drop)>1e-6:raise ValueError(f'{name}: invalid AC bias; do not use this result')
    result=dict(case=name,corner=c,temp=t,vdd=v,ibias_uA=b,cl_pF=cl,rc=rc or 'nom',input_V=1.65,**phase(r))
    if result['pm_deg']<60:raise ValueError(f'{name}: phase margin below 60 degrees')
    return result

def range_case(q):
    c,t,v,b=q;name=f'range_{c}_{t}_{v}_{b}'
    z=buffer(c,t,v,b,vin=f'PWL(0 1.65 20u 1.65 2.02m {v} 2.04m {v} 6.04m 0 6.06m 0 8.06m 1.65)')
    z+=['.options reltol=1e-5 abstol=1e-12 vntol=1e-6 gmin=1e-12 method=gear','.tran 1u 8.06m','.save V(VIN) V(OUT) I(VDD)']
    r=run(name,z);vi=r['v(vin)'];err=r['v(out)']-vi;inside=(vi>=.1)&(vi<=v-.1)
    down=(r['time']>2.05e-3)&(r['time']<6.04e-3);x=vi[down];order=np.argsort(x);x=x[order];good=(abs(err[down][order])<=.005)
    lo=hi=int(np.argmin(abs(x-v/2)))
    if not good[lo]:raise ValueError(f'{name}: middle of range invalid')
    while lo>0 and good[lo-1]:lo-=1
    while hi<len(x)-1 and good[hi+1]:hi+=1
    result=dict(case=name,corner=c,temp=t,vdd=v,ibias_uA=b,min_error_mV=float(min(err[inside])*1e3),max_error_mV=float(max(err[inside])*1e3),lower_5mV_limit_V=float(x[lo]),upper_5mV_limit_V=float(x[hi]),upper_headroom_V=float(v-x[hi]))
    if max(abs(err[inside]))>.005:raise ValueError(f'{name}: tracking failed inside 100 mV rail allowance')
    return result

def mc_case(seed,ladder=False):
    name=f'{"ladder" if ladder else "buffer"}_mc_{seed:03}'
    if ladder:
        z=header(mm=True)+['VL N0 0 .3','VH N64 0 3.0']+[f'XR{k} N{k} N{k+1} 0 SKY_R1K' for k in range(64)]
        z+=['.op','.save I(VH) '+' '.join(f'V(N{k})' for k in range(64))]
    else:
        pts=[(0,.3)]
        for k in range(1,64):pts += [(k*100e-6-100e-9,.3+(k-1)*LSB),(k*100e-6,.3+k*LSB)]
        pts.append((64*100e-6,.3+63*LSB))
        pwl='PWL('+ ' '.join(f'{t:.12g} {v:.12g}' for t,v in pts)+')'
        z=buffer(mm=True,vin=pwl)+['.options method=gear reltol=1e-5 abstol=1e-12 vntol=1e-6 gmin=1e-12','.tran 1u 6.4m','.save V(VIN) V(OUT)']
    r=run(name,z,[f'setseed {seed}','reset','run',f'write {name}.raw all'])
    if ladder:
        out=np.array([r[f'v(n{k})'][0] for k in range(64)]);dnl=np.diff(out)/LSB-1;inl=(out-out[0]-np.arange(64)*(out[-1]-out[0])/63)/LSB

        if max(abs(dnl))>.5 or max(abs(inl))>.2:raise ValueError(f'{name}: matching target failed')
        return dict(seed=seed,max_abs_DNL_LSB=float(max(abs(dnl))),max_abs_INL_LSB=float(max(abs(inl))),span_error_LSB=float((out[-1]-out[0]-63*LSB)/LSB))
    out=np.interp((np.arange(64)+.8)*100e-6,r['time'],r['v(out)']);err=out-(.3+np.arange(64)*LSB)
    if max(abs(err))>.5*LSB or not np.all(np.diff(out)>0):raise ValueError(f'{name}: amplifier tracking failed')
    return dict(seed=seed,max_abs_error_LSB=float(max(abs(err))/LSB),zero_error_LSB=float(err[0]/LSB),span_error_LSB=float((err[-1]-err[0])/LSB))

def smoke():
    z=buffer(vin='PULSE(.3 2.9578125 10u 100n 100n 40u 80u)')+['.options method=gear reltol=1e-5 abstol=1e-12 vntol=1e-6 gmin=1e-12','.tran 20n 100u','.save V(VIN) V(OUT)']
    r=run('smoke_step',z);t=r['time'];err=abs(r['v(out)']-r['v(vin)']);settle=[]
    for lo,hi in [(10e-6,50e-6),(50.1e-6,90e-6)]:
        bad=np.where((t>=lo)&(t<hi)&(err>.5*LSB))[0]
        settle.append(float((t[bad[-1]+1]-lo)*1e6) if len(bad) else 0)
    if max(settle)>20:raise ValueError('Smoke test settling failed')
    return dict(step_settling_us=settle,midpoint_AC=ac_case(('tt',25,3.3,1,20,None)))

def parallel(fn,cases):
    with concurrent.futures.ThreadPoolExecutor(max_workers=A.jobs) as ex:return list(ex.map(fn,cases))

result={};suites=['smoke','range','ac','rc','mismatch'] if A.suite=='all' else [A.suite]
for suite in suites:
    print('Running',suite,flush=True)
    if suite=='smoke':result[suite]=smoke()
    if suite=='range':
        cases=[(c,t,v,1) for c in ['tt','ff','ss','fs','sf'] for t in [-40,25,110] for v in [3.135,3.3,3.465]]
        cases += [(c,t,v,b) for c in ['tt','ff','ss','fs','sf'] for t in [-40,110] for v in [3.135,3.465] for b in [.8,1.2]]
        result[suite]=parallel(range_case,cases)
    if suite=='ac':result[suite]=parallel(ac_case,[(c,t,v,b,cl,None) for c in ['tt','ff','ss','fs','sf'] for t in [-40,25,110] for v in [3.135,3.465] for b in [.8,1.2] for cl in [0,20]])
    if suite=='rc':
        for c,rc in itertools.product(['tt','ff','ss','fs','sf'],['hh','hl','lh','ll']):model(c,rc)
        result[suite]=parallel(ac_case,[(c,t,3.135,.8,20,rc) for c in ['tt','ff','ss','fs','sf'] for t in [-40,25,110] for rc in ['hh','hl','lh','ll']])
    if suite=='mismatch':
        model(mm=True);result[suite]=dict(buffer=parallel(mc_case,range(1,A.runs+1)),ladder=parallel(lambda n:mc_case(n,True),range(1,A.runs+1)))

if 'mismatch' in result:
    rows=result['mismatch']['buffer']
    audit=dict(zero_limit_LSB=.2,span_limit_LSB=.1,zero_failures=[x['seed'] for x in rows if abs(x['zero_error_LSB'])>.2],span_failures=[x['seed'] for x in rows if abs(x['span_error_LSB'])>.1])
    audit['status']='REVIEW_REQUIRED' if audit['zero_failures'] or audit['span_failures'] else 'PASS'
    result['mismatch']['allocation_audit']=audit
    print('Mismatch allocation audit:',audit)
path=ROOT/'results'/('latest_validation_'+A.suite+'.json');path.write_text(json.dumps(result,indent=2)+'\n');print('Checks completed:',path)
