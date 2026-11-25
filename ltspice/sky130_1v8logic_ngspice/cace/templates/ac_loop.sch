v {xschem version=3.4.4 file_version=1.2
}
G {}
K {}
V {}
S {}
E {}
T {CACE testbench ac_loop: buffer loop gain, loop broken at INM} -700 -760 0 0 0.6 0.6 {}
T {VREFH has its own source at the VDDA voltage so the string current can be read} -700 420 0 0 0.3 0.3 {}
C {devices/lab_pin.sym} -100.0 -40.0 0 0 {name=lp1 sig_type=std_logic lab=inp}
C {devices/lab_pin.sym} -100.0 40.0 0 0 {name=lp2 sig_type=std_logic lab=inm}
C {devices/lab_pin.sym} 0.0 -80.0 0 0 {name=lp3 sig_type=std_logic lab=vdd}
C {devices/gnd.sym} 0.0 80.0 0 0 {name=lg4 lab=GND}
C {devices/lab_pin.sym} -100.0 0.0 0 0 {name=lp5 sig_type=std_logic lab=ibias}
C {devices/lab_pin.sym} 120.0 0.0 0 0 {name=lp6 sig_type=std_logic lab=out}
C {buffer_ota.sym} 0 0 0 0 {name=XOTA}
C {devices/vsource.sym} -500 300 0 0 {name=Vvdd value="DC CACE\{Vvdd\}" savecurrent=false}
C {devices/lab_pin.sym} -500 270 0 0 {name=lp7 sig_type=std_logic lab=vdd}
C {devices/gnd.sym} -500 330 0 0 {name=lg8 lab=GND}
C {devices/isource.sym} -380 300 0 0 {name=Ibias value="DC CACE\{Ibias\}"}
C {devices/lab_pin.sym} -380 270 0 0 {name=lp9 sig_type=std_logic lab=vdd}
C {devices/lab_pin.sym} -380 330 0 0 {name=lp10 sig_type=std_logic lab=ibias}
C {devices/vsource.sym} -260 300 0 0 {name=Vin value="DC CACE\{Vin\}" savecurrent=false}
C {devices/lab_pin.sym} -260 270 0 0 {name=lp11 sig_type=std_logic lab=inp}
C {devices/gnd.sym} -260 330 0 0 {name=lg12 lab=GND}
C {devices/ind.sym} 300 -300 0 0 {name=Lbreak value=1T m=1}
C {devices/lab_pin.sym} 300 -330 0 0 {name=lp13 sig_type=std_logic lab=out}
C {devices/lab_pin.sym} 300 -270 0 0 {name=lp14 sig_type=std_logic lab=inm}
C {devices/capa.sym} 420 -300 0 0 {name=Cbreak value=1T m=1}
C {devices/lab_pin.sym} 420 -330 0 0 {name=lp15 sig_type=std_logic lab=inm}
C {devices/lab_pin.sym} 420 -270 0 0 {name=lp16 sig_type=std_logic lab=acin}
C {devices/vsource.sym} 540 -300 0 0 {name=Vac value="DC 0 AC 1" savecurrent=false}
C {devices/lab_pin.sym} 540 -330 0 0 {name=lp17 sig_type=std_logic lab=acin}
C {devices/gnd.sym} 540 -270 0 0 {name=lg18 lab=GND}
C {devices/res.sym} 300 300 0 0 {name=Rload value=CACE\{Rload\} m=1}
C {devices/lab_pin.sym} 300 270 0 0 {name=lp19 sig_type=std_logic lab=out}
C {devices/gnd.sym} 300 330 0 0 {name=lg20 lab=GND}
C {devices/capa.sym} 420 300 0 0 {name=Cload value=CACE\{Cload\} m=1}
C {devices/lab_pin.sym} 420 270 0 0 {name=lp21 sig_type=std_logic lab=out}
C {devices/gnd.sym} 420 330 0 0 {name=lg22 lab=GND}
C {devices/code_shown.sym} -700 -600 0 0 {name=SETUP only_toplevel=false value="* CACE testbench ac_loop for dac6_1v8
* CACE\{filename\}_CACE\{N\}: corner CACE\{corner\}, CACE\{temperature\} C
.lib CACE\{PDK_ROOT\}/CACE\{PDK\}/libs.tech/combined/sky130.lib.spice CACE\{corner\}
.include CACE\{DUT_path\}
.option TEMP=CACE\{temperature\}
.option SEED=CACE[CACE\{seed=12345\} + CACE\{iterations=0\}]
.option warn=1
"}
C {devices/code_shown.sym} 700 -600 0 0 {name=CONTROL only_toplevel=false value=".control
set wr_singlescale
set num_threads=1
ac dec 40 0.1 1G
let lg = -v(out)/v(inm)
let lg_db = db(lg)
let lg_ph = 180/pi*cph(lg)
wrdata CACE\{filename\}_CACE\{N\}.data lg_db lg_ph
quit
.endc
"}
