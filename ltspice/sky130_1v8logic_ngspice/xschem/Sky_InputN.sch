v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {Sky_InputN: generated from the LTspice schematic by tools/gen_xschem.py} -900 -560 0 0 0.4 0.4 {}
C {devices/ipin.sym} -900 -500 0 0 {name=p1 lab=INP}
C {devices/ipin.sym} -900 -470 0 0 {name=p2 lab=INM}
C {devices/iopin.sym} -900 -440 0 0 {name=p3 lab=VDD}
C {devices/iopin.sym} -900 -410 0 0 {name=p4 lab=VSS}
C {devices/iopin.sym} -900 -380 0 0 {name=p5 lab=IBIAS}
C {devices/opin.sym} -900 -350 0 0 {name=p6 lab=G2}
C {sky130_fd_pr/nfet_01v8.sym} -500 -400 0 0 {name=XNTAIL W=7 L=4 nf=1 mult=10 ad=2.03 pd=14.58 as=2.03 ps=14.58 nrd=0.0414286 nrs=0.0414286 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -480 -430 0 0 {name=l1 sig_type=std_logic lab=SN}
C {devices/lab_pin.sym} -520 -400 0 0 {name=l2 sig_type=std_logic lab=IBIAS}
C {devices/lab_pin.sym} -480 -370 0 0 {name=l3 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -480 -400 0 0 {name=l4 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/nfet_01v8.sym} -180 -400 0 0 {name=XNPLUS W=7 L=8 nf=1 mult=8 ad=2.03 pd=14.58 as=2.03 ps=14.58 nrd=0.0414286 nrs=0.0414286 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -160 -430 0 0 {name=l5 sig_type=std_logic lab=NA}
C {devices/lab_pin.sym} -200 -400 0 0 {name=l6 sig_type=std_logic lab=INP}
C {devices/lab_pin.sym} -160 -370 0 0 {name=l7 sig_type=std_logic lab=SN}
C {devices/lab_pin.sym} -160 -400 0 0 {name=l8 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/nfet_01v8.sym} 140 -400 0 0 {name=XNMINUS W=7 L=8 nf=1 mult=8 ad=2.03 pd=14.58 as=2.03 ps=14.58 nrd=0.0414286 nrs=0.0414286 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 160 -430 0 0 {name=l9 sig_type=std_logic lab=NB}
C {devices/lab_pin.sym} 120 -400 0 0 {name=l10 sig_type=std_logic lab=INM}
C {devices/lab_pin.sym} 160 -370 0 0 {name=l11 sig_type=std_logic lab=SN}
C {devices/lab_pin.sym} 160 -400 0 0 {name=l12 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/pfet_01v8.sym} 460 -400 0 0 {name=XPNA W=7 L=0.25 nf=1 mult=128 ad=2.03 pd=14.58 as=2.03 ps=14.58 nrd=0.0414286 nrs=0.0414286 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 480 -370 0 0 {name=l13 sig_type=std_logic lab=NA}
C {devices/lab_pin.sym} 440 -400 0 0 {name=l14 sig_type=std_logic lab=NA}
C {devices/lab_pin.sym} 480 -430 0 0 {name=l15 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 480 -400 0 0 {name=l16 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/pfet_01v8.sym} 780 -400 0 0 {name=XPNAX W=7 L=0.25 nf=1 mult=128 ad=2.03 pd=14.58 as=2.03 ps=14.58 nrd=0.0414286 nrs=0.0414286 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 800 -370 0 0 {name=l17 sig_type=std_logic lab=NAA}
C {devices/lab_pin.sym} 760 -400 0 0 {name=l18 sig_type=std_logic lab=NA}
C {devices/lab_pin.sym} 800 -430 0 0 {name=l19 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 800 -400 0 0 {name=l20 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/nfet_01v8.sym} 1100 -400 0 0 {name=XNNAA W=7 L=8 nf=1 mult=16 ad=2.03 pd=14.58 as=2.03 ps=14.58 nrd=0.0414286 nrs=0.0414286 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 1120 -430 0 0 {name=l21 sig_type=std_logic lab=NAA}
C {devices/lab_pin.sym} 1080 -400 0 0 {name=l22 sig_type=std_logic lab=NAA}
C {devices/lab_pin.sym} 1120 -370 0 0 {name=l23 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 1120 -400 0 0 {name=l24 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/nfet_01v8.sym} -500 -180 0 0 {name=XNNAX W=7 L=8 nf=1 mult=16 ad=2.03 pd=14.58 as=2.03 ps=14.58 nrd=0.0414286 nrs=0.0414286 sa=0 sb=0 sd=0 model=nfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -480 -210 0 0 {name=l25 sig_type=std_logic lab=G2}
C {devices/lab_pin.sym} -520 -180 0 0 {name=l26 sig_type=std_logic lab=NAA}
C {devices/lab_pin.sym} -480 -150 0 0 {name=l27 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} -480 -180 0 0 {name=l28 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/pfet_01v8.sym} -180 -180 0 0 {name=XPNB W=7 L=0.25 nf=1 mult=128 ad=2.03 pd=14.58 as=2.03 ps=14.58 nrd=0.0414286 nrs=0.0414286 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} -160 -150 0 0 {name=l29 sig_type=std_logic lab=NB}
C {devices/lab_pin.sym} -200 -180 0 0 {name=l30 sig_type=std_logic lab=NB}
C {devices/lab_pin.sym} -160 -210 0 0 {name=l31 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} -160 -180 0 0 {name=l32 sig_type=std_logic lab=VDD}
C {sky130_fd_pr/pfet_01v8.sym} 140 -180 0 0 {name=XPNBX W=7 L=0.25 nf=1 mult=128 ad=2.03 pd=14.58 as=2.03 ps=14.58 nrd=0.0414286 nrs=0.0414286 sa=0 sb=0 sd=0 model=pfet_01v8 spiceprefix=X}
C {devices/lab_pin.sym} 160 -150 0 0 {name=l33 sig_type=std_logic lab=G2}
C {devices/lab_pin.sym} 120 -180 0 0 {name=l34 sig_type=std_logic lab=NB}
C {devices/lab_pin.sym} 160 -210 0 0 {name=l35 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 160 -180 0 0 {name=l36 sig_type=std_logic lab=VDD}
