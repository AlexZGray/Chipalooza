#!/usr/bin/env python3
"""Verify Sky130 DAC LTspice transients using Python standard library only."""

import argparse
import bisect
import csv
import json
import math
import re
import struct
import sys
from pathlib import Path

BASE = Path(__file__).resolve().parent
LSB = 2.7 / 64
RUNS = ("Top", "Min_Supply", "Hot_Fast", "Cold_Skew", "Overload")


def require(condition, message):
    if not condition:
        raise ValueError(message)


def raw(path):
    """Read selected traces from normal or FastAccess real binary RAW files."""
    blob = path.read_bytes()
    encoding = "utf-16-le" if blob[:2] in (b"T\0", b"\xff\xfe") else "utf-8-sig"
    marker_encoding = "utf-16-le" if encoding == "utf-16-le" else "utf-8"
    marker = "Binary:\n".encode(marker_encoding)
    if marker not in blob:
        marker = "Binary:\r\n".encode(marker_encoding)
    require(marker in blob, f"{path.name}: expected a binary LTspice RAW file")
    end = blob.index(marker)
    header = blob[:end].decode(encoding)
    payload = memoryview(blob)[end + len(marker):]
    require("Transient Analysis" in header, f"{path.name}: expected transient analysis")
    count = int(re.search(r"No\. Variables:\s*(\d+)", header).group(1))
    points = int(re.search(r"No\. Points:\s*(\d+)", header).group(1))
    names = re.findall(r"^\s*\d+\s+(\S+)\s+\S+", header, re.M)
    flags = re.search(r"^Flags:\s*(.*)", header, re.M).group(1).lower().split()
    require("real" in flags and "complex" not in flags, "Expected real transient data")
    require(len(names) == count and points > 1, "Incomplete RAW header")
    size = 8 if "double" in flags else 4
    row_bytes = 8 + (count - 1) * size
    require(len(payload) == points * row_bytes, f"{path.name}: incomplete RAW data")
    wanted = set(name.lower() for name in names)
    result = {}
    for column, name in enumerate(names):
        name = name.lower()
        if name not in wanted:
            continue
        fmt = struct.Struct("<d" if column == 0 or size == 8 else "<f")
        start = 0 if column == 0 else 8 + (column - 1) * size
        stride = row_bytes
        if "fastaccess" in flags:
            start = 0 if column == 0 else points * (8 + (column - 1) * size)
            stride = fmt.size
        values = [fmt.unpack_from(payload, start + k * stride)[0] for k in range(points)]
        require(all(math.isfinite(v) for v in values), f"Non-finite values in {name}")
        result[name] = values
    require(wanted <= result.keys(), f"Missing traces: {sorted(wanted - result.keys())}")
    times = result["time"]
    require(abs(times[-1] - 0.008) < 1e-10, f"{path.name}: simulation must finish at 8 ms")
    require(all(a <= b for a, b in zip(times, times[1:])), "Expected an unstepped run")
    return result


def sample(run, name, time):
    t=run['time']; j=bisect.bisect_left(t,time)
    if j==0:return run[name][0]
    if j==len(t):return run[name][-1]
    a=(time-t[j-1])/(t[j]-t[j-1]) if t[j]!=t[j-1] else 0
    return run[name][j-1]*(1-a)+run[name][j]*a


def analyse(name, dvdd):
    path=BASE/('DAC6_Sky130_'+name+'.raw');run=raw(path)
    monitor='v(xcore:en_mon)' if name=='Integration' else 'v(en_mon)'
    codes=json.loads((BASE/'stimulus.json').read_text())['codes']; rows=[]
    for code in range(64):
        t=code*1e-4+80e-6; ideal=.3+code*LSB; out=sample(run,'v(out)',t)
        rows.append(dict(code=code,ideal_V=ideal,output_V=out,tap_V=sample(run,'v(tap)',t),error_LSB=(out-ideal)/LSB))
        for bit in range(6):
            expected=dvdd*((code>>bit)&1)
            require(abs(sample(run,f'v(d{bit})',t)-expected)<.001,'Wrong stimulus amplitude')
        require(abs(sample(run,monitor,t)-dvdd)<.01,'Internal enable monitor did not assert')
    out=[x['output_V'] for x in rows]; errors=[x['error_LSB'] for x in rows]
    dnl=[(b-a)/LSB-1 for a,b in zip(out,out[1:])]
    inl=[(v-out[0]-i*(out[-1]-out[0])/63)/LSB for i,v in enumerate(out)]
    gain=(out[-1]-out[0]-63*LSB)/LSB
    settling=[]
    for slot in (65,66,67,68,69,70,71,74,75,76,77,78):
        start=slot*1e-4; stop=start+99e-6; target=.3+codes[slot]*LSB
        indices=range(bisect.bisect_left(run['time'],start),bisect.bisect_right(run['time'],stop))
        outside=[k for k in indices if abs(run['v(out)'][k]-target)>.5*LSB]
        elapsed=0 if not outside else run['time'][outside[-1]+1]-start
        require(abs(sample(run,'v(out)',stop)-target)<=.5*LSB,'Did not settle')
        settling.append(dict(slot=slot,code=codes[slot],time_us=elapsed*1e6))
    disabled=sample(run,'v(out)',7.3e-3)
    require(abs(disabled-.3)<.2*LSB,'Reset error')
    require(sample(run,monitor,7.3e-3)<.01,'Internal enable monitor did not reset')
    require(max(map(abs,errors))<=.5,'Absolute error exceeded 0.5 LSB')
    require(abs(errors[0])<=.2,'Zero error exceeded 0.2 LSB')
    require(abs(gain)<=.1,'Span error exceeded 0.1 LSB')
    require(max(map(abs,inl))<=.2,'INL exceeded 0.2 LSB')
    require(max(map(abs,dnl))<=.5 and min(dnl)>-1,'DNL/monotonicity failed')
    require(max(x['time_us'] for x in settling)<=20,'20 us settling target failed')
    steady=[-sample(run,'i(vdd)',i*1e-4+80e-6) for i in range(64)]
    digital=[-sample(run,'i(vlogic)',i*1e-4+80e-6) for i in range(64)]
    refs=[-sample(run,'i(vhigh)',i*1e-4+80e-6) for i in range(64)]
    require(max(steady)<=1e-3,'Static IDDA exceeded 1 mA')
    require(max(digital)<=50e-6,'Static IDDD exceeded 50 uA')
    require(max(refs)<=60e-6,'Reference current exceeded 60 uA')
    ref=-sample(run,'i(vhigh)',3.28e-3)
    result=dict(status='PASS',case=name,code0_V=out[0],code63_V=out[-1],max_abs_error_LSB=max(map(abs,errors)),zero_error_LSB=errors[0],gain_error_LSB=gain,max_abs_DNL_LSB=max(map(abs,dnl)),max_abs_endpoint_INL_LSB=max(map(abs,inl)),max_settling_us=max(x['time_us'] for x in settling),settling=settling,max_steady_IDDA_uA=max(steady)*1e6,peak_IDDA_uA=-min(run['i(vdd)'])*1e6,string_current_uA=ref*1e6,disabled_output_V=disabled)
    result.update(max_steady_IDDD_uA=max(digital)*1e6,max_reference_current_uA=max(refs)*1e6)
    return result,rows


