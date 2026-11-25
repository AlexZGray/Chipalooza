v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {DAC_Bank8: generated from the LTspice schematic by tools/gen_xschem.py} -900 -560 0 0 0.4 0.4 {}
C {devices/iopin.sym} -900 -500 0 0 {name=p1 lab=LO}
C {devices/iopin.sym} -900 -470 0 0 {name=p2 lab=HI}
C {devices/ipin.sym} -900 -440 0 0 {name=p3 lab=S0}
C {devices/ipin.sym} -900 -410 0 0 {name=p4 lab=S0B}
C {devices/ipin.sym} -900 -380 0 0 {name=p5 lab=S1}
C {devices/ipin.sym} -900 -350 0 0 {name=p6 lab=S1B}
C {devices/ipin.sym} -900 -320 0 0 {name=p7 lab=S2}
C {devices/ipin.sym} -900 -290 0 0 {name=p8 lab=S2B}
C {devices/iopin.sym} -900 -260 0 0 {name=p9 lab=VDD}
C {devices/iopin.sym} -900 -230 0 0 {name=p10 lab=VSS}
C {devices/opin.sym} -900 -200 0 0 {name=p11 lab=Y}
C {sky130_fd_pr/res_high_po_0p69.sym} -500 -400 0 0 {name=XR1 L=7.33 model=res_high_po_0p69 spiceprefix=X mult=4}
C {devices/lab_pin.sym} -500 -370 0 0 {name=l1 sig_type=std_logic lab=T1}
C {devices/lab_pin.sym} -500 -430 0 0 {name=l2 sig_type=std_logic lab=LO}
C {devices/lab_pin.sym} -520 -400 0 0 {name=l3 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/res_high_po_0p69.sym} -180 -400 0 0 {name=XR2 L=7.33 model=res_high_po_0p69 spiceprefix=X mult=4}
C {devices/lab_pin.sym} -180 -370 0 0 {name=l4 sig_type=std_logic lab=T2}
C {devices/lab_pin.sym} -180 -430 0 0 {name=l5 sig_type=std_logic lab=T1}
C {devices/lab_pin.sym} -200 -400 0 0 {name=l6 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/res_high_po_0p69.sym} 140 -400 0 0 {name=XR3 L=7.33 model=res_high_po_0p69 spiceprefix=X mult=4}
C {devices/lab_pin.sym} 140 -370 0 0 {name=l7 sig_type=std_logic lab=T3}
C {devices/lab_pin.sym} 140 -430 0 0 {name=l8 sig_type=std_logic lab=T2}
C {devices/lab_pin.sym} 120 -400 0 0 {name=l9 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/res_high_po_0p69.sym} 460 -400 0 0 {name=XR4 L=7.33 model=res_high_po_0p69 spiceprefix=X mult=4}
C {devices/lab_pin.sym} 460 -370 0 0 {name=l10 sig_type=std_logic lab=T4}
C {devices/lab_pin.sym} 460 -430 0 0 {name=l11 sig_type=std_logic lab=T3}
C {devices/lab_pin.sym} 440 -400 0 0 {name=l12 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/res_high_po_0p69.sym} 780 -400 0 0 {name=XR5 L=7.33 model=res_high_po_0p69 spiceprefix=X mult=4}
C {devices/lab_pin.sym} 780 -370 0 0 {name=l13 sig_type=std_logic lab=T5}
C {devices/lab_pin.sym} 780 -430 0 0 {name=l14 sig_type=std_logic lab=T4}
C {devices/lab_pin.sym} 760 -400 0 0 {name=l15 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/res_high_po_0p69.sym} 1100 -400 0 0 {name=XR6 L=7.33 model=res_high_po_0p69 spiceprefix=X mult=4}
C {devices/lab_pin.sym} 1100 -370 0 0 {name=l16 sig_type=std_logic lab=T6}
C {devices/lab_pin.sym} 1100 -430 0 0 {name=l17 sig_type=std_logic lab=T5}
C {devices/lab_pin.sym} 1080 -400 0 0 {name=l18 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/res_high_po_0p69.sym} -500 -180 0 0 {name=XR7 L=7.33 model=res_high_po_0p69 spiceprefix=X mult=4}
C {devices/lab_pin.sym} -500 -150 0 0 {name=l19 sig_type=std_logic lab=T7}
C {devices/lab_pin.sym} -500 -210 0 0 {name=l20 sig_type=std_logic lab=T6}
C {devices/lab_pin.sym} -520 -180 0 0 {name=l21 sig_type=std_logic lab=VSS}
C {sky130_fd_pr/res_high_po_0p69.sym} -180 -180 0 0 {name=XR8 L=7.33 model=res_high_po_0p69 spiceprefix=X mult=4}
C {devices/lab_pin.sym} -180 -150 0 0 {name=l22 sig_type=std_logic lab=HI}
C {devices/lab_pin.sym} -180 -210 0 0 {name=l23 sig_type=std_logic lab=T7}
C {devices/lab_pin.sym} -200 -180 0 0 {name=l24 sig_type=std_logic lab=VSS}
C {DAC_Mux8.sym} 140 -180 0 0 {name=xXSELECT}
C {devices/lab_pin.sym} 50.0 -310.0 0 0 {name=l25 sig_type=std_logic lab=LO}
C {devices/lab_pin.sym} 50.0 -290.0 0 0 {name=l26 sig_type=std_logic lab=T1}
C {devices/lab_pin.sym} 50.0 -270.0 0 0 {name=l27 sig_type=std_logic lab=T2}
C {devices/lab_pin.sym} 50.0 -250.0 0 0 {name=l28 sig_type=std_logic lab=T3}
C {devices/lab_pin.sym} 50.0 -230.0 0 0 {name=l29 sig_type=std_logic lab=T4}
C {devices/lab_pin.sym} 50.0 -210.0 0 0 {name=l30 sig_type=std_logic lab=T5}
C {devices/lab_pin.sym} 50.0 -190.0 0 0 {name=l31 sig_type=std_logic lab=T6}
C {devices/lab_pin.sym} 50.0 -170.0 0 0 {name=l32 sig_type=std_logic lab=T7}
C {devices/lab_pin.sym} 50.0 -150.0 0 0 {name=l33 sig_type=std_logic lab=S0}
C {devices/lab_pin.sym} 50.0 -130.0 0 0 {name=l34 sig_type=std_logic lab=S0B}
C {devices/lab_pin.sym} 50.0 -110.0 0 0 {name=l35 sig_type=std_logic lab=S1}
C {devices/lab_pin.sym} 50.0 -90.0 0 0 {name=l36 sig_type=std_logic lab=S1B}
C {devices/lab_pin.sym} 50.0 -70.0 0 0 {name=l37 sig_type=std_logic lab=S2}
C {devices/lab_pin.sym} 50.0 -50.0 0 0 {name=l38 sig_type=std_logic lab=S2B}
C {devices/lab_pin.sym} 230.0 -310.0 0 0 {name=l39 sig_type=std_logic lab=VDD}
C {devices/lab_pin.sym} 230.0 -290.0 0 0 {name=l40 sig_type=std_logic lab=VSS}
C {devices/lab_pin.sym} 230.0 -270.0 0 0 {name=l41 sig_type=std_logic lab=Y}
