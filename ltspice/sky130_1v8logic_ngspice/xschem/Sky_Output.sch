v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {Sky_Output: generated from the LTspice schematic by tools/gen_xschem.py} -900 -560 0 0 0.4 0.4 {}
C {devices/ipin.sym} -900 -500 0 0 {name=p1 lab=G2}
C {devices/ipin.sym} -900 -470 0 0 {name=p2 lab=BP}
C {devices/iopin.sym} -900 -440 0 0 {name=p3 lab=VDD}
C {devices/iopin.sym} -900 -410 0 0 {name=p4 lab=VSS}
C {devices/opin.sym} -900 -380 0 0 {name=p5 lab=OUT}
C {sky130_fd_pr/pfet_01v8.sym} -500 -400 0 0 {name=XPOUT W=7 L=4 nf=1 mult=100 ad=2.03 pd=14.58 as=2.03 ps=14.58 nrd=0.0414286 nrs=0.0414286 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -480 -370 0 0 {name=l1 sig_type=std_logic lab=OUT}
C {devices/lab_pin.sym} -520 -400 0 0 {name=l2 sig_type=std_logic lab=BP}
C {devices/lab_pin.sym} -480 -430 0 0 {name=l3 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -480 -400 0 0 {name=l4 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/nfet_01v8.sym} -180 -400 0 0 {name=XNOUT W=7 L=1 nf=1 mult=36 ad=2.03 pd=14.58 as=2.03 ps=14.58 nrd=0.0414286 nrs=0.0414286 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -160 -430 0 0 {name=l5 sig_type=std_logic lab=OUT}
C {devices/lab_pin.sym} -200 -400 0 0 {name=l6 sig_type=std_logic lab=G2}
C {devices/lab_pin.sym} -160 -370 0 0 {name=l7 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -160 -400 0 0 {name=l8 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/res_high_po_0p69.sym} 140 -400 0 0 {name=XRC L=2.2 model=res_high_po_0p69 spiceprefix=X mult=1}
C {devices/lab_pin.sym} 140 -370 0 0 {name=l9 sig_type=std_logic lab=N001}
C {devices/lab_pin.sym} 140 -430 0 0 {name=l10 sig_type=std_logic lab=G2}
C {devices/lab_pin.sym} 120 -400 0 0 {name=l11 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/cap_mim_m3_1.sym} 460 -400 0 0 {name=XCC model=cap_mim_m3_1 W=149.822 L=149.822 MF=1 spiceprefix=X}
C {devices/lab_pin.sym} 460 -430 0 0 {name=l12 sig_type=std_logic lab=N001}
C {devices/lab_pin.sym} 460 -370 0 0 {name=l13 sig_type=std_logic lab=OUT}
