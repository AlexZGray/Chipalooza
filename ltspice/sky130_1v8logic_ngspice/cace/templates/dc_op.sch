v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {CACE testbench dc_op: one code, DC} -700 -760 0 0 0.6 0.6 {}
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
C {devices/code_shown.sym} -700 -600 0 0 {name=SETUP only_toplevel=false value="* CACE testbench dc_op for dac6_1v8
* CACE\{filename\}_CACE\{N\}: corner CACE\{corner\}, CACE\{temperature\} C
.lib CACE\{PDK_ROOT\}/CACE\{PDK\}/libs.tech/combined/sky130.lib.spice CACE\{corner\}
.include CACE\{DUT_path\}
.option TEMP=CACE\{temperature\}
.option SEED=CACE[CACE\{seed=12345\} + CACE\{iterations=0\}]
.option warn=1
Vd0 d0 GND DC CACE[CACE\{b[0]\} * CACE\{Vvdd\}]
Vd1 d1 GND DC CACE[CACE\{b[1]\} * CACE\{Vvdd\}]
Vd2 d2 GND DC CACE[CACE\{b[2]\} * CACE\{Vvdd\}]
Vd3 d3 GND DC CACE[CACE\{b[3]\} * CACE\{Vvdd\}]
Vd4 d4 GND DC CACE[CACE\{b[4]\} * CACE\{Vvdd\}]
Vd5 d5 GND DC CACE[CACE\{b[5]\} * CACE\{Vvdd\}]
"}
C {devices/code_shown.sym} 600 -600 0 0 {name=CONTROL only_toplevel=false value=".control
set wr_singlescale
set num_threads=1
op
let idd = -i(Vvdd)
let istring = -i(Vrefh)
wrdata CACE\{filename\}_CACE\{N\}.data v(out) idd istring
quit
.endc
"}
