#!/usr/bin/env python3
"""Convert the LTspice block schematics of ../../sky130_1v8logic/blocks into one SPICE
subcircuit library (input to gen_xschem.py).

Usage: python3 asc2net.py ../../sky130_1v8logic/blocks ../reference/circuit.lib

Nets are found by joining wire end points, wire T-junctions, net flags and symbol pins.
nmos4/pmos4 pin offsets are LTspice's; block pins come from the .asy files in SpiceOrder."""
import re, pathlib, sys
B=pathlib.Path(sys.argv[1])
BUILTIN={'nmos4':[('D',48,0),('G',0,80),('S',48,96),('B',48,48)],'pmos4':[('D',48,0),('G',0,80),('S',48,96),('B',48,48)]}
def tf(x,y,rot):
    m=rot.startswith('M'); a=int(rot[1:])
    if m: x=-x
    for _ in range(a//90): x,y=-y,x
    return x,y
def asy_pins(name):
    pins=[];cur=None
    for ln in (B/(name+'.asy')).read_text().splitlines():
        t=ln.split()
        if t and t[0]=='PIN': cur=[int(t[1]),int(t[2]),None,None]; pins.append(cur)
        elif t and t[0]=='PINATTR' and t[1]=='PinName': cur[2]=t[2]
        elif t and t[0]=='PINATTR' and t[1]=='SpiceOrder': cur[3]=int(t[2])
    pins.sort(key=lambda p:p[3]); return [(p[2],p[0],p[1]) for p in pins]
def convert(name):
    wires=[];flags=[];syms=[];ports=[]
    for ln in (B/(name+'.asc')).read_text().splitlines():
        t=ln.split()
        if not t: continue
        if t[0]=='WIRE': wires.append(tuple(map(int,t[1:5])))
        elif t[0]=='FLAG': flags.append((int(t[1]),int(t[2]),t[3]))
        elif t[0]=='SYMBOL': syms.append(dict(sym=t[1].split('\\')[-1],x=int(t[2]),y=int(t[3]),rot=t[4],attr={}))
        elif t[0]=='SYMATTR': syms[-1]['attr'][t[1]]=ln.split(None,2)[2]
    pts=set()
    for w in wires: pts.add(w[:2]); pts.add(w[2:])
    for f in flags: pts.add(f[:2])
    inst=[]
    for s in syms:
        pins=BUILTIN.get(s['sym']) or asy_pins(s['sym'])
        pp=[(n,s['x']+tf(dx,dy,s['rot'])[0],s['y']+tf(dx,dy,s['rot'])[1]) for n,dx,dy in pins]
        for _,x,y in pp: pts.add((x,y))
        inst.append((s,pp))
    par={p:p for p in pts}
    def f(p):
        while par[p]!=p: par[p]=par[par[p]]; p=par[p]
        return p
    def u(a,b): par[f(a)]=f(b)
    for w in wires:
        u(w[:2],w[2:])
        x1,y1,x2,y2=w
        for p in pts:
            if (x1==x2==p[0] and min(y1,y2)<=p[1]<=max(y1,y2)) or (y1==y2==p[1] and min(x1,x2)<=p[0]<=max(x1,x2)): u(p,w[:2])
    names={}
    for x,y,n in flags:
        r=f((x,y))
        if r in names and names[r]!=n: raise SystemExit(f'{name}: short {names[r]} {n}')
        names[r]=n
    k=[0]
    def net(p):
        r=f(p)
        if r not in names: k[0]+=1; names[r]=f'N{k[0]:03d}'
        return '0' if names[r]=='0' else names[r]
    lines=[]
    for s,pp in inst:
        nets=[net((x,y)) for _,x,y in pp]
        a=s['attr']; nm=a['InstName']
        if s['sym'] in BUILTIN: lines.append(f"X_{nm} {' '.join(nets)} {a['Value']} {a.get('SpiceLine','')}")
        elif s['sym'] in ('Sky_R','Sky_C'): lines.append(f"X_{nm} {' '.join(nets)} {a['Value']} {a.get('SpiceLine','')}")
        else: lines.append(f"X_{nm} {' '.join(nets)} {s['sym']}")
    ports=[n for n,_,_ in asy_pins(name)]
    unk=[n for n in set(sum([l.split()[1:] for l in lines],[])) if n.startswith('N') and n[1:].isdigit()]
    return f".subckt {name} {' '.join(ports)}\n"+'\n'.join(lines)+f"\n.ends {name}\n", ports
out=[]
for n in ['CMOS_INV','CMOS_TG','DAC_Mux2','DAC_Mux8','DAC_Bank8','DAC_String64','DAC_Control','Sky_Bias','Sky_InputP','Sky_InputN','Sky_Output','Sky_OTA','DAC_Buffer','DAC6_Sky130_Core']:
    t,_=convert(n); out.append(t)
open(sys.argv[2],'w').write('\n'.join(out))
