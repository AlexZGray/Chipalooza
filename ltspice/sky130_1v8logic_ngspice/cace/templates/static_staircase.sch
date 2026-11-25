v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {CACE testbench static_staircase: all 64 codes, settled} -700 -760 0 0 0.6 0.6 {}
T {VREFH has its own source at the VDDA voltage so the string current can be read} -700 420 0 0 0.3 0.3 {}
C {devices/lab_pin.sym} -90.0 -60.0 0 0 {name=lp1 sig_type=std_logic lab=d0}
C {devices/lab_pin.sym} -90.0 -40.0 0 0 {name=lp2 sig_type=std_logic lab=d1}
C {devices/lab_pin.sym} -90.0 -20.0 0 0 {name=lp3 sig_type=std_logic lab=d2}
C {devices/lab_pin.sym} -90.0 0.0 0 0 {name=lp4 sig_type=std_logic lab=d3}
C {devices/lab_pin.sym} -90.0 20.0 0 0 {name=lp5 sig_type=std_logic lab=d4}
C {devices/lab_pin.sym} -90.0 40.0 0 0 {name=lp6 sig_type=std_logic lab=d5}
C {devices/lab_pin.sym} -90.0 60.0 0 0 {name=lp7 sig_type=std_logic lab=en}
C {devices/lab_pin.sym} 90.0 -60.0 0 0 {name=lp8 sig_type=std_logic lab=vdd}
C {devices/gnd.sym} 90.0 -40.0 0 0 {name=lg9 lab=GND}
C {devices/lab_pin.sym} 90.0 -20.0 0 0 {name=lp10 sig_type=std_logic lab=vrefl}
C {devices/lab_pin.sym} 90.0 0.0 0 0 {name=lp11 sig_type=std_logic lab=vrefh}
C {devices/lab_pin.sym} 90.0 20.0 0 0 {name=lp12 sig_type=std_logic lab=ibias}
C {devices/lab_pin.sym} 90.0 40.0 0 0 {name=lp13 sig_type=std_logic lab=tap}
C {devices/lab_pin.sym} 90.0 60.0 0 0 {name=lp14 sig_type=std_logic lab=out}
C {dac6_1v8.sym} 0 0 0 0 {name=XDUT}
C {devices/vsource.sym} -500 300 0 0 {name=Vvdd value="DC CACE\{Vvdd\}" savecurrent=false}
C {devices/lab_pin.sym} -500 270 0 0 {name=lp15 sig_type=std_logic lab=vdd}
C {devices/gnd.sym} -500 330 0 0 {name=lg16 lab=GND}
C {devices/vsource.sym} -380 300 0 0 {name=Vrefh value="DC CACE\{Vvdd\}" savecurrent=false}
C {devices/lab_pin.sym} -380 270 0 0 {name=lp17 sig_type=std_logic lab=vrefh}
C {devices/gnd.sym} -380 330 0 0 {name=lg18 lab=GND}
C {devices/vsource.sym} -260 300 0 0 {name=Vrefl value="DC 0" savecurrent=false}
C {devices/lab_pin.sym} -260 270 0 0 {name=lp19 sig_type=std_logic lab=vrefl}
C {devices/gnd.sym} -260 330 0 0 {name=lg20 lab=GND}
C {devices/isource.sym} -140 300 0 0 {name=Ibias value="DC CACE\{Ibias\}"}
C {devices/lab_pin.sym} -140 270 0 0 {name=lp21 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -140 330 0 0 {name=lp22 sig_type=std_logic lab=ibias}
C {devices/vsource.sym} -20 300 0 0 {name=Ven value="DC CACE[CACE\{ena\} * CACE\{Vvdd\}]" savecurrent=false}
C {devices/lab_pin.sym} -20 270 0 0 {name=lp23 sig_type=std_logic lab=en}
C {devices/gnd.sym} -20 330 0 0 {name=lg24 lab=GND}
C {devices/res.sym} 300 300 0 0 {name=Rload value=CACE\{Rload\} m=1}
C {devices/lab_pin.sym} 300 270 0 0 {name=lp25 sig_type=std_logic lab=out}
C {devices/gnd.sym} 300 330 0 0 {name=lg26 lab=GND}
C {devices/capa.sym} 420 300 0 0 {name=Cload value=CACE\{Cload\} m=1}
C {devices/lab_pin.sym} 420 270 0 0 {name=lp27 sig_type=std_logic lab=out}
C {devices/gnd.sym} 420 330 0 0 {name=lg28 lab=GND}
C {devices/code_shown.sym} -700 -600 0 0 {name=SETUP only_toplevel=false value="* CACE testbench static_staircase for dac6_1v8
* CACE\{filename\}_CACE\{N\}: corner CACE\{corner\}, CACE\{temperature\} C
.lib CACE\{PDK_ROOT\}/CACE\{PDK\}/libs.tech/combined/sky130.lib.spice CACE\{corner\}
.include CACE\{DUT_path\}
.option TEMP=CACE\{temperature\}
.option SEED=CACE[CACE\{seed=12345\} + CACE\{iterations=0\}]
.option warn=1
* Six data bits decoded from the staircase voltage on node code
VCODE code GND PWL(0 0 30u 0 30.01u 1 60u 1 60.01u 2 90u 2 90.01u 3 120u 3 120.01u 4 132u 4 132.01u 5 144u 5 144.01u 6 156u 6 156.01u 7 168u 7 168.01u 8 180u 8 180.01u 9 192u 9 192.01u 10 204u 10 204.01u 11 216u 11 216.01u 12 228u 12 228.01u 13 240u 13 240.01u 14 252u 14 252.01u 15 264u 15 264.01u 16 276u 16 276.01u 17 288u 17 288.01u 18 300u 18 300.01u 19 312u 19 312.01u 20 324u 20 324.01u 21 336u 21 336.01u 22 348u 22 348.01u 23 360u 23 360.01u 24 372u 24 372.01u 25 384u 25 384.01u 26 396u 26 396.01u 27 408u 27 408.01u 28 420u 28 420.01u 29 432u 29 432.01u 30 444u 30 444.01u 31 456u 31 456.01u 32 468u 32 468.01u 33 480u 33 480.01u 34 492u 34 492.01u 35 504u 35 504.01u 36 516u 36 516.01u 37 528u 37 528.01u 38 540u 38 540.01u 39 552u 39 552.01u 40 564u 40 564.01u 41 576u 41 576.01u 42 588u 42 588.01u 43 600u 43 600.01u 44 612u 44 612.01u 45 624u 45 624.01u 46 636u 46 636.01u 47 648u 47 648.01u 48 660u 48 660.01u 49 672u 49 672.01u 50 684u 50 684.01u 51 696u 51 696.01u 52 708u 52 708.01u 53 720u 53 720.01u 54 732u 54 732.01u 55 744u 55 744.01u 56 756u 56 756.01u 57 768u 57 768.01u 58 780u 58 780.01u 59 792u 59 792.01u 60 804u 60 804.01u 61 816u 61 816.01u 62 828u 62 828.01u 63)
Bd0 d0 GND V=\{CACE\{Vvdd\}*(floor((v(code)+0.5)/1)-2*floor((v(code)+0.5)/2))\}
Bd1 d1 GND V=\{CACE\{Vvdd\}*(floor((v(code)+0.5)/2)-2*floor((v(code)+0.5)/4))\}
Bd2 d2 GND V=\{CACE\{Vvdd\}*(floor((v(code)+0.5)/4)-2*floor((v(code)+0.5)/8))\}
Bd3 d3 GND V=\{CACE\{Vvdd\}*(floor((v(code)+0.5)/8)-2*floor((v(code)+0.5)/16))\}
Bd4 d4 GND V=\{CACE\{Vvdd\}*(floor((v(code)+0.5)/16)-2*floor((v(code)+0.5)/32))\}
Bd5 d5 GND V=\{CACE\{Vvdd\}*(floor((v(code)+0.5)/32)-2*floor((v(code)+0.5)/64))\}
"}
C {devices/code_shown.sym} 600 -600 0 0 {name=CONTROL only_toplevel=false value=".control
set wr_singlescale
set num_threads=1
tran 100n 840u
let idd = -i(Vvdd)
let istring = -i(Vrefh)
wrdata CACE\{filename\}_CACE\{N\}.data v(code) v(out) v(tap) idd istring
quit
.endc
"}
