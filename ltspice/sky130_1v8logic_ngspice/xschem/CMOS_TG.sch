v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {CMOS_TG: generated from the LTspice schematic by tools/gen_xschem.py} -900 -560 0 0 0.4 0.4 {}
C {devices/ipin.sym} -900 -500 0 0 {name=p1 lab=IN}
C {devices/opin.sym} -900 -470 0 0 {name=p2 lab=OUT}
C {devices/ipin.sym} -900 -440 0 0 {name=p3 lab=EN}
C {devices/ipin.sym} -900 -410 0 0 {name=p4 lab=ENB}
C {devices/iopin.sym} -900 -380 0 0 {name=p5 lab=VDD}
C {devices/iopin.sym} -900 -350 0 0 {name=p6 lab=VSS}
C {sky130_fd_pr/nfet_01v8.sym} -500 -400 0 0 {name=XN W=7 L=0.5 nf=1 mult=4 ad=2.03 pd=14.58 as=2.03 ps=14.58 nrd=0.0414286 nrs=0.0414286 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -480 -430 0 0 {name=l1 sig_type=std_logic lab=OUT}
C {devices/lab_pin.sym} -520 -400 0 0 {name=l2 sig_type=std_logic lab=EN}
C {devices/lab_pin.sym} -480 -370 0 0 {name=l3 sig_type=std_logic lab=IN}
C {devices/lab_pin.sym} -480 -400 0 0 {name=l4 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/pfet_01v8.sym} -180 -400 0 0 {name=XP W=7 L=0.5 nf=1 mult=8 ad=2.03 pd=14.58 as=2.03 ps=14.58 nrd=0.0414286 nrs=0.0414286 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -160 -370 0 0 {name=l5 sig_type=std_logic lab=OUT}
C {devices/lab_pin.sym} -200 -400 0 0 {name=l6 sig_type=std_logic lab=ENB}
C {devices/lab_pin.sym} -160 -430 0 0 {name=l7 sig_type=std_logic lab=IN}
C {devices/lab_pin.sym} -160 -400 0 0 {name=l8 sig_type=std_logic lab=VDD}
