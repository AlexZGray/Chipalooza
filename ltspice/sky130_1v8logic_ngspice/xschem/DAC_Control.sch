v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {DAC_Control: generated from the LTspice schematic by tools/gen_xschem.py} -900 -560 0 0 0.4 0.4 {}
C {devices/ipin.sym} -900 -500 0 0 {name=p1 lab=D0}
C {devices/ipin.sym} -900 -470 0 0 {name=p2 lab=D1}
C {devices/ipin.sym} -900 -440 0 0 {name=p3 lab=D2}
C {devices/ipin.sym} -900 -410 0 0 {name=p4 lab=D3}
C {devices/ipin.sym} -900 -380 0 0 {name=p5 lab=D4}
C {devices/ipin.sym} -900 -350 0 0 {name=p6 lab=D5}
C {devices/ipin.sym} -900 -320 0 0 {name=p7 lab=EN}
C {devices/iopin.sym} -900 -290 0 0 {name=p8 lab=VDDA}
C {devices/iopin.sym} -900 -260 0 0 {name=p9 lab=VSS}
C {devices/opin.sym} -900 -230 0 0 {name=p10 lab=S0}
C {devices/opin.sym} -900 -200 0 0 {name=p11 lab=S0B}
C {devices/opin.sym} -900 -170 0 0 {name=p12 lab=S1}
C {devices/opin.sym} -900 -140 0 0 {name=p13 lab=S1B}
C {devices/opin.sym} -900 -110 0 0 {name=p14 lab=S2}
C {devices/opin.sym} -900 -80 0 0 {name=p15 lab=S2B}
C {devices/opin.sym} -900 -50 0 0 {name=p16 lab=S3}
C {devices/opin.sym} -900 -20 0 0 {name=p17 lab=S3B}
C {devices/opin.sym} -900 10 0 0 {name=p18 lab=S4}
C {devices/opin.sym} -900 40 0 0 {name=p19 lab=S4B}
C {devices/opin.sym} -900 70 0 0 {name=p20 lab=S5}
C {devices/opin.sym} -900 100 0 0 {name=p21 lab=S5B}
C {devices/opin.sym} -900 130 0 0 {name=p22 lab=E}
C {devices/opin.sym} -900 160 0 0 {name=p23 lab=EB}
C {CMOS_INV.sym} -500 -400 0 0 {name=xXD0_B}
C {devices/lab_pin.sym} -590.0 -420.0 0 0 {name=l1 sig_type=std_logic lab=D0}
C {devices/lab_pin.sym} -410.0 -420.0 0 0 {name=l2 sig_type=std_logic lab=S0B}
C {devices/lab_pin.sym} -410.0 -400.0 0 0 {name=l3 sig_type=std_logic lab=VDDA}
C {devices/lab_pin.sym} -410.0 -380.0 0 0 {name=l4 sig_type=std_logic lab=VSS}
C {CMOS_INV.sym} -180 -400 0 0 {name=xXD0_T}
C {devices/lab_pin.sym} -270.0 -420.0 0 0 {name=l5 sig_type=std_logic lab=S0B}
C {devices/lab_pin.sym} -90.0 -420.0 0 0 {name=l6 sig_type=std_logic lab=S0}
C {devices/lab_pin.sym} -90.0 -400.0 0 0 {name=l7 sig_type=std_logic lab=VDDA}
C {devices/lab_pin.sym} -90.0 -380.0 0 0 {name=l8 sig_type=std_logic lab=VSS}
C {CMOS_INV.sym} 140 -400 0 0 {name=xXD1_B}
C {devices/lab_pin.sym} 50.0 -420.0 0 0 {name=l9 sig_type=std_logic lab=D1}
C {devices/lab_pin.sym} 230.0 -420.0 0 0 {name=l10 sig_type=std_logic lab=S1B}
C {devices/lab_pin.sym} 230.0 -400.0 0 0 {name=l11 sig_type=std_logic lab=VDDA}
C {devices/lab_pin.sym} 230.0 -380.0 0 0 {name=l12 sig_type=std_logic lab=VSS}
C {CMOS_INV.sym} 460 -400 0 0 {name=xXD1_T}
C {devices/lab_pin.sym} 370.0 -420.0 0 0 {name=l13 sig_type=std_logic lab=S1B}
C {devices/lab_pin.sym} 550.0 -420.0 0 0 {name=l14 sig_type=std_logic lab=S1}
C {devices/lab_pin.sym} 550.0 -400.0 0 0 {name=l15 sig_type=std_logic lab=VDDA}
C {devices/lab_pin.sym} 550.0 -380.0 0 0 {name=l16 sig_type=std_logic lab=VSS}
C {CMOS_INV.sym} 780 -400 0 0 {name=xXD2_B}
C {devices/lab_pin.sym} 690.0 -420.0 0 0 {name=l17 sig_type=std_logic lab=D2}
C {devices/lab_pin.sym} 870.0 -420.0 0 0 {name=l18 sig_type=std_logic lab=S2B}
C {devices/lab_pin.sym} 870.0 -400.0 0 0 {name=l19 sig_type=std_logic lab=VDDA}
C {devices/lab_pin.sym} 870.0 -380.0 0 0 {name=l20 sig_type=std_logic lab=VSS}
C {CMOS_INV.sym} 1100 -400 0 0 {name=xXD2_T}
C {devices/lab_pin.sym} 1010.0 -420.0 0 0 {name=l21 sig_type=std_logic lab=S2B}
C {devices/lab_pin.sym} 1190.0 -420.0 0 0 {name=l22 sig_type=std_logic lab=S2}
C {devices/lab_pin.sym} 1190.0 -400.0 0 0 {name=l23 sig_type=std_logic lab=VDDA}
C {devices/lab_pin.sym} 1190.0 -380.0 0 0 {name=l24 sig_type=std_logic lab=VSS}
C {CMOS_INV.sym} -500 -180 0 0 {name=xXD3_B}
C {devices/lab_pin.sym} -590.0 -200.0 0 0 {name=l25 sig_type=std_logic lab=D3}
C {devices/lab_pin.sym} -410.0 -200.0 0 0 {name=l26 sig_type=std_logic lab=S3B}
C {devices/lab_pin.sym} -410.0 -180.0 0 0 {name=l27 sig_type=std_logic lab=VDDA}
C {devices/lab_pin.sym} -410.0 -160.0 0 0 {name=l28 sig_type=std_logic lab=VSS}
C {CMOS_INV.sym} -180 -180 0 0 {name=xXD3_T}
C {devices/lab_pin.sym} -270.0 -200.0 0 0 {name=l29 sig_type=std_logic lab=S3B}
C {devices/lab_pin.sym} -90.0 -200.0 0 0 {name=l30 sig_type=std_logic lab=S3}
C {devices/lab_pin.sym} -90.0 -180.0 0 0 {name=l31 sig_type=std_logic lab=VDDA}
C {devices/lab_pin.sym} -90.0 -160.0 0 0 {name=l32 sig_type=std_logic lab=VSS}
C {CMOS_INV.sym} 140 -180 0 0 {name=xXD4_B}
C {devices/lab_pin.sym} 50.0 -200.0 0 0 {name=l33 sig_type=std_logic lab=D4}
C {devices/lab_pin.sym} 230.0 -200.0 0 0 {name=l34 sig_type=std_logic lab=S4B}
C {devices/lab_pin.sym} 230.0 -180.0 0 0 {name=l35 sig_type=std_logic lab=VDDA}
C {devices/lab_pin.sym} 230.0 -160.0 0 0 {name=l36 sig_type=std_logic lab=VSS}
C {CMOS_INV.sym} 460 -180 0 0 {name=xXD4_T}
C {devices/lab_pin.sym} 370.0 -200.0 0 0 {name=l37 sig_type=std_logic lab=S4B}
C {devices/lab_pin.sym} 550.0 -200.0 0 0 {name=l38 sig_type=std_logic lab=S4}
C {devices/lab_pin.sym} 550.0 -180.0 0 0 {name=l39 sig_type=std_logic lab=VDDA}
C {devices/lab_pin.sym} 550.0 -160.0 0 0 {name=l40 sig_type=std_logic lab=VSS}
C {CMOS_INV.sym} 780 -180 0 0 {name=xXD5_B}
C {devices/lab_pin.sym} 690.0 -200.0 0 0 {name=l41 sig_type=std_logic lab=D5}
C {devices/lab_pin.sym} 870.0 -200.0 0 0 {name=l42 sig_type=std_logic lab=S5B}
C {devices/lab_pin.sym} 870.0 -180.0 0 0 {name=l43 sig_type=std_logic lab=VDDA}
C {devices/lab_pin.sym} 870.0 -160.0 0 0 {name=l44 sig_type=std_logic lab=VSS}
C {CMOS_INV.sym} 1100 -180 0 0 {name=xXD5_T}
C {devices/lab_pin.sym} 1010.0 -200.0 0 0 {name=l45 sig_type=std_logic lab=S5B}
C {devices/lab_pin.sym} 1190.0 -200.0 0 0 {name=l46 sig_type=std_logic lab=S5}
C {devices/lab_pin.sym} 1190.0 -180.0 0 0 {name=l47 sig_type=std_logic lab=VDDA}
C {devices/lab_pin.sym} 1190.0 -160.0 0 0 {name=l48 sig_type=std_logic lab=VSS}
C {CMOS_INV.sym} -500 40 0 0 {name=xXEN_B}
C {devices/lab_pin.sym} -590.0 20.0 0 0 {name=l49 sig_type=std_logic lab=EN}
C {devices/lab_pin.sym} -410.0 20.0 0 0 {name=l50 sig_type=std_logic lab=EB}
C {devices/lab_pin.sym} -410.0 40.0 0 0 {name=l51 sig_type=std_logic lab=VDDA}
C {devices/lab_pin.sym} -410.0 60.0 0 0 {name=l52 sig_type=std_logic lab=VSS}
C {CMOS_INV.sym} -180 40 0 0 {name=xXEN_T}
C {devices/lab_pin.sym} -270.0 20.0 0 0 {name=l53 sig_type=std_logic lab=EB}
C {devices/lab_pin.sym} -90.0 20.0 0 0 {name=l54 sig_type=std_logic lab=E}
C {devices/lab_pin.sym} -90.0 40.0 0 0 {name=l55 sig_type=std_logic lab=VDDA}
C {devices/lab_pin.sym} -90.0 60.0 0 0 {name=l56 sig_type=std_logic lab=VSS}