def protocol(name,dvdd):
    r=raw(BASE/('DAC6_Sky130_'+name+'.raw'));codes=json.loads((BASE/'stimulus.json').read_text())['codes']
    enables=[];resets=[]
    def settle(start,stop,target):
        ids=range(bisect.bisect_left(r['time'],start),bisect.bisect_right(r['time'],stop))
        bad=[k for k in ids if abs(r['v(out)'][k]-target)>.5*LSB]
        require(abs(sample(r,'v(out)',stop)-target)<=.5*LSB,'Protocol output did not settle')
        return 0 if not bad else (r['time'][bad[-1]+1]-start)*1e6
    for j in range(1,80):
        edge=j*1e-4
        require(sample(r,'v(en)',edge-5e-6)<.3*dvdd,'EN low setup failed')
        require(sample(r,'v(en)',edge+5e-6)<.3*dvdd,'Data setup before EN failed')
        enables.append(settle(edge+5.1e-6,edge+89e-6,.3+codes[j]*LSB))
        resets.append(settle(edge-10e-6,edge+5e-6,.3))
    require(max(enables)<=20 and max(resets)<=20,'Protocol settling exceeded 20 us')
    return dict(status='PASS',max_enable_settling_us=max(enables),max_reset_settling_us=max(resets),code_setup_us=5.0,EN_low_setup_us=9.9)


def main():
    import argparse
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--all',action='store_true',help='Also require all three corner examples and the intentional overload');p.add_argument('--protocol',action='store_true',help='Also check both host-protocol examples');p.add_argument('--integration',action='store_true',help='Also check the reusable core and the 10 Meg / 10 pF tap-probe fixture');args=p.parse_args()
    cases=[('Top',1.8)]
    if args.all:cases += [('Min_Supply',1.71),('Hot_Fast',1.89),('Cold_Skew',1.71)]
    if args.integration:cases += [('Integration',1.8),('Tap_Probe',1.8)]
    results={};outdir=BASE/'results';outdir.mkdir(exist_ok=True)
    for name,dv in cases:
        result,rows=analyse(name,dv);results[name]=result
        with (outdir/('latest_'+name+'_codes.csv')).open('w',newline='') as f:
            w=csv.DictWriter(f,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows)
    if args.all:
        r=raw(BASE/'DAC6_Sky130_Overload.raw');v=sample(r,'v(out)',6.38e-3);require(abs(v-(.3+63*LSB))>1,'Expected 1k overload failure was absent');results['Overload']=dict(status='EXPECTED_FAILURE_CONFIRMED',code63_V=v)

    if args.protocol:
        for name,dv in [('Protocol',1.8),('Protocol_Min',1.71)]:results[name]=protocol(name,dv)
    if args.integration:
        _,baseline=analyse('Top',1.8);_,integrated=analyse('Integration',1.8)
        delta=max(abs(a['output_V']-b['output_V']) for a,b in zip(baseline,integrated))
        require(delta<1e-6,'Reusable-core output differs from architecture sheet by over 1 uV')
        results['Integration']['max_difference_from_Top_uV']=delta*1e6
    (outdir/'latest.json').write_text(json.dumps(results,indent=2)+'\n')
    print(json.dumps(results,indent=2))


if __name__=='__main__':
    try:main()
    except (ValueError,OSError) as error:
        print(str(error),file=sys.stderr);raise SystemExit(1)
